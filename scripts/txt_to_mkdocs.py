#!/usr/bin/env python3
"""
Convert scraped D&D wiki .txt files to MkDocs-ready .md files.
Reads from scraped-dnd5e/ and scraped-dnd2024/, outputs to docs/.
Improved formatting, especially for 2024 backgrounds.
"""

import os
import re
import sys
from datetime import date
from pathlib import Path

GENERATOR_STAMP = f"<!-- generated-by: scripts/txt_to_mkdocs.py v{date.today().isoformat()} -->"

# Wiki prefix -> docs subfolder
WIKI_MAP = {
    "dnd5e-wikidot-com": "dnd5e",
    "dnd2024-wikidot-com": "dnd2024",
}

# Multi-word categories (match first, longest first)
MULTI_CATEGORIES = [
    "wondrous-items",
    "adventuring-gear",
    "spell-list",
    "spell-lists",
    "magic-item",
    "magic-items",
]

# Category -> folder name
CATEGORY_TO_FOLDER = {
    "background": "backgrounds",
    "feat": "feats",
    "discipline": "disciplines",
    "spell": "spells",
    "spells": "spells",
    "lineage": "lineage",
    "race": "races",
    "armor": "armor",
    "wondrous-items": "wondrous-items",
    "adventuring-gear": "adventuring-gear",
    "adventuring": "adventuring-gear",
    "spell-list": "spell-lists",
    "spell-lists": "spell-lists",
    "magic-item": "magic-items",
    "magic-items": "magic-items",
    "artificer": "artificer",
    "barbarian": "barbarian",
    "bard": "bard",
    "cleric": "cleric",
    "druid": "druid",
    "fighter": "fighter",
    "monk": "monk",
    "mystic": "mystic",
    "paladin": "paladin",
    "ranger": "ranger",
    "rogue": "rogue",
    "sorcerer": "sorcerer",
    "warlock": "warlock",
    "wizard": "wizard",
    "reference": "reference",
    "ua": "unearthed-arcana",
}

# Section headers to convert to ##
SECTION_HEADERS = {
    "Features",
    "Suggested Characteristics",
    "Personality Traits",
    "Ideals",
    "Bonds",
    "Flaws",
    "Proficiencies",
    "Equipment",
    "Languages",
    "Skill Proficiencies",
    "Tool Proficiencies",
    "Tool Proficiency",
    "Source",
    "Ability Scores",
    "Feat",
}

# Lines to strip from top of content
STRIP_TOP = {"Fold", "Unfold", "Table of Contents"}


def parse_filename(filename: str) -> tuple[str | None, str, str]:
    name = Path(filename).stem
    for prefix, wiki_folder in WIKI_MAP.items():
        if name.startswith(prefix + "-"):
            rest = name[len(prefix) + 1 :]
            break
    else:
        return None, "", ""

    parts = rest.split("-")
    category = ""
    item_slug = rest

    # Try multi-word categories first
    for mc in MULTI_CATEGORIES:
        mc_parts = mc.split("-")
        if len(parts) >= len(mc_parts) and "-".join(parts[: len(mc_parts)]) == mc:
            category = mc
            item_slug = "-".join(parts[len(mc_parts) :]) if len(parts) > len(mc_parts) else mc
            break

    if not category and len(parts) >= 2:
        category = parts[0]
        item_slug = "-".join(parts[1:])
    elif not category and len(parts) == 1:
        category = "reference"
        item_slug = parts[0]

    folder = CATEGORY_TO_FOLDER.get(category, category + "s" if category else "reference")
    return wiki_folder, folder, item_slug or "page"


def slug_to_title(slug: str) -> str:
    return " ".join(w.capitalize() for w in slug.replace("-", " ").split())


def _looks_like_content(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    if len(s) > 60:
        return True
    if s.endswith(".") or " and " in s or " the " in s:
        return True
    return False


def convert_content(text: str, title: str, category: str) -> str:
    lines = [line.rstrip() for line in text.splitlines()]
    out = []
    i = 0

    # Skip ToC block
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped in STRIP_TOP or "Table of Contents" in stripped:
            i += 1
            continue
        if _looks_like_content(lines[i]):
            break
        i += 1

    out.append(f"# {title}\n")
    out.append(GENERATOR_STAMP + "\n\n")

    # Collect flavor description until first "Key:" line
    description = []
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.endswith(":") and len(stripped) < 60:
            potential_key = stripped.rstrip(":").strip()
            if potential_key in {"Source", "Ability Scores", "Feat", "Skill Proficiencies",
                                 "Tool Proficiency", "Tool Proficiencies", "Languages", "Equipment"}:
                break
        if stripped or description:  # keep blank lines inside description
            description.append(line)
        i += 1

    if description:
        out.append("\n".join(description).strip() + "\n\n")

    # Special handling for backgrounds
    if category == "backgrounds":
        out.append("## Benefits\n\n")
        out.append("| Feature                | Details                                      |\n")
        out.append("|------------------------|----------------------------------------------|\n")

        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            if not stripped:
                i += 1
                continue
            if stripped.endswith(":"):
                key = stripped.rstrip(":").strip()
                i += 1
                value_lines = []
                while i < len(lines) and (lines[i].strip() and not lines[i].strip().endswith(":")):
                    value_lines.append(lines[i].strip())
                    i += 1
                value = " ".join(value_lines)

                # Format lists
                value = value.replace(", ", "<br>").replace(" and ", "<br>")

                # Special equipment formatting: parse "Choose A or B: (A) ...; or (B) ..." or "(A)" and "(B)" patterns
                if "Equipment" in key and (
                    "Choose A or B" in value or "or (B)" in value or ("(A)" in value and "(B)" in value)
                ):
                    if ":" in value:
                        value = value.split(":", 1)[1].strip()
                    parts = re.split(r";\s*or\s*", value)
                    if len(parts) == 2:
                        a = parts[0].strip().lstrip("(A)").strip().replace(", ", "<br>").replace(" and ", "<br>")
                        b = parts[1].strip().lstrip("(B)").strip().replace(", ", "<br>").replace(" and ", "<br>")
                        value = "<ul><li><strong>A:</strong> " + a + "</li><li><strong>B:</strong> " + b + "</li></ul>"

                out.append(f"| **{key}** | {value} |\n")
            else:
                # Remaining content (e.g., 5e feature description + suggested characteristics)
                if lines[i:]:
                    out.append("\n" + "\n".join(lines[i:]).strip() + "\n")
                break

        out.append("\n")
        return "".join(out).strip() + "\n"

    # Fallback: original-style conversion for non-background pages
    prev_blank = True
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            out.append("")
            prev_blank = True
            i += 1
            continue

        header_candidate = stripped.rstrip(":").strip()
        if header_candidate in SECTION_HEADERS and prev_blank:
            out.append(f"\n## {header_candidate}\n")
            prev_blank = False
        else:
            out.append(line)
            prev_blank = stripped == ""

        i += 1

    return "\n".join(out).strip() + "\n"


def convert_file(txt_path: Path, docs_root: Path) -> Path | None:
    filename = txt_path.name
    wiki_folder, category_folder, item_slug = parse_filename(filename)
    if not wiki_folder:
        return None

    item_clean = item_slug.replace(",", "").replace(".txt", "")
    slug_clean = re.sub(r"[^\w\-]", "", item_clean) or "page"
    out_dir = docs_root / wiki_folder / category_folder
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{slug_clean}.md"

    try:
        content = txt_path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        print(f"  Warning: could not read {txt_path}: {e}", file=sys.stderr)
        return None

    title = slug_to_title(item_clean)
    md_content = convert_content(content, title, category_folder)

    out_path.write_text(md_content, encoding="utf-8")
    return out_path


def main():
    repo_root = Path(__file__).resolve().parent.parent
    docs_root = repo_root / "docs"
    scraped_dirs = [
        repo_root / "scraped-dnd5e",
        repo_root / "scraped-dnd2024",
    ]

    total = 0
    for scraped_dir in scraped_dirs:
        if not scraped_dir.is_dir():
            print(f"Skipping (not found): {scraped_dir}", file=sys.stderr)
            continue
        for txt_path in scraped_dir.glob("*.txt"):
            result = convert_file(txt_path, docs_root)
            if result:
                total += 1
                if total <= 5 or total % 500 == 0:
                    print(f"  [{total}] {txt_path.name} -> {result.relative_to(docs_root)}", file=sys.stderr)

    print(f"Converted {total} files to {docs_root}", file=sys.stderr)


if __name__ == "__main__":
    main()