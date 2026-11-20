---
name: sr5e-life-modules
description: Rules, datasets, and CLI validator for Shadowrun 5th Edition Life Modules character creation (750 Karma, stage selection rules, prerequisites/post-requisites, age progression, skill groups, qualities limits, and placeholder/choice modules).
---

# Shadowrun 5e Life Modules Character Creation

This skill governs **Life Modules** character generation using the dedicated JSON datasets under `data/life_modules/` (sourced from the user's Life Modules master spreadsheet rather than Chummer's `lifemodules.xml`) and provides a deterministic Python CLI for searching modules and validating complete character builds.

> [!IMPORTANT]
> **Strict Rule Grounding — Never Make Up Rules**:
> - **NEVER guess, improvise, or hallucinate mechanics, quality effects, or rule descriptions** from memory or other RPG systems.
> - Before stating how any quality, module, or rule works, verify it against the workspace XML datasets (`data/qualities.xml`, `data/lifemodules.xml`, etc.), `data/life_modules/rules.json`, or official SR5 rulebook text. If the exact rule text is not present in the local data and cannot be verified, state what is in the data and ask the user rather than inventing mechanics.

---

## 1. Datasets & CLI Utility

All data lives under `data/life_modules/`:
- `metatypes.json` (36 metatypes & metavariants)
- `nationalities.json` (61 nationality modules, including *Shadows in Focus: Butte* and Chummer primary/secondary language options)
- `formative_years.json` (38 formative years modules)
- `teen_years.json` (36 teen years modules)
- `further_education.json` (88 further education modules, including *Shadows in Focus: Butte*)
- `real_life.json` (151 real life modules, including *Shadows in Focus: Butte*)
- `skill_groups.json` (15 SR5 Core skill groups aligned to module active skill keys)
- `skill_attributes.json` (72 active skill → linked attribute mappings + 10 focus-area presets)
- `rules.json` (complete Karma, cap, quality, age, and Tour of Duty Rank rules)

### CLI Commands (`scripts/life_modules.py`)
```bash
# Search modules by stage, attribute, skill, quality, or keyword
python scripts/life_modules.py search "magic" --stage teen_years
python scripts/life_modules.py search --stage real_life --attr LOG --skill Hacking

# Show full JSON details for a module (notes, choices, prerequisites, skills)
python scripts/life_modules.py show "Test Subject"
python scripts/life_modules.py show "Regular Job"

# Recommend legal modules for the next stage (story or munchkin mode)
python scripts/life_modules.py recommend --stage further_education --build-file char.json --mode story --theme "medic"
python scripts/life_modules.py recommend --stage real_life --build-file char.json --mode munchkin --focus face

# Validate, price post-module raises, and render a running Markdown character sheet
python scripts/life_modules.py evaluate --build-file char.json --markdown
python scripts/life_modules.py evaluate --build-file char.json --sheet-out char_sheet.md
```

---

## 1B. Step-by-Step Creation Workflow & Recommendation Modes

When assisting a player step-by-step, maintain a running JSON build file (e.g. `character.json`) and regenerate the running Markdown character sheet (`--sheet-out character_sheet.md`) after each stage so the player always sees live **ratings, dice pools, Karma remaining, age, and pending choices/placeholders**.

### Focus Areas & Playstyle Modes
At the start of character creation, capture:
1. **`focus_areas`** (one or more presets: `street_samurai`, `face`, `decker`, `technomancer`, `rigger`, `mage`, `adept`, `infiltrator`, `medic`, `investigator` — and/or an explicit `core_skills` list).
2. **`playstyle`**:
   - **`story` (Story / Character-Based)**: Prioritize narrative fit, thematic continuity, and character concept. **Do NOT push optimization** — **ONLY advise mechanically when a character's core skills are estimated to finish below a dice pool of `12` at the end of character creation** (either finalized `< 12`, or remaining Karma is insufficient to bring sub-12 core skills to `12`).
   - **`munchkin` (Mechanical Optimization)**: Rank candidate modules via `recommend --mode munchkin` by weighted Karma-efficiency (focus attributes, focus skills, and raw Karma-equivalent value per Karma spent) and actively report Karma needed to hit `12+` dice pools.

### Full End-to-End `character.json` Schema
`evaluate --build-file character.json` supports both partial mid-build files and complete end-of-chargen builds:
- **Identity & Mode**: `name`, `concept`, `playstyle` (`"story"` | `"munchkin"`), `focus_areas`, `core_skills`, `finalized` (`true`/`false`)
- **Stage Selections**: `metatype`, `awakened_quality`, `nationality`, `formative_years`, `teen_years`, `further_education` (list), `real_life` (ordered list)
- **Resolutions**:
  - `resolved_placeholders`: `[{"module": "UCAS Seattle", "placeholder": "[Language]", "chosen": "English", "ranks": 1}]`
  - `resolved_choices`: `[{"module": "Regular Job", "active_skills": {"Con": 3, "Etiquette": 3}}]`
  - `duplicate_quality_replacements`: `[{"replaced": "...", "with": "...", "karma": 5}]`
- **Post-Module Karma Spending**:
  - `attribute_raises`: `{"AGI": 2, "INT": 1}` (`New × 5` Karma)
  - `active_skill_raises`: `{"Pistols": 2}` (`New × 2` Karma, cap 7)
  - `knowledge_skill_raises`: `{"Seattle Street Politics": 2}` (spends free `(INT + LOG) × 2` points first, then `New × 1` Karma, cap 9)
  - `specializations`: `{"Pistols": ["Semi-Automatics"]}` (`7` Karma each)
  - `manual_positive_qualities`: `[{"name": "Mentor Spirit", "karma": 5, "is_mastery": false, "from_tradition": false}]`
  - `manual_negative_qualities`: `[{"name": "Code of Honor", "karma": 15, "from_tradition": false}]`
  - `negative_quality_buyoffs`: `[{"name": "Uneducated", "karma": 8}]`
  - `spells` / `complex_forms` (`5` Karma each), `karma_for_nuyen` (max `200`, `2,000¥`/Karma), `essence` (default `6.0`)
- **Contacts, Extra Contact Pools & Loyalty Modifiers**:
  - `contacts`: `[{"name": "Fixer", "archetype": "Fixer", "connection": 4, "loyalty": 3, "pool": "standard", "connection_modifier": 0, "loyalty_modifier": 0, "blackmail": false, "notes": []}]` (`CHA × 3` free points in `standard` pool first, overflow `1` Karma/pt)
  - `extra_contact_points`: `0` (adds flat bonus free contact points to the `standard` pool)
  - `extra_contact_pools`: `[{"id": "custom_pool", "label": "Custom Pool", "points": 8, "min_connection": 1, "max_connection": 6, "allows_karma_overflow": false}]`
  - `contact_loyalty_modifiers` / `contact_notes`: custom notes or modifiers affecting Contact Connection/Loyalty
  - **Automatic Quality Handling**: Automatically detects and applies **`Friends in High Places`** (creates a dedicated `CHA × 4` pool `high_places` for Connection 8–12 contacts), **`Networker`** (`-1` pt/contact, min 1), **`Massive Network`** (`-2` pts/contact, min 2), **`Candle in the Darkness`** (`5K`, verifies a `Code of Honor` negative quality is present and applies `+2` effective Loyalty across all contacts while upheld, or `-1` if `code_of_honor_broken: true`), **`Ex-Con`** (`15K` negative, enforces Loyalty `4+` on Corporate contacts and Loyalty `5–6` on Law Enforcement contacts), **`Made Man`** (adds a free Syndicate Group Contact at Forced Loyalty 3), **`Prime Datahaven Membership`** (adds a free Connection 5 / Forced Loyalty 3 Datahaven Group Contact), **`Black Market Pipeline`**, **`Sensei`**, **`Home Ground (You Know a Guy)`**, **`Dealer Connection`**, **`Privileged Family Name`**, **`Trustworthy`**, **`Solid Rep`**, and **`Bad Rep`**.

---

## 2. Budget, Caps & Derived Formulas

| Rule | Value / Formula |
| :--- | :--- |
| **Starting Karma** | **750 Karma** |
| **Karma-to-Nuyen** | **2,000¥ per 1 Karma**, up to **200 Karma** (400,000¥ max) |
| **Attribute Natural Max** | `Metatype Starting Value + 5` (Special Attributes `MAG`/`RES` max `6`) |
| **Active Skill Cap (Chargen)** | **7** |
| **Knowledge / Language Skill Cap** | **9** |
| **Free Knowledge / Language Points** | `(INT + LOG) × 2` |
| **Free Contact Karma** | `CHA × 3` |
| **Post-Module Raise Costs** | Attributes `New × 5`, Active Skills `New × 2`, Knowledge `New × 1`, Specializations `7` |

### Awakened & Emerged Karma Costs
| Quality | Karma Cost |
| :--- | :---: |
| **Aspected Magician** *(incl. FA variants: Aware, Apprentice, Enchanter, Explorer)* | 15 |
| **Technomancer** | 15 |
| **Adept** | 20 |
| **Magician** | 30 |
| **Mystic Adept** | 35 |

---

## 3. Stage Selection & Age Progression Rules

| Stage | Selection Limit | Age Progression |
| :--- | :--- | :--- |
| **Metatypes** | Single choice (max 1) | — |
| **Nationalities** | Single choice (max 1) | Nationality + Formative Years cover up to **10 years old** |
| **Formative Years** | Single choice (max 1) | *(included in age 10 above)* |
| **Teen Years** | Single choice (max 1) | Ages character to **17 years old** |
| **Further Education** | Single choice, **with two exceptions** (below) | **+2 years**: Community College, Trade/Technical School (`TradeTechnicalSchool`, `Trade School Shop`), Corp College Student, Student Athlete<br>**+4 years**: State College / State University, Ivy League, Military Academy, Craft Apprenticeship, Religious Study |
| **Real Life** | Unlimited (as many as affordable) | **+4 years** per Real Life module |

### Further Education Exceptions
1. **Two-Stage Upgrade**: You may take a **Community College** or **Trade School** (`TradeTechnicalSchool`, `Trade School Shop`) module and then also take a **State University** or **Ivy League** module.
2. **Student Athlete Add-On**: One **Student Athlete** module (`StudentAthlete`) may be added to any selection or selections of Further Education modules.

---

## 4. Qualities Rules

- **Positive Qualities (25 Karma cap)**:
  - Positive qualities gained from **Life Modules** do **NOT** count against the 25 Karma cap.
  - Positive qualities gained from **Traditions** do **NOT** count against the 25 Karma cap.
  - **Mastery Qualities** (subtype of positive qualities primarily from *Forbidden Arcana* and the *Neon-Anarchist* sourcebook playtest) do **NOT** count against the 25 Karma cap.
- **Negative Qualities (25 Karma cap)**:
  - Negative qualities gained from **Life Modules** **DO** count against the 25 Karma cap.
  - Negative qualities gained from **Traditions** do **NOT** count against the 25 Karma cap.
  - **Overflow**: A character **may** exceed 25 Karma of negative qualities via Life Modules alone, in which case they cannot select any additional negative qualities after choosing modules (`remaining_allowance = max(0, 25 - module_negative_karma)`).
- **Duplicate Qualities**: If you receive the same quality twice across modules and it cannot advance to a higher tier, select another quality of the same Karma cost.
- **Buying Off Negative Qualities**: You may buy off negative qualities obtained from Life Modules using extra Karma.
- **SINner Non-Stacking**: SINner qualities from modules do **not** stack; only the highest-severity SINner applies (`National 5 < Criminal 10 < Corporate Limited 15 < Corporate 25`).

---

## 5. Skill Groups, Placeholders & Choice Modules

- **Skill Groups**: Each rank in a Skill Group adds `+1` to every member Active Skill per **SR5 Core** (`data/life_modules/skill_groups.json`). Notably, **Biotechnology** includes all 4 skills (`Biotechnology`, `Cybertechnology`, `First Aid`, `Medicine`).
- **Active Skill Cap Rollover (Cap 7)**: Active skills that exceed the chargen cap of `7` via Life Modules are **not wasted** — excess points roll over to other skills in the **same Skill Group** (e.g., `Computer > 7` rolls over into `Hardware` or `Software` in `Electronics`). If the skill is not part of a Skill Group (or all skills in its group are at `7`), the excess rolls over to another active skill with the **same linked attribute** (configurable via `"skill_rollovers": [{"from": "Computer", "to": "Hardware", "ranks": 1}]`).
- **Placeholder Knowledge Skills (`[...]`)**: Any knowledge skill with `is_placeholder: true` (enclosed in brackets, e.g. `[Language]`, `[City]`, `[Academic]`) is a placeholder—during character creation the player picks a specific skill matching that description.
- **Module Notes & Choice Modules**: Top-cell notes (e.g., `Test Subject` granting 16,000¥ in augmentations, `Bag of Organs` granting 32,000¥ in bioware) are stored in `"note"`, and modules with open skill/attribute allocations (`Regular Job`, `Postgraduate Studies`, `Celebrity`, `Drifter`, `Craftsman`, `ProfessionalAthlete`, etc.) include a structured `"choices"` array.

---

## 6. Module Prerequisites, Post-Requisites & Tour of Duty Rank

- **Preparatory School** *(Teen Years)*: Cannot be chosen if you have `Fugitive` or `Isolated Rural Upbringing`.
- **Magical Education** *(Teen Years, all 4 variants)*: Requires the matching Awakened quality (`Magician`, `Adept`, `Aspected Magician`, or `Mystic Adept`). **Post-requisite**: Must pick either Further Education module(s) and then a `Corporate` Real Life module, or go straight to a `Corporate` Real Life module if skipping Further Education.
- **Military Academy** *(Further Education, all vocations)*: **Post-requisite**: After taking this, you must choose at least one **Tour of Duty** Real Life module.
- **Private Investigator** *(Real Life)*: May not be picked until you have completed a **Tour of Duty**, **Law Enforcement**, **Covert Operations**, **Shadow Work**, or **Corporate** Real Life module.
- **Tour of Duty — Medical Corps** *(all 5 variants)*: Requires completing the `Nurse` or `Medicine` module from Further Education.
- **Awakened / Technomancer Modules**: Modules granting Resonance/Tasking skills require `Technomancer`; modules granting Sorcery/Conjuring/Enchanting/Magic skills require the appropriate Awakened quality.
- **Tour of Duty Rank**: When starting a Tour of Duty module, having the **Rank** quality at the **5 Karma** level makes you an **NCO**; having **Rank** at the **20 Karma** level makes you an **Officer**.
