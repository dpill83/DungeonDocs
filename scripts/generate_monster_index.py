#!/usr/bin/env python3
"""
Generate docs/{edition}/monsters/ index pages from monsters.json:
  by-name.md (one alphabetical table), by-cr.md (grouped by CR), by-type.md (grouped by type),
  and a short landing index.md.
Edition is configurable via EDITION constant or DUNGEONDOCS_EDITION env.
"""

import json
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EDITION = os.environ.get("DUNGEONDOCS_EDITION", "dnd2024")
MONSTERS_DIR = REPO_ROOT / "docs" / EDITION / "monsters"
JSON_PATH = MONSTERS_DIR / "monsters.json"

SOURCE_DISPLAY = {
    "MM": "Monster Manual",
    "VGM": "Volo's Guide to Monsters",
    "MTF": "Mordenkainen's Tome of Foes",
    "DMG": "Dungeon Master's Guide",
    "DMG2024": "Dungeon Master's Guide (2024)",
    "PHB": "Player's Handbook",
    "PHB2024": "Player's Handbook (2024)",
    "TCE": "Tasha's Cauldron of Everything",
    "XGE": "Xanathar's Guide to Everything",
}

CR_ORDER = [
    "0", "1/8", "1/4", "1/2", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
    "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
]


def escape_cell(s: str) -> str:
    return (s or "").replace("|", "\\|")


def row(entry: dict, include_cr: bool = True, include_type: bool = True) -> str:
    name = escape_cell(entry.get("name", ""))
    slug = entry.get("slug", "")
    cr = entry.get("cr", "")
    type_ = escape_cell(entry.get("type", ""))
    link = f"[{name}]({slug}.md)"
    if include_cr and include_type:
        return f"| {link} | {cr} | {type_} |\n"
    if include_cr:
        return f"| {link} | {cr} |\n"
    if include_type:
        return f"| {link} | {type_} |\n"
    return f"| {link} |\n"


def main() -> None:
    if not JSON_PATH.exists():
        print(f"monsters.json not found: {JSON_PATH}")
        return
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    if not data:
        for name in ("index", "by-name", "by-cr", "by-type"):
            (MONSTERS_DIR / f"{name}.md").write_text(
                f"# Monsters\n\nNo monsters yet. Run parse_monsters_az.py first.\n",
                encoding="utf-8",
            )
        print("Wrote empty index, by-name, by-cr, by-type")
        return

    by_cr: dict[str, list[dict]] = {cr: [] for cr in CR_ORDER}
    by_type: dict[str, list[dict]] = {}
    for entry in data:
        cr = entry.get("cr", "0")
        if cr not in by_cr:
            by_cr[cr] = []
        by_cr[cr].append(entry)
        t = entry.get("type") or "unknown"
        if t not in by_type:
            by_type[t] = []
        by_type[t].append(entry)
    for cr in by_cr:
        by_cr[cr].sort(key=lambda x: (x.get("name") or "").lower())
    for t in by_type:
        by_type[t].sort(key=lambda x: (x.get("name") or "").lower())

    # Alphabetical for by-name (data is already sorted by CR then name from parse script; re-sort by name only)
    by_name = sorted(data, key=lambda x: (x.get("name") or "").lower())

    # --- index.md (landing) ---
    index_lines = [
        "# Monsters\n\n",
        "Browse the bestiary by [name](by-name.md), [Challenge Rating](by-cr.md), or [creature type](by-type.md). "
        "See [Stat blocks](stat-blocks.md) for rules.\n",
    ]
    (MONSTERS_DIR / "index.md").write_text("".join(index_lines), encoding="utf-8")
    print(f"Wrote {MONSTERS_DIR / 'index.md'}")

    # --- by-name.md (one alphabetical table) ---
    by_name_lines = [
        "# Monsters by Name\n\n",
        "| Name | CR | Type |\n",
        "| --- | --- | --- |\n",
    ]
    for entry in by_name:
        by_name_lines.append(row(entry, include_cr=True, include_type=True))
    (MONSTERS_DIR / "by-name.md").write_text("".join(by_name_lines), encoding="utf-8")
    print(f"Wrote {MONSTERS_DIR / 'by-name.md'}")

    # --- by-cr.md (headings per CR, table under each) ---
    by_cr_lines = ["# Monsters by Challenge Rating\n\n"]
    for cr in CR_ORDER:
        entries = by_cr.get(cr, [])
        by_cr_lines.append(f"## CR {cr}\n\n")
        if not entries:
            by_cr_lines.append("No monsters.\n\n")
            continue
        by_cr_lines.append("| Name | Type |\n")
        by_cr_lines.append("| --- | --- |\n")
        for entry in entries:
            by_cr_lines.append(row(entry, include_cr=False, include_type=True))
        by_cr_lines.append("\n")
    (MONSTERS_DIR / "by-cr.md").write_text("".join(by_cr_lines), encoding="utf-8")
    print(f"Wrote {MONSTERS_DIR / 'by-cr.md'}")

    # --- by-type.md (headings per type, table under each) ---
    by_type_lines = ["# Monsters by Type\n\n"]
    for type_key in sorted(by_type.keys(), key=str.lower):
        entries = by_type[type_key]
        heading = type_key.capitalize()
        by_type_lines.append(f"## {heading}\n\n")
        by_type_lines.append("| Name | CR |\n")
        by_type_lines.append("| --- | --- |\n")
        for entry in entries:
            by_type_lines.append(row(entry, include_cr=True, include_type=False))
        by_type_lines.append("\n")
    (MONSTERS_DIR / "by-type.md").write_text("".join(by_type_lines), encoding="utf-8")
    print(f"Wrote {MONSTERS_DIR / 'by-type.md'}")


if __name__ == "__main__":
    main()
