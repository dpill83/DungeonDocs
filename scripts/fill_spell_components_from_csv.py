#!/usr/bin/env python3
"""
Fill missing spell material components from data/dd-5e-spell-component-database.csv.
Updates spell .md files and index.md, then regenerates data/spells_missing_material_components.txt.
"""

import csv
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

# Reuse logic from list_spells_missing_material_components
from list_spells_missing_material_components import (
    DATA_DIR,
    INDEX_PATH,
    SPELLS_DIR,
    build_components_with_material,
    generate_txt,
    has_material_but_not_described,
    parse_index,
    update_index_components,
    update_spell_md,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = DATA_DIR / "dd-5e-spell-component-database.csv"


def normalize_name_for_match(name: str) -> str:
    """Lowercase, normalize apostrophes/hyphens to space, collapse spaces for matching."""
    if not name:
        return ""
    s = name.lower().strip()
    for c in ("'", "'", "'", "`", "\u2019", "-"):
        s = s.replace(c, " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def normalize_name_collapsed(name: str) -> str:
    """Like normalize_name_for_match but collapse all spaces (e.g. 'non detection' -> 'nondetection')."""
    return re.sub(r"\s+", "", normalize_name_for_match(name))


def alias_keys_for_match(name: str) -> list[str]:
    """Return normalized key and optional alternate (e.g. 'evil and good' <-> 'good and evil')."""
    key = normalize_name_for_match(name)
    keys = [key]
    # "protection from evil and good" <-> "protection from good and evil"
    m = re.match(r"^(.+\s)(\w+)\s+and\s+(\w+)$", key)
    if m:
        prefix, a, b = m.group(1), m.group(2), m.group(3)
        if a != b:
            keys.append(prefix + b + " and " + a)
    return keys


def load_csv_components(csv_path: Path) -> dict[str, str]:
    """
    Load CSV: Level, Spell Name, Component.
    Return mapping: normalized spell name -> single component string (multiple joined with ' or ').
    """
    result: dict[str, list[str]] = {}
    if not csv_path.exists():
        return {}

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            spell_name = (row.get("Spell Name") or "").strip()
            component = (row.get("Component") or "").strip()
            if not spell_name or not component:
                continue
            key = normalize_name_for_match(spell_name)
            if key not in result:
                result[key] = []
            if component not in result[key]:
                result[key].append(component)

    # Join multiple components with " or "; add collapsed key and "and"/"or" alias
    out: dict[str, str] = {}
    for name_key, comps in result.items():
        desc = " or ".join(comps)
        out[name_key] = desc
        out[re.sub(r"\s+", "", name_key)] = desc  # "non detection" -> "nondetection"
        m = re.match(r"^(.+\s)(\w+)\s+and\s+(\w+)$", name_key)
        if m:
            prefix, a, b = m.group(1), m.group(2), m.group(3)
            if a != b:
                out[prefix + b + " and " + a] = desc
        if " and " in name_key:
            out[name_key.replace(" and ", " or ")] = desc  # "Locate Animals and Plants" <-> "or"
    return out


def main() -> None:
    if not CSV_PATH.exists():
        print(f"ERROR: {CSV_PATH} not found")
        return
    if not INDEX_PATH.exists():
        print(f"ERROR: {INDEX_PATH} not found")
        return

    csv_components = load_csv_components(CSV_PATH)
    spells = parse_index(INDEX_PATH)
    updated_spells = dict(spells)
    applied = 0

    for slug, spell in spells.items():
        if not has_material_but_not_described(spell["components"]):
            continue
        name = spell["name"]
        desc = None
        keys_to_try = list(alias_keys_for_match(name)) + [normalize_name_collapsed(name)]
        for key in keys_to_try:
            if key in csv_components:
                desc = csv_components[key]
                break
        if not desc:
            continue
        new_components = build_components_with_material(spell["components"], desc)
        if new_components == spell["components"]:
            continue
        update_spell_md(slug, new_components)
        updated_spells[slug] = {**spell, "components": new_components}
        applied += 1

    if applied:
        update_index_components(INDEX_PATH, updated_spells)
        print(f"Applied {applied} component description(s) from CSV.")
    else:
        print("No spell components applied (no matches or already filled).")

    # Regenerate missing list
    spells = parse_index(INDEX_PATH)
    generate_txt(spells)
    print("Regenerated spells_missing_material_components.txt.")


if __name__ == "__main__":
    main()
