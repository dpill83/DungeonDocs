# DungeonDocs – Project Specification

## What We Have (Starting Point)

The repo scaffold includes:

- **Scripts:** `scrape_dnd_wiki.py`, `txt_to_mkdocs.py`, and crawl batch files
- **Pipeline:** Scrape wikidot → txt files in `scraped-dnd2024/` → convert to `docs/` markdown → MkDocs builds `site/`
- **Sample content:** `docs/dnd5e/backgrounds/` with a few sample pages
- **Theme:** MkDocs Material with search plugin

This scaffolding sets the repo up for success. We grow from here in small increments.

---

## Purpose

Searchable D&D reference from wikidot sources. Start with one category (backgrounds), validate design and pipeline, then expand.

---

## Guardrails: Start Small, Scale Up

- **Phase 1 = backgrounds only.** Do not build the whole site.
- Validate look, search, responsiveness, and navigation with this small set.
- Add content incrementally by category (backgrounds → feats → spells, etc.) only after Phase 1 is solid.
- Avoid full-site crawl until the pipeline and UX are validated.

---

## Content Priority

| Phase | Scope |
|-------|-------|
| **Phase 1** | D&D backgrounds only (scrape a limited set from the D&D wiki) |
| **Phase 2** | Expand to other categories (feats, spells, etc.) |
| **Phase 3** | D&D 5e (dnd5e.wikidot.com) once the current edition is stable |

---

## Requirements

- **Responsive:** Works on desktop, tablet, and mobile
- **Search:** In-page search (MkDocs Material search)
- **Theme:** MkDocs Material

---

## Out of Scope (for now)

- 5e content
- Feats, spells, classes, items, etc. (until backgrounds are done and validated)
- Full-site crawl
