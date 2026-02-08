#!/usr/bin/env python3
"""
Standardize D&D 2024 magic item markdown files to a consistent format.
Uses all.md (index) as source of truth for name, item_type, rarity, attunement.
Source (book) comes from data/item_sources.csv (default: UNKNOWN).
Preserves item body text exactly; only changes formatting and headers.
"""

import argparse
import csv
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ITEMS_DIR = REPO_ROOT / "docs" / "dnd2024" / "magic-items"
DATA_DIR = REPO_ROOT / "data"
INDEX_FILE = ITEMS_DIR / "all.md"
SOURCES_CSV = DATA_DIR / "item_sources.csv"
FAILURES_JSON = DATA_DIR / "item_format_failures.json"
WARNINGS_CSV = DATA_DIR / "item_format_warnings.csv"
SCALING_ITEMS_CSV = DATA_DIR / "item_scaling_items.csv"

# Section header -> rarity
RARITY_FROM_HEADING = {
    "common magic items": "Common",
    "uncommon magic items": "Uncommon",
    "rare magic items": "Rare",
    "very rare magic items": "Very Rare",
    "legendary magic items": "Legendary",
    "artifacts": "Artifact",
}

# Source code -> full book name (for italicized Source line).
# Lookup is case-insensitive and whitespace-insensitive (e.g. "DMG 2024" and "DMG2024" resolve the same).
SOURCE_RENDER = {
    "DMG2024": "Dungeon Master's Guide (2024)",
    "PHB2024": "Player's Handbook (2024)",
    "PHB": "Player's Handbook",
    "DMG": "Dungeon Master's Guide",
    "TCE": "Tasha's Cauldron of Everything",
    "XGE": "Xanathar's Guide to Everything",
    "FRHOF": "Forgotten Realms - Heroes of Faerun",
    "FRAIF": "Forgotten Realms: Adventures in Faerun",
    "EFOTA": "Essentials from the Outer Planes",
    "WTTHC": "Wanderer's Tales from the Witchlight Carnival",
    "LFL": "Lost Fragments of Lost Lore",
    "NF": "Netherdeep",
    "UNI AND THE HUNT FOR THE LOST HORN": "Uni and the Hunt for the Lost Horn",
    "SCAG": "Sword Coast Adventurer's Guide",
    "VGM": "Volo's Guide to Monsters",
    "MTF": "Mordenkainen's Tome of Foes",
    "EGW": "Explorer's Guide to Wildemount",
    "ERLW": "Eberron: Rising from the Last War",
}

# Normalized key -> italicized full name (built at module load)
def _normalize_source_code(code: str) -> str:
    """Case- and whitespace-insensitive key for source lookup."""
    return re.sub(r"\s+", "", (code or "").strip().upper())


SOURCE_RENDER_NORMALIZED = {
    _normalize_source_code(k): f"*{v}*" for k, v in SOURCE_RENDER.items()
}

SOURCE_LINE_RE = re.compile(r"^Source:\s*", re.IGNORECASE)

# Preamble type/rarity line only: our exact output format (Type, Rarity or Type, Rarity, requires attunement).
# Do NOT match variant breakdown lines in body (e.g. "Weapon (Any Ammunition), Uncommon(+1), Rare (+2), or Very Rare (+3)").
SINGLE_RARITIES = r"(?:Rarity Varies|Common|Uncommon|Rare|Very Rare|Legendary|Artifact)"
TYPE_RARITY_LINE_RE = re.compile(
    r"^\s*\*?\s*[A-Za-z][A-Za-z\s]+,\s*"
    + SINGLE_RARITIES
    + r"(?:\s*,\s*requires attunement(?:\s+by\s+[^,*]+)?)?\s*\*?\s*$"
)


def looks_like_variant_breakdown(line: str) -> bool:
    """True if line looks like body variant text (e.g. Uncommon(+1), Rare (+2), or Very Rare (+3))."""
    stripped = line.strip()
    if " or " in stripped:
        return True
    if re.search(r"\(\+\d\)", stripped):
        return True
    return False


def render_source(code: str) -> str:
    """Return italicized book name for Source line. Lookup is case- and whitespace-insensitive. Unknown/blank -> *Unknown*."""
    if not code or not str(code).strip():
        return "*Unknown*"
    key = _normalize_source_code(str(code))
    return SOURCE_RENDER_NORMALIZED.get(key, "*Unknown*")


def parse_index(index_path: Path) -> dict[str, dict]:
    """Parse all.md into item dict keyed by slug."""
    text = index_path.read_text(encoding="utf-8")
    items: dict[str, dict] = {}
    current_rarity: str | None = None

    for line in text.splitlines():
        stripped = line.strip()

        # Section header: ## Common Magic Items, ## Artifacts, etc.
        if stripped.startswith("## "):
            heading = stripped[3:].strip().lower()
            current_rarity = RARITY_FROM_HEADING.get(heading)
            continue

        if current_rarity is None:
            continue

        # Table row: | [Name](slug.md) | Type | Attunement | Price | [Consumable] |
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue

        parts = [p.strip() for p in stripped.split("|")[1:-1]]
        if len(parts) < 4:
            continue

        # Use first 4 columns; 5th (Consumable) if present is ignored
        name_cell, item_type, attunement_cell, _price = parts[:4]
        if name_cell.lower() == "item name" or not name_cell:
            continue

        link_match = re.match(r"\[([^\]]+)\]\(([^)]+)\.md\)", name_cell)
        if not link_match:
            continue

        name = link_match.group(1)
        slug = link_match.group(2)

        attunement = None
        if attunement_cell and attunement_cell.replace("—", "").replace("-", "").strip():
            a = attunement_cell.strip()
            if "attunement" in a.lower():
                attunement = "requires attunement" if a.lower() == "requires attunement" else a

        if slug in items:
            items[slug]["rarities"].add(current_rarity)
        else:
            items[slug] = {
                "name": name,
                "slug": slug,
                "item_type": item_type.strip(),
                "rarities": {current_rarity},
                "attunement": attunement,
            }

    return items


def rarity_display(rarities: set[str]) -> str:
    """If multiple rarities, return 'Rarity Varies'; else return the single rarity."""
    if len(rarities) > 1:
        return "Rarity Varies"
    if len(rarities) == 1:
        return next(iter(rarities))
    return "Rarity Varies"


def is_preamble_line(line: str) -> bool:
    """Return True if line is part of preamble (to skip when extracting body).
    Do NOT treat variant breakdown lines in body as preamble (e.g. 'Uncommon(+1), Rare (+2), or Very Rare (+3)').
    """
    stripped = line.strip()
    if not stripped:
        return True
    if stripped.startswith("# "):
        return True
    if stripped.startswith("<!--") and "-->" in stripped:
        return True
    if stripped.startswith("<!--"):
        return True
    if stripped.endswith("-->"):
        return True
    if SOURCE_LINE_RE.match(stripped):
        return True
    if looks_like_variant_breakdown(line):
        return False
    if TYPE_RARITY_LINE_RE.match(stripped):
        return True
    return False


def extract_body(content: str, item_slug: str, warnings: list[tuple[str, str, str]]) -> str:
    """
    Extract item body from content. Strips ALL leading preamble (title, comments,
    Source, type/rarity line, and any duplicate copies). Returns body unchanged.
    """
    lines = content.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Multi-line HTML comment
        if stripped.startswith("<!--") and "-->" not in stripped:
            i += 1
            while i < len(lines) and "-->" not in lines[i]:
                i += 1
            if i < len(lines):
                i += 1
            continue

        if not is_preamble_line(line):
            break
        i += 1

    body_lines = lines[i:]
    body = "\n".join(body_lines).strip()

    if not body:
        warnings.append((item_slug, "empty_body", "No body text found after preamble"))

    return body


def load_or_create_sources(item_slugs: set[str], item_data: dict[str, dict]) -> dict[str, str]:
    """Load item_sources.csv; create if missing. Return slug -> source (normalized upper for lookup)."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    sources: dict[str, str] = {}
    if SOURCES_CSV.exists():
        with open(SOURCES_CSV, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                slug = row.get("slug", "").strip()
                source = row.get("source", "UNKNOWN").strip()
                if slug:
                    sources[slug] = source

    for slug in item_slugs:
        if slug not in sources:
            sources[slug] = "UNKNOWN"

    return sources


def save_sources(sources: dict[str, str], item_data: dict[str, dict]) -> None:
    """Save item_sources.csv, preserving non-UNKNOWN values."""
    rows = []
    for slug, source in sorted(sources.items()):
        name = item_data.get(slug, {}).get("name", slug)
        rows.append({"slug": slug, "name": name, "source": source.upper(), "notes": ""})

    with open(SOURCES_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["slug", "name", "source", "notes"])
        writer.writeheader()
        writer.writerows(rows)


def format_item_page(item: dict, source: str, body: str) -> str:
    """Build the formatted magic item page content. Uses rarity_display (Rarity Varies if multi-rarity)."""
    source_display = render_source(source)
    rarities = item.get("rarities", set())
    if isinstance(rarities, str):
        rarities = {rarities}
    disp = rarity_display(rarities)
    type_rarity = f"{item['item_type']}, {disp}"
    if item.get("attunement"):
        type_rarity += f", {item['attunement']}"

    parts = [
        f"# {item['name']}",
        "",
        f"Source: {source_display}",
        "",
        type_rarity,
        "",
        body,
    ]
    return "\n".join(parts)


def get_item_files() -> list[Path]:
    """Return list of item .md files to process (exclude index/list/category pages)."""
    exclude = {"all.md", "consumable.md", "crafting.md", "crafting-magical-items.md", "index.md"}
    files = []
    for f in ITEMS_DIR.glob("*.md"):
        if f.name.lower() in exclude:
            continue
        files.append(f)
    return sorted(files)


def main() -> None:
    parser = argparse.ArgumentParser(description="Format magic item markdown files")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Write to items_formatted/ instead of overwriting in place",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output directory (default: items_formatted/ when dry-run, else in-place)",
    )
    args = parser.parse_args()

    output_dir: Path | None = None
    if args.dry_run or args.output:
        output_dir = Path(args.output) if args.output else REPO_ROOT / "items_formatted"
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Dry run: writing to {output_dir}")

    if not INDEX_FILE.exists():
        print(f"ERROR: index not found: {INDEX_FILE}")
        return

    items = parse_index(INDEX_FILE)
    print(f"Parsed {len(items)} items from {INDEX_FILE.name}")

    scaling_items = [
        {"slug": slug, "name": item["name"], "rarities_found": ",".join(sorted(item["rarities"]))}
        for slug, item in items.items()
        if len(item["rarities"]) > 1
    ]
    print(f"Scaling items (multi-rarity): {len(scaling_items)}")

    item_slugs = set(items.keys())
    sources = load_or_create_sources(item_slugs, items)
    save_sources(sources, items)

    # One-time diagnostic: total items, distinct source codes, codes not in SOURCE_RENDER
    distinct_codes = set(sources.values())
    missing_render = sorted([c for c in distinct_codes if c and render_source(c) == "*Unknown*"])
    print(f"Source diagnostic: {len(sources)} items, {len(distinct_codes)} distinct source code(s).")
    if missing_render:
        print(f"  Codes not in SOURCE_RENDER: {missing_render}")
    else:
        print("  All source codes have SOURCE_RENDER entries.")

    failures: dict[str, list[str]] = {"not_in_index": [], "parse_errors": []}
    warnings: list[tuple[str, str, str]] = []
    processed = 0

    for fpath in get_item_files():
        slug = fpath.stem
        if slug not in items:
            failures["not_in_index"].append(slug)
            continue

        item = items[slug]
        source = sources.get(slug, "UNKNOWN")

        try:
            content = fpath.read_text(encoding="utf-8")
        except Exception as e:
            failures["parse_errors"].append(f"{slug}: {e}")
            continue

        body = extract_body(content, slug, warnings)
        formatted = format_item_page(item, source, body)

        out_path = output_dir / fpath.name if output_dir else fpath
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(formatted, encoding="utf-8")
        processed += 1

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(FAILURES_JSON, "w", encoding="utf-8") as f:
        json.dump(failures, f, indent=2)

    with open(WARNINGS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["slug", "warning_type", "message"])
        writer.writerows(warnings)

    with open(SCALING_ITEMS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["slug", "name", "rarities_found"])
        writer.writeheader()
        writer.writerows(scaling_items)

    print(f"Processed: {processed}")
    print(f"Not in index: {len(failures['not_in_index'])}")
    print(f"Parse errors: {len(failures['parse_errors'])}")
    print(f"Warnings: {len(warnings)}")
    print(f"Scaling items: {len(scaling_items)}")
    print(f"Failures: {FAILURES_JSON}")
    print(f"Warnings: {WARNINGS_CSV}")
    print(f"Scaling list: {SCALING_ITEMS_CSV}")


if __name__ == "__main__":
    main()
