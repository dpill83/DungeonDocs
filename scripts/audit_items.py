#!/usr/bin/env python3
"""
Audit D&D 2024 magic item markdown files for formatting compliance.
Validates required structure (title, Source, type/rarity line, body), lists UNKNOWN sources,
and warns on rarity mismatches (scaling vs single-rarity).
"""

import csv
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ITEMS_DIR = REPO_ROOT / "docs" / "dnd2024" / "magic-items"
DATA_DIR = REPO_ROOT / "data"
SOURCES_CSV = DATA_DIR / "item_sources.csv"
INDEX_FILE = ITEMS_DIR / "all.md"

EXCLUDE = {"all.md", "consumable.md", "crafting.md", "crafting-magical-items.md", "index.md"}

RARITY_FROM_HEADING = {
    "common magic items": "Common",
    "uncommon magic items": "Uncommon",
    "rare magic items": "Rare",
    "very rare magic items": "Very Rare",
    "legendary magic items": "Legendary",
    "artifacts": "Artifact",
}

# Type/rarity line: type(s), comma, rarity (Rarity Varies or single), optional ", requires attunement..."
TYPE_RARITY_RE = re.compile(
    r"^\s*\*?\s*[A-Za-z][A-Za-z\s]+,\s*"
    r"(Rarity Varies|Common|Uncommon|Rare|Very Rare|Legendary|Artifact)"
    r"(?:\s*,\s*requires attunement(?:\s+by\s+[^,*]+)?)?\s*\*?\s*$"
)


def parse_index(index_path: Path) -> dict[str, dict]:
    """Parse all.md into item dict keyed by slug with rarities set (for audit)."""
    if not index_path.exists():
        return {}
    text = index_path.read_text(encoding="utf-8")
    items: dict[str, dict] = {}
    current_rarity: str | None = None

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            heading = stripped[3:].strip().lower()
            current_rarity = RARITY_FROM_HEADING.get(heading)
            continue
        if current_rarity is None:
            continue
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        parts = [p.strip() for p in stripped.split("|")[1:-1]]
        if len(parts) < 4:
            continue
        name_cell = parts[0]
        if name_cell.lower() == "item name" or not name_cell:
            continue
        link_match = re.match(r"\[([^\]]+)\]\(([^)]+)\.md\)", name_cell)
        if not link_match:
            continue
        slug = link_match.group(2)
        if slug in items:
            items[slug]["rarities"].add(current_rarity)
        else:
            items[slug] = {"name": link_match.group(1), "rarities": {current_rarity}}
    return items


def get_item_files() -> list[Path]:
    """Return item .md files to audit."""
    files = []
    for f in ITEMS_DIR.glob("*.md"):
        if f.name.lower() in EXCLUDE:
            continue
        files.append(f)
    return sorted(files)


def parse_item_file(path: Path) -> dict:
    """
    Parse an item file and extract structure. Returns dict with keys:
    has_title, has_source, has_type_rarity_line, body_present, source_value, rarity_in_file
    """
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()

    result = {
        "has_title": False,
        "has_source": False,
        "has_type_rarity_line": False,
        "body_present": False,
        "source_value": None,
        "rarity_in_file": None,
    }

    body_start = len(lines)
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("# "):
            result["has_title"] = True
        elif re.match(r"^Source:\s*\*", stripped, re.IGNORECASE):
            result["has_source"] = True
            result["source_value"] = stripped
        else:
            mo = TYPE_RARITY_RE.match(stripped)
            if mo:
                result["has_type_rarity_line"] = True
                result["rarity_in_file"] = mo.group(1)
                body_start = i + 1

    body_lines = []
    for i in range(body_start, len(lines)):
        body_lines.append(lines[i])
    body = "\n".join(body_lines).strip()
    result["body_present"] = len(body) > 0

    return result


def load_sources() -> dict[str, str]:
    """Load item_sources.csv into slug -> source mapping."""
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
    item_files = get_item_files()
    sources = load_sources()
    index_items = parse_index(INDEX_FILE)

    required = [
        "has_title",
        "has_source",
        "has_type_rarity_line",
        "body_present",
    ]

    missing_required: list[tuple[str, list[str]]] = []
    unknown_sources: list[str] = []
    scaling_should_say_varies: list[str] = []
    single_should_not_say_varies: list[str] = []

    for fpath in item_files:
        slug = fpath.stem
        try:
            parsed = parse_item_file(fpath)
        except Exception as e:
            print(f"ERROR parsing {fpath.name}: {e}")
            continue

        missing = [r for r in required if not parsed[r]]
        if missing:
            missing_required.append((slug, missing))

        src_val = parsed.get("source_value") or ""
        csv_src = sources.get(slug, "UNKNOWN")
        if "*Unknown*" in src_val or csv_src.upper() == "UNKNOWN":
            unknown_sources.append(slug)

        index_rarities = index_items.get(slug, {}).get("rarities", set())
        file_rarity = parsed.get("rarity_in_file")
        if len(index_rarities) > 1 and file_rarity != "Rarity Varies":
            scaling_should_say_varies.append(slug)
        elif len(index_rarities) == 1 and file_rarity == "Rarity Varies":
            single_should_not_say_varies.append(slug)

    print("=== Magic Item Audit Report ===\n")

    if missing_required:
        print(f"Items missing required lines ({len(missing_required)}):")
        for slug, missing in sorted(missing_required)[:25]:
            print(f"  {slug}: missing {missing}")
        if len(missing_required) > 25:
            print(f"  ... and {len(missing_required) - 25} more")
        print()
    else:
        print("All item files have required structure.\n")

    if scaling_should_say_varies:
        print(f"Scaling items (index has >1 rarity) but file metadata not 'Rarity Varies' ({len(scaling_should_say_varies)}):")
        for slug in sorted(scaling_should_say_varies)[:20]:
            print(f"  {slug}")
        if len(scaling_should_say_varies) > 20:
            print(f"  ... and {len(scaling_should_say_varies) - 20} more")
        print()

    if single_should_not_say_varies:
        print(f"Single-rarity items (index has 1 rarity) but file says 'Rarity Varies' ({len(single_should_not_say_varies)}):")
        for slug in sorted(single_should_not_say_varies)[:20]:
            print(f"  {slug}")
        if len(single_should_not_say_varies) > 20:
            print(f"  ... and {len(single_should_not_say_varies) - 20} more")
        print()

    if unknown_sources:
        print(f"Items with Source = Unknown ({len(unknown_sources)}):")
        for slug in sorted(unknown_sources)[:30]:
            print(f"  {slug}")
        if len(unknown_sources) > 30:
            print(f"  ... and {len(unknown_sources) - 30} more")
        print()
    else:
        print("No items with Unknown source.\n")

    print(f"Total item files audited: {len(item_files)}")


if __name__ == "__main__":
    main()
