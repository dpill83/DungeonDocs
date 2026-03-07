#!/usr/bin/env python3
"""
Parse monsters-A-Z.md into monsters.json (metadata) and one .md file per monster.
Edition folder is configurable via EDITION constant or DUNGEONDOCS_EDITION env.
"""

import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EDITION = os.environ.get("DUNGEONDOCS_EDITION", "dnd2024")
MONSTERS_DIR = REPO_ROOT / "docs" / EDITION / "monsters"
INPUT_FILE = REPO_ROOT / "monsters-A-Z.md"

# CR sort order (string values)
CR_ORDER = [
    "0", "1/8", "1/4", "1/2", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
    "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
]

# Normalized source codes (for disambiguation); A-Z file has no source, so we leave source absent
KNOWN_SOURCE_CODES = frozenset({"MM", "VGM", "MTF", "DMG", "DMG2024", "PHB", "PHB2024", "TCE", "XGE"})


def slug_from_name(name: str) -> str:
    """Apply plan slug rules: lowercase, remove apostrophes, strip punctuation, spaces to hyphens."""
    if not name or not name.strip():
        return ""
    s = name.strip().lower()
    # 1. Apostrophes: remove
    s = s.replace("'", "")
    # 2. All other punctuation: strip (remove)
    s = re.sub(r"[^\w\s-]", "", s)
    # 3. Spaces -> single hyphen
    s = re.sub(r"\s+", "-", s)
    # 4. Collapse hyphens, strip leading/trailing
    s = re.sub(r"-+", "-", s).strip("-")
    # 5. Only [a-z0-9-]
    s = re.sub(r"[^a-z0-9-]", "", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s


def parse_cr(line: str) -> str | None:
    """Extract CR from a line like '**CR** 10 (XP 5,900...)' or '**CR** 1/8 (XP 25...)'."""
    m = re.search(r"\*\*CR\*\*\s*(\d+(?:/\d+)?)", line, re.IGNORECASE)
    if m:
        return m.group(1)
    return None


def parse_italic_line(line: str) -> tuple[str | None, str | None, str | None]:
    """Parse _Size Type, Alignment_ -> (size, type, alignment). Type = first word after size."""
    line = line.strip()
    if not line.startswith("_") or not line.endswith("_"):
        return None, None, None
    inner = line[1:-1].strip()
    if "," in inner:
        part0, part1 = inner.split(",", 1)
        size_type = part0.strip()
        alignment = part1.strip().lower()
    else:
        size_type = inner
        alignment = None
    words = size_type.split()
    if not words:
        return None, None, alignment
    size = words[0]
    # Type is the last word before the comma (e.g. "Medium Humanoid" -> Humanoid, "Large or Huge Elemental" -> Elemental)
    type_word = words[-1].lower() if len(words) > 1 else None
    return size, type_word, alignment


def extract_blocks(content: str) -> list[tuple[str, str]]:
    """Split content by lines starting with '### ' (exactly three #) so we don't split on ####."""
    blocks = []
    current_name: str | None = None
    current_lines: list[str] = []
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("### ") and not stripped.startswith("#### "):
            if current_name is not None:
                body = "# " + current_name + "\n\n" + "\n".join(current_lines).strip()
                blocks.append((current_name, body))
            current_name = stripped[4:].strip()  # after "### "
            current_lines = []
        else:
            if current_name is not None:
                current_lines.append(line)
    if current_name is not None:
        body = "# " + current_name + "\n\n" + "\n".join(current_lines).strip()
        blocks.append((current_name, body))
    return blocks


def parse_block(name: str, body: str) -> dict:
    """From a block body, extract cr, type, size, alignment. Return dict for JSON entry."""
    cr = None
    size = None
    type_val = None
    alignment = None
    for line in body.split("\n"):
        line_stripped = line.strip()
        if cr is None:
            c = parse_cr(line)
            if c is not None:
                cr = c
        if size is None and line_stripped.startswith("_"):
            s, t, a = parse_italic_line(line_stripped)
            if s:
                size = s
            if t:
                type_val = t
            if a:
                alignment = a
    return {
        "name": name,
        "cr": cr or "0",
        "type": type_val or "unknown",
        "size": size,
        "alignment": alignment,
    }


def disambiguate_slug(base_slug: str, used_slugs: set, source: str | None, source_counter: dict) -> str:
    """Return unique slug; if base_slug taken, append -<source> or -2, -3."""
    if base_slug not in used_slugs:
        used_slugs.add(base_slug)
        return base_slug
    if source and source.upper() in KNOWN_SOURCE_CODES:
        suffix = "-" + source.lower()
        candidate = base_slug + suffix
        if candidate not in used_slugs:
            used_slugs.add(candidate)
            return candidate
    # -2, -3, ...
    key = base_slug
    n = source_counter.get(key, 1) + 1
    source_counter[key] = n
    candidate = f"{base_slug}-{n}"
    used_slugs.add(candidate)
    return candidate


def monster_sort_key(entry: dict) -> tuple[int, str]:
    """Sort by CR order then name."""
    cr = entry.get("cr", "0")
    try:
        cr_idx = CR_ORDER.index(cr)
    except ValueError:
        cr_idx = 999
    return (cr_idx, (entry.get("name") or "").lower())


def main() -> None:
    if not INPUT_FILE.exists():
        print(f"Input not found: {INPUT_FILE}", file=sys.stderr)
        sys.exit(1)
    content = INPUT_FILE.read_text(encoding="utf-8", errors="replace")
    blocks = extract_blocks(content)
    if not blocks:
        print("No ### blocks found.", file=sys.stderr)
        sys.exit(1)
    MONSTERS_DIR.mkdir(parents=True, exist_ok=True)
    used_slugs: set[str] = set()
    source_counter: dict[str, int] = {}
    entries: list[dict] = []
    default_source = None  # A-Z file has no source; leave absent
    for name, body in blocks:
        parsed = parse_block(name, body)
        base_slug = slug_from_name(name)
        if not base_slug:
            base_slug = f"monster-{len(entries) + 1}"
        slug = disambiguate_slug(base_slug, used_slugs, parsed.get("source") or default_source, source_counter)
        path_rel = f"docs/{EDITION}/monsters/{slug}.md"
        entry = {
            "name": name,
            "slug": slug,
            "cr": parsed["cr"],
            "type": parsed["type"],
        }
        if parsed.get("size"):
            entry["size"] = parsed["size"]
        if parsed.get("alignment"):
            entry["alignment"] = parsed["alignment"]
        if default_source:
            entry["source"] = default_source
        entry["path"] = path_rel
        entries.append(entry)
        md_path = MONSTERS_DIR / f"{slug}.md"
        md_path.write_text(body, encoding="utf-8")
    entries.sort(key=monster_sort_key)
    json_path = MONSTERS_DIR / "monsters.json"
    json_path.write_text(
        json.dumps(entries, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Wrote {len(entries)} monsters to {MONSTERS_DIR}", file=sys.stderr)
    print(f"Wrote {json_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
