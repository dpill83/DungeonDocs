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
