#!/usr/bin/env python3
"""
Add Consumable column to docs/dnd2024/magic-items/all.md and generate
docs/dnd2024/magic-items/consumable.md with consumable-only items.
Derives consumable status from Type + slug per plan rules.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ITEMS_DIR = REPO_ROOT / "docs" / "dnd2024" / "magic-items"
INDEX_FILE = ITEMS_DIR / "all.md"
CONSUMABLE_FILE = ITEMS_DIR / "consumable.md"

CONSUMABLE_TYPES = {"Potion", "Scroll"}

CONSUMABLE_AMMUNITION_SLUGS = {
    "ammunition-of-slaying",
    "ammunition-1-2-or-3",
    "walloping-ammunition",
}

CONSUMABLE_WONDROUS_SLUGS = {
    "bag-of-beans",
    "bead-of-force",
    "bead-of-nourishment",
    "bead-of-refreshment",
    "chime-of-opening",
    "dust-of-disappearance",
    "dust-of-dryness",
    "dust-of-sneezing-and-choking",
    "elemental-gem",
    "keoghtom-s-ointment",
    "necklace-of-fireballs",
    "nolzur-s-marvelous-pigments",
    "perfume-of-bewitching",
    "pot-of-awakening",
    "quaal-s-feather-token",
    "sovereign-glue",
    "universal-solvent",
}


def is_consumable(slug: str, item_type: str) -> bool:
    """Return True if the item is consumable per plan rules."""
    if item_type in CONSUMABLE_TYPES:
        return True
    if item_type == "Weapon" and slug in CONSUMABLE_AMMUNITION_SLUGS:
        return True
    if item_type == "Wondrous Item" and slug in CONSUMABLE_WONDROUS_SLUGS:
        return True
    return False


def transform_table_line(line: str) -> str:
    """
    If line is a table row with exactly 4 columns, append Consumable column.
    Otherwise return line unchanged.
    """
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return line

    parts = [p.strip() for p in stripped.split("|")[1:-1]]
    if len(parts) != 4:
        return line

    name_cell, item_type, attunement, price = parts

    # Header row
    if name_cell.lower() == "item name":
        return line.rstrip().rstrip("|").rstrip() + " | Consumable |"

    # Separator row
    if "---" in item_type:
        return line.rstrip().rstrip("|").rstrip() + " | --- |"

    # Data row
    link_match = re.match(r"\[([^\]]+)\]\(([^)]+)\.md\)", name_cell)
    if not link_match:
        return line
    slug = link_match.group(2)
    consumable_val = "Yes" if is_consumable(slug, item_type) else "—"
    return line.rstrip().rstrip("|").rstrip() + f" | {consumable_val} |"


def collect_consumable_items(text: str) -> list[dict]:
    """Parse all.md text and return list of consumable items with rarity."""
    items: list[dict] = []
    current_rarity: str | None = None
    rarity_from_heading = {
        "common magic items": "Common",
        "uncommon magic items": "Uncommon",
        "rare magic items": "Rare",
        "very rare magic items": "Very Rare",
        "legendary magic items": "Legendary",
        "artifacts": "Artifact",
    }

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            heading = stripped[3:].strip().lower()
            current_rarity = rarity_from_heading.get(heading)
            continue

        if current_rarity is None:
            continue
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue

        parts = [p.strip() for p in stripped.split("|")[1:-1]]
        if len(parts) < 4:
            continue
        name_cell, item_type = parts[0], parts[1]
        if name_cell.lower() == "item name" or "---" in str(parts[1]):
            continue

        link_match = re.match(r"\[([^\]]+)\]\(([^)]+)\.md\)", name_cell)
        if not link_match:
            continue
        name = link_match.group(1)
        slug = link_match.group(2)
        attunement = parts[2] if len(parts) > 2 else "—"
        price = parts[3] if len(parts) > 3 else "—"

        if is_consumable(slug, item_type):
            items.append({
                "name": name,
                "slug": slug,
                "type": item_type,
                "attunement": attunement,
                "price": price,
                "rarity": current_rarity,
            })

    return items


def write_consumable_md(items: list[dict]) -> None:
    """Write consumable.md with items grouped by rarity."""
    rarity_order = ["Common", "Uncommon", "Rare", "Very Rare", "Legendary", "Artifact"]
    by_rarity: dict[str, list[dict]] = {r: [] for r in rarity_order}
    for item in items:
        r = item["rarity"]
        if r in by_rarity:
            by_rarity[r].append(item)

    lines = [
        "# Consumable Magic Items",
        "",
        "Magic items that are consumed or expended upon use.",
        "",
    ]

    for rarity in rarity_order:
        subset = by_rarity[rarity]
        if not subset:
            continue
        heading = {
            "Common": "## Common",
            "Uncommon": "## Uncommon",
            "Rare": "## Rare",
            "Very Rare": "## Very Rare",
            "Legendary": "## Legendary",
            "Artifact": "## Artifacts",
        }[rarity]
        lines.append(heading)
        lines.append("")
        lines.append("| Item Name | Type | Attunement | Price |")
        lines.append("| --- | --- | --- | --- |")
        for item in subset:
            link = f"[{item['name']}]({item['slug']}.md)"
            lines.append(f"| {link} | {item['type']} | {item['attunement']} | {item['price']} |")
        lines.append("")

    CONSUMABLE_FILE.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    if not INDEX_FILE.exists():
        raise SystemExit(f"Index not found: {INDEX_FILE}")

    text = INDEX_FILE.read_text(encoding="utf-8")
    transformed = [transform_table_line(line) for line in text.splitlines()]
    INDEX_FILE.write_text("\n".join(transformed) + "\n", encoding="utf-8")
    print(f"Updated {INDEX_FILE} with Consumable column")

    # Collect consumable items from transformed text (before writing, use transformed)
    transformed_text = "\n".join(transformed)
    items = collect_consumable_items(transformed_text)
    write_consumable_md(items)
    print(f"Generated {CONSUMABLE_FILE} with {len(items)} consumable items")


if __name__ == "__main__":
    main()
