# Scripts

## Spell Formatting

Standardize D&D 2024 spell markdown files to match `dungeondocs-formatting-guide-spells.md`.

### format_spells.py

Rebuilds spell page headers and stat blocks using `docs/dnd2024/spells/index.md` as the source of truth. Preserves spell body text exactly. Source (book) comes from `data/spell_sources.csv` (default: UNKNOWN).

```bash
python scripts/format_spells.py
```

Options:

- `--dry-run` – Write to `spells_formatted/` instead of overwriting in place
- `--output DIR` – Write to a custom directory instead of in-place

Outputs:

- `data/format_failures.json` – Spells not found in index, parse errors
- `data/format_warnings.csv` – Warnings (missing fields, ambiguous body start, etc.)

### audit_spells.py

Validates spell files for required structure and lists spells with Source = UNKNOWN.

```bash
python scripts/audit_spells.py
```

## Magic Item Formatting

Standardize D&D 2024 magic item markdown files to a consistent format (see `dungeondocs-formatting-guide-magic-items.md`).

### format_items.py

Rebuilds magic item page headers using `docs/dnd2024/magic-items/all.md` as the source of truth for name, type, rarity, and attunement. Preserves item body text exactly. Source (book) comes from `data/item_sources.csv` (default: UNKNOWN).

```bash
python scripts/format_items.py
```

Options:

- `--dry-run` – Write to `items_formatted/` instead of overwriting in place
- `--output DIR` – Write to a custom directory instead of in-place

Outputs:

- `data/item_format_failures.json` – Items not found in index, parse errors
- `data/item_format_warnings.csv` – Warnings (missing fields, empty body, etc.)
- `data/item_sources.csv` – Created/updated with slug, name, source, notes (default source UNKNOWN; non-UNKNOWN preserved on reruns)

### audit_items.py

Validates magic item files for required structure (title, Source line, type/rarity line, non-empty body) and lists items with Source = Unknown.

```bash
python scripts/audit_items.py
```
