#!/usr/bin/env python3
"""
Action Points Management Method

Systematische registratie, beheer en prioritering van actiepunten
uit overlay-bronnen met behoud van status en traceerbaarheid.

Usage:
  python action_points.py --method extract [--scope overlay] [--mode incremental]
  python action_points.py --method clear [--older_than 7]
  python action_points.py --method prioritize [--strategy impact-urgency] [--scope all|todo]
  python action_points.py --method update_status --id ap-2026-001 --status done [--note ""]
"""

import json
import os
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# ============================================================================
# Configuration & Constants
# ============================================================================

OVERLAY_ROOT = Path(__file__).parent.parent.parent / "overlay"
ACTION_POINTS_DIR = OVERLAY_ROOT / "action_points"
ACTION_POINTS_FILE = ACTION_POINTS_DIR / "action_points.json"
ACTION_POINTS_MD_FILE = ACTION_POINTS_DIR / "action_points.md"
BACKUP_FILE = ACTION_POINTS_DIR / ".action_points.backup.json"

PRIORITY_MATRIX = {
    ("onmiddellijk", "hoog"): "hoog",
    ("onmiddellijk", "middel"): "hoog",
    ("onmiddellijk", "laag"): "middel",
    ("korttermijn", "hoog"): "hoog",
    ("korttermijn", "middel"): "middel",
    ("korttermijn", "laag"): "middel",
    ("middellang", "hoog"): "middel",
    ("middellang", "middel"): "middel",
    ("middellang", "laag"): "laag",
    ("langetermijn", "hoog"): "middel",
    ("langetermijn", "middel"): "laag",
    ("langetermijn", "laag"): "laag",
}

DETECTION_PATTERNS = {
    "checklist": r"\[\s*\]",  # [ ] or [  ]
    "todo_keyword": r"\b(actiepunt|todo|action item|volgende stap|moet nog|dient te|open vraag|beslissing nodig|needs|requires)\b",
    "risk_pattern": r"(risico|risk|gevaar|danger|threat)\s*[:=]",
    "gap_pattern": r"(gap|ontbrekend|missing|niet present)\s*[:=]",
}

# ============================================================================
# Data Models
# ============================================================================

class Status(str, Enum):
    TODO = "todo"
    DONE = "done"

class Priority(str, Enum):
    HOOG = "hoog"
    MIDDEL = "middel"
    LAAG = "laag"

class Urgentie(str, Enum):
    ONMIDDELLIJK = "onmiddellijk"
    KORTTERMIJN = "korttermijn"
    MIDDELLANG = "middellang"
    LANGETERMIJN = "langetermijn"

class Impact(str, Enum):
    HOOG = "hoog"
    MIDDEL = "middel"
    LAAG = "laag"

@dataclass
class SourceReference:
    bestand: str
    heading: Optional[str] = None
    quote: Optional[str] = None

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}

@dataclass
class ActionPoint:
    id: str
    titel: str
    beschrijving: str
    bron: SourceReference
    status: Status = Status.TODO
    prioriteit: Priority = Priority.MIDDEL
    urgentie: Urgentie = Urgentie.KORTTERMIJN
    impact: Optional[Impact] = Impact.MIDDEL
    aangemaakt_op: str = None
    gewijzigd_op: str = None
    afgerond_op: Optional[str] = None
    opmerking: Optional[str] = None

    def __post_init__(self):
        if not self.aangemaakt_op:
            self.aangemaakt_op = datetime.utcnow().isoformat() + "Z"
        if not self.gewijzigd_op:
            self.gewijzigd_op = self.aangemaakt_op

    def to_dict(self):
        data = asdict(self)
        data["bron"] = self.bron.to_dict()
        data["status"] = self.status.value
        data["prioriteit"] = self.prioriteit.value
        data["urgentie"] = self.urgentie.value
        if data["impact"]:
            data["impact"] = data["impact"].value
        return {k: v for k, v in data.items() if v is not None}

    @classmethod
    def from_dict(cls, data):
        data = data.copy()
        bron_data = data.pop("bron")
        data["bron"] = SourceReference(**bron_data)
        data["status"] = Status(data["status"])
        data["prioriteit"] = Priority(data["prioriteit"])
        data["urgentie"] = Urgentie(data["urgentie"])
        if data.get("impact"):
            data["impact"] = Impact(data["impact"])
        return cls(**data)

# ============================================================================
# Utility Functions
# ============================================================================

def ensure_action_points_dir():
    """Ensure action_points directory and file exist."""
    ACTION_POINTS_DIR.mkdir(parents=True, exist_ok=True)
    if not ACTION_POINTS_FILE.exists():
        init_action_points_file()

def init_action_points_file():
    """Initialize empty action_points.json."""
    initial_data = {
        "schema_id": "action-point-list",
        "schema_version": "1.0.0",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "generator": "action_points.py initialization",
        "action_points": []
    }
    save_action_points(initial_data)

def load_action_points() -> List[ActionPoint]:
    """Load action points from JSON file."""
    ensure_action_points_dir()
    if not ACTION_POINTS_FILE.exists():
        return []
    
    with open(ACTION_POINTS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return [ActionPoint.from_dict(ap) for ap in data.get("action_points", [])]

def save_action_points(data_or_points):
    """Save action points to JSON file."""
    ensure_action_points_dir()
    
    # If dict, write as-is; if list, wrap in schema
    if isinstance(data_or_points, dict):
        data = data_or_points
    else:
        points = data_or_points
        data = {
            "schema_id": "action-point-list",
            "schema_version": "1.0.0",
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "generator": "action_points.py",
            "action_points": [p.to_dict() for p in points]
        }
    
    with open(ACTION_POINTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Sync readable markdown view
    points = [ActionPoint.from_dict(ap) for ap in data.get("action_points", [])]
    generate_markdown_view(points)

def generate_markdown_view(points: List["ActionPoint"]):
    """Generate human-readable markdown view from action points list."""
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    todo = [p for p in points if p.status == Status.TODO]
    done = [p for p in points if p.status == Status.DONE]

    def priority_badge(p):
        return {"hoog": "🔴 hoog", "middel": "🟡 middel", "laag": "🟢 laag"}.get(p.prioriteit.value, p.prioriteit.value)

    def render_point(ap):
        bron_str = ap.bron.bestand
        if ap.bron.heading:
            bron_str += f" — {ap.bron.heading}"
        lines = [
            f"### {ap.id} — {ap.titel}",
            f"",
            f"{ap.beschrijving}",
            f"",
            f"| Veld | Waarde |",
            f"|------|--------|",
            f"| Prioriteit | {priority_badge(ap)} |",
            f"| Urgentie | {ap.urgentie.value} |",
            f"| Impact | {ap.impact.value if ap.impact else '—'} |",
            f"| Bron | `{bron_str}` |",
            f"| Aangemaakt | {ap.aangemaakt_op[:10]} |",
        ]
        if ap.afgerond_op:
            lines.append(f"| Afgerond | {ap.afgerond_op[:10]} |")
        if ap.opmerking:
            lines.append(f"| Opmerking | {ap.opmerking} |")
        return "\n".join(lines)

    sections = []
    sections.append(f"""---
title: Actiepunten
type: Action Points
auto_generated: true
language: nl
description: Automatisch gegenereerde weergave — bewerk uitsluitend via de action_points methode
---

# Actiepunten

> Gegenereerd op {now}. Bron: `action_points.json`.  
> Niet handmatig bewerken.""")

    if todo:
        sections.append(f"\n## Todo ({len(todo)})\n")
        todo_sorted = sorted(todo, key=lambda p: (["hoog", "middel", "laag"].index(p.prioriteit.value), p.urgentie.value))
        sections.extend(render_point(p) for p in todo_sorted)
    else:
        sections.append("\n## Todo\n\n_Geen openstaande actiepunten._")

    if done:
        sections.append(f"\n## Done ({len(done)})\n")
        sections.extend(render_point(p) for p in done)

    with open(ACTION_POINTS_MD_FILE, 'w', encoding='utf-8') as f:
        f.write("\n\n".join(sections) + "\n")

def next_action_point_id() -> str:
    """Generate next action point ID."""
    existing = load_action_points()
    year = datetime.now().year
    existing_ids = [int(ap.id.split('-')[-1]) for ap in existing if ap.id.startswith(f"ap-{year}-")]
    next_num = (max(existing_ids) if existing_ids else 0) + 1
    return f"ap-{year}-{next_num:03d}"

def find_action_point(id: str) -> Optional[ActionPoint]:
    """Find action point by ID."""
    for ap in load_action_points():
        if ap.id == id:
            return ap
    return None

def scan_markdown_files(scope: str = "overlay", include: str = "**/*.md", 
                       exclude: Optional[List[str]] = None) -> List[str]:
    """Scan for markdown files to extract from."""
    if exclude is None:
        exclude = ["action_points/**", "**/archive/**", "**/*.bak.md", "**/resources/**"]
    
    scope_path = OVERLAY_ROOT.parent / scope if not scope.startswith("/") else Path(scope)
    if not scope_path.exists():
        return []
    
    md_files = list(scope_path.glob(include))
    
    # Filter by exclude patterns
    filtered = []
    for f in md_files:
        rel_path = f.relative_to(scope_path.parent).as_posix()
        skip = False
        for excl in exclude:
            if Path(rel_path).match(excl):
                skip = True
                break
        if not skip:
            filtered.append(str(f))
    
    return filtered

def detect_action_point_candidates(md_file: str) -> List[Tuple[str, str]]:
    """Detect potential action point candidates in markdown file."""
    candidates = []
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        current_heading = None
        for i, line in enumerate(lines):
            # Track current heading
            if line.startswith('#'):
                current_heading = line.strip('# \n')
            
            # Check patterns
            if re.search(DETECTION_PATTERNS["checklist"], line) and '[ ]' in line:
                candidates.append((current_heading, line.strip()))
            elif re.search(DETECTION_PATTERNS["todo_keyword"], line, re.IGNORECASE):
                candidates.append((current_heading, line.strip()))
            elif re.search(DETECTION_PATTERNS["risk_pattern"], line, re.IGNORECASE):
                candidates.append((current_heading, line.strip()))
        
    except Exception as e:
        print(f"Error scanning {md_file}: {e}", file=sys.stderr)
    
    return candidates

# ============================================================================
# Sub-Methods
# ============================================================================

def method_extract(scope: str = "overlay", mode: str = "incremental", auto_extract: bool = True):
    """Extract action points from markdown files."""
    print(f"\n=== Action Points Extract ===")
    print(f"Scope: {scope}")
    print(f"Mode: {mode}")
    
    md_files = scan_markdown_files(scope=scope)
    existing = load_action_points()
    candidates = []
    
    for md_file in md_files:
        file_cands = detect_action_point_candidates(md_file)
        for heading, quote in file_cands:
            candidates.append((md_file, heading, quote))
    
    if not candidates:
        print("No action point candidates found.")
        return
    
    print(f"\nFound {len(candidates)} candidate(s):")
    approved = []
    
    for i, (file, heading, quote) in enumerate(candidates):
        print(f"\n[{i+1}/{len(candidates)}]")
        print(f"  File: {file}")
        print(f"  Heading: {heading}")
        print(f"  Quote: {quote[:80]}...")
        print(f"  \n  Approve? (a/s/e for approve/skip/edit): ", end='', flush=True)
        
        choice = input().lower().strip()
        if choice == 'a':
            print("    Title? ", end='', flush=True)
            titel = input().strip()
            print("    Description? ", end='', flush=True)
            beschrijving = input().strip()
            print("    Urgency (onmiddellijk/korttermijn/middellang/langetermijn)? [korttermijn]: ", end='', flush=True)
            urgentie_input = input().strip().lower() or "korttermijn"
            
            try:
                urgentie = Urgentie(urgentie_input)
                ap = ActionPoint(
                    id=next_action_point_id(),
                    titel=titel,
                    beschrijving=beschrijving,
                    bron=SourceReference(
                        bestand=file.replace(str(OVERLAY_ROOT.parent) + "/", ""),
                        heading=heading,
                        quote=quote[:200]
                    ),
                    urgentie=urgentie
                )
                approved.append(ap)
                print(f"    ✓ Added: {ap.id}")
            except ValueError:
                print(f"    ✗ Invalid urgency value")
        elif choice == 's':
            print("    Skipped.")
    
    if approved:
        existing.extend(approved)
        save_action_points(existing)
        print(f"\n✓ Saved {len(approved)} new action point(s)")
    else:
        print("\nNo action points to save.")

def method_clear(older_than: int = 7):
    """Clear completed action points."""
    print(f"\n=== Action Points Clear ===")
    print(f"Removing done action points older than {older_than} days")
    
    points = load_action_points()
    cutoff = datetime.utcnow() - timedelta(days=older_than)
    
    to_remove = []
    for ap in points:
        if ap.status == Status.DONE and ap.afgerond_op:
            completed_date = datetime.fromisoformat(ap.afgerond_op.replace('Z', '+00:00'))
            if completed_date < cutoff:
                to_remove.append(ap)
    
    if not to_remove:
        print(f"No action points to remove (0 done items older than {older_than} days)")
        return
    
    print(f"\nCandidates to remove ({len(to_remove)}):")
    for ap in to_remove:
        print(f"  - {ap.id}: {ap.titel}")
        print(f"    Done: {ap.afgerond_op}")
    
    print(f"\nRemove these {len(to_remove)} point(s)? (y/n): ", end='', flush=True)
    if input().lower().strip() == 'y':
        # Backup
        with open(ACTION_POINTS_FILE, 'r') as f:
            with open(BACKUP_FILE, 'w') as bf:
                bf.write(f.read())
        
        remaining = [ap for ap in points if ap not in to_remove]
        save_action_points(remaining)
        print(f"✓ Removed {len(to_remove)} action point(s). Backup saved.")
    else:
        print("Cancelled.")

def method_prioritize(strategy: str = "impact-urgency", scope: str = "todo"):
    """Prioritize action points."""
    print(f"\n=== Action Points Prioritize ===")
    print(f"Strategy: {strategy}")
    
    points = load_action_points()
    
    # Filter by scope
    if scope == "todo":
        points = [p for p in points if p.status == Status.TODO]
    
    if not points:
        print("No action points to prioritize.")
        return
    
    print(f"\nRecalculating priorities for {len(points)} point(s) using {strategy}:\n")
    
    updated = []
    for ap in points:
        old_priority = ap.prioriteit
        
        if strategy == "impact-urgency":
            key = (ap.urgentie.value, ap.impact.value if ap.impact else "middel")
            new_priority = PRIORITY_MATRIX.get(key, "middel")
            ap.prioriteit = Priority(new_priority)
        
        ap.gewijzigd_op = datetime.utcnow().isoformat() + "Z"
        updated.append(ap)
        
        if old_priority != ap.prioriteit:
            print(f"  {ap.id}: {old_priority} → {ap.prioriteit}")
    
    save_action_points(updated)
    print(f"\n✓ Prioritized {len(updated)} action point(s)")

def method_update_status(id: str, new_status: str, note: Optional[str] = None):
    """Update action point status."""
    ap = find_action_point(id)
    if not ap:
        print(f"Action point {id} not found.")
        return
    
    old_status = ap.status
    ap.status = Status(new_status)
    ap.gewijzigd_op = datetime.utcnow().isoformat() + "Z"
    
    if new_status == "done":
        ap.afgerond_op = datetime.utcnow().isoformat() + "Z"
    else:
        ap.afgerond_op = None
    
    if note:
        ap.opmerking = note
    
    points = load_action_points()
    idx = next(i for i, p in enumerate(points) if p.id == id)
    points[idx] = ap
    
    save_action_points(points)
    print(f"✓ Updated {id}: {old_status} → {ap.status}")

# ============================================================================
# CLI Entry Point
# ============================================================================

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    method = None
    kwargs = {}
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--method":
            method = sys.argv[i + 1]
            i += 2
        elif arg == "--scope":
            kwargs["scope"] = sys.argv[i + 1]
            i += 2
        elif arg == "--older_than":
            kwargs["older_than"] = int(sys.argv[i + 1])
            i += 2
        elif arg == "--strategy":
            kwargs["strategy"] = sys.argv[i + 1]
            i += 2
        elif arg == "--id":
            kwargs["id"] = sys.argv[i + 1]
            i += 2
        elif arg == "--status":
            kwargs["new_status"] = sys.argv[i + 1]
            i += 2
        elif arg == "--note":
            kwargs["note"] = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    if not method:
        print("Error: --method is required")
        sys.exit(1)
    
    if method == "extract":
        method_extract(**kwargs)
    elif method == "clear":
        method_clear(**kwargs)
    elif method == "prioritize":
        method_prioritize(**kwargs)
    elif method == "update_status":
        method_update_status(**kwargs)
    else:
        print(f"Unknown method: {method}")
        sys.exit(1)

if __name__ == "__main__":
    main()
