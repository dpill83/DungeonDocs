# DungeonDocs Magic Items Formatting Guidelines

This document is the **style guide for Magic Items pages only** on the DungeonDocs MkDocs site. The goal is consistent, readable magic item pages that work with Material for MkDocs (light and dark themes) while **never rephrasing or altering any original text**.

## Instructions for AI Assistants

**Your task is formatting.** Apply the structure and conventions below. Stay focused on: title, Source line, Rarity/Type/Attunement when applicable, and exact description text. Use **bold** for optional section headings. When the source mentions another magic item by name, link to that item’s page.

**Source:** Add a **Source:** line (e.g. `Source: Dungeon Master's Guide`) when the item comes from a known book; omit only if the source cannot be determined.

**Images:** Do **not** add or use images on magic item pages. Magic item pages use text-only layout.

## Core Principles

1. **Never rephrase or change any text**  
   All mechanical descriptions and item text must remain exactly as provided in the source. Only add Markdown formatting, structure, and links to other magic items.

2. **No admonitions**  
   Do **not** use `!!! info`, `!!! note`, or any other admonition blocks. They cause visual issues in some renders.

3. **No content tabs**  
   Do **not** use `=== "Tab Name"` syntax on individual magic item pages. Use standard headings (e.g. `##`, `###`) when grouping content.

4. **No images**  
   Magic item pages are text-only. Do not add header images or other images.

5. **Link to other magic items**  
   When the description mentions another magic item by name (e.g. "Portable Hole", "Heward's Handy Haversack"), add a markdown link to that item’s page: `[Item Name](item-slug.md)`. Use the same slug pattern as the rest of the site (lowercase, hyphens, e.g. `portable-hole.md`, `heward-s-handy-haversack.md`).

## Magic Item Page Pattern

Use this structure for every individual magic item page.

```markdown
# [Item Name]

Source: [Book Name]

**[Rarity]** [Type] (Attunement required when applicable.)

[Exact description paragraph(s) from the source.]

**Optional section heading.**  
[Exact text when the source has a named section.]
```

- **Title**: One `#` heading with the item name. Use title case and the same spelling as the source (e.g. "Boots of False Tracks", "Flame Tongue").
- **Source**: Add `Source: [Book Name]` directly below the title when known (e.g. Dungeon Master's Guide, Player's Handbook).
- **Rarity / Type / Attunement**: When the source gives them, add one line: **Rarity** Type (and "Attunement" or "Attunement required" when applicable). Examples: `**Common** Wondrous Item.` or `**Rare** Weapon (Attunement required).` Omit this line if the source does not specify.
- **Description**: Exact text from the source. Keep paragraph breaks as in the source.
- **Optional sections**: If the source has a named subsection (e.g. "Variant", "Random tables"), use **bold** for that heading, then the exact text on the next line(s).
- **Tables**: When the source includes a table (e.g. potion variants by rarity), use markdown table syntax. Example:

```markdown
| Potion | HP Regained | Rarity     |
|--------|-------------|------------|
| Potion of Healing | 2d4 + 2 | Common    |
| Potion of Healing (greater) | 4d4 + 4 | Uncommon |
```

- **Cross-references**: When the description names another magic item, link it: `[Portable Hole](portable-hole.md)`. Do not change the surrounding wording.

## Conventions

- **Bold**: Use **double asterisks** for rarity (e.g. **Common**, **Rare**) and for optional section headings.
- **Rarity**: Use the standard terms: Common, Uncommon, Rare, Very Rare, Legendary, Artifact.
- **Type**: Use the source’s type (e.g. Wondrous Item, Armor, Weapon, Potion, Scroll).
- **Attunement**: If the item requires attunement, say so on the Rarity/Type line or in the description exactly as in the source.
- **Price**: When the source gives a price (e.g. "100 GP", "B+100 GP"), use it as given. No need to repeat price on every item page unless the source does.
- **Paragraphs**: Keep natural paragraph breaks; do not rephrase.

## All Magic Items / index page

The "All Magic Items" landing page (e.g. all.md) should list items in a structured way so users can find and open individual pages.

- Use **markdown tables** with columns such as: Item Name (linked), Type, Attuned, Price (or Rarity).
- Group by rarity if desired: `## Common`, `## Uncommon`, etc., with a table under each heading.
- Item Name column: use markdown links to the individual item page, e.g. `[Boots of False Tracks](boots-of-false-tracks.md)`.
- Do **not** output a long flattened list (name, type, attuned, price as separate lines with no table). Use proper table syntax.
- If the list is very long, grouping by rarity or type with headings and one table per group keeps the page scannable.

## Maintaining Consistency

When creating or editing a Magic Item page: use the structure above, insert the raw text without changes, add links to other magic items when they are named, and use only the approved Markdown (no images, no admonitions, no tabs). This keeps every magic item page visually cohesive and easy to scan across the DungeonDocs site.
