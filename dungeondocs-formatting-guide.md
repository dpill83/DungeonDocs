```markdown
# DungeonDocs Page Formatting Guidelines

This document is the **canonical style guide** for formatting content across the DungeonDocs MkDocs site—species, classes, and all other docs. The goal is consistent, visually appealing, readable pages that work reliably with Material for MkDocs (both light and dark themes) while **never rephrasing or altering any original text**.

## Core Principles

1. **Never rephrase or change any text**  
   All descriptive lore, flavor text, and mechanical descriptions must remain exactly as provided in the source. Only add Markdown formatting, structure, and images.

2. **No admonitions**  
   Do **not** use `!!! info`, `!!! note`, or any other admonition blocks. They cause visual issues in some renders.

3. **No content tabs**  
   Do **not** use `=== "Tab Name"` syntax. Use standard headings instead for full scrollable visibility.

4. **Images**  
   - Always include relevant, high-quality artwork.
   - Use **only** `<div align="center">` with `<img src="URL" alt="descriptive alt text" width="NUMBER"/>`. Do **not** use custom or assistant-specific markup (e.g. `<grok-card>`, `image_card`, `render_searched_image`, or any similar non-standard elements). Plain HTML `<img>` inside the approved `<div>` is required.
   - **Image sources must be working links**: every `src` must resolve and render in the built site (no broken URLs, 404s, or hotlink-blocked/403 images).
   - Header image: 800–900 width.
   - Section images: 700–800 width.
   - Choose images that thematically match the content exactly.
   - **Do not use images from these URLs** (they return access denied):  
     - `https://cdnb.artstation.com`  
     - `https://static.wikia.nocookie.net/`
     - `https://i.pinimg.com`
     Use alternative image sources instead.

5. **Structure**  
   Structure varies by content type (species, class, subclass, index, etc.). Use a clear heading hierarchy, a main header image, and section images where they add value. Apply the patterns below as appropriate.

### Species page pattern

```markdown
# [Species Name]

<div align="center">
  <img src="MAIN_HEADER_IMAGE_URL" alt="Descriptive alt text" width="900"/>
</div>

[Introductory text exactly as provided]

## [Species Name] Traits
| Trait         | Description     |
| ------------- | --------------- |
| Creature Type | [Exact text]    |
| Size          | [Exact text]    |
| Speed         | [Exact text]    |

**Trait Name**  
[Exact description text]
```

### Class / subclass page pattern

```markdown
# [Class or Subclass Name]

<div align="center">
  <img src="HEADER_IMAGE_URL" alt="Descriptive alt text" width="900"/>
</div>

[Intro text exactly as provided]

## [Section Heading]

[Content with ## / ### / #### as needed; centered images for key options or subclasses when useful]
```

### Index / list page pattern (e.g. species.md, class index)

Use direct `##` headings for categories (no tabs). Place a centered thematic image above each category list.

```markdown
# [Topic] (e.g. Species, Warlock)

<div align="center">
  <img src="HEADER_IMAGE" alt="..." width="900"/>
</div>

[Intro text]

## Category Name

<div align="center">
  <img src="CATEGORY_IMAGE" alt="..." width="800"/>
</div>

- **[Item Name](link.md)**
- **[Next](link.md)**
```

## Conventions to Follow

- **Tables**: Use markdown tables for structured stats (e.g. Creature Type, Size, Speed on species; table data as provided).
- **Bold labels**: Bold key names in **double asterisks**, then the exact text on the next line(s).
- **Paragraphs**: Keep natural paragraph breaks; do not rephrase.
- **Variants / options**: Use `##` for main variants, `###` for groups, `####` for individual options; add a centered image per option when it adds clear visual distinction.
- **Images**: Header 800–900 width; section images 700–800; only working image links; no admonitions or tabs.

## Maintaining Consistency

When creating or editing any page:
1. Use the structure that fits the content type (species, class, index, etc.).
2. Insert the raw text without changes.
3. Add images that precisely match the content and use working links only.
4. Use only the approved Markdown/HTML elements in this guide (no admonitions, no content tabs).

This keeps every page visually cohesive and professional across the DungeonDocs site.
```

This Markdown file is the complete, self-contained guide for the project. Refer to it (or paste relevant sections) when creating or editing any DungeonDocs page—species, classes, or other content.
