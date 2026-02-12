---
name: Integrate 2014 Missing Races
overview: Add missing 2014 species (Half-Elf, Half-Orc plus Exotic/Monstrous), reorganize the species index into Common, Exotic, Monstrous, Setting Specific, and Legacy (2014), and label any 2014-only option as (Legacy).
todos: []
isProject: false
---

# Integrate Missing Races from 2014 (Expanded)

## Context

The docs use **species** under [docs/dnd2024/species/](docs/dnd2024/species/). Goals:

1. Add the two missing 2014 PHB species: **Half-Elf** and **Half-Orc**.
2. Reorganize species into: **Common** (2024), **Exotic**, **Monstrous**, **Setting Specific**, and **Legacy (2014)**.
3. **Label rule:** Any species from 2014 that is not in the 2024 rules gets **(Legacy)** in its display name (in all.md and in mkdocs.yml nav).

**2024 PHB species** (no Legacy label): Aasimar, Dragonborn, Dwarf, Elf, Gnome, Goliath, Halfling, Human, Orc, Tiefling.

**2014-only core:** Half-Elf, Half-Orc → **(Legacy)**.

---

## 0. Source: docs/dnd5e/ (use existing content)

Most of this information already exists in the repo under **docs/dnd5e/** (currently excluded from the site build via `mkdocs.yml` exclude `dnd5e/**`).

- **[docs/dnd5e/lineage/](docs/dnd5e/lineage/)** — 87 lineage (race/species) .md files, including:
  - **2014 PHB:** half-elf.md, half-orc.md, plus dwarf, elf, gnome, halfling, human, dragonborn, tiefling.
  - **Exotic (your list):** aarakocra, aasimar, changeling, deep-gnome, duergar, eladrin, fairy, firbolg, genasi-air/earth/fire/water, githyanki, githzerai, goliath, harengon, kenku, locathah, owlin, satyr, sea-elf, shadar-kai, tabaxi, tortle, triton, verdan.
  - **Monstrous:** bugbear, centaur, goblin, grung, hobgoblin, kobold, lizardfolk, minotaur, orc, shifter, yuan-ti.md.
  - **Setting-specific:** kender (Dragonlance), kalashtar, warforged (Eberron), dhampir, hexblood, reborn (Ravenloft), loxodon, simic-hybrid, vedalken (Ravnica), astral elf, autognome, giff, hadozee, plasmoid, thri-kreen (Spelljammer), leonin (Theros), plus Plane Shift (aetherborn, aven, khenra, kor, merfolk, naga, siren, vampire).
- **[docs/dnd5e/reference/lineage.md](docs/dnd5e/reference/lineage.md)** — Index with the exact structure: Standard Lineages, Exotic Lineages, Monstrous Lineages, Setting Specific Lineages (Dragonlance, Eberron, Plane Shift, Ravenloft, Ravnica, Spelljammer, Theros), plus UA. Use this as the reference for how to structure [docs/dnd2024/species/all.md](docs/dnd2024/species/all.md).

**Integration approach:**

1. **Copy/adapt** content from `docs/dnd5e/lineage/*.md` into `docs/dnd2024/species/` for any species you want on the 2024 site. Optionally normalize format (e.g. add Creature Type/Size/Speed table to match existing dnd2024 species pages).
2. **Add (Legacy)** to display names and a *Source: 2014 … (Legacy)* line on each page that is 2014-only.
3. **Build all.md** using the same section order as dnd5e/reference/lineage.md (Common → Exotic → Monstrous → Setting Specific), then Lorwyn and Legacy (2014). Link only to species that have a page in dnd2024/species/ (either pre-existing or copied from dnd5e/lineage).
4. **No need to write content from scratch** for Half-Elf, Half-Orc, or the Exotic/Monstrous list — use the dnd5e lineage files as the source and adapt.

**Filename mapping (dnd5e lineage → dnd2024 species):** Most match (e.g. half-elf.md, aarakocra.md). Exceptions: deep-gnome.md, genasi-air.md (and earth/fire/water), sea-elf.md, shadar-kai.md, yuan-ti.md. Use the same filenames in dnd2024/species/ when copying.

---

## 1. Reorganized Species Index (all.md)

Restructure [docs/dnd2024/species/all.md](docs/dnd2024/species/all.md) into these sections:

- **Common Species** — 2024 Player's Handbook (Aasimar, Dragonborn, Dwarf, Elf, Gnome, Goliath, Halfling, Human, Orc, Tiefling). No (Legacy).
- **Exotic** — List all Exotic species; link only where a page exists; add (Legacy) for 2014-era options not in 2024.
- **Monstrous** — Same for Monstrous species.
- **Setting Specific** — Subsections by setting (Dragonlance, Eberron, Plane Shift, Ravenloft, Ravnica, Spelljammer, Theros). Link species that belong to each; Eberron already has Changeling, Kalashtar, Khoravar, Shifter, Warforged.
- **Legacy Species (2014)** — Explicit list of 2014-only options (Half-Elf, Half-Orc, and any Exotic/Monstrous that are 2014-only). Each shows **(Legacy)** and links when the page exists.
- **Lorwyn Species** — Keep existing (Boggart, Faerie, Flamekin, Lorwyn Changeling, Rimekin).
- **Exotic (other)** — Dhampir and any that don’t fit above.

Add a one-line intro note that **(Legacy)** means the option is from the 2014 rules and is not part of the 2024 core.

---

## 2. Exotic Species (your list)

**Source:** All have a corresponding file in **docs/dnd5e/lineage/** (e.g. aarakocra.md, deep-gnome.md). Copy into dnd2024/species/ when you want the page on the 2024 site.

| Species | In dnd2024? | In dnd5e/lineage? | In 2024 PHB? | Label |
|--------|-------------|-------------------|--------------|--------|
| Aarakocra | No | Yes (aarakocra.md) | No | (Legacy) |
| Aasimar | Yes | Yes | Yes | — |
| Changeling | Yes | Yes | No (Eberron) | (Legacy) or setting |
| Deep Gnome | No | Yes (deep-gnome.md) | No | (Legacy) |
| Duergar | No | Yes (duergar.md) | No | (Legacy) |
| Eladrin | No | Yes (eladrin.md) | In Elf 2024 | Optional (Legacy) |
| Fairy | Yes (Faerie) | Yes (fairy.md) | No | (Legacy) or keep Faerie |
| Firbolg | No | Yes (firbolg.md) | No | (Legacy) |
| Genasi (Air/Earth/Fire/Water) | No | Yes (genasi-*.md) | No | (Legacy) |
| Githyanki / Githzerai | No | Yes | No | (Legacy) |
| Goliath | Yes | Yes | Yes | — |
| Harengon | No | Yes (harengon.md) | No | (Legacy) |
| Kenku | No | Yes (kenku.md) | No | (Legacy) |
| Locathah | No | Yes (locathah.md) | No | (Legacy) |
| Owlin | No | Yes (owlin.md) | No | (Legacy) |
| Satyr | No | Yes (satyr.md) | No | (Legacy) |
| Sea Elf | No | Yes (sea-elf.md) | In Elf 2024? | Optional (Legacy) |
| Shadar-Kai | No | Yes (shadar-kai.md) | No | (Legacy) |
| Tabaxi | No | Yes (tabaxi.md) | No | (Legacy) |
| Tortle | No | Yes (tortle.md) | No | (Legacy) |
| Triton | No | Yes (triton.md) | No | (Legacy) |
| Verdan | No | Yes (verdan.md) | No | (Legacy) |

In all.md Exotic section: list all; link only where a dnd2024 species page exists. Add **(Legacy)** to display names for 2014-only. Populate pages by copying from dnd5e/lineage and adding Legacy source line.

---

## 3. Monstrous Species (your list)

**Source:** All have a file in **docs/dnd5e/lineage/** (e.g. bugbear.md, yuan-ti.md). Copy into dnd2024/species/ when you want the page on the 2024 site.

| Species | In dnd2024? | In dnd5e/lineage? | In 2024 PHB? | Label |
|--------|-------------|-------------------|--------------|--------|
| Bugbear | No | Yes (bugbear.md) | No | (Legacy) |
| Centaur | No | Yes (centaur.md) | No | (Legacy) |
| Goblin | No | Yes (goblin.md) | No | (Legacy) |
| Grung | No | Yes (grung.md) | No | (Legacy) |
| Hobgoblin | No | Yes (hobgoblin.md) | No | (Legacy) |
| Kobold | No | Yes (kobold.md) | No | (Legacy) |
| Lizardfolk | No | Yes (lizardfolk.md) | No | (Legacy) |
| Minotaur | No | Yes (minotaur.md) | No | (Legacy) |
| Orc | Yes | Yes (orc.md) | Yes | — |
| Shifter | Yes | Yes (shifter.md) | No (Eberron) | (Legacy) or setting |
| Yuan-Ti | No | Yes (yuan-ti.md) | No | (Legacy) |

In all.md Monstrous section: list all; link where dnd2024 species page exists; **(Legacy)** for 2014-only. Populate by copying from dnd5e/lineage.

---

## 4. Setting Specific

**Source:** [docs/dnd5e/reference/lineage.md](docs/dnd5e/reference/lineage.md) lists which species belong to each setting. Corresponding .md files live in docs/dnd5e/lineage/ (e.g. kender.md, kalashtar.md, warforged.md, dhampir.md, loxodon.md, leonin.md).

Categories (from dnd5e):

- **Dragonlance** — Kender (kender.md in dnd5e/lineage)
- **Eberron** — Changeling, Kalashtar, Khoravar, Shifter, Warforged (already in dnd2024/species)
- **Plane Shift** — Aetherborn, Aven, Khenra, Kor, Merfolk, Naga, Siren, Vampire (all in dnd5e/lineage)
- **Ravenloft** — Dhampir, Hexblood, Reborn (dnd5e/lineage)
- **Ravnica** — Loxodon, Simic Hybrid, Vedalken (dnd5e/lineage)
- **Spelljammer** — Astral Elf, Autognome, Giff, Hadozee, Plasmoid, Thri-kreen (dnd5e/lineage)
- **Theros** — Leonin (dnd5e/lineage)

In all.md add a "Setting Specific" section with these subheadings. Eberron can be filled immediately (link to existing dnd2024 species). For other settings, link when you copy the corresponding lineage file from dnd5e into dnd2024/species.

---

## 5. Legacy (2014) Labeling

- **Nav (mkdocs.yml):** For 2014-only species use **(Legacy)** in display name, e.g. `Half-Elf (Legacy): dnd2024/species/half-elf.md`. Apply to existing nav entries that are 2014-only (e.g. Changeling, Shifter if you treat them as Legacy).
- **all.md:** Same: `[Half-Elf (Legacy)](half-elf.md)`.
- **On the species page:** Optional line under title or in intro, e.g. *Source: 2014 Player's Handbook (Legacy).*

No Legacy label for: Aasimar, Dragonborn, Dwarf, Elf, Gnome, Goliath, Halfling, Human, Orc, Tiefling.

---

## 6. Files to Add (priority)

**Source files:** Copy from [docs/dnd5e/lineage/](docs/dnd5e/lineage/) into docs/dnd2024/species/, then add *Source: 2014 … (Legacy).* and optionally normalize to dnd2024 species format (Creature Type/Size/Speed table).

**Phase 1 (2014 PHB):**

- [docs/dnd2024/species/half-elf.md](docs/dnd2024/species/half-elf.md) — Copy from [docs/dnd5e/lineage/half-elf.md](docs/dnd5e/lineage/half-elf.md); add **(Legacy)** and source line.
- [docs/dnd2024/species/half-orc.md](docs/dnd2024/species/half-orc.md) — Copy from [docs/dnd5e/lineage/half-orc.md](docs/dnd5e/lineage/half-orc.md); add **(Legacy)** and source line.

**Phase 2 (optional):** For any Exotic or Monstrous species, copy the corresponding file from docs/dnd5e/lineage/ to docs/dnd2024/species/ (same or matching filename), add Source 2014 … (Legacy) and **(Legacy)** in nav and all.md.

---

## 7. Files to Update

1. **[docs/dnd2024/species/all.md](docs/dnd2024/species/all.md)**  
   Reorganize into: Common Species → Exotic → Monstrous → Setting Specific → Lorwyn Species → Legacy Species (2014). Populate Exotic and Monstrous from tables (links only where pages exist). Add Setting Specific with Eberron filled and optional placeholders for others. Add Legacy section with Half-Elf (Legacy), Half-Orc (Legacy), and other 2014-only species. Intro note on **(Legacy)**.

2. **[mkdocs.yml](mkdocs.yml)**  
   Add `Half-Elf (Legacy): dnd2024/species/half-elf.md`, `Half-Orc (Legacy): dnd2024/species/half-orc.md`. Optionally add **(Legacy)** to other 2014-only species in nav. Optionally group nav (Common, Exotic, Monstrous, Setting Specific, Legacy).

---

## 8. Species Page Format (new pages)

For Half-Elf, Half-Orc, and any new Exotic/Monstrous:

- **Title:** `# Half-Elf` (or species name); *Source: 2014 … (Legacy).* in intro if applicable.
- **Layout:** Centered image, flavor text, `## [Species] Traits` with table (Creature Type, Size, Speed) and special traits (2014 SRD/PHB wording).
- **ASI:** If using 2014 rules, include Ability Score Increase in traits.

**Half-Elf (2014 SRD):** +2 CHA, +1 to two others; Darkvision 60 ft.; Fey Ancestry; Skill Versatility (two skills); Languages Common, Elvish, one extra. Medium, 30 ft.

**Half-Orc (2014 SRD):** +2 STR, +1 CON; Darkvision 60 ft.; Menacing; Relentless Endurance; Savage Attacks. Medium, 30 ft. Languages Common, Orc.

---

## Summary

- **Source:** Use [docs/dnd5e/lineage/](docs/dnd5e/lineage/) and [docs/dnd5e/reference/lineage.md](docs/dnd5e/reference/lineage.md) — copy/adapt into dnd2024/species/ instead of writing from scratch.
- **Labeling:** 2014-only species → **(Legacy)** in all.md and mkdocs nav.
- **Structure:** all.md → Common, Exotic, Monstrous, Setting Specific, Lorwyn, Legacy (2014); mirror dnd5e/reference/lineage.md.
- **Add:** half-elf.md and half-orc.md by copying from dnd5e/lineage/ and adding (Legacy); optionally copy other Exotic/Monstrous from dnd5e/lineage/ in Phase 2.
- **Update:** all.md (full restructure), mkdocs.yml (Half-Elf (Legacy), Half-Orc (Legacy), and (Legacy) on other 2014-only species as desired).
