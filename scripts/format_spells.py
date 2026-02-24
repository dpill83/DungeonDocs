#!/usr/bin/env python3
"""
Standardize D&D 2024 spell markdown files to match dungeondocs-formatting-guide-spells.md.
Uses index.md as source of truth for Name, School, Spell lists, Casting Time, Range,
Components, Duration. Source (book) comes from data/spell_sources.csv (default: UNKNOWN).
Preserves spell body text exactly; only changes formatting and headers.
"""

import argparse
import csv
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SPELLS_DIR = REPO_ROOT / "docs" / "dnd2024" / "spells"
SPELLS_JSON = SPELLS_DIR / "spells.json"
DATA_DIR = REPO_ROOT / "data"
SOURCES_CSV = DATA_DIR / "spell_sources.csv"
FAILURES_JSON = DATA_DIR / "format_failures.json"
WARNINGS_CSV = DATA_DIR / "format_warnings.csv"

# Abbreviated material components: M(C) or M(C*) without description
COMPONENTS_ABBREV_RE = re.compile(r"M\s*\(\s*C\s*\*?\s*\)", re.IGNORECASE)

LEVEL_TAB_TO_LEVEL = {
    "Cantrip": 0,
    "1st Level": 1,
    "2nd Level": 2,
    "3rd Level": 3,
    "4th Level": 4,
    "5th Level": 5,
    "6th Level": 6,
    "7th Level": 7,
    "8th Level": 8,
    "9th Level": 9,
}

LEVEL_LABELS = [
    "Cantrip",
    "1st Level",
    "2nd Level",
    "3rd Level",
    "4th Level",
    "5th Level",
    "6th Level",
    "7th Level",
    "8th Level",
    "9th Level",
]

# Source code -> full book name (for italicized Source line)
SOURCE_RENDER = {
    "PHB2024": "Player's Handbook (2024)",
    "PHB": "Player's Handbook",
    "DMG": "Dungeon Master's Guide",
    "TCE": "Tasha's Cauldron of Everything",
    "XGE": "Xanathar's Guide to Everything",
    "FRHOF": "Forgotten Realms Heroes of the Forgotten",
    "SCAG": "Sword Coast Adventurer's Guide",
    "VGM": "Volo's Guide to Monsters",
    "MTF": "Mordenkainen's Tome of Foes",
    "EGW": "Explorer's Guide to Wildemount",
    "ERLW": "Eberron: Rising from the Last War",
    "AI": "Acquisitions Incorporated",
    "IDRotF": "Icewind Dale: Rime of the Frostmaiden",
}

# Stat-like line patterns (to skip when extracting body)
STAT_LABEL_PATTERNS = (
    r"^Casting Time:$",
    r"^Range:$",
    r"^Components:$",
    r"^Duration:$",
)
STAT_LABEL_RE = re.compile("|".join(STAT_LABEL_PATTERNS))

STAT_VALUE_PATTERNS = (
    r"^(Action|Reaction|Bonus Action|1 minute|Instantaneous|8 hours|1 hour|"
    r"1 round|10 minutes|24 hours|Touch|Self|Until dispelled|Special|"
    r"Up to 1 minute|Up to 1 hour|Up to 10 minutes|Up to 1 day|Up to 8 hours)$",
    r"^Concentration, up to .+$",
    r"^[0-9]+ (feet|miles?)$",
    r"^(C,? up to .+)$",
    r"^C up to .+$",
    r"^Action or R$",
    r"^1 minute or R$",
    r"^1 hour or R$",
    r"^10 minutes or R$",
    r"^Reaction\(\*\)$",
    r"^Bonus Action\(\*\)$",
    r"^Action or Ritual$",
)
STAT_VALUE_RE = re.compile("|".join(STAT_VALUE_PATTERNS), re.IGNORECASE)

# Components: V, S, M, or V, S, M (something with letters/numbers)
COMPONENTS_RE = re.compile(r"^(V|S|M|V, S|V, S, M|S, M)[,\s].*$", re.IGNORECASE)

# Level line (Cantrip X, 1st Level X, Level 1 X, etc.)
LEVEL_LINE_RE = re.compile(r"^(Cantrip|\d+(?:st|nd|rd|th) Level|Level \d+)\s+")

# Source line (Source: anything)
SOURCE_LINE_RE = re.compile(r"^Source:\s*", re.IGNORECASE)


def render_source(code: str) -> str:
    """Return italicized book name for Source line. Unknown/blank -> *Unknown*."""
    if not code or not str(code).strip():
        return "*Unknown*"
    c = str(code).strip()
    for key, full_name in SOURCE_RENDER.items():
        if key.upper() == c.upper():
            return f"*{full_name}*"
    return "*Unknown*"


def _normalize_name_for_lookup(name: str) -> str:
    """Normalize spell name for JSON lookup (apostrophe variants)."""
    if not name:
        return name
    # Replace common apostrophe/quote chars with straight quote for matching
    for c in ("'", "'", "'", "`", "\u2019"):
        name = name.replace(c, "'")
    return name


def load_components_from_json(json_path: Path) -> dict[str, str]:
    """
    Load spells.json and return mapping: normalized spell name -> components string.
    Only includes entries where components contain full material description (M ().
    """
    result: dict[str, str] = {}
    if not json_path.exists():
        return result
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return result
    for spell_name, entry in data.items():
        if not isinstance(entry, dict):
            continue
        comp = entry.get("components")
        if not isinstance(comp, str) or "M (" not in comp:
            continue
        result[_normalize_name_for_lookup(spell_name)] = comp
    return result


def is_abbreviated_components(components: str) -> bool:
    """True if components string uses M(C) or M(C*) placeholder without description."""
    return bool(COMPONENTS_ABBREV_RE.search(components))


def resolve_components(components: str, spell_name: str, json_components: dict[str, str]) -> str:
    """
    If components is abbreviated (M(C) / M(C*)), return full components from json_components
    when available; otherwise return original.
    """
    if not is_abbreviated_components(components):
        return components
    key = _normalize_name_for_lookup(spell_name)
    return json_components.get(key, components)

# Upcast heading variants to normalize
UPCAST_PATTERN = re.compile(
    r"(\*+\s*)?(Using a Higher-Level Spell Slot\.|At Higher Levels\.?)(\s*\*+)?",
    re.IGNORECASE,
)
UPCAST_REPLACEMENT = "**Using a Higher-Level Spell Slot.**  "


def parse_index(index_path: Path) -> dict[str, dict]:
    """Parse index.md into spell dict keyed by slug."""
    text = index_path.read_text(encoding="utf-8")
    spells: dict[str, dict] = {}
    current_level: int | None = None

    for line in text.splitlines():
        line = line.strip()
        # Check for tab header: === "Cantrip" or === "1st Level"
        tab_match = re.match(r'=== "([^"]+)"', line)
        if tab_match:
            label = tab_match.group(1)
            if label in LEVEL_TAB_TO_LEVEL:
                current_level = LEVEL_TAB_TO_LEVEL[label]
            continue

        if current_level is None:
            continue

        # Parse table row: | [Name](slug.md) | School | Spell lists | ...
        if not line.startswith("|") or not line.endswith("|"):
            continue

        parts = [c.strip() for c in line.split("|")[1:-1]]
        if len(parts) < 7:
            continue

        name_cell, school, spell_lists, casting_time, range_val, components, duration = parts[:7]
        if name_cell.lower() == "name" or not name_cell:
            continue

        # Extract name and slug from [Name](slug.md)
        link_match = re.match(r"\[([^\]]+)\]\(([^)]+)\.md\)", name_cell)
        if not link_match:
            continue

        name = link_match.group(1)
        slug = link_match.group(2)

        spells[slug] = {
            "name": name,
            "slug": slug,
            "level": current_level,
            "school": school,
            "spell_lists": spell_lists,
            "casting_time": casting_time,
            "range": range_val,
            "components": components,
            "duration": duration,
        }

    return spells


def normalize_duration(duration: str) -> str:
    """Convert C, up to X to Concentration, up to X."""
    if re.match(r"^C,?\s*up to ", duration, re.IGNORECASE):
        return re.sub(r"^C,?\s*", "Concentration, ", duration, flags=re.IGNORECASE)
    if re.match(r"^C up to ", duration, re.IGNORECASE):
        return re.sub(r"^C ", "Concentration, ", duration, flags=re.IGNORECASE)
    return duration


def is_stat_like_line(line: str) -> bool:
    """Return True if line looks like a stat block line (to skip when extracting body)."""
    stripped = line.strip()
    if not stripped:
        return False
    if STAT_LABEL_RE.match(stripped):
        return True
    if LEVEL_LINE_RE.match(stripped):
        return True
    if STAT_VALUE_RE.match(stripped):
        return True
    if COMPONENTS_RE.match(stripped):
        return True
    # Short fragments that are likely stat values
    if len(stripped) < 25 and stripped in (
        "Action", "Reaction", "Bonus Action", "Touch", "Self",
        "Instantaneous", "1 minute", "1 hour", "8 hours", "24 hours",
        "1 round", "10 minutes", "30 feet", "60 feet", "90 feet",
        "120 feet", "15 feet", "10 feet", "spell",
    ):
        return True
    # "Reaction, which you take when..." - casting time mixed with prose
    if stripped.startswith("Reaction,") or stripped.startswith("Bonus Action,"):
        return True
    return False


def is_preamble_line(line: str) -> bool:
    """
    Return True if line is part of header/stat preamble (to skip when extracting body).
    Strips ALL such content including repeated stat blocks.
    """
    stripped = line.strip()
    if not stripped:
        return True
    if stripped.startswith("# "):
        return True
    if stripped.startswith("<!--") and stripped.endswith("-->"):
        return True
    if SOURCE_LINE_RE.match(stripped):
        return True
    if LEVEL_LINE_RE.match(stripped):
        return True
    if stripped.startswith("Casting Time:") or stripped.startswith("Range:") or stripped.startswith("Components:") or stripped.startswith("Duration:"):
        return True
    if is_stat_like_line(stripped):
        return True
    return False


def extract_body(content: str, spell_slug: str, warnings: list[tuple[str, str, str]]) -> str:
    """
    Extract spell body text from content. Strips ALL leading header/stat preamble
    (title, Source, level line, stat block - including any duplicate copies).
    Returns body with upcast heading normalized.
    """
    lines = content.splitlines()
    body_start_idx = len(lines)

    for i, line in enumerate(lines):
        if not is_preamble_line(line):
            body_start_idx = i
            break

    body_lines = lines[body_start_idx:]
    body = "\n".join(body_lines).strip()

    if not body:
        warnings.append((spell_slug, "empty_body", "No body text found after stat block"))

    # Normalize upcast heading
    body = normalize_upcast_heading(body)

    return body


def normalize_upcast_heading(body: str) -> str:
    """Replace upcast heading variants with guide format."""
    return UPCAST_PATTERN.sub(UPCAST_REPLACEMENT, body)


def load_or_create_sources(spell_slugs: set[str]) -> dict[str, str]:
    """Load spell_sources.csv; create if missing. Return slug -> source mapping."""
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

    # Ensure all spells have an entry; default UNKNOWN
    for slug in spell_slugs:
        if slug not in sources:
            sources[slug] = "UNKNOWN"

    return sources


def save_sources(sources: dict[str, str], spell_data: dict[str, dict]) -> None:
    """Save spell_sources.csv, preserving non-UNKNOWN values."""
    rows = []
    for slug, source in sorted(sources.items()):
        name = spell_data.get(slug, {}).get("name", slug)
        rows.append({"slug": slug, "name": name, "source": source, "notes": ""})

    with open(SOURCES_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["slug", "name", "source", "notes"])
        writer.writeheader()
        writer.writerows(rows)


def format_spell_page(
    spell: dict,
    source: str,
    body: str,
) -> str:
    """Build the formatted spell page content."""
    level_label = LEVEL_LABELS[spell["level"]]
    duration = normalize_duration(spell["duration"])
    source_display = render_source(source)

    parts = [
        f"# {spell['name']}",
        "",
        f"Source: {source_display}",
        "",
        f"{level_label} {spell['school']} ({spell['spell_lists']})",
        "",
        f"Casting Time: {spell['casting_time']}",
        f"Range: {spell['range']}",
        f"Components: {spell['components']}",
        f"Duration: {duration}",
        "",
        body,
    ]
    return "\n".join(parts)


def get_spell_files() -> list[Path]:
    """Return list of spell .md files to process (exclude index, all, school pages, spells)."""
    exclude = {"index.md", "all.md", "spells.md"}
    files = []
    for f in SPELLS_DIR.glob("*.md"):
        if f.name in exclude:
            continue
        if f.name.endswith("-school.md"):
            continue
        files.append(f)
    return sorted(files)


def update_index_components(index_path: Path, spells: dict[str, dict]) -> None:
    """
    Rewrite index.md so each table row's Components cell uses the resolved (enriched)
    components from the spells dict. Preserves table structure and other columns.
    Handles both 8-column (Name | Level | ... | Components) and 7-column (Name | School | ... | Components) tables.
    """
    lines = index_path.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            out.append(line)
            continue
        parts = [p.strip() for p in stripped.split("|")[1:-1]]
        if len(parts) < 7 or parts[0].lower() == "name":
            out.append(line)
            continue
        link_match = re.match(r"\[([^\]]+)\]\(([^)]+)\.md\)", parts[0])
        if not link_match:
            out.append(line)
            continue
        slug = link_match.group(2)
        if slug not in spells:
            out.append(line)
            continue
        # Components: 8-column table -> index 6; 7-column table -> index 5
        comp_idx = 6 if len(parts) >= 8 else 5
        parts[comp_idx] = spells[slug]["components"]
        prefix = line[: len(line) - len(line.lstrip())]
        out.append(prefix + "| " + " | ".join(parts) + " |")
    index_path.write_text("\n".join(out) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Format spell markdown files")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Write to spells_formatted/ instead of overwriting in place",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output directory (default: spells_formatted/ when dry-run, else in-place)",
    )
    args = parser.parse_args()

    output_dir: Path | None = None
    if args.dry_run or args.output:
        output_dir = Path(args.output) if args.output else REPO_ROOT / "spells_formatted"
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Dry run: writing to {output_dir}")

    # Parse index
    index_path = SPELLS_DIR / "index.md"
    if not index_path.exists():
        print("ERROR: index.md not found")
        return

    spells = parse_index(index_path)
    print(f"Parsed {len(spells)} spells from index.md")

    # Enrich components from spells.json when index has M(C) / M(C*)
    json_components = load_components_from_json(SPELLS_JSON)
    for slug, spell in spells.items():
        spell["components"] = resolve_components(
            spell["components"], spell["name"], json_components
        )

    # Update index.md Components column when writing in place
    if output_dir is None:
        update_index_components(index_path, spells)

    # Load/create sources
    spell_slugs = set(spells.keys())
    sources = load_or_create_sources(spell_slugs)
    save_sources(sources, spells)

    failures: dict[str, list[str]] = {"not_in_index": [], "parse_errors": []}
    warnings: list[tuple[str, str, str]] = []
    processed = 0

    spell_files = get_spell_files()

    for fpath in spell_files:
        slug = fpath.stem
        if slug not in spells:
            failures["not_in_index"].append(slug)
            continue

        spell = spells[slug]
        source = sources.get(slug, "UNKNOWN")

        try:
            content = fpath.read_text(encoding="utf-8")
        except Exception as e:
            failures["parse_errors"].append(f"{slug}: {e}")
            continue

        body = extract_body(content, slug, warnings)
        formatted = format_spell_page(spell, source, body)

        out_path = output_dir / fpath.name if output_dir else fpath
        if output_dir:
            out_path = output_dir / fpath.name
        else:
            out_path = fpath

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(formatted, encoding="utf-8")
        processed += 1

    # Write logs
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(FAILURES_JSON, "w", encoding="utf-8") as f:
        json.dump(failures, f, indent=2)

    with open(WARNINGS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["slug", "warning_type", "message"])
        writer.writerows(warnings)

    # Summary
    print(f"Processed: {processed}")
    print(f"Not in index: {len(failures['not_in_index'])}")
    print(f"Parse errors: {len(failures['parse_errors'])}")
    print(f"Warnings: {len(warnings)}")
    print(f"Failures: {FAILURES_JSON}")
    print(f"Warnings: {WARNINGS_CSV}")


if __name__ == "__main__":
    main()
