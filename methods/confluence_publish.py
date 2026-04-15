from datetime import datetime
from html import escape
from pathlib import Path
from typing import Optional
from urllib import parse, request
from urllib.error import HTTPError
import base64
import json
import re

ROOT = Path(__file__).resolve().parents[2]
OVERLAY_ROOT = ROOT / "overlay"
EXPORT = ROOT / "export"
CONFLUENCE_PROFILE_PATH = OVERLAY_ROOT / "confluence_profile.json"
MKDOCS_PROFILE_PATH = OVERLAY_ROOT / "mkdocs_profile.json"
CONFLUENCE_LOCK_PATH = OVERLAY_ROOT / "confluence_nav_lock.json"
STAMP = datetime.now().strftime("%Y%m%d-%H%M")
REPORT_PATH = EXPORT / f"confluence-publish-{STAMP}.json"

EXCLUDED_DIRS = {"meetings", "planning", "action_points"}
EXCLUDED_FILES = {"mkdocs_profile.json"}


def load_profile() -> dict:
    if CONFLUENCE_PROFILE_PATH.exists():
        return json.loads(CONFLUENCE_PROFILE_PATH.read_text(encoding="utf-8"))
    if MKDOCS_PROFILE_PATH.exists():
        return json.loads(MKDOCS_PROFILE_PATH.read_text(encoding="utf-8"))
    raise FileNotFoundError(
        f"Geen profiel gevonden. Maak {CONFLUENCE_PROFILE_PATH} aan of gebruik {MKDOCS_PROFILE_PATH}."
    )


def list_overlay_sources() -> list[Path]:
    result: list[Path] = []
    for file_path in sorted(OVERLAY_ROOT.rglob("*.md")):
        rel = file_path.relative_to(ROOT)
        if rel.parts[0] != "overlay":
            continue
        if len(rel.parts) > 1 and rel.parts[1] in EXCLUDED_DIRS:
            continue
        if file_path.name in EXCLUDED_FILES:
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
    if not CONFLUENCE_LOCK_PATH.exists():
        return {}
    return json.loads(CONFLUENCE_LOCK_PATH.read_text(encoding="utf-8"))


def save_lock(lock_data: dict[str, str]) -> None:
    CONFLUENCE_LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFLUENCE_LOCK_PATH.write_text(json.dumps(lock_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


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


def render_section_markdown(section: dict, files: list[Path]) -> str:
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
        lines.append(f"Bron: {rel}")
        lines.append("")

        body_lines = body.splitlines()
        if body_lines and body_lines[0].startswith("# "):
            body_lines = body_lines[1:]
        lines.extend(body_lines)
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def markdown_to_confluence_storage(markdown: str) -> str:
    lines = markdown.splitlines()
    output: list[str] = []
    in_ul = False
    in_ol = False
    in_code = False
    code_buffer: list[str] = []

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            output.append("</ul>")
            in_ul = False
        if in_ol:
            output.append("</ol>")
            in_ol = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            close_lists()
            if in_code:
                joined = "\n".join(code_buffer)
                output.append(f"<pre><code>{escape(joined)}</code></pre>")
                code_buffer = []
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_buffer.append(line)
            continue

        if not stripped:
            close_lists()
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading_match:
            close_lists()
            level = len(heading_match.group(1))
            text = escape(heading_match.group(2).strip())
            output.append(f"<h{level}>{text}</h{level}>")
            continue

        ul_match = re.match(r"^[-*]\s+(.+)$", stripped)
        if ul_match:
            if in_ol:
                output.append("</ol>")
                in_ol = False
            if not in_ul:
                output.append("<ul>")
                in_ul = True
            output.append(f"<li>{escape(ul_match.group(1).strip())}</li>")
            continue

        ol_match = re.match(r"^\d+\.\s+(.+)$", stripped)
        if ol_match:
            if in_ul:
                output.append("</ul>")
                in_ul = False
            if not in_ol:
                output.append("<ol>")
                in_ol = True
            output.append(f"<li>{escape(ol_match.group(1).strip())}</li>")
            continue

        close_lists()
        output.append(f"<p>{escape(stripped)}</p>")

    close_lists()
    if in_code:
        joined = "\n".join(code_buffer)
        output.append(f"<pre><code>{escape(joined)}</code></pre>")

    return "\n".join(output)


def confluence_headers(username: str, api_token: str) -> dict[str, str]:
    raw = f"{username}:{api_token}".encode("utf-8")
    encoded = base64.b64encode(raw).decode("ascii")
    return {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def confluence_request(base_url: str, method: str, path: str, headers: dict[str, str], payload: Optional[dict] = None) -> dict:
    url = f"{base_url.rstrip('/')}{path}"
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, method=method, headers=headers, data=data)
    try:
        with request.urlopen(req) as response:
            body = response.read().decode("utf-8")
            if not body:
                return {}
            return json.loads(body)
    except HTTPError as error:
        details = error.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Confluence API fout ({error.code}) op {path}: {details}") from error


def find_page_by_title(base_url: str, space_key: str, title: str, headers: dict[str, str]) -> Optional[dict]:
    cql = f'space="{space_key}" and title="{title}" and type=page'
    encoded_cql = parse.quote(cql, safe="")
    path = f"/wiki/rest/api/content/search?cql={encoded_cql}&expand=version,ancestors"
    data = confluence_request(base_url, "GET", path, headers)
    results = data.get("results", [])
    if not results:
        return None
    return results[0]


def upsert_page(
    base_url: str,
    space_key: str,
    title: str,
    body_storage: str,
    parent_page_id: Optional[str],
    headers: dict[str, str],
    dry_run: bool,
) -> dict:
    existing = find_page_by_title(base_url, space_key, title, headers)
    ancestors = []
    if parent_page_id:
        ancestors = [{"id": str(parent_page_id)}]

    if existing is None:
        payload = {
            "type": "page",
            "title": title,
            "space": {"key": space_key},
            "body": {"storage": {"value": body_storage, "representation": "storage"}},
        }
        if ancestors:
            payload["ancestors"] = ancestors

        if dry_run:
            return {"action": "create", "title": title, "dry_run": True}

        created = confluence_request(base_url, "POST", "/wiki/rest/api/content", headers, payload)
        return {
            "action": "create",
            "title": title,
            "page_id": created.get("id"),
            "version": created.get("version", {}).get("number"),
        }

    page_id = existing["id"]
    current_version = int(existing.get("version", {}).get("number", 1))
    payload = {
        "id": page_id,
        "type": "page",
        "title": title,
        "version": {"number": current_version + 1},
        "body": {"storage": {"value": body_storage, "representation": "storage"}},
    }
    if ancestors:
        payload["ancestors"] = ancestors

    if dry_run:
        return {
            "action": "update",
            "title": title,
            "page_id": page_id,
            "from_version": current_version,
            "to_version": current_version + 1,
            "dry_run": True,
        }

    updated = confluence_request(
        base_url,
        "PUT",
        f"/wiki/rest/api/content/{page_id}",
        headers,
        payload,
    )
    return {
        "action": "update",
        "title": title,
        "page_id": page_id,
        "version": updated.get("version", {}).get("number", current_version + 1),
    }


def build_page_title(section_title: str, title_prefix: Optional[str]) -> str:
    if not title_prefix:
        return section_title
    return f"{title_prefix.strip()} - {section_title}"


def require_env(name: str) -> str:
    value = __import__("os").environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Verplichte environment variabele ontbreekt: {name}")
    return value


def parse_bool_env(name: str, default: bool) -> bool:
    raw = __import__("os").environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


def main() -> None:
    profile = load_profile()
    sources = list_overlay_sources()
    assignments = build_assignments(sources, profile)

    base_url = require_env("CONFLUENCE_BASE_URL")
    space_key = require_env("CONFLUENCE_SPACE_KEY")
    username = require_env("CONFLUENCE_USERNAME")
    api_token = require_env("CONFLUENCE_API_TOKEN")

    parent_page_id = __import__("os").environ.get("CONFLUENCE_PARENT_PAGE_ID", "").strip() or None
    title_prefix = __import__("os").environ.get("CONFLUENCE_TITLE_PREFIX", "").strip()
    dry_run = parse_bool_env("CONFLUENCE_DRY_RUN", True)

    headers = confluence_headers(username, api_token)

    report = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "dry_run": dry_run,
        "space_key": space_key,
        "parent_page_id": parent_page_id,
        "title_prefix": title_prefix,
        "results": [],
    }

    for section in profile["sections"]:
        section_files = sorted(assignments.get(section["id"], []), key=lambda p: p.relative_to(ROOT).as_posix())
        markdown = render_section_markdown(section, section_files)
        storage = markdown_to_confluence_storage(markdown)
        title = build_page_title(section["title"], title_prefix)

        result = upsert_page(
            base_url=base_url,
            space_key=space_key,
            title=title,
            body_storage=storage,
            parent_page_id=parent_page_id,
            headers=headers,
            dry_run=dry_run,
        )
        result["section_id"] = section["id"]
        result["source_count"] = len(section_files)
        report["results"].append(result)

    EXPORT.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(REPORT_PATH)


if __name__ == "__main__":
    main()
