from datetime import datetime
from pathlib import Path
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[2]
OVERLAY_ROOT = ROOT / "overlay"
EXPORT = ROOT / "export"
STAMP = datetime.now().strftime("%Y%m%d-%H%M")
WORK = EXPORT / f"mkdocs-export-{STAMP}"
PROFILE_PATH = OVERLAY_ROOT / "mkdocs_profile.json"
LOCK_PATH = OVERLAY_ROOT / "mkdocs_nav_lock.json"


def load_profile() -> dict:
    if not PROFILE_PATH.exists():
        raise FileNotFoundError(
            f"Overlay-profiel ontbreekt: {PROFILE_PATH}. Maak dit bestand aan met secties en regels."
        )
    return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = value.replace("&", " en ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "pagina"


def list_overlay_sources() -> list[Path]:
    excluded_dirs = {"meetings", "planning"}
    excluded_files = {"mkdocs_profile.json"}
    result = []
    for file_path in sorted(OVERLAY_ROOT.rglob("*.md")):
        rel = file_path.relative_to(ROOT)
        if rel.parts[0] != "overlay":
            continue
        if len(rel.parts) > 1 and rel.parts[1] in excluded_dirs:
            continue
        if file_path.name in excluded_files:
            continue
        result.append(file_path)
    return result


def strip_frontmatter(content: str) -> tuple[dict, str]:
    text = content.strip()
    if not text.startswith("---\n"):
        return {}, text
    end_marker = "\n---\n"
    end_index = text.find(end_marker, 4)
    if end_index == -1:
        return {}, text

    fm_block = text[4:end_index]
    body = text[end_index + len(end_marker):].lstrip()
    metadata = {}
    for line in fm_block.splitlines():
        if ":" in line and not line.strip().startswith("-"):
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()
    return metadata, body


def extract_doc_title(path: Path, body: str, metadata: dict) -> str:
    if metadata.get("title"):
        return metadata["title"]
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem.replace("_", " ").replace("-", " ").title()


def classify_source(rel_path: str, profile: dict) -> str:
    rel_lower = rel_path.lower()
    for section in profile["sections"]:
        for token in section.get("match_any", []):
            if token.lower() in rel_lower:
                return section["id"]
    return profile.get("fallback_section", "overig")


def load_lock() -> dict[str, str]:
    if not LOCK_PATH.exists():
        return {}
    return json.loads(LOCK_PATH.read_text(encoding="utf-8"))


def save_lock(lock_data: dict[str, str]) -> None:
    LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOCK_PATH.write_text(json.dumps(lock_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_assignments(sources: list[Path], profile: dict) -> dict[str, list[Path]]:
    section_ids = {section["id"] for section in profile["sections"]}
    lock = load_lock()
    assignments = {section["id"]: [] for section in profile["sections"]}

    for src in sources:
        rel = src.relative_to(ROOT).as_posix()
        locked_section = lock.get(rel)
        if locked_section in section_ids:
            section_id = locked_section
        else:
            section_id = classify_source(rel, profile)
            if section_id not in section_ids:
                section_id = profile.get("fallback_section", "overig")
            lock[rel] = section_id
        assignments[section_id].append(src)

    save_lock(lock)
    return assignments


def render_section_page(section: dict, files: list[Path]) -> str:
    lines = [f"# {section['title']}", ""]
    intro = section.get("intro", "")
    if intro:
        lines.append(intro)
        lines.append("")

    if not files:
        lines.append("Nog geen broncontent beschikbaar binnen de gekozen scope.")
        return "\n".join(lines).rstrip() + "\n"

    for source in files:
        rel = source.relative_to(ROOT).as_posix()
        raw = source.read_text(encoding="utf-8", errors="ignore")
        metadata, body = strip_frontmatter(raw)
        title = extract_doc_title(source, body, metadata)

        lines.append(f"## {title}")
        lines.append("")
        lines.append(f"Bron: `{rel}`")
        lines.append("")

        body_lines = body.splitlines()
        if body_lines and body_lines[0].startswith("# "):
            body_lines = body_lines[1:]
        lines.extend(body_lines)
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def mkdocs_yml_from_profile(profile: dict) -> str:
    lines = [
        f"site_name: {profile['site_name']}",
        f"site_description: {profile['site_description']}",
        "use_directory_urls: false",
        "",
        "theme:",
        "  name: material",
        "  language: nl",
        "  features:",
        "    - navigation.sections",
        "    - navigation.expand",
        "    - content.code.copy",
        "",
        "markdown_extensions:",
        "  - admonition",
        "  - tables",
        "  - toc:",
        "      permalink: true",
        "  - pymdownx.superfences:",
        "      custom_fences:",
        "        - name: mermaid",
        "          class: mermaid",
        "          format: !!python/name:pymdownx.superfences.fence_code_format",
        "  - pymdownx.details",
        "  - pymdownx.highlight",
        "",
        "extra_javascript:",
        "  - https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js",
        "  - assets/javascripts/mermaid-init.js",
        "",
        "nav:",
        "  - Home:",
    ]

    for section in profile["sections"]:
        lines.append(f"      - {section['title']}: {section['doc_path']}")

    return "\n".join(lines) + "\n"


def main() -> None:
    profile = load_profile()

    (WORK / "docs/assets/javascripts").mkdir(parents=True, exist_ok=True)
    (WORK / "docs/assets/javascripts/mermaid-init.js").write_text(
        "document.addEventListener('DOMContentLoaded', function () { if (window.mermaid) { window.mermaid.initialize({ startOnLoad: true }); } });\n",
        encoding="utf-8",
    )

    sources = list_overlay_sources()
    assignments = build_assignments(sources, profile)

    for section in profile["sections"]:
        out_path = WORK / "docs" / section["doc_path"]
        out_path.parent.mkdir(parents=True, exist_ok=True)
        files = sorted(assignments.get(section["id"], []), key=lambda p: p.relative_to(ROOT).as_posix())
        out_path.write_text(render_section_page(section, files), encoding="utf-8")

    (WORK / "mkdocs.yml").write_text(mkdocs_yml_from_profile(profile), encoding="utf-8")

    (WORK / "README_EXPORT.md").write_text(
        "# README_EXPORT\n\n## Gebruik\n1. pip install mkdocs mkdocs-material pymdown-extensions\n2. mkdocs serve\n3. mkdocs build\n",
        encoding="utf-8",
    )

    zip_path = EXPORT / f"mkdocs-export-{STAMP}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for file_path in sorted(WORK.rglob("*")):
            if file_path.is_file():
                archive.write(file_path, file_path.relative_to(WORK))

    print(WORK)
    print(zip_path)


if __name__ == "__main__":
    main()
