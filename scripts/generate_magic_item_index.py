#!/usr/bin/env python3
"""
Generate docs/dnd2024/magic-items/index.md (All Magic Items with rarity tabs) and
type category pages (armor.md, weapon.md, etc.) with rarity tabs.
Reads from docs/dnd2024/magic-items/all.md; does not modify all.md or individual item files.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ITEMS_DIR = REPO_ROOT / "docs" / "dnd2024" / "magic-items"
ALL_MD = ITEMS_DIR / "all.md"
INDEX_MD = ITEMS_DIR / "index.md"

RARITY_ORDER = ["Common", "Uncommon", "Rare", "Very Rare", "Legendary", "Artifact"]

RARITY_FROM_HEADING = {
    "common magic items": "Common",
    "uncommon magic items": "Uncommon",
    "rare magic items": "Rare",
    "very rare magic items": "Very Rare",
    "legendary magic items": "Legendary",
    "artifacts": "Artifact",
}


def escape_table_cell(s: str) -> str:
    """Escape pipe in table cells for markdown."""
    return s.replace("|", "\\|")


def type_to_slug(item_type: str) -> str:
    """Map Type to filename slug (e.g. 'Wondrous Item' -> 'wondrous-item')."""
    return item_type.strip().lower().replace(" ", "-")


def parse_all_md(text: str) -> list[dict]:
    """
    Parse all.md content. Return list of items, each:
    { name, slug, type, rarity, attunement, price, consumable }.
    """
    items: list[dict] = []
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
        if len(parts) < 5:
            continue
        name_cell, item_type, attunement, price, consumable = parts[0], parts[1], parts[2], parts[3], parts[4]
        if name_cell.lower() == "item name" or "---" in str(parts[1]):
            continue

        link_match = re.match(r"\[([^\]]+)\]\(([^)]+)\.md\)", name_cell)
        if not link_match:
            continue
        name = link_match.group(1)
        slug = link_match.group(2)
        items.append({
            "name": name,
            "slug": slug,
            "type": item_type,
            "rarity": current_rarity,
            "attunement": attunement,
            "price": price,
            "consumable": consumable,
        })
    return items


def items_by_rarity(items: list[dict]) -> dict[str, list[dict]]:
    """Group items by rarity; sort each list by name."""
    by_rarity: dict[str, list[dict]] = {r: [] for r in RARITY_ORDER}
    for item in items:
        r = item["rarity"]
        if r in by_rarity:
            by_rarity[r].append(item)
    for r in RARITY_ORDER:
        by_rarity[r].sort(key=lambda x: (x["name"].lower(), x["slug"]))
    return by_rarity


def render_index(by_rarity: dict[str, list[dict]]) -> str:
    """Render index.md content: All tab (with Rarity column) + one tab per rarity."""
    out: list[str] = []
    out.append("# All Magic Items\n\n")
    out.append("Magic items by rarity. Click an item name to open its page. [All Magic Items](all.md).\n\n")

    # All tab: alphabetical by name
    all_rows: list[tuple[str, dict]] = []
    for rarity in RARITY_ORDER:
        for item in by_rarity[rarity]:
            all_rows.append((rarity, item))
    all_rows.sort(key=lambda x: (x[1]["name"].lower(), x[1]["slug"]))
    out.append('=== "All"\n')
    out.append("    | Item Name | Rarity | Type | Attunement | Price | Consumable |\n")
    out.append("    | --- | --- | --- | --- | --- | --- |\n")
    for rarity, item in all_rows:
        link = f"[{escape_table_cell(item['name'])}]({item['slug']}.md)"
        out.append(f"    | {link} | {escape_table_cell(rarity)} | {escape_table_cell(item['type'])} | {escape_table_cell(item['attunement'])} | {escape_table_cell(item['price'])} | {escape_table_cell(item['consumable'])} |\n")

    # One tab per rarity
    for rarity in RARITY_ORDER:
        rows = by_rarity[rarity]
        out.append(f'=== "{rarity}"\n')
        if not rows:
            out.append("    No items in this category.\n")
            continue
        out.append("    | Item Name | Type | Attunement | Price | Consumable |\n")
        out.append("    | --- | --- | --- | --- | --- |\n")
        for item in rows:
            link = f"[{escape_table_cell(item['name'])}]({item['slug']}.md)"
            out.append(f"    | {link} | {escape_table_cell(item['type'])} | {escape_table_cell(item['attunement'])} | {escape_table_cell(item['price'])} | {escape_table_cell(item['consumable'])} |\n")

    return "".join(out)


def render_type_page(type_label: str, type_slug: str, by_rarity: dict[str, list[dict]], type_filter: str) -> str:
    """
    Render one type page (e.g. armor.md). type_filter is the exact Type string (e.g. "Armor").
    Tabs by rarity; only rarities that have at least one item of this type.
    """
    out: list[str] = []
    out.append(f"# {type_label}\n\n")
    out.append(f"Magic items of type {type_label}. [All Magic Items](all.md).\n\n")

    for rarity in RARITY_ORDER:
        rows = [i for i in by_rarity[rarity] if i["type"] == type_filter]
        out.append(f'=== "{rarity}"\n')
        if not rows:
            out.append("    No items in this category.\n")
            continue
        out.append("    | Item Name | Attunement | Price | Consumable |\n")
        out.append("    | --- | --- | --- | --- |\n")
        for item in rows:
            link = f"[{escape_table_cell(item['name'])}]({item['slug']}.md)"
            out.append(f"    | {link} | {escape_table_cell(item['attunement'])} | {escape_table_cell(item['price'])} | {escape_table_cell(item['consumable'])} |\n")

    return "".join(out)


def main() -> None:
    if not ALL_MD.exists():
        raise SystemExit(f"Source not found: {ALL_MD}")

    text = ALL_MD.read_text(encoding="utf-8")
    items = parse_all_md(text)
    if not items:
        raise SystemExit("No items parsed from all.md")

    by_rarity = items_by_rarity(items)

    index_content = render_index(by_rarity)
    INDEX_MD.write_text(index_content, encoding="utf-8")
    print(f"Generated {INDEX_MD}")

    # Collect types that appear (preserve display form, e.g. "Wondrous Item")
    types_seen: dict[str, str] = {}  # slug -> display label (first seen)
    for item in items:
        t = item["type"]
        slug = type_to_slug(t)
        if slug not in types_seen:
            types_seen[slug] = t

    for type_slug, type_label in sorted(types_seen.items()):
        type_content = render_type_page(type_label, type_slug, by_rarity, type_label)
        (ITEMS_DIR / f"{type_slug}.md").write_text(type_content, encoding="utf-8")
        print(f"Generated {ITEMS_DIR / f'{type_slug}.md'}")

    print(f"Done: index.md and {len(types_seen)} type pages.")


if __name__ == "__main__":
    main()
