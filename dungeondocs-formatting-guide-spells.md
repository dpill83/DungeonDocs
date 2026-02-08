# DungeonDocs Spells Formatting Guidelines

This document is the **style guide for Spells pages only** on the DungeonDocs MkDocs site. The goal is consistent, readable spell pages that work with Material for MkDocs (light and dark themes) while **never rephrasing or altering any original text**.

## Instructions for AI Assistants

**Your task is formatting.** Apply the structure and conventions below. Stay focused on: title, Source line, level/school/class line, stat block (Casting Time, Range, Components, Duration), and exact description text. Optional sections (e.g. **Using a Higher-Level Spell Slot.**) use **bold** for the section heading.

**Source:** Look up which D&D book the spell is from (e.g. Player's Handbook, Xanathar's Guide). Add a **Source:** line for every spell; omit only if you cannot determine the source.

**Images:** Do **not** add or use images on spell pages. Spell pages use text-only layout.

## Core Principles

1. **Never rephrase or change any text**  
   All mechanical descriptions and spell text must remain exactly as provided in the source. Only add Markdown formatting and structure.

2. **No admonitions**  
   Do **not** use `!!! info`, `!!! note`, or any other admonition blocks. They cause visual issues in some renders.

3. **No content tabs**  
   Do **not** use `=== "Tab Name"` syntax on individual spell pages. Use the structure below instead.

4. **No images**  
   Spell pages are text-only. Do not add header images or other images to spell pages.

## Spells Page Pattern

Use this structure for every spell page.

```markdown
# [Spell Name]

Source: [Book Name]

Level [X] [School] ([Class1], [Class2], ...)

Casting Time: [e.g. Action, Bonus Action, Reaction, 1 minute]
Range: [e.g. Self, Touch, 30 feet, 120 feet]
Components: [V, S, M (description if material)]
Duration: [e.g. Instantaneous, 1 hour, Concentration, up to 1 minute]

[Exact description paragraph(s) from the source.]

**Using a Higher-Level Spell Slot.**  
[Exact text when the spell has an upcast section.]
```

- **Source**: Add `Source: [Book Name]` directly below the title. Include for every spell when the source can be determined.
- **Level line**: One line: spell level (or "Cantrip"), school name, then class list in parentheses. Example: `Level 1 Enchantment (Cleric, Paladin)`.
- **Stat block**: One line per field. Use "Casting Time:", "Range:", "Components:", "Duration:" with the value on the same line after a space.
- **Components**: Use "V" (verbal), "S" (somatic), "M" (material). For material components, add parentheses with the exact description and cost when given, e.g. `M (a Holy Symbol worth 5+ GP)`.
- **Duration**: For concentration spells, write "Concentration, up to [time]" (e.g. `Concentration, up to 1 minute`). Use "C" only in tables or indexes, not in the spell page stat block.
- **Description**: Exact text from the source. Keep paragraph breaks as in the source.
- **Optional sections**: If the source has "Using a Higher-Level Spell Slot", "At Higher Levels", or similar, use **bold** for that heading, then the exact description on the next line(s).

## Example (Bless)

```markdown
# Bless

Source: Player's Handbook

Level 1 Enchantment (Cleric, Paladin)

Casting Time: Action
Range: 30 feet
Components: V, S, M (a Holy Symbol worth 5+ GP)
Duration: Concentration, up to 1 minute

You bless up to three creatures within range. Whenever a target makes an attack roll or a saving throw before the spell ends, the target adds 1d4 to the attack roll or save.

**Using a Higher-Level Spell Slot.** You can target one additional creature for each spell slot level above 1.
```

## Conventions

- **Bold section headings**: Use **double asterisks** for optional headings like "Using a Higher-Level Spell Slot." or "At Higher Levels." Then put the exact description on the next line(s).
- **Source line**: Add `Source: [Book Name]` below the title for every spell when the source can be determined.
- **One line per stat**: Casting Time, Range, Components, and Duration each get one line in the form `Label: value`.
- **No tables on spell pages**: Do not turn the stat block into a table; keep the labeled-line format above.
- **Paragraphs**: Keep natural paragraph breaks; do not rephrase.

## Maintaining Consistency

When creating or editing a Spells page: use the structure above, insert the raw text without changes, and use only the approved Markdown (no images, no admonitions, no tabs). This keeps every spell page visually cohesive and easy to scan across the DungeonDocs site.
