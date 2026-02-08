# DungeonDocs Equipment Formatting Guidelines

This document is the **style guide for Equipment pages only** on the DungeonDocs MkDocs site. The goal is consistent, readable equipment pages that work with Material for MkDocs (light and dark themes) while **never rephrasing or altering any original text**.

## Instructions for AI Assistants

**Your task is formatting.** Apply the structure and conventions below. Stay focused on: title, intro text, **markdown tables** for item lists (weapons, armor, adventuring gear, etc.), and **headings** for rules (Properties, Mastery, Armor Training, etc.). Keep all mechanical and descriptive text exactly as in the source.

**Source:** Add a **Source:** line (e.g. `Source: Player's Handbook (2024)`) when the equipment content comes from a known book; omit only if the source cannot be determined.

**Images:** Do **not** add or use images on equipment pages. Equipment pages use text and tables only.

## Core Principles

1. **Never rephrase or change any text**  
   All mechanical descriptions, table data, and rule text must remain exactly as provided in the source. Only add Markdown formatting and structure.

2. **No admonitions**  
   Do **not** use `!!! info`, `!!! note`, or any other admonition blocks. They cause visual issues in some renders.

3. **No content tabs**  
   Do **not** use `=== "Tab Name"` syntax on equipment pages. Use standard headings (e.g. `##`, `###`) for full scrollable visibility.

4. **No images**  
   Equipment pages are text and tables only. Do not add header images or other images.

5. **Use markdown tables for item lists**  
   Weapon tables, armor tables, adventuring gear tables, poison tables, and similar lists must use proper markdown table syntax (e.g. `| Name | Damage | Properties | ... |`). Do **not** output table data as flattened line-by-line text.

## Equipment Page Types

### Category pages (Weapons, Armor, Adventuring Gear, Tools, Poisons, etc.)

Use this structure for category-level equipment pages (weapon.md, armor.md, adventuring-gear.md, tool.md, poison.md, currency.md, mounts-and-vehicles.md, trinket.md, crafting.md).

```markdown
# [Category Name]

Source: [Book Name]

[Intro paragraph(s) from the source—e.g. what the table shows, how categories work.]

## [Subsection—e.g. Weapon Proficiency, Properties, Armor Training]

[Exact rule text. Use **bold** for inline terms when the source does.]

### [Sub-subsection if needed—e.g. Ammunition, Finesse]

[Exact definition text.]

## [Table section—e.g. Weapon Tables, Light Armor]

| Column 1 | Column 2 | Column 3 | ... |
|----------|----------|----------|-----|
| Value    | Value    | Value    | ... |
```

- **Title**: One `#` heading with the category name (e.g. Weapon, Armor, Adventuring Gear).
- **Source**: Add `Source: [Book Name]` directly below the title when known.
- **Intro**: Exact text from the source that describes the table or category. Use `##` for major sections (e.g. Properties, Mastery Properties, Armor Training).
- **Rules**: Use `###` or `####` for individual property names or rule subsections. Keep wording exactly as in the source.
- **Tables**: Use markdown tables. Align columns for readability. Include a table caption line above the table if the source has one (e.g. `Table: Simple Melee Weapons`). Use `—` for empty cells where the source has no value.
- **Weight and cost**: Use a space before units (e.g. `2 lb.`, `1 GP`, `5 SP`). Use `—` for "no weight" or "varies" when that is what the source says.

### Equipment index / landing page

The equipment index (e.g. index.md, all.md) lists categories with links. Use this structure:

```markdown
# Equipment

[Short intro: e.g. that this is mundane equipment, selling rule, link to DMG for magic items.]

## Mundane equipment

- [Weapons](weapon.md) – [Short description]
- [Armor](armor.md) – [Short description]
- [Adventuring Gear](adventuring-gear.md) – [Short description]

## Mundane items

- [Mounts and Vehicles](mounts-and-vehicles.md) – ...
- [Trinkets](trinket.md) – ...
- [Currency](currency.md) – ...
- [Poisons](poison.md) – ...

## Tools and crafting

- [Tools](tool.md) – ...
- [Crafting](crafting.md) – ...
```

- Use `##` for section headings (Mundane equipment, Mundane items, Tools and crafting).
- Use bullet lists with `[Label](filename.md) – description`. Links are relative to the equipments folder.
- Keep intro and descriptions brief and accurate; do not rephrase rule text.

### Per-item pages (future / optional)

If individual equipment item pages are added later (e.g. one page per weapon or armor), use a consistent pattern:

```markdown
# [Item Name]

Source: [Book Name]

**Category:** [e.g. Simple Melee Weapon, Light Armor]
**Damage:** [e.g. 1d6 Slashing] (weapons only)
**Properties:** [e.g. Light, Thrown (Range 20/60)] (weapons only)
**Mastery:** [e.g. Nick] (weapons only)
**Armor Class (AC):** [e.g. 11 + Dex modifier] (armor only)
**Weight:** [e.g. 2 lb.]
**Cost:** [e.g. 5 GP]

[Exact description or special rules from the source, if any.]
```

- One `#` title (item name).
- Source line when known.
- **Bold** labels for stats, then value on the same line or next line.
- Omit fields that do not apply (e.g. no Damage on armor).

## Conventions

- **Tables**: Use markdown tables for all item lists (weapons, armor, adventuring gear, poisons, currency, mounts, etc.). Column headers and cell values must match the source exactly.
- **Headings**: Use `##` for major sections (e.g. Properties, Weapon Tables, Light Armor), `###` for subsections (e.g. Ammunition, Finesse), `####` for specific items with descriptions (e.g. in tools or adventuring gear).
- **Bold**: Use **double asterisks** for inline terms when the source emphasizes them (e.g. **Category.**, **Armor Class (AC).**). Use bold for property/rule names in definition lists.
- **Weight and cost**: Use `lb.` for weight; use `GP`, `SP`, `CP`, `EP`, `PP` for currency. Include a space before the unit (e.g. `2 lb.`, `5 GP`). Use `—` or `-` for empty or N/A cells as in the source.
- **Paragraphs**: Keep natural paragraph breaks; do not rephrase.

## Maintaining Consistency

When creating or editing an Equipment page: use the structure above, insert the raw text and table data without changes, and use only the approved Markdown (no images, no admonitions, no tabs). Prefer markdown tables over flattened line-by-line data. This keeps every equipment page visually cohesive and easy to scan across the DungeonDocs site.
