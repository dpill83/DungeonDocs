# DungeonDocs Feats Formatting Guidelines

This document is the **style guide for Feats pages only** on the DungeonDocs MkDocs site. The goal is consistent, readable feat pages that work with Material for MkDocs (light and dark themes) while **never rephrasing or altering any original text**.

## Instructions for AI Assistants

**Your task is formatting.** Apply the structure and conventions below. Stay focused on: title, Source line, "You gain the following benefits.", and **bold** benefit names with exact description text.

**Source:** Look up which D&D book the feat is from (e.g. search for the feat name + "5e source" or "D&D 2024" + book name). Add a **Source:** line (e.g. `Source: Player's Handbook`) for every feat; omit only if you cannot determine the source.

**Images:** Do **not** use image-generation tools (do not create or generate new images). **Do** search for an existing image on the web and insert its working URL into the `<img src="..."/>` so the feat page has a real image. Never leave `HEADER_IMAGE_URL` or a placeholder in the final output—find and use a real image URL that fits the feat and follows the image rules below.

## Core Principles

1. **Never rephrase or change any text**  
   All mechanical descriptions and benefit text must remain exactly as provided in the source. Only add Markdown formatting, structure, and images.

2. **No admonitions**  
   Do **not** use `!!! info`, `!!! note`, or any other admonition blocks. They cause visual issues in some renders.

3. **No content tabs**  
   Do **not** use `=== "Tab Name"` syntax. Use the structure below instead.

4. **Images**  
   - **Do not use image-generation tools** (do not create or generate new images). **Do** search for an existing image online and insert its working URL so each feat has a real header image—never leave `HEADER_IMAGE_URL` or a placeholder.
   - Use **only** `<div align="center">` with `<img src="URL" alt="descriptive alt text" width="NUMBER"/>`. Do **not** use custom or assistant-specific markup (e.g. `<grok-card>`, `image_card`, or any similar non-standard elements). Plain HTML `<img>` inside the approved `<div>` is required.
   - **Image sources must be working links**: every `src` must resolve and render in the built site (no broken URLs, 404s, or hotlink-blocked/403 images).
   - Header image: 800–900 width.
   - **Do not use images from these URLs** (they return access denied):  
     - `https://cdnb.artstation.com`  
     - `https://static.wikia.nocookie.net/`  
     - `https://i.pinimg.com`  
     Use alternative image sources instead.

## Feats Page Pattern

Use this structure for every Feats page.

```markdown
# [Feat Name]

<div align="center">
  <img src="HEADER_IMAGE_URL" alt="Descriptive alt text" width="900"/>
</div>

Source: [Book Name]

You gain the following benefits.

**Benefit Name**  
Exact description text for this benefit.

**Another Benefit**  
Exact description text.
```

- **Source**: Look up which book the feat is from (e.g. Player's Handbook, Xanathar's Guide) and add `Source: [Book Name]` directly below the header image, before "You gain the following benefits." Always include the Source line; omit only if the source cannot be determined.
- **Benefits**: Use **bold** for the benefit name on one line, then the description on the next line(s). Do **not** use `##` headings for individual benefits.

## Conventions

- **Bold benefit names**: Use **double asterisks** for each benefit title, then the exact description on the next line(s).
- **Source line**: Look up the feat's source book and add `Source: [Book Name]` (e.g. `Source: Player's Handbook`) below the header image. Include it for every feat when the source can be determined.
- **Tables**: Use tables only when the source material includes a table for the feat.
- **Paragraphs**: Keep natural paragraph breaks; do not rephrase.

## Maintaining Consistency

When creating or editing a Feats page: use the structure above, insert the raw text without changes, and use only the approved Markdown/HTML image markup. This keeps every feat page visually cohesive and professional across the DungeonDocs site.
