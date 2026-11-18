# Shadowrun 5e Data & Drone Customization Guidelines

## 1. Workspace & Data Structure
- `data/`: 43 raw Chummer5a XML files (`weapons.xml`, `vehicles.xml`, `gear.xml`, `armor.xml`, `traditions.xml`, etc.).
- `filtered_weapons.csv`: Curated Machine Pistols, Heavy Pistols, SMGs (non-2050).
- `filtered_drones.csv`: Pre-filtered drones (Body $\ge 4$, Cost $\le 50\text{k}¥$, Body+Armor $\ge 10$, Mod Slots $\ge 4$, non-Huge, non-2050).
- `.agents/skills/`: 10 specialized rules skills covering drones, vehicle combat, traditions, magic, essence, matrix, recoil, and explosives.

## 2. General Query & Parsing Rules
- **Mod Slots**: If `<modslots>` is explicitly defined in `vehicles.xml`, use it. If omitted or empty, default base Mod Slots to `Body`.
- **Sourcebook Coverage**: 
  - Supports English Core & Sourcebooks (SR5, SG, FA, HT, SSP, DTR, etc.).
  - Supports German Pegasus-exclusive releases: `SAG` (*State of the Art ADL*), `SOTG` (*Datapuls SOTA 2080*), `DATG` (*Datapuls Verschlusssache*), `HAMG` (*Datapuls Hamburg*), and `SHB` (*Schattenhandbuch*).
- **Era Filtering**: Weapons, vehicles, and drones with source `2050` or `(2050)` in the name represent legacy gear and must be excluded unless explicitly requested.
- **Ammo Codes**: Cylinder/revolver magazines are designated by `(cy)`.

## 3. Dedicated Skill Directory
1. **`sr5e-drone-customization`**: Drone mod slots, attribute caps ($2\times$), zero-math ($0.5$), upgrade costs, weapon mounts, ammo feeds, and autosofts.
2. **`sr5e-condition-monitors`**: Physical, Stun, and Matrix condition monitors across characters, spirits, vehicles, drones, sprites, and devices; physical damage resistance & soak.
3. **`sr5e-traditions`**: Dedicated skill covering all 74 traditions from `data/traditions.xml` (SR5, SG, FA, HT, SSP, and German Pegasus releases). Includes advanced *Forbidden Arcana* rules and the CLI query tool `python .agents/skills/sr5e-traditions/scripts/query_tradition.py`.
4. **`sr5e-magic-drain-and-spirits`**: Spell drain calculation (min 2), Stun vs Physical drain threshold, summoning & binding drain, spirit attribute scaling by Force, and Immunity to Normal Weapons (Hardened Armor = $2\times\text{Force}$, auto-soak = $\text{Force}$).
5. **`sr5e-drone-autosofts-and-swarms`**: Local drone autosoft capacity ($\lceil\text{Pilot}/2\rceil$), RCC program sharing, autosoft models, and *Rigger 5.0* Swarm operations.
6. **`sr5e-rigger-operations`**: Autonomous vs Remote Control vs Jumped In (VR); VCR rating bonuses and limits; Hot-Sim vs Cold-Sim initiative/biofeedback; Gunnery tests; Collision and Ramming formulas.
7. **`sr5e-recoil-and-firing-modes`**: Natural RC ($1 + \lceil\text{Str}/3\rceil$), drone mount RC ($\text{Body} + \text{Mount RC}$), progressive recoil across firing modes (SS, SA, BF, LB, FA), and reset actions.
8. **`sr5e-cyberware-essence-and-grades`**: Grade multipliers (Used, Standard, Alpha, Beta, Delta), the Cyber-Bio essence split ($\max + 0.5\min$), essence holes, and cyberlimb capacity.
9. **`sr5e-matrix-and-pan-defense`**: PAN device slaving, mutual defense vs Direct Connection, Marks (1-4), Matrix actions (Brute Force, Hack on the Fly, Control Device), and Noise vs Noise Reduction.
10. **`sr5e-explosives-and-chunky-salsa`**: Grenade scatter ($2\text{D}6 - \text{hits}$), blast damage drop-off ($-2\text{ DV}/\text{m}$), barrier penetration, and the Chunky Salsa reflected shockwave rule.

## 4. Drone Customization Core Formulas
- **Zero Value Math**: When an attribute is 0 (e.g. Microdrone Body 0), use $0.5$ for calculations and scaling.
- **Free Upgrade (0 Mod Points)**: Once per drone, one attribute may be increased by $+1$ ($+3$ for Armor) without spending Mod Points. Nuyen cost still applies. Body is excluded.
- **Downgrades**:
  - *Standard Downgrade*: Once per drone, decrease an attribute by $-1$ ($-3$ for Armor) to gain $+1$ Mod Point. Cannot lower to 0 (except Speed).
  - *Body Downgrade*: Reducing Body by 1 grants 2 Mod Points (net $+1$ Mod Point). Body cannot drop below half starting value ($\ge \text{Base}/2$).
- **Attribute Upgrade Costs & Formulas**:
  - Handling: $\text{Rating} \times \text{Body} \times 200¥$ | Avail = $\text{Rating} \times 2$
  - Speed: $(\text{Rating} \times \text{Body} \times 2) \times 200¥$ | Avail = $\text{Rating} \times 2$
  - Acceleration: $\text{Rating} \times \text{Body} \times 200¥$ | Avail = $\text{Rating} \times 4$
  - Armor: $\text{Rating} \times \text{Body} \times 200¥$ | Avail = $\text{Rating}$ (Restricted `R` if $>6$, Forbidden `F` if $>12$). Weight allowance = $3 \times \text{Body}$. Excess: $-1$ Handling/Speed per 3 pts, $-1$ Acceleration per 6 pts.
  - Sensor (Array): $\text{Rating} \times 1{,}000¥$ | Avail = $\text{Rating} \times 2$
  - Sensor (Single): $\text{Rating} \times 100¥$ | Avail = $\text{Rating} \times 2$
  - Pilot Programs (0 MP): R1 (100¥, Avail 4), R2 (400¥), R3 (1,800¥, 8R), R4 (3,200¥, 12R), R5 (10,000¥, 16F), R6 (20,000¥, 24F).
  - Smartsoft (0 MP): Rating 3 autosoft (Pilot $\ge 3$), 1,500¥.

## 5. Condition Monitor Formulas
*(All divisions rounded up: $\lceil x / 2 \rceil$)*
- Vehicles (Physical): $12 + \lceil \text{Body} / 2 \rceil$
- Drones (Physical): $6 + \lceil \text{Body} / 2 \rceil$
- Sprites (Matrix): $8 + \lceil \text{Level} / 2 \rceil$
- Characters & Spirits (Stun): $8 + \lceil \text{Willpower} / 2 \rceil$
- Characters & Spirits (Physical): $8 + \lceil \text{Body} / 2 \rceil$
- Devices (Matrix): $8 + \lceil \text{Device Rating} / 2 \rceil$
- Physical Damage Resistance: $\text{Body} + \text{Armor} \pm \text{AP}$. Net unsoaked damage marks Physical Condition Monitor.
