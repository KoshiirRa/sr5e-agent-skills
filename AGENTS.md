# Shadowrun 5e Data & Drone Customization Guidelines

## 1. Workspace & Data Structure
- `data/`: 43 raw Chummer5a XML files (`weapons.xml`, `vehicles.xml`, `gear.xml`, `armor.xml`, etc.).
- `filtered_weapons.csv`: Curated Machine Pistols, Heavy Pistols, SMGs (non-2050).
- `filtered_drones.csv`: Pre-filtered drones (Body $\ge 4$, Cost $\le 50\text{k}¥$, Body+Armor $\ge 10$, Mod Slots $\ge 4$, non-Huge, non-2050).

## 2. General Query & Parsing Rules
- **Mod Slots**: If `<modslots>` is explicitly defined in `vehicles.xml`, use it. If omitted or empty, default base Mod Slots to `Body`.
- **German Books**: Pegasus-exclusive book codes include `SAG` (*State of the Art ADL*), `SOTG` (*Datapuls SOTA 2080*), `HAMG` (*Datapuls Hamburg*), and `SHB` (*Schattenhandbuch*).
- **Era Filtering**: Weapons, vehicles, and drones with source `2050` or `(2050)` in the name represent legacy gear and must be excluded unless explicitly requested.
- **Ammo Codes**: Cylinder/revolver magazines are designated by `(cy)`.

## 3. Drone Customization & Attribute Rules
- **Attribute Ceiling**: No physical attribute can be raised above $2\times$ its starting base value.
- **Zero Value Math**: When an attribute is 0 (e.g. Microdrone Body 0), use $0.5$ for calculations and scaling.
- **Free Upgrade (0 Mod Points)**: Once per drone, one attribute may be increased by $+1$ ($+3$ for Armor) without spending Mod Points. Nuyen cost still applies. Body is excluded.
- **Downgrades**:
  - *Standard Downgrade*: Once per drone, decrease an attribute by $-1$ ($-3$ for Armor) to gain $+1$ Mod Point. Cannot lower to 0 (except Speed).
  - *Body Downgrade*: Reducing Body by 1 grants 2 Mod Points (net $+1$ Mod Point). Body cannot drop below half starting value ($\ge \text{Base}/2$). Availability = $\text{Mod Points Gained} \times 3$. Body can never be upgraded.

### Attribute Upgrade Costs & Formulas
*(Note: If Body is 0, substitute 0.5)*
- **Handling**: Cost = $\text{Rating} \times \text{Body} \times 200¥$ | Avail = $\text{Rating} \times 2$
- **Speed**: Cost = $(\text{Rating} \times \text{Body} \times 2) \times 200¥$ | Avail = $\text{Rating} \times 2$
- **Acceleration**: Cost = $\text{Rating} \times \text{Body} \times 200¥$ | Avail = $\text{Rating} \times 4$
- **Armor**: Cost = $\text{Rating} \times \text{Body} \times 200¥$ | Avail = $\text{Rating}$ (Restricted `R` if $>6$, Forbidden `F` if $>12$).
  - *Encumbrance Penalty*: Weight allowance = $3 \times \text{Body}$. Every 3 points above this threshold gives $-1$ Handling and $-1$ Speed; every 6 points above also gives $-1$ Acceleration. If Handling $< 1$, Speed $< 0$, or Acceleration $< 0$, drone is immobilized.
- **Sensor**:
  - *Full Array*: Cost = $\text{Rating} \times 1{,}000¥$ | Avail = $\text{Rating} \times 2$
  - *Single Sensor*: Cost = $\text{Rating} \times 100¥$ | Avail = $\text{Rating} \times 2$
- **Pilot Programs (0 MP)**: Pure software upgrade; replaces drone's Pilot rating:
  - Rating 1: Avail 4, 100¥
  - Rating 2: Avail —, 400¥
  - Rating 3: Avail 8R, 1,800¥
  - Rating 4: Avail 12R, 3,200¥
  - Rating 5: Avail 16F, 10,000¥
  - Rating 6: Avail 24F, 20,000¥
- **Smartsoft (0 MP)**: Autosoft Rating 3 (requires Pilot $\ge 3$). Cost = 1,500¥. Enables smartgun operation.

## 4. Drone Weapon Mounts & Ammo Modifications
- **Mount Sizes & Base Costs**:
  - **Micro**: 0 MP, Avail 8R (Single-shot bullet or dart)
  - **Mini**: 1 MP, Avail 4R (Hold-out pistol, light pistol, reach 0 melee, single-shot grenade)
  - **Small**: 2 MP, Avail 8R (Heavy pistol, machine pistol)
  - **Standard**: 3 MP, Avail 10F (Submachine gun, under-barrel grenade launcher)
  - **Large**: 4 MP, Avail 12F (Shotgun, hunting rifle, assault rifle, grenade launcher)
  - **Huge**: 5 MP, Avail 16F (Sniper rifle, light or medium machine gun)
  - **Heavy**: 6 MP, Avail 20F (Heavy machine gun, rocket launcher, assault cannon)
- **Mount Concealment**:
  - *Blow-Away Panels*: Cost = $25¥ \times \text{MP of Mount}$ (0 MP cost). One-shot deployment.
  - *Pop-Up / Pop-Out / Pop-Under*: Cost = $+1\text{ MP}$ and $100¥ \times \text{MP of Mount}$.
- **Ammunition Mods**:
  - *Extra Ammo Bin*: Doubled weapon ammo capacity. Costs $1\text{ MP}$ and $50¥$.
  - *Belt Feed Conversion*: Changes ammo code to `100(belt)`. Costs $2\text{ MP}$ and $500¥$.
  - *Belt Feed + Extra Ammo Bins*: Each extra bin adds $+100$ rounds of belt ammo (1 MP and 50¥ each).

## 5. Condition Monitor Formulas
*(All divisions are rounded up: $\lceil x / 2 \rceil$)*
- **Vehicles (Physical)**: $12 + \lceil \text{Body} / 2 \rceil$
- **Drones (Physical)**: $6 + \lceil \text{Body} / 2 \rceil$
- **Sprites (Matrix)**: $8 + \lceil \text{Level} / 2 \rceil$
- **Characters & Spirits (Stun)**: $8 + \lceil \text{Willpower} / 2 \rceil$
- **Characters & Spirits (Physical)**: $8 + \lceil \text{Body} / 2 \rceil$
- **Devices (Matrix)**: $8 + \lceil \text{Device Rating} / 2 \rceil$

## 6. Damage Resistance & Soak
- **Physical Damage Resistance Pool**: Resisted with $\text{Body} + \text{Armor} \pm \text{AP}$ (AP adjusts effective Armor value; effective Armor cannot drop below 0).
- **Damage Resolution**: Each hit scored reduces incoming Modified Damage by 1. Net unsoaked damage is marked directly onto the target's Physical Condition Monitor.
