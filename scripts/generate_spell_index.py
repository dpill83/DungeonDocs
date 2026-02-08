#!/usr/bin/env python3
"""
Generate docs/dnd2024/spells/index.md (All Spells with level tabs) and
regenerate the eight *-school.md pages with level tabs and proper tables.
Reads from class spell-list.md files; builds merged spell data and name->slug from existing spell files.
"""

import re
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
SPELLS_DIR = DOCS / "dnd2024" / "spells"
CLASSES_DIR = DOCS / "dnd2024" / "classes"

# Level section headers in spell-list.md -> level index (0 = Cantrip, 1 = 1st, ...)
LEVEL_HEADERS = [
    "## Cantrips",
    "## 1st-Level Spells",
    "## 2nd-Level Spells",
    "## 3rd-Level Spells",
    "## 4th-Level Spells",
    "## 5th-Level Spells",
    "## 6th-Level Spells",
    "## 7th-Level Spells",
    "## 8th-Level Spells",
    "## 9th-Level Spells",
]
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
SCHOOLS = [
    "Abjuration",
    "Conjuration",
    "Divination",
    "Enchantment",
    "Evocation",
    "Illusion",
    "Necromancy",
    "Transmutation",
]
SCHOOL_FILES = [s.lower().replace(" ", "-") + "-school.md" for s in SCHOOLS]


def normalize_name_to_key(name: str) -> str:
    """Normalize spell name for matching: strip markdown bold, collapse punctuation/spaces."""
    s = name.strip()
    if s.startswith("**") and s.endswith("**"):
        s = s[2:-2].strip()
    s = re.sub(r"[\s'\/]+", " ", s).lower().strip()
    return s


def slug_to_key(slug: str) -> str:
    """Convert filename slug to same key format as normalize_name_to_key."""
    return slug.replace("-", " ").lower()


def build_slug_map() -> dict[str, str]:
    """Build name_key -> slug from existing spell .md files (exclude school pages and index)."""
    slug_map: dict[str, str] = {}
    for f in SPELLS_DIR.glob("*.md"):
        if f.name.endswith("-school.md") or f.name in ("index.md", "all.md"):
            continue
        slug = f.stem
        key = slug_to_key(slug)
        slug_map[key] = slug
    return slug_map


def parse_table_row(line: str) -> list[str] | None:
    """Parse a markdown table row into cells. Returns None if not a valid data row."""
    line = line.strip()
    if not line.startswith("|") or not line.endswith("|"):
        return None
    parts = [c.strip() for c in line.split("|")[1:-1]]
    if len(parts) < 7:
        return None
    return parts[:7]


def header_to_level(stripped: str) -> int | None:
    """Map a section header to level index (0 = Cantrip, 1 = 1st, ...). Returns None if not a level header."""
    for lev, header in enumerate(LEVEL_HEADERS):
        if stripped == header:
            return lev
    if stripped in ("## Cantrips", "### Cantrips"):
        return 0
    m = re.match(r"^##+ Level (\d) Spells?$", stripped)
    if m:
        return int(m.group(1))
    m = re.match(r"^### (\d)(?:st|nd|rd|th) Level$", stripped)
    if m:
        return int(m.group(1))
    return None


def parse_spell_list(path: Path) -> list[tuple[int, str, str, str, str, str, str]]:
    """Parse a class spell-list.md; return list of (level_index, name, school, spell_lists, casting_time, range, components, duration)."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    result: list[tuple[int, str, str, str, str, str, str]] = []
    current_level: int | None = None

    for i, line in enumerate(lines):
        stripped = line.strip()
        level_from_header = header_to_level(stripped)
        if level_from_header is not None:
            current_level = level_from_header
        if current_level is None:
            continue
        parts = parse_table_row(line)
        if not parts:
            continue
        name, school, spell_lists, casting_time, range_val, components, duration = parts
        if name.lower() == "name" or not name:
            continue
        result.append((current_level, name, school, spell_lists, casting_time, range_val, components, duration))

    return result


def merge_spell_data(slug_map: dict[str, str]) -> dict[str, dict]:
    """
    Parse all class spell-list.md files and merge by slug.
    Returns dict slug -> { level, name, school, spell_lists, casting_time, range, components, duration }.
    name is first seen display name; spell_lists is merged (unique, sorted).
    """
    spell_lists_paths = list(CLASSES_DIR.glob("*/spell-list.md"))
    merged: dict[str, dict] = {}

    for path in spell_lists_paths:
        for level, name, school, spell_lists, casting_time, range_val, components, duration in parse_spell_list(path):
            key = normalize_name_to_key(name)
            slug = slug_map.get(key)
            if not slug:
                continue
            if slug not in merged:
                merged[slug] = {
                    "level": level,
                    "name": name.strip(),
                    "school": school.strip(),
                    "spell_lists": set(),
                    "casting_time": casting_time.strip(),
                    "range": range_val.strip(),
                    "components": components.strip(),
                    "duration": duration.strip(),
                }
            for part in re.split(r",\s*", spell_lists):
                merged[slug]["spell_lists"].add(part.strip())
            merged[slug]["level"] = level
            merged[slug]["school"] = school.strip()
            merged[slug]["casting_time"] = casting_time.strip()
            merged[slug]["range"] = range_val.strip()
            merged[slug]["components"] = components.strip()
            merged[slug]["duration"] = duration.strip()

    for slug, data in merged.items():
        data["spell_lists"] = ", ".join(sorted(data["spell_lists"]))

    return merged


def escape_table_cell(s: str) -> str:
    """Escape pipe in table cells for markdown."""
    return s.replace("|", "\\|")


def update_class_spell_lists(slug_map: dict[str, str]) -> None:
    """
    Rewrite each class spell-list.md to replace spell names with links to spell pages.
    Uses ../../spells/{slug}.md as the relative path from classes/{class}/spell-list.md.
    """
    spell_list_paths = list(CLASSES_DIR.glob("*/spell-list.md"))
    for path in spell_list_paths:
        lines = path.read_text(encoding="utf-8").splitlines()
        new_lines: list[str] = []
        unmapped: list[str] = []

        for line in lines:
            stripped = line.strip()
            if not stripped.startswith("|") or not stripped.endswith("|"):
                new_lines.append(line)
                continue

            parts = [c.strip() for c in stripped.split("|")[1:-1]]
            if len(parts) < 2:
                new_lines.append(line)
                continue

            name_cell = parts[0]
            if not name_cell or name_cell.lower() == "name":
                new_lines.append(line)
                continue

            # Skip separator rows
            if re.match(r"^[\s\-]+$", name_cell):
                new_lines.append(line)
                continue

            # Extract display name: strip ** or extract from [Text](url)
            display_name = name_cell
            link_match = re.match(r"\[([^\]]+)\]\([^)]+\)", name_cell)
            if link_match:
                display_name = link_match.group(1).strip()
            elif display_name.startswith("**") and display_name.endswith("**"):
                display_name = display_name[2:-2].strip()

            key = normalize_name_to_key(display_name)
            slug = slug_map.get(key)
            if not slug and " s " in key:
                slug = slug_map.get(key.replace(" s ", "s "))
            if slug:
                link_cell = f"[{escape_table_cell(display_name)}](../../spells/{slug}.md)"
                parts[0] = link_cell
                new_lines.append("| " + " | ".join(parts) + " |")
            else:
                unmapped.append(f"{path.name}: {display_name}")
                new_lines.append(line)

        path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        if unmapped:
            for u in unmapped[:5]:  # log first 5 per file
                print(f"  Unmapped: {u}")
            if len(unmapped) > 5:
                print(f"  ... and {len(unmapped) - 5} more in {path.name}")

    print("Updated class spell lists with spell links.")


def table_row(display_name: str, slug: str, school: str, spell_lists: str, casting_time: str, range_val: str, components: str, duration: str) -> str:
    clean_name = display_name.strip()
    if clean_name.startswith("**") and clean_name.endswith("**"):
        clean_name = clean_name[2:-2].strip()
    link = f"[{escape_table_cell(clean_name)}]({slug}.md)"
    return f"| {link} | {escape_table_cell(school)} | {escape_table_cell(spell_lists)} | {escape_table_cell(casting_time)} | {escape_table_cell(range_val)} | {escape_table_cell(components)} | {escape_table_cell(duration)} |"


def render_tabbed_tables(spells_by_level: dict[int, list[dict]], school_filter: str | None = None) -> str:
    """Render level tabs; each tab has a table. If school_filter is set, only include that school."""
    out: list[str] = []
    for level in range(10):
        rows = spells_by_level.get(level, [])
        if school_filter:
            rows = [r for r in rows if r["school"] == school_filter]
        if not rows:
            out.append(f'=== "{LEVEL_LABELS[level]}"\n')
            out.append("    No spells in this category.\n")
            continue
        out.append(f'=== "{LEVEL_LABELS[level]}"\n')
        out.append("    | Name | School | Spell lists | Casting Time | Range | Components | Duration |\n")
        out.append("    |------|--------|-------------|--------------|-------|------------|----------|\n")
        for r in rows:
            out.append("    " + table_row(
                r["name"], r["slug"], r["school"], r["spell_lists"],
                r["casting_time"], r["range"], r["components"], r["duration"]
            ) + "\n")
    return "".join(out)


def main() -> None:
    slug_map = build_slug_map()
    merged = merge_spell_data(slug_map)

    spells_by_level: dict[int, list[dict]] = {i: [] for i in range(10)}
    for slug, data in merged.items():
        level = data["level"]
        spells_by_level[level].append({
            "slug": slug,
            "name": data["name"],
            "school": data["school"],
            "spell_lists": data["spell_lists"],
            "casting_time": data["casting_time"],
            "range": data["range"],
            "components": data["components"],
            "duration": data["duration"],
        })

    for level in range(10):
        spells_by_level[level].sort(key=lambda r: (r["name"].lower(), r["slug"]))

    index_content = "# All Spells\n\n"
    index_content += "Spells by level. Click a spell name to open its page.\n\n"
    index_content += render_tabbed_tables(spells_by_level, school_filter=None)

    (SPELLS_DIR / "index.md").write_text(index_content, encoding="utf-8")

    for school, filename in zip(SCHOOLS, SCHOOL_FILES):
        school_content = f"# {school} School\n\n"
        school_content += f"Spells of the {school} school. [All Spells](index.md).\n\n"
        school_content += render_tabbed_tables(spells_by_level, school_filter=school)
        (SPELLS_DIR / filename).write_text(school_content, encoding="utf-8")

    print("Generated index.md and 8 *-school.md files.")

    update_class_spell_lists(slug_map)


if __name__ == "__main__":
    main()
