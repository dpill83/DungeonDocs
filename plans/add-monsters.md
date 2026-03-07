# Plan: Add Monsters to DungeonDocs

## Overview

Add a Monsters section to DungeonDocs by (1) wiring the converter for future scraped monster content, (2) using existing `monsters.md` and `monsters-A-Z.md` as the initial content source, (3) creating the docs folder, per-monster pages, index by CR, and nav. **Edition folder (e.g. `dnd2024` or `dnd5e`) is configurable, not hardcoded.**

## Configurable edition folder

Do **not** hardcode `dnd2024`. Use one of:

- **Scripts:** Single constant at top of each script (e.g. `EDITION = "dnd2024"`) or CLI arg (e.g. `--edition dnd5e`) or env var (e.g. `DUNGEONDOCS_EDITION`). All paths use it: `docs/{edition}/monsters/`, `docs/{edition}/monsters/monsters.json`, etc.
- **mkdocs.yml:** Nav and exclude-search use the same value; either maintain by hand when switching, or use a single placeholder (e.g. `EDITION` in a comment) so you only change one place.

Default can remain `dnd2024`; switching to `dnd5e` (or another folder) is then a one-line change per script or one env var.

## Content sources (existing files)

| File | Purpose |
|------|---------|
| **monsters.md** | Reference: stat block rules (Size, Type, AC, CR, Traits, Actions, etc.). No stat blocks. Use as the Monsters section reference page. |
| **monsters-A-Z.md** | Bestiary: single file with hundreds of stat blocks. Structure: `## Group` and `### Monster Name` per block; each block has italic `_Size Type, Alignment_`, **CR** line, and `#### Traits` / `#### Actions`. Split by `###` to produce one `.md` per monster. |

## 1. Converter (for future scraped content)

**File:** `scripts/txt_to_mkdocs.py`

- In `CATEGORY_TO_FOLDER`, add:
  - `"monster": "monsters"`
  - `"creatures": "monsters"`
- No change to `convert_content()` required for initial rollout.
- Converter already uses `WIKI_MAP` for wiki → folder (e.g. `dnd2024`, `dnd5e`); monster output is `docs/{wiki_folder}/monsters/` — no hardcoded edition in converter.

## Pipeline: JSON-first (recommended)

**Recommendation: parse to JSON first, then generate markdown and indexes from JSON.**

- **Parse once:** `monsters-A-Z.md` → extract each stat block; for each block produce metadata (name, slug, cr, type, optionally size, alignment, source) and the raw markdown body.
- **Write:** (1) `monsters.json` — array of metadata only (no full body in JSON). (2) One `.md` file per monster (content only). (3) Index generator reads **only** `monsters.json` and writes `index.md` and `all.md`; no parsing of markdown tables.
- **Why JSON-first:** Single source of truth for metadata; easy to sort/filter by CR or type; index script stays simple and robust; matches existing `spells.json` pattern; adding fields (e.g. source book) is schema + JSON only; same scripts can target `dnd2024` or `dnd5e` by changing the edition folder.

Flow: `monsters-A-Z.md` → parse script → `monsters.json` + per-monster `.md` → index script (reads JSON) → `index.md` + `all.md`.

## JSON schema (monsters.json)

Define before implementation. Root is an array of monster objects. **CR is stored as a string** so values like `"1/8"` and `"1/2"` don’t require number hacks.

**Example entry:**

```json
{
  "name": "Aboleth",
  "slug": "aboleth",
  "cr": "10",
  "type": "aberration",
  "size": "Large",
  "alignment": "lawful evil",
  "source": "MM",
  "path": "docs/{edition}/monsters/aboleth.md"
}
```

**Fields:**

| Field | Type | Required | Notes |
|-------|------|----------|--------|
| `name` | string | yes | Display name (e.g. "Young Black Dragon") |
| `slug` | string | yes | Filename without `.md` (lowercase, hyphenated) |
| `cr` | string | yes | Challenge Rating: `"0"`, `"1/8"`, `"1/4"`, `"1/2"`, `"1"` … `"30"` |
| `type` | string | yes | Creature type, lowercase (e.g. "aberration", "elemental") |
| `size` | string | no | e.g. "Large", "Medium" |
| `alignment` | string | no | e.g. "lawful evil", "neutral" |
| `source` | string | no | Normalized code (e.g. MM, VGM); display name via shared mapping. |
| `path` | string | no | Relative path to the monster’s `.md` file; can be derived from `slug` and edition at build time if omitted |

Parse script and index script both use this schema. Sort order for index: by CR (use a fixed order list for string CR: 0, 1/8, 1/4, 1/2, 1 … 30), then by `name`.

## Decisions before implementation (locked)

### Slug rules

Apply in order to the monster **name** to produce `slug`:

1. **Lowercase** the string.
2. **Apostrophes:** Remove. (e.g. "Baba Yaga's" → "baba yagas"; no trailing 's' kept as separate token.)
3. **All other punctuation:** Strip (remove). Includes: periods, commas, parentheses, ampersands, colons, semicolons, etc. No replacement — delete the character.
4. **Spaces:** Replace each space or run of spaces with a single hyphen.
5. **Hyphens:** Collapse any run of hyphens to one; strip leading and trailing hyphens.
6. **Allowed characters:** Final slug must contain only `[a-z0-9-]`. If any other character remains (e.g. accented letters), strip it or replace with nothing.
7. **Empty result:** If the slug is empty after these steps, use a fallback (e.g. `monster-<index>` or skip and log).

Examples: "Young Black Dragon" → `young-black-dragon`; "Baba Yaga's X" → `baba-yagas-x`; "Iron Golem (variant)" → `iron-golem-variant`.

### Duplicate names / disambiguation

**Duplicate slugs are disambiguated.** When generating a slug, if that slug is already used by an earlier monster in the same run:

- **If `source` is normalized:** Append `-<source_code>` (lowercase). Example: second "Goblin" from VGM → `goblin-vgm`. The first monster with that base slug keeps the base slug (e.g. `goblin`).
- **If `source` is missing or not normalized:** Append `-2`, `-3`, … in encounter order.

Detection is by exact slug after applying slug rules; disambiguation is applied in the order monsters are processed (e.g. document order in monsters-A-Z.md).

### Source: free text vs normalized

**Source is stored as a normalized code** (e.g. `MM`, `VGM`, `DMG2024`). A shared mapping (e.g. in the parse/index script or `data/monster_sources.csv`) maps code → display name for use in generated markdown or index tables. This matches the pattern used in `format_items.py` / `format_spells.py` (`SOURCE_RENDER` / CSV). Benefits: consistent display, reliable disambiguation when appending `-<source_code>` to slugs, and easier filtering by source.

- **In JSON:** Store the code only (e.g. `"source": "MM"`).
- **When displaying:** Look up code in the mapping; if missing, show the code as-is or add it to the mapping.
- **Parse from A-Z:** If the source file has no source info, leave `source` absent or use a default (e.g. `MM`) until you have a real source field in the input; optional later enhancement to parse or infer source.

## 2. Docs structure

- **Monsters root:** `docs/{edition}/monsters/` (edition from config: e.g. `dnd2024` or `dnd5e`).
- **Reference page:** Copy `monsters.md` → `docs/{edition}/monsters/stat-blocks.md`; add to nav as "Stat blocks" or "Using monsters".
- **Metadata:** `docs/{edition}/monsters/monsters.json` — array of objects matching the JSON schema above. Generated by parse script.
- **Index page:** `docs/{edition}/monsters/index.md` — generated by index script from JSON (tabbed by CR).
- **Table page:** `docs/{edition}/monsters/all.md` — generated by index script from JSON (single table; optional).

## 3. Parse script (monsters-A-Z → JSON + per-monster .md)

**New file:** `scripts/parse_monsters_az.py` (or `split_monsters_az.py`)

- **Config:** Edition folder at top or CLI/env (e.g. `EDITION = "dnd2024"`). Paths: `REPO_ROOT / "docs" / EDITION / "monsters"`.
- **Input:** `monsters-A-Z.md` (repo root).
- **Logic:** Split on `### `. For each segment: **Title** from line after `### `; **Slug** from title (lowercase, hyphenate); **CR** from `**CR** N (XP ...)` (0, 1/8, 1/4, 1/2, 1 … 30); **Type** from italic `_Size Type, Alignment_` (first word after size); **Body** = rest of segment (normalize to single `# <Title>` at top).
- **Output:** Write `docs/{edition}/monsters/monsters.json`: array of objects matching the JSON schema (name, slug, cr, type required; size, alignment, source, path optional). Source = normalized code; use slug rules and disambiguation rules above. Sorted by CR (string order: 0, 1/8, 1/4, 1/2, 1 … 30) then name. Write one file per monster: `docs/{edition}/monsters/<slug>.md` (body only).
- Handle missing CR/type (default or skip); duplicate slugs handled per disambiguation rules.

## 4. Index generation script (JSON → index.md + all.md)

**New file:** `scripts/generate_monster_index.py`

- **Config:** Same edition as parse script (constant or CLI/env).
- **Input:** `docs/{edition}/monsters/monsters.json` only (no markdown parsing).
- **Output:** `docs/{edition}/monsters/index.md`: intro + link to Stat blocks; tabbed blocks "All" and "CR 0", "CR 1/8", …; each tab = table `[Name](slug.md) | CR | Type`. Optionally `docs/{edition}/monsters/all.md`: single table of all monsters.
- CR order: 0, 1/8, 1/4, 1/2, 1, 2, … 30. If no monsters, emit empty table(s).

## 5. Navigation and search

**File:** `mkdocs.yml`

- Use the chosen edition folder (e.g. `dnd2024` or `dnd5e`) in one place so changing edition is a single edit.
- Under `nav:`, add **Monsters** (e.g. after Species):
  - **Stat blocks:** `{edition}/monsters/stat-blocks.md`
  - **All Monsters:** `{edition}/monsters/index.md`
- Optionally add `{edition}/monsters` and `{edition}/monsters/all` to `plugins.exclude-search.exclude`.

## 6. Implementation order

1. Add `monster` / `creatures` to `CATEGORY_TO_FOLDER` in `scripts/txt_to_mkdocs.py`.
2. Define edition constant/CLI/env in parse and index scripts (default e.g. `dnd2024`).
3. Create `docs/{edition}/monsters/` and copy `monsters.md` → `docs/{edition}/monsters/stat-blocks.md`.
4. Implement parse script: read `monsters-A-Z.md`, emit `monsters.json` + per-monster `.md`.
5. Implement index script: read `monsters.json`, emit `index.md` and optionally `all.md`.
6. Run parse script, then index script; spot-check monster pages and index.
7. Update `mkdocs.yml` (Monsters nav, optional exclude-search) using the same edition value.

## 7. Optional later

- **format_monsters.py:** Normalize stat-block layout in `.md`; add monster section headers to `SECTION_HEADERS` in `txt_to_mkdocs.py` if needed.
- **Second edition:** Use same scripts with different `EDITION` (e.g. `dnd5e`) and a separate bestiary file to populate `docs/dnd5e/monsters/`.

## Files to add or change

| Action | File |
|--------|------|
| Edit | `scripts/txt_to_mkdocs.py` |
| Create | `docs/{edition}/monsters/stat-blocks.md` (from `monsters.md`) |
| Create | `scripts/parse_monsters_az.py` (or `split_monsters_az.py`) |
| Create | `scripts/generate_monster_index.py` |
| Create or edit | `data/monster_sources.csv` or SOURCE_RENDER in script (code → display name for source) |
| Create | `docs/{edition}/monsters/monsters.json` (by parse script) |
| Create | `docs/{edition}/monsters/index.md` (by index script) |
| Create | `docs/{edition}/monsters/all.md` (optional, by index script) |
| Create | `docs/{edition}/monsters/<slug>.md` (many, by parse script) |
| Edit | `mkdocs.yml` |

`{edition}` = configurable (e.g. `dnd2024` or `dnd5e`).
