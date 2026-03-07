#!/usr/bin/env python3
"""
Rewrite monster .md files into a web-native stat block layout: HTML structure with
compact summary, 6-ability grid, details section, and distinct Traits/Actions/etc. sections.
Reads from docs/{edition}/monsters/*.md (skips index, by-name, by-cr, by-type, stat-blocks).
"""

import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EDITION = os.environ.get("DUNGEONDOCS_EDITION", "dnd2024")
MONSTERS_DIR = REPO_ROOT / "docs" / EDITION / "monsters"

SKIP_FILES = frozenset({"index.md", "by-name.md", "by-cr.md", "by-type.md", "stat-blocks.md"})


def parse_abilities(table_html: str) -> list[tuple[str, str, str, str]]:
    """Extract (abbrev, score, mod, save) for each of STR, DEX, CON, INT, WIS, CHA."""
    abilities = []
    # Match <td><strong>STR</strong></td><td>21</td><td>+5</td><td>+5</td> etc.
    pattern = r"<td><strong>(STR|DEX|CON|INT|WIS|CHA)</strong></td>\s*<td>([^<]*)</td>\s*<td>([^<]*)</td>\s*<td>([^<]*)</td>"
    for m in re.finditer(pattern, table_html, re.IGNORECASE):
        abilities.append((m.group(1).upper(), m.group(2), m.group(3), m.group(4)))
    return abilities


def parse_detail_line(line: str) -> tuple[str, str] | None:
    """Return (label, value) for lines like **Skills** History +12, ... or **CR** 10 (...)."""
    m = re.match(r"\*\*([^*]+)\*\*\s*(.*)", line.strip())
    if m:
        return (m.group(1).strip(), m.group(2).strip().replace("<br>", "").strip())
    return None


def inline_to_html(text: str) -> str:
    """Convert _italic_ and **bold** and **_bold italic_** to HTML. Preserve <br> and &emsp;."""
    out = []
    i = 0
    while i < len(text):
        if text[i : i + 3] == "**_":
            end = text.find("_**", i + 3)
            if end == -1:
                out.append("<strong><em>" + inline_to_html(text[i + 3 :].replace("<", "&lt;").replace(">", "&gt;")) + "</em></strong>")
                return "".join(out)
            out.append("<strong><em>" + text[i + 3 : end].replace("<", "&lt;").replace(">", "&gt;") + "</em></strong>")
            i = end + 3
        elif text[i : i + 2] == "**":
            end = text.find("**", i + 2)
            if end == -1:
                out.append("<strong>" + text[i + 2 :].replace("<", "&lt;").replace(">", "&gt;") + "</strong>")
                return "".join(out)
            out.append("<strong>" + text[i + 2 : end].replace("<", "&lt;").replace(">", "&gt;") + "</strong>")
            i = end + 2
        elif text[i : i + 1] == "_" and i + 1 < len(text) and text[i + 1] != "_":
            end = text.find("_", i + 1)
            if end == -1:
                out.append("<em>" + text[i + 1 :].replace("<", "&lt;").replace(">", "&gt;") + "</em>")
                return "".join(out)
            out.append("<em>" + text[i + 1 : end].replace("<", "&lt;").replace(">", "&gt;") + "</em>")
            i = end + 1
        elif text[i : i + 4] == "<br>":
            out.append("<br>")
            i += 4
        elif text[i : i + 6] == "&emsp;":
            out.append("&emsp;")
            i += 6
        else:
            out.append(text[i].replace("<", "&lt;").replace(">", "&gt;"))
            i += 1
    return "".join(out)


def format_monster(content: str) -> str:
    """Parse monster markdown and return new content with HTML stat block."""
    lines = content.split("\n")
    # Strip trailing next-monster header if present
    while lines and re.match(r"^## [A-Z]", lines[-1].strip()):
        lines.pop()
    i = 0
    title = ""
    subtitle = ""
    ac = initiative = hp = speed = ""
    table_html = ""
    details: list[tuple[str, str]] = []
    sections: list[tuple[str, str]] = []  # (heading, body)

    # Title
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("# "):
            title = line.strip().lstrip("# ").strip()
            i += 1
            break
        i += 1
    if not title:
        return content

    # Subtitle _Size Type, Alignment_
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if s.startswith("_") and s.endswith("_"):
            subtitle = s[1:-1].strip()
            i += 1
            break
        i += 1

    # AC, Initiative, HP, Speed (may be 1 or 2 lines with <br>)
    chunk = []
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("<table"):
            break
        chunk.append(line)
        i += 1
    chunk_text = " ".join(chunk)
    for part in re.split(r"\s*<br>\s*", chunk_text):
        if "**AC**" in part:
            m = re.search(r"\*\*AC\*\*\s*(\d+)", part)
            if m:
                ac = m.group(1)
        if "**Initiative**" in part:
            m = re.search(r"\*\*Initiative\*\*\s*([^<\s]+(?:\s*\([^)]+\))?)", part)
            if m:
                initiative = m.group(1).strip()
        if "**HP**" in part:
            m = re.search(r"\*\*HP\*\*\s*([^<]+)", part)
            if m:
                hp = m.group(1).strip()
        if "**Speed**" in part:
            m = re.search(r"\*\*Speed\*\*\s*([^<]+)", part)
            if m:
                speed = m.group(1).strip()

    # Table
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("<table"):
            table_parts = [lines[i]]
            i += 1
            while i < len(lines) and "</table>" not in lines[i]:
                table_parts.append(lines[i])
                i += 1
            if i < len(lines):
                table_parts.append(lines[i])
                i += 1
            table_html = "\n".join(table_parts)
            break
        i += 1
        if i < len(lines):
            line = lines[i]

    abilities = parse_abilities(table_html)

    # Details (**Skills**, **Senses**, etc.) until ####
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("#### "):
            break
        d = parse_detail_line(line)
        if d:
            details.append(d)
        i += 1

    # Sections: #### Name, <hr>, content until next ####
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("#### "):
            section_title = line.strip().lstrip("#").strip()
            i += 1
            # skip <hr> and blank
            while i < len(lines) and (lines[i].strip() == "" or lines[i].strip() == "<hr>"):
                i += 1
            body_lines = []
            while i < len(lines) and not lines[i].strip().startswith("#### "):
                body_lines.append(lines[i])
                i += 1
            body = "\n".join(body_lines).strip()
            body_html_parts = []
            for para in re.split(r"\n\n+", body):
                para = para.strip()
                if not para:
                    continue
                body_html_parts.append("<p>" + inline_to_html(para.replace("\n", "<br>\n")) + "</p>")
            sections.append((section_title, "\n".join(body_html_parts)))
        else:
            i += 1

    # Build output
    out = [f'<div class="monster-stat-block">']
    out.append(f'  <header class="monster-header">')
    out.append(f'    <h1 class="monster-title">{title}</h1>')
    out.append(f'    <p class="monster-subtitle">{subtitle}</p>')
    out.append(f'  </header>')
    out.append(f'  <div class="monster-summary">')
    out.append(f'    <span class="monster-summary-item"><strong>AC</strong> {ac}</span>')
    out.append(f'    <span class="monster-summary-item"><strong>Initiative</strong> {initiative}</span>')
    out.append(f'    <span class="monster-summary-item"><strong>HP</strong> {hp}</span>')
    out.append(f'    <span class="monster-summary-item"><strong>Speed</strong> {speed}</span>')
    out.append(f'  </div>')
    out.append(f'  <div class="monster-abilities" role="list">')
    for abbr, score, mod, save in abilities:
        out.append(f'    <div class="monster-ability" role="listitem">')
        out.append(f'      <span class="monster-ability-name">{abbr}</span>')
        out.append(f'      <span class="monster-ability-score">{score}</span>')
        out.append(f'      <span class="monster-ability-mod">{mod}</span>')
        out.append(f'      <span class="monster-ability-save">{save}</span>')
        out.append(f'    </div>')
    out.append(f'  </div>')
    out.append(f'  <dl class="monster-details">')
    for label, value in details:
        out.append(f'    <dt>{label}</dt>')
        out.append(f'    <dd>{inline_to_html(value)}</dd>')
    out.append(f'  </dl>')
    for section_title, section_body in sections:
        slug = section_title.lower().replace(" ", "-")
        out.append(f'  <section class="monster-section monster-section-{slug}" aria-labelledby="section-{slug}">')
        out.append(f'    <h2 class="monster-section-title" id="section-{slug}">{section_title}</h2>')
        out.append(f'    <div class="monster-section-content">')
        out.append(section_body)
        out.append(f'    </div>')
        out.append(f'  </section>')
    out.append("</div>")
    return "\n".join(out)


def main() -> None:
    if not MONSTERS_DIR.is_dir():
        print(f"Not a directory: {MONSTERS_DIR}")
        sys.exit(1)
    count = 0
    for path in sorted(MONSTERS_DIR.glob("*.md")):
        if path.name in SKIP_FILES:
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        try:
            new_content = format_monster(raw)
            path.write_text(new_content, encoding="utf-8")
            count += 1
        except Exception as e:
            print(f"Error {path.name}: {e}", file=sys.stderr)
    print(f"Formatted {count} monster pages.")


if __name__ == "__main__":
    main()
