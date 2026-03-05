# Ruleset Terminology Update – Summary

## Terminology map (old → new)

| Old | New | Where applied |
|-----|-----|----------------|
| Legacy (2014) | 5e (2014) | Nav section label (Backgrounds subsection) |
| Acolyte (Legacy), etc. | Acolyte (5e 2014), etc. | Nav item labels for backgrounds and species |
| Half-Elf (Legacy), Half-Orc (Legacy) | Half-Elf (5e 2014), Half-Orc (5e 2014) | Nav (Species) |
| *(Legacy)* (in species list) | *(5e 2014)* | docs/dnd2024/species/all.md |
| *(Legacy)* (in backgrounds tab) | *(5e 2014)* | docs/dnd2024/backgrounds/index.md tab "5e (2014)" |
| # X (Legacy) (page title) | # X (5e 2014) | 15 background/species page titles |
| *Source: … (Legacy).* | *Source: … (5e 2014).* | All background and species Source lines in docs/dnd2024 |
| legacy content (formatting guide) | older content | dungeondocs-formatting-guide-spells.md (avoids ruleset ambiguity) |

**Unchanged by design**

- **URLs/slugs**: `acolyte-legacy.md`, `half-elf.md`, etc. unchanged (backwards compatibility).
- **Internal names**: No `isLegacy`/`ruleset` fields in code; only nav and content text changed.
- **Game terms**: "Infernal Legacy", "Fiendish Legacy", "Ancestral Legacy", tiefling legacies, "salted-legacy" (adventure name), and generic English "legacy" in body copy were not changed.

---

## Diff summary by file

### Config / nav
- **mkdocs.yml** – Nav: "Legacy (2014):" → "5e (2014):"; all "X (Legacy):" → "X (5e 2014):" for backgrounds and species (Half-Elf, Half-Orc).

### Index / explainer pages
- **docs/dnd2024/species/all.md** – "(Legacy)" → "(5e 2014)" in note and in species list; added explainer: "5e (2014) = 2014 rules. 5.5e (2024) = 2024 revised rules."
- **docs/dnd2024/backgrounds/index.md** – Tab "Legacy (2014)" → "5e (2014)"; explainer added; all "[X (Legacy)]" → "[X (5e 2014)]" in that tab.

### Background and species content (Source + titles)
- **86 files** under `docs/dnd2024/backgrounds/` and `docs/dnd2024/species/`: `*Source: … (Legacy).*` → `*Source: … (5e 2014).*`
- **15 background pages**: `# X (Legacy)` → `# X (5e 2014)` (acolyte-legacy, archaeologist-legacy, charlatan-legacy, criminal-legacy, entertainer-legacy, hermit-legacy, house-agent-legacy, noble-legacy, sage-legacy, sailor-legacy, soldier-legacy, city-watch, clan-crafter, guild-artisan, athlete).

### Documentation
- **dungeondocs-formatting-guide-spells.md** – "legacy content" → "older content" (component formatting note).

---

## Explainer text added

- **Species** (`docs/dnd2024/species/all.md`):  
  "5e (2014) = 2014 rules. 5.5e (2024) = 2024 revised rules."
- **Backgrounds** (`docs/dnd2024/backgrounds/index.md`, tab "5e (2014)"):  
  "5e (2014) = 2014 rules. 5.5e (2024) = 2024 revised rules. *(5e 2014)* indicates backgrounds from the 2014 rules and other sources, not part of the 2024 core."

---

## Search / filter behavior

- **No code changes** to search or filters; MkDocs Material search still indexes all content under `dnd2024/`.
- **Viewing by ruleset**: Users can view only 5e (2014) content via the "5e (2014)" nav section (backgrounds and species). The rest of the site remains 5.5e (2024) core. No new filter/toggle was added; behavior unchanged.

---

## Tests

- **tests/test_txt_to_mkdocs.py** – Passes (no assertions on "Legacy" or nav labels). No test or snapshot updates required.

---

## Remaining TODOs / risky areas

1. **docs/dnd5e/** – The 5e (2014) wiki content under `docs/dnd5e/` was not relabeled; it is excluded from the main nav (plugin `exclude: dnd5e/**`). If you later expose it, consider adding a clear "5e (2014)" label or banner.
2. **Scraped / generated content** – `docs/dnd5e/homes/home.md` and any converter output: future scrapes may reintroduce "Legacy" or "Current ruleset" from the source wiki. The manually added 5.5e pointer in home.md is kept; watch for overwrites when re-running the converter.
3. **Remaining "legacy" in body copy** – A few docs still use the word "legacy" in non-ruleset sense (e.g. tiefling "Fiendish Legacy", adventure "salted-legacy", generic "inheritor of a famed legacy"). Left as-is; only ruleset-related labels were changed.
4. **Redirects** – No URL or slug changes were made, so no redirects were added.

---

## Checklist used (Legacy classification)

| Location | Type | Action taken |
|----------|------|--------------|
| mkdocs.yml nav section "Legacy (2014)" | (a) UI label | → "5e (2014)" |
| mkdocs.yml nav items "X (Legacy)" | (a) UI label | → "X (5e 2014)" |
| species/all.md *(Legacy)* | (a) UI label | → *(5e 2014)* + explainer |
| backgrounds/index.md tab and table | (a) UI label | → "5e (2014)" tab, [X (5e 2014)] + explainer |
| Page titles # X (Legacy) | (a) UI label | → # X (5e 2014) |
| *Source: … (Legacy).* | (a) UI label | → *Source: … (5e 2014).* |
| dungeondocs-formatting-guide-spells "legacy content" | (c) docs | → "older content" |
| File names *-legacy.md | (b) internal/slug | Kept for backwards compatibility |
| Tiefling/lineage "Infernal Legacy" etc. | Game term | Unchanged |
| Image URL salted-legacy | Asset name | Unchanged |
