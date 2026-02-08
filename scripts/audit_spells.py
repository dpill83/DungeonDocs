#!/usr/bin/env python3
"""
Audit D&D 2024 spell markdown files for formatting compliance.
Validates required structure, lists UNKNOWN sources, and optionally checks body integrity.
"""

import csv
import hashlib
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SPELLS_DIR = REPO_ROOT / "docs" / "dnd2024" / "spells"
DATA_DIR = REPO_ROOT / "data"
SOURCES_CSV = DATA_DIR / "spell_sources.csv"

EXCLUDE = {"index.md", "all.md", "spells.md"}


def get_spell_files() -> list[Path]:
    """Return spell .md files to audit."""
    files = []
    for f in SPELLS_DIR.glob("*.md"):
        if f.name in EXCLUDE:
            continue
        if f.name.endswith("-school.md"):
            continue
        files.append(f)
    return sorted(files)


def parse_spell_file(path: Path) -> dict:
    """
    Parse a spell file and extract structure. Returns dict with keys:
    has_title, has_source, has_level_line, has_casting_time, has_range,
    has_components, has_duration, body_present, source_value, body_hash
    """
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()

    result = {
        "has_title": False,
        "has_source": False,
        "has_level_line": False,
        "has_casting_time": False,
        "has_range": False,
        "has_components": False,
        "has_duration": False,
        "body_present": False,
        "source_value": None,
        "body_hash": None,
    }

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            result["has_title"] = True
        elif stripped.startswith("Source:"):
            result["has_source"] = True
            result["source_value"] = stripped[7:].strip()
        elif re.match(r"^(Cantrip|\d+(?:st|nd|rd|th) Level) ", stripped):
            result["has_level_line"] = True
        elif stripped.startswith("Casting Time:"):
            result["has_casting_time"] = True
        elif stripped.startswith("Range:"):
            result["has_range"] = True
        elif stripped.startswith("Components:"):
            result["has_components"] = True
        elif stripped.startswith("Duration:"):
            result["has_duration"] = True

    # Body: everything after Duration line
    in_header = True
    body_lines = []
    for line in lines:
        if in_header and line.strip().startswith("Duration:"):
            in_header = False
            continue
        if not in_header:
            body_lines.append(line)

    body = "\n".join(body_lines).strip()
    result["body_present"] = len(body) > 0
    if body:
        result["body_hash"] = hashlib.sha256(body.encode("utf-8")).hexdigest()[:16]

    return result


def load_sources() -> dict[str, str]:
    """Load spell_sources.csv into slug -> source mapping."""
    if not SOURCES_CSV.exists():
        return {}
    sources = {}
    with open(SOURCES_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            slug = row.get("slug", "").strip()
            source = row.get("source", "UNKNOWN").strip()
            if slug:
                sources[slug] = source
    return sources


def main() -> None:
    spell_files = get_spell_files()
    sources = load_sources()

    required = [
        "has_title",
        "has_source",
        "has_level_line",
        "has_casting_time",
        "has_range",
        "has_components",
        "has_duration",
        "body_present",
    ]

    missing_required: list[tuple[str, list[str]]] = []
    unknown_sources: list[str] = []

    for fpath in spell_files:
        slug = fpath.stem
        try:
            parsed = parse_spell_file(fpath)
        except Exception as e:
            print(f"ERROR parsing {fpath.name}: {e}")
            continue

        missing = [r for r in required if not parsed[r]]
        if missing:
            missing_required.append((slug, missing))

        src = parsed.get("source_value") or sources.get(slug, "UNKNOWN")
        if src.upper() in ("UNKNOWN", "*UNKNOWN*"):
            unknown_sources.append(slug)

    # Report
    print("=== Spell Audit Report ===\n")

    if missing_required:
        print(f"Spells missing required lines ({len(missing_required)}):")
        for slug, missing in sorted(missing_required)[:20]:
            print(f"  {slug}: missing {missing}")
        if len(missing_required) > 20:
            print(f"  ... and {len(missing_required) - 20} more")
        print()
    else:
        print("All spell files have required structure.\n")

    if unknown_sources:
        print(f"Spells with Source = UNKNOWN ({len(unknown_sources)}):")
        for slug in sorted(unknown_sources)[:30]:
            print(f"  {slug}")
        if len(unknown_sources) > 30:
            print(f"  ... and {len(unknown_sources) - 30} more")
        print()
    else:
        print("No spells with UNKNOWN source.\n")

    print(f"Total spell files audited: {len(spell_files)}")


if __name__ == "__main__":
    main()
