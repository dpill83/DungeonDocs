#!/usr/bin/env python3
"""
Generate docs/dnd2024/unearthed-arcana/index.md from the UA folder.
Scans for spell-*, subclass-*, magic-item-*, class-*, feat-* and groups them
into sections with readable display names and links.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
UA_DIR = REPO_ROOT / "docs" / "dnd2024" / "unearthed-arcana"
INDEX_MD = UA_DIR / "index.md"

# Prefix (filename start) -> (section title, display order)
PREFIX_SECTIONS = [
    ("spell-", "Spells"),
    ("subclass-", "Subclasses"),
    ("magic-item-", "Magic Items"),
    ("class-", "Classes"),
    ("feat-", "Feats"),
]

SKIP_FILES = {"index.md", "all.md"}


def slug_to_display(slug: str) -> str:
    """Convert filename slug (after prefix) to display name: replace - with space, title case."""
    s = slug.replace("-", " ").title()
    # Common possessive: "S " in "Tasha S Mind" -> "'s "
    if " S " in s:
        s = s.replace(" S ", "'s ")
    return s


def main() -> None:
    groups: dict[str, list[tuple[str, str]]] = {title: [] for _, title in PREFIX_SECTIONS}
    prefix_map = {p: title for p, title in PREFIX_SECTIONS}

    for f in sorted(UA_DIR.glob("*.md")):
        if f.name in SKIP_FILES:
            continue
        stem = f.stem
        for prefix, section_title in PREFIX_SECTIONS:
            if stem.startswith(prefix):
                rest = stem[len(prefix) :]
                display = slug_to_display(rest)
                groups[section_title].append((display, f.name))
                break

    lines = [
        "# Unearthed Arcana",
        "",
        "Playtest and optional content from Unearthed Arcana. This material is not part of the core rules and may be revised in future publications.",
        "",
    ]

    for _, section_title in PREFIX_SECTIONS:
        items = groups[section_title]
        if not items:
            continue
        lines.append(f"## {section_title}")
        lines.append("")
        for display, filename in sorted(items, key=lambda x: x[0].lower()):
            lines.append(f"- [{display}]({filename})")
        lines.append("")

    INDEX_MD.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {INDEX_MD}")


if __name__ == "__main__":
    main()
