#!/usr/bin/env python3
"""
Spells missing material component descriptions: generate a fill-in list or apply your edits.

  --generate   (default) Write data/spells_missing_material_components.txt with a blank
               "component: " line under each spell. Fill in the description after the colon.

  --apply      Read the txt file, apply any filled-in "component:" lines to the spell .md
               files and index.md, then regenerate the txt with only spells still missing.
"""

import argparse
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SPELLS_DIR = REPO_ROOT / "docs" / "dnd2024" / "spells"
INDEX_PATH = SPELLS_DIR / "index.md"
DATA_DIR = REPO_ROOT / "data"
OUTPUT_FILE = DATA_DIR / "spells_missing_material_components.txt"

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

COMPONENTS_ABBREV_RE = re.compile(r"M\s*\(\s*C\s*\*?\s*\)", re.IGNORECASE)


def has_material_but_not_described(components: str) -> bool:
    """True if components include M but do not give the full material description."""
    if "M" not in components:
        return False
    if COMPONENTS_ABBREV_RE.search(components):
        return True
    if "M (" not in components:
        return True
    return False


def parse_index(index_path: Path) -> dict[str, dict]:
    """Parse index.md into spell dict keyed by slug (from level tabs)."""
    text = index_path.read_text(encoding="utf-8")
    spells: dict[str, dict] = {}
    current_level: int | None = None

    for line in text.splitlines():
        line = line.strip()
        tab_match = re.match(r'=== "([^"]+)"', line)
        if tab_match:
            label = tab_match.group(1)
            if label in LEVEL_TAB_TO_LEVEL:
                current_level = LEVEL_TAB_TO_LEVEL[label]
            continue

        if current_level is None:
            continue

        if not line.startswith("|") or not line.endswith("|"):
            continue

        parts = [c.strip() for c in line.split("|")[1:-1]]
        if len(parts) < 7:
            continue

        name_cell, school, spell_lists, casting_time, range_val, components, duration = parts[:7]
        if name_cell.lower() == "name" or not name_cell:
            continue

        link_match = re.match(r"\[([^\]]+)\]\(([^)]+)\.md\)", name_cell)
        if not link_match:
            continue

        name = link_match.group(1)
        slug = link_match.group(2)

        spells[slug] = {
            "name": name,
            "slug": slug,
            "level": current_level,
            "components": components,
        }

    return spells


def build_components_with_material(current: str, material_description: str) -> str:
    """Replace M / M(C) / M(C*) with M (material_description)."""
    desc = material_description.strip()
    if not desc:
        return current
    # M(C) or M(C*) -> M (description)
    new_val = COMPONENTS_ABBREV_RE.sub(f"M ({desc})", current)
    if new_val != current:
        return new_val
    # Bare M (e.g. "V, S, M") -> M (description)
    new_val = re.sub(r"\bM\b", f"M ({desc})", current, count=1)
    return new_val


def generate_txt(spells: dict[str, dict]) -> None:
    """Write fill-in-the-blank txt; only spells missing material description."""
    missing = [
        (s["name"], s["slug"], s["components"])
        for s in spells.values()
        if has_material_but_not_described(s["components"])
    ]
    missing.sort(key=lambda x: (x[0].lower(), x[1]))

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "Spells with Material (M) components but no full description.",
        "Fill in the 'component:' line for each spell. Then run:",
        "  python scripts/list_spells_missing_material_components.py --apply",
        "to update the spell pages and index, and regenerate this list.",
        "",
        "Format: spellcasting focus can substitute unless there's a cost or consumed note.",
        "Example: component: diamonds worth 300 gp, which the spell consumes",
        "",
        "---",
        "",
    ]
    for name, slug, components in missing:
        lines.append(f"{name}")
        lines.append(f"  slug: {slug}")
        lines.append(f"  file: docs/dnd2024/spells/{slug}.md")
        lines.append(f"  current Components: {components}")
        lines.append("  component: ")
        lines.append("")

    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {len(missing)} spells to {OUTPUT_FILE}")


def parse_fill_in_txt(content: str) -> list[tuple[str, str, str, str]]:
    """
    Parse the fill-in file. Returns list of (name, slug, current_components, filled_component).
    filled_component is empty if they didn't fill in anything.
    """
    blocks = content.split("\n\n")
    result = []
    for block in blocks:
        block = block.strip()
        if not block or block.startswith("Spells with") or block.startswith("Fill in") or block.startswith("Format:") or block.startswith("Example:") or block == "---":
            continue
        lines = block.splitlines()
        name = slug = current = filled = ""
        for line in lines:
            line_stripped = line.strip()
            if line_stripped.startswith("slug:"):
                slug = line_stripped[5:].strip()
            elif line_stripped.startswith("current Components:"):
                current = line_stripped[len("current Components:"):].strip()
            elif line_stripped.startswith("component:"):
                filled = line_stripped[len("component:"):].strip()
            elif line_stripped and not line_stripped.startswith("file:"):
                name = line_stripped
        if slug and current and has_material_but_not_described(current):
            result.append((name, slug, current, filled))
    return result


def update_spell_md(slug: str, new_components: str) -> None:
    """Set Components: line in docs/dnd2024/spells/<slug>.md."""
    path = SPELLS_DIR / f"{slug}.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r"^Components: .+$",
        f"Components: {new_components}",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    path.write_text(text, encoding="utf-8")


def update_index_components(index_path: Path, spells: dict[str, dict]) -> None:
    """Set Components cell for each spell in index.md (8- and 7-column tables)."""
    lines = index_path.read_text(encoding="utf-8").splitlines()
    out = []
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
        comp_idx = 6 if len(parts) >= 8 else 5
        parts[comp_idx] = spells[slug]["components"]
        prefix = line[: len(line) - len(line.lstrip())]
        out.append(prefix + "| " + " | ".join(parts) + " |")
    index_path.write_text("\n".join(out) + "\n", encoding="utf-8")


def apply_txt(spells_index: dict[str, dict]) -> int:
    """
    Read OUTPUT_FILE, apply filled-in component lines to .md and index, return count applied.
    """
    if not OUTPUT_FILE.exists():
        print(f"File not found: {OUTPUT_FILE}")
        return 0

    content = OUTPUT_FILE.read_text(encoding="utf-8")
    entries = parse_fill_in_txt(content)
    applied = 0
    updated_spells = dict(spells_index)

    for name, slug, current_components, filled in entries:
        if not filled:
            continue
        new_components = build_components_with_material(current_components, filled)
        if new_components == current_components:
            continue
        update_spell_md(slug, new_components)
        updated_spells[slug] = {**spells_index.get(slug, {}), "components": new_components}
        applied += 1

    if applied:
        update_index_components(INDEX_PATH, updated_spells)
    return applied


def main() -> None:
    parser = argparse.ArgumentParser(description="Spells missing material components: generate list or apply edits")
    parser.add_argument("--apply", action="store_true", help="Apply filled-in component lines and regenerate list")
    args = parser.parse_args()

    if not INDEX_PATH.exists():
        print(f"ERROR: {INDEX_PATH} not found")
        return

    spells = parse_index(INDEX_PATH)

    if args.apply:
        n = apply_txt(spells)
        print(f"Applied {n} component description(s).")
        # Regenerate list from current index (so spell data is up to date)
        spells = parse_index(INDEX_PATH)
        generate_txt(spells)
        print("Regenerated spell list.")
    else:
        generate_txt(spells)


if __name__ == "__main__":
    main()
