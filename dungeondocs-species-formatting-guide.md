```markdown
# DungeonDocs Species Page Formatting Guidelines

This document serves as the **canonical style guide and "seed"** for formatting all species pages in the DungeonDocs MkDocs site. The goal is consistent, visually appealing, readable pages that work reliably with Material for MkDocs (both light and dark themes) while **never rephrasing or altering any original text**.

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

5. **Structure Pattern** (apply to every species page)

```markdown
# [Species Name]

<!-- generated-by: scripts/txt_to_mkdocs.py v2026-02-03 -->

<div align="center">
  <img src="MAIN_HEADER_IMAGE_URL" alt="Descriptive alt text for the species" width="900"/>
</div>

[Introductory descriptive text exactly as provided]

[If there are sub-variants (e.g., Lorwyn/Shadowmoor), use ## headings with centered images]

## [Species Name] Traits

| Trait         | Description                                                                 |
| ------------- | --------------------------------------------------------------------------- |
| Creature Type | [Exact text]                                                                |
| Size          | [Exact text]                                                                |
| Speed         | [Exact text]                                                                |

As a [Species], you have these special traits.

**Trait Name**  
[Exact description text]

**Next Trait Name**  
[Exact description text]

[For traits with options/sub-choices (e.g., Celestial Revelation):]
### Sub-section Heading (e.g., Transformation Options)

#### Option Name
<div align="center">
  <img src="OPTION_SPECIFIC_IMAGE_URL" alt="Descriptive alt for this option" width="700"/>
</div>

[Exact option description]

[Repeat for each option]
```

## Specific Examples to Follow

- **Basic traits table**: Always use a 3-row table for Creature Type, Size, Speed.
- **Trait descriptions**: Bold the trait name in **double asterisks**, followed by the exact text on new lines.
- **Multi-paragraph traits**: Keep natural paragraph breaks.
- **Sub-variants**: Use `## Variant Name` with a centered image above the text block.
- **Choices/Options**: Use `###` for grouping and `####` for individual options, each with its own centered image when it adds clear visual distinction.

## Species List Page (species.md)

Use direct `##` headings for categories (no tabs). Place a large centered thematic image above each category list.

Example structure:
```markdown
# Species

<div align="center">
  <img src="HEADER_IMAGE" ... />
</div>

[Intro text]

## Parts of a Species

[Table as provided]

## Common Species

<div align="center">
  <img src="CATEGORY_IMAGE" ... />
</div>

- **[Species](link.md)**
- **[Next](link.md)**

## Next Category

[Repeat pattern]
```

## Maintaining Consistency

Copy this entire document as your "seed" reference. When generating a new page:
1. Start with the exact structure above.
2. Insert the raw text without changes.
3. Add images that precisely match the content.
4. Use only the approved Markdown elements listed.

This ensures every page looks visually cohesive and professional across the entire DungeonDocs site.
```

This Markdown file is the complete, self-contained guide and seed you can save (e.g., as `formatting-guidelines.md`) and refer to—or paste relevant sections—when creating future pages. It locks in the exact style we've developed together.