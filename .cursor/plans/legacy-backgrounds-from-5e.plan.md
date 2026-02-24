---
name: ""
overview: ""
todos: []
isProject: false
---

# Add missing 5e backgrounds as legacy

## Source of truth

Use the following canonical list (your categories) to decide what gets a legacy page. Only add a legacy version for backgrounds that **exist in both 5e and 2024** when the 5e and 2024 content **meaningfully differ**; all others from this list that are missing from 2024 get a new legacy page.

---

## Your list (by category)

### Common backgrounds

- Acolyte *(has 2024 → legacy only if different)*
- Anthropologist
- Archaeologist *(has 2024 → legacy only if different)*
- Athlete
- Charlatan *(has 2024 → legacy only if different)*
- City Watch
- Clan Crafter
- Cloistered Scholar
- Courtier
- Criminal *(has 2024 → legacy only if different)*
- Entertainer *(has 2024 → legacy only if different)*
- Faceless
- Faction Agent
- Far Traveler
- Feylost
- Fisher
- Folk Hero
- Giant Foundling
- Gladiator
- Guild Artisan *(2024 has "Artisan" → legacy only if different)*
- Guild Merchant
- Haunted One
- Hermit *(has 2024 → legacy only if different)*
- House Agent *(has 2024 → legacy only if different)*
- Inheritor
- Investigator (SCAG)
- Investigator (VRGR)
- Knight
- Knight of the Order
- Marine
- Mercenary Veteran
- Noble *(has 2024 → legacy only if different)*
- Outlander
- Pirate
- Rewarded
- Ruined
- Rune Carver
- Sage *(has 2024 → legacy only if different)*
- Sailor *(has 2024 → legacy only if different)*
- Shipwright
- Smuggler
- Soldier *(has 2024 → legacy only if different)*
- Spy
- Urban Bounty Hunter
- Urchin
- Uthgardt Tribe Member
- Waterdhavian Noble
- Witchlight Hand

### AL: Curse of Strahd

- Black Fist Double Agent, Dragon Casualty, Iron Route Bandit, Phlan Insurgent, Stojanow Prisoner, Ticklebelly Nomad

### AL: Mulmaster

- Caravan Specialist, Earthspur Miner, Harborfolk, Mulmaster Aristocrat, Phlan Refugee

### AL: Hillsfar

- Cormanthor Refugee, Gate Urchin, Hillsfar Merchant, Hillsfar Smuggler, Secret Identity, Shade Fanatic, Trade Sheriff

### Acquisitions Inc.

- Celebrity Adventurer's Scion, Failed Merchant, Gambler, Plaintiff, Rival Intern

### Amonkhet (Plane Shift)

- Dissenter, Initiate, Vizier

### Dragonlance

- Knight of Solamnia, Mage of High Sorcery

### Innistrad (Plane Shift)

- Inquisitor

### Planescape

- Gate Warden, Planar Philosopher

### Ravnica

- Azorius Functionary, Boros Legionnaire, Dimir Operative, Golgari Agent, Gruul Anarch, Izzet Engineer, Orzhov Representative, Rakdos Cultist, Selesnya Initiate, Simic Scientist

### Strixhaven

- Lorehold Student, Prismari Student, Quandrix Student, Silverquill Student, Witherbloom Student

### Wildemount

- Grinner, Volstrucker Agent

### Spelljammer

- Astral Drifter, Wildspacer

### Excluded from plan

- **Unearthed Arcana:** None Available (per your list)
- **Homebrew:** Ashari *(optional: include or skip per your preference)*

---

## 2024 equivalents (for “legacy only if different”)

From [docs/dnd2024/backgrounds/index.md](docs/dnd2024/backgrounds/index.md), these 5e names have a 2024 counterpart:


| Your list name | 2024 slug/file   | Action                                                                 |
| -------------- | ---------------- | ---------------------------------------------------------------------- |
| Acolyte        | acolyte.md       | Compare; add acolyte-legacy.md only if different                       |
| Archaeologist  | archaeologist.md | Compare; add archaeologist-legacy.md only if different                 |
| Charlatan      | charlatan.md     | Compare; add charlatan-legacy.md only if different                     |
| Criminal       | criminal.md      | Compare; add criminal-legacy.md only if different                      |
| Entertainer    | entertainer.md   | Compare; add entertainer-legacy.md only if different                   |
| Guild Artisan  | artisan.md       | Compare; add guild-artisan.md as legacy only if different from Artisan |
| Hermit         | hermit.md        | Compare; add hermit-legacy.md only if different                        |
| House Agent    | house-agent.md   | Compare; add house-agent-legacy.md only if different                   |
| Noble          | noble.md         | Compare; add noble-legacy.md only if different                         |
| Sage           | sage.md          | Compare; add sage-legacy.md only if different                          |
| Sailor         | sailor.md        | Compare; add sailor-legacy.md only if different                        |
| Soldier        | soldier.md       | Compare; add soldier-legacy.md only if different                       |


All other names on your list have **no** 2024 page → add as new legacy page with slug from name (e.g. urchin.md, folk-hero.md, city-watch.md). For duplicates (Investigator SCAG vs VRGR), use distinct slugs (e.g. investigator-scag.md, investigator-vrgr.md).

---

## Rule for overlapping backgrounds

- **Only if there is a difference:** For Acolyte, Sage, Charlatan, Criminal, Entertainer, Hermit, Noble, Sailor, Soldier, Archaeologist, House Agent, Guild Artisan vs Artisan: compare 5e vs 2024 benefits/features. If they differ (e.g. 5e has Languages + narrative feature, 2024 has Ability Scores + Feat), add the legacy page. If effectively identical, do not add.
- **Missing-only:** Every other background on your list gets a legacy page (copy from dnd5e, add *Source: … (Legacy).*).

---

## Implementation

**File naming**

- **Has 2024 counterpart and differs:** `{slug}-legacy.md` (e.g. acolyte-legacy.md).
- **No 2024 counterpart:** `{slug}.md` (e.g. urchin.md, folk-hero.md). Use kebab-case; for “Investigator (SCAG)” use investigator-scag.md.

**File location**

- All under `docs/dnd2024/backgrounds/`.

**Content**

- Copy from `docs/dnd5e/backgrounds/<corresponding-file>.md`. Add at top: `*Source: [Book name] (Legacy).`* (e.g. *Source: 2014 Player's Handbook (Legacy).* or *Source: Curse of Strahd (Legacy).*).

**Index (Legacy tab)**

- In [docs/dnd2024/backgrounds/index.md](docs/dnd2024/backgrounds/index.md), add a sixth tab **"Legacy (2014)"**.
- Under that tab, mirror your structure: **Common**, then **AL: Curse of Strahd**, **AL: Mulmaster**, **AL: Hillsfar**, **Acquisitions Inc.**, **Amonkhet**, **Dragonlance**, **Innistrad**, **Planescape**, **Ravnica**, **Strixhaven**, **Wildemount**, **Spelljammer**. In each section, list only backgrounds that have a legacy page (table or list with links). Omit categories that have no legacy pages.

**Nav**

- In [mkdocs.yml](mkdocs.yml), add each new legacy page under Backgrounds. Use “(Legacy)” in the label when the page is the 2014 version of an existing 2024 background (e.g. “Acolyte (Legacy)”); otherwise use the background name (e.g. “Urchin (Legacy)” or “Urchin”).

---

## Suggested order of work

1. **Overlap comparison** – For the 12 overlapping names, compare 5e vs 2024; decide yes/no for each legacy page and create `*-legacy.md` only where different.
2. **Common missing** – Create legacy pages for all Common backgrounds that are missing-only (and, if different, for overlaps). Use your Common list order.
3. **Setting-specific** – Create legacy pages by section (AL, Acquisitions Inc., Dragonlance, Ravnica, etc.). Match slug to existing dnd5e filenames where present.
4. **Index** – Add “Legacy (2014)” tab and tables/lists by category.
5. **Nav** – Update mkdocs.yml with all new pages.

---

## Optional

- **Homebrew (Ashari):** Include only if you want homebrew in the legacy list; otherwise skip.
- **Investigator (SCAG)** vs **Investigator (VRGR):** Ensure two files (e.g. investigator-scag.md, investigator-vrgr.md) and both linked in the Legacy tab under Common.

