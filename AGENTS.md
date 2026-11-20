# AGENTS.md — Shadowrun 5e Data & Rules Intelligence Guidance

## 1. Scope & Mission
This repository provides an automated, deterministic rules reference engine, equipment query CLI, and structured skill catalog for **Shadowrun 5th Edition (SR5)**.

All agents operating in this workspace must use these codified instructions, mathematical invariants, and XML dataset tools to resolve combat, drone customization, spellcasting/drain, matrix actions, essence calculations, and character progression accurately.

---

## 2. Technical Stack & Runtime Requirements
- **Python Runtime**: Target Python 3.10+ / 3.12+ (standard library only for XML queries: `xml.etree.ElementTree`, `pathlib`, `argparse`, `json`).
- **Data Grounding**: 43 raw Chummer5a XML data files stored under `./data/` (`weapons.xml`, `vehicles.xml`, `gear.xml`, `armor.xml`, `cyberware.xml`, `bioware.xml`, `spells.xml`, `traditions.xml`, `priorities.xml`, etc.).
- **Line Endings**: Enforce strict LF (`\n`) formatting on all Python scripts, Markdown documentation, and CSV files.
- **CLI Utilities**:
  - `python scripts/query_chummer.py <type> [search]`: General equipment & rules query tool.
  - `python scripts/query_tradition.py [search]`: Magical tradition & Forbidden Arcana lookup tool.

---

## 3. Development Environment & Dev-VM Standards (`dev-vm`)
- **Dev Host**: Dedicated Linux development environment on `dev-vm` (`10.42.42.54`), Ubuntu 26.04 LTS on hypervisor `LAB-HOST` (`10.42.42.26`), user `marty@10.42.42.54`.
- **Shared Project Path**: `/home/marty/projects/sr5e-agent-skills/`
- **POSIX Pathing**: When operating on or interacting with `dev-vm`, ALWAYS use native Linux POSIX paths (`/home/marty/projects/sr5e-agent-skills/...`). Never use Windows backslash pathing in Linux contexts.
- **Dev Offloading**: Offload heavy script evaluations, builds, test runs, and remote git operations to `dev-vm`.
- **Secret & Token Security**: NEVER pass raw GitHub tokens (e.g., `gho_...`, `ghp_...`, `github_pat_...`) inline in CLI commands or single-line environment overrides. Plaintext token strings in process arguments or logs trigger automated secret scanning and instant revocation. Rely strictly on `gh auth` keyring credentials or environment variables set outside execution strings.

---

## 4. Repository Architecture & Layout

```text
├── AGENTS.md                                                # Universal agent directives & operational guidelines
├── README.md                                                # Workspace overview & data notes
├── filtered_weapons.csv                                     # Curated non-2050 Heavy Pistols, Machine Pistols, SMGs
├── filtered_drones.csv                                      # Budget heavy-duty modern drones (Body >= 4, Mod Slots >= 4)
├── scripts/
│   ├── query_chummer.py                                     # Convenience wrapper for Chummer5a XML querying
│   └── query_tradition.py                                   # Convenience wrapper for Tradition querying
├── data/                                                    # 43 raw Chummer5a XML data files
│   ├── weapons.xml, vehicles.xml, gear.xml, armor.xml
│   ├── cyberware.xml, bioware.xml, spells.xml, traditions.xml
│   ├── priorities.xml, skills.xml, qualities.xml, critters.xml, etc.
└── .agents/
    └── skills/                                              # 13 modular, deep-dive rules skills
        ├── sr5e-drone-customization/                        # Drone mod slots, upgrade costs & caps
        ├── sr5e-condition-monitors/                         # Condition monitors across all entity types
        ├── sr5e-data-query-and-extraction/                  # XML query utilities and filtering rules
        ├── sr5e-traditions/                                 # 74 traditions + Forbidden Arcana rules
        ├── sr5e-magic-drain-and-spirits/                    # Drain formulas, spirit scaling, and ITNW
        ├── sr5e-drone-autosofts-and-swarms/                 # Drone local storage, RCC sharing, and swarms
        ├── sr5e-rigger-operations/                          # Control modes, VCR bonuses, and collisions
        ├── sr5e-recoil-and-firing-modes/                    # Recoil compensation, firing modes, progressive recoil
        ├── sr5e-cyberware-essence-and-grades/               # Grade multipliers, Cyber-Bio split, cyberlimbs
        ├── sr5e-matrix-and-pan-defense/                     # PAN slaving, direct connection, marks, and noise
        ├── sr5e-explosives-and-chunky-salsa/                # Scatter, blast falloff, and chunky salsa reflections
        ├── sr5e-chargen-and-karma/                          # Priority chargen, Sum-to-Ten, and Karma progression
        └── sr5e-combat-turn-and-actions/                    # Combat sequence, passes, and interrupt defense
```

---

## 5. Domain Invariants & Rules Standards

### A. Data Query & Sourcebook Standards
- **Mod Slots Precedence**: Use explicit `<modslots>` from `vehicles.xml` if present; if missing or blank, default to `Body`.
- **Era Filtering**: Items tagged with source `2050` or `(2050)` in the name represent legacy gear and MUST be excluded unless explicitly requested.
- **German Pegasus Coverage**: Account for Pegasus-exclusive releases: `SAG` (*State of the Art ADL*), `SOTG` (*Datapuls SOTA 2080*), `DATG` (*Datapuls Verschlusssache*), `HAMG` (*Datapuls Hamburg*), and `SHB` (*Schattenhandbuch*).
- **Ammo Codes**: Cylinder/revolver magazines are designated by `(cy)`.

### B. Drone Customization Invariants
- **Zero Value Math**: When an attribute is 0 (e.g. Microdrone Body 0), use **$0.5$** for all calculations and scaling. No multiplying by 0 for free upgrades.
- **Attribute Ceiling**: No physical attribute can be raised above **$2\times$ its starting base value**.
- **Body Restriction**: A drone's Body attribute **CAN NEVER BE INCREASED**.
- **Free Upgrade (0 MP)**: Once per drone, one attribute may be increased by $+1$ ($+3$ for Armor) without spending Mod Points (nuyen cost still applies).
- **Downgrades**:
  - *Standard Downgrade*: Once per drone, decrease an attribute by $-1$ ($-3$ for Armor) to gain $+1$ Mod Point. Cannot drop to 0 (except Speed).
  - *Body Downgrade*: Reducing Body by 1 grants 2 Mod Points (net $+1$ Mod Point). Body cannot drop below half starting value ($\ge \text{Base}/2$).
- **Armor Encumbrance**: Drone carries up to $3\times\text{Body}$ armor freely. Every $+3$ points over: $-1$ Handling and $-1$ Speed; every $+6$ points over: $-1$ Acceleration. If Handling $< 1$, Speed $< 0$, or Acceleration $< 0$, drone is immobilized.

### C. Condition Monitor Formulas
*(All divisions rounded up: $\lceil x / 2 \rceil$)*
- Vehicles (Physical): $12 + \lceil \text{Body} / 2 \rceil$
- Drones (Physical): $6 + \lceil \text{Body} / 2 \rceil$
- Characters & Spirits (Physical): $8 + \lceil \text{Body} / 2 \rceil$
- Characters & Spirits (Stun): $8 + \lceil \text{Willpower} / 2 \rceil$
- Sprites (Matrix): $8 + \lceil \text{Level} / 2 \rceil$
- Devices (Matrix): $8 + \lceil \text{Device Rating} / 2 \rceil$
- Physical Damage Resistance: Resisted with $\text{Body} + \max(0, \text{Armor} \pm \text{AP})$.

---

## 6. Complete Skills Catalog & Links

1. [**`sr5e-data-query-and-extraction`**](file:///.agents/skills/sr5e-data-query-and-extraction/SKILL.md): CLI query tool and filtering rules across all 43 XML files.
2. [**`sr5e-drone-customization`**](file:///.agents/skills/sr5e-drone-customization/SKILL.md): Mod slots, attribute costs, weapon mounts, ammo mods, pilot programs, and smartsoft.
3. [**`sr5e-condition-monitors`**](file:///.agents/skills/sr5e-condition-monitors/SKILL.md): Condition monitors and physical damage resistance across all entities.
4. [**`sr5e-traditions`**](file:///.agents/skills/sr5e-traditions/SKILL.md): Comprehensive reference and CLI tool for all 74 traditions, spirits, and Forbidden Arcana rules.
5. [**`sr5e-magic-drain-and-spirits`**](file:///.agents/skills/sr5e-magic-drain-and-spirits/SKILL.md): Spellcasting drain thresholds, summoning, spirit attributes by Force, and ITNW.
6. [**`sr5e-drone-autosofts-and-swarms`**](file:///.agents/skills/sr5e-drone-autosofts-and-swarms/SKILL.md): Local drone capacity, RCC sharing, and Rigger 5.0 Swarm operations.
7. [**`sr5e-rigger-operations`**](file:///.agents/skills/sr5e-rigger-operations/SKILL.md): Control modes, VCR bonuses, Gunnery tests, and collision damage.
8. [**`sr5e-recoil-and-firing-modes`**](file:///.agents/skills/sr5e-recoil-and-firing-modes/SKILL.md): Progressive recoil accumulation, natural RC, and weapon accessories.
9. [**`sr5e-cyberware-essence-and-grades`**](file:///.agents/skills/sr5e-cyberware-essence-and-grades/SKILL.md): Grade multipliers, the Cyber-Bio essence split, and cyberlimb capacity.
10. [**`sr5e-matrix-and-pan-defense`**](file:///.agents/skills/sr5e-matrix-and-pan-defense/SKILL.md): PAN slaving, Marks, matrix actions, and noise falloff.
11. [**`sr5e-explosives-and-chunky-salsa`**](file:///.agents/skills/sr5e-explosives-and-chunky-salsa/SKILL.md): Grenade scatter, blast falloff, and confined-space shockwaves.
12. [**`sr5e-chargen-and-karma`**](file:///.agents/skills/sr5e-chargen-and-karma/SKILL.md): Priority creation table, Sum-to-Ten, and Karma advancement costs.
13. [**`sr5e-combat-turn-and-actions`**](file:///.agents/skills/sr5e-combat-turn-and-actions/SKILL.md): Combat Turn sequence, action economy, and defensive interrupt actions.
