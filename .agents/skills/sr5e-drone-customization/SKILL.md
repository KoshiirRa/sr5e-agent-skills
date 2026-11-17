---
name: sr5e-drone-customization
description: Rules, limits, and calculations for Shadowrun 5th Edition drone customization, mod slots, free upgrades, downgrades, attribute caps, drone weapon mounts, pilot programs, and autosofts.
---

# Shadowrun 5e Drone Customization & Mod Slots System

This skill defines the operational standards and mathematical calculations for customizing drones in Shadowrun 5th Edition (SR5) based on Chummer5a XML data and table rules.

---

## 1. Mod Slots Determination

1. **Explicit XML Tag**:
   If a drone has an explicit `<modslots>` value in `vehicles.xml`, use that number.
2. **Default Fallback**:
   If `<modslots>` is missing, blank, or omitted, default the drone's available base Mod Slots to its `Body` attribute:
   $$\text{Base Mod Slots} = \begin{cases} \text{int}(\langle\text{modslots}\rangle), & \text{if present in XML} \\ \text{int}(\langle\text{body}\rangle), & \text{otherwise} \end{cases}$$
3. **Pre-installed Mods**:
   Any pre-installed mods or mounts (under `<mods>` or `<weaponmounts>`) consume mod slots according to standard rules unless marked as native/stock.

---

## 2. Zero-Handling Standard (Math & Scaling)

- When an attribute is $0$ (such as a Microdrone's Body or a drone with Armor 0), **use $0.5$ in place of $0$** for any calculations, multipliers, or cost formulas.
- *Rule against exploits*: No multiplying by 0 to generate infinite free upgrades or zero-cost bypasses.

---

## 3. General Attribute Customization Rules

### A. General Limits & Ceilings
- **Body Restriction**: A drone's `Body` attribute **CANNOT** be increased under any circumstances.
- **Attribute Ceiling (2x Cap)**:
  No physical attribute can ever be raised to more than **twice its starting base value**:
  $$\text{Attribute}_{\text{max}} = 2 \times \max(\text{Base Attribute}, 0.5)$$

### B. Free Attribute Upgrade (Zero Mod Points)
- Every drone is eligible for **one** attribute increase without expending any Mod Points:
  - **Armor**: $+3$
  - **Any other eligible attribute** (Handling, Speed, Acceleration, Sensor): $+1$
- **Constraints**:
  - Can only be done **once per drone** (cannot apply to multiple attributes).
  - Body cannot be selected.
  - Consumes $0$ Mod Points.
  - Still requires normal financial payment in **nuyen (¥)** (using the upgrade cost formulas below).
  - Still bounded by the $2 \times \text{Base}$ ceiling.

### C. Attribute Downgrades (Extra Mod Points)
- **Standard Attribute Downgrade**:
  - Decreasing any standard attribute by $1$ (or Armor by $3$) grants **$+1$ Mod Point**.
  - Can only be done **once per drone**.
  - Cannot reduce an attribute to $0$ (**except for Speed**, which may drop to 0).
- **Body Downgrade**:
  - Reducing Body by $1$ generates $2$ Mod Points, yielding a **net gain of $+1$ Mod Point** (since reducing Body also drops base slots by 1).
  - **Floor Constraint**: Body may not be reduced lower than **half its starting value** ($\text{New Body} \ge \frac{\text{Starting Body}}{2}$). E.g., Body 3 can drop to 2 (since $2 \ge 1.5$), but not to 1.
  - **Availability**: $\text{Mod Points Gained} \times 3$.

---

## 4. Specific Attribute Upgrade Formulas & Costs

*(Note: In all formulas, if the drone's $\text{Body} = 0$, substitute $\text{Body} = 0.5$)*.

### Handling
- **Availability**: $\text{Upgraded Handling} \times 2$
- **Cost**:
  $$\text{Cost} = \text{Upgraded Handling} \times \text{Body} \times 200¥$$

### Speed
- **Availability**: $\text{Upgraded Speed} \times 2$
- **Cost**:
  $$\text{Cost} = (\text{Upgraded Speed} \times \text{Body} \times 2) \times 200¥$$
  *(Example: Increasing to Speed 5 on a Body 2 drone costs $((5 \times 2) \times 2) \times 200 = 20 \times 200 = 4{,}000¥$)*

### Acceleration
- **Availability**: $\text{Upgraded Acceleration} \times 4$
- **Cost**:
  $$\text{Cost} = \text{Upgraded Acceleration} \times \text{Body} \times 200¥$$

### Armor
- **Availability**: $\text{Upgraded Armor}$
  - **Legality**:
    - $\text{Armor} \le 6$: Standard / Legal
    - $6 < \text{Armor} \le 12$: Restricted (`R`)
    - $\text{Armor} > 12$: Forbidden (`F`)
- **Cost**:
  $$\text{Cost} = \text{Upgraded Armor} \times \text{Body} \times 200¥$$
- **Weight & Encumbrance Penalties**:
  - **Free Capacity Threshold**: Drone can carry up to $3 \times \text{Body}$ in Armor without penalty.
  - **Excess Armor Penalties**:
    - For every **$3$ points** above $3 \times \text{Body}$: **$-1$ Handling** and **$-1$ Speed**.
    - For every **$6$ points** above $3 \times \text{Body}$: **$-1$ Acceleration**.
  - **Immobilization Threshold**: If encumbrance causes **Handling $< 1$**, or either **Speed $< 0$** or **Acceleration $< 0$**, the drone is completely immobilized and unable to move.

### Sensor
- **Availability**: $\text{Upgraded Sensor} \times 2$
- **Cost**:
  - **Full Array Upgrade**: $\text{Upgraded Sensor Rating} \times 1{,}000¥$
  - **Single Sensor Element Upgrade**: $\text{Target Sensor Rating} \times 100¥$

---

## 5. Drone Software (Pilots & Autosofts)

Software upgrades cost **0 Mod Points** (0 MP).

### A. Pilot Programs
- **Function**: Replaces the factory Pilot rating of the drone.
- **Pilot Upgrade Table**:

| Pilot Rating | Availability | Cost (¥) | Legality |
| :---: | :---: | :---: | :--- |
| **1** | 4 | 100¥ | Legal |
| **2** | — | 400¥ | Legal |
| **3** | 8R | 1,800¥ | Restricted |
| **4** | 12R | 3,200¥ | Restricted |
| **5** | 16F | 10,000¥ | Forbidden |
| **6** | 24F | 20,000¥ | Forbidden |

### B. Specialized Autosofts
- **Smartsoft**:
  - **Function**: Allows the drone to utilize smartgun-equipped weapons and smartlink features.
  - **Rating**: 3 (requires drone **Pilot $\ge 3$**).
  - **Cost**: 1,500¥.
  - **MP Cost**: 0 MP.

---

## 6. Drone Weapon Mounts & Ammo Options

### A. Base Weapon Mounts

| Mount Size | Mod Points (MP) | Avail | Compatible Weapon Classes |
| :--- | :---: | :---: | :--- |
| **Micro** | 0 MP | 8R | Single-shot bullet or dart |
| **Mini** | 1 MP | 4R | Hold-out pistol, light pistol, reach 0 melee weapons, single-shot grenade |
| **Small** | 2 MP | 8R | Heavy pistol, machine pistol |
| **Standard** | 3 MP | 10F | Sub-machine gun, under-barrel grenade launcher |
| **Large** | 4 MP | 12F | Shotgun, hunting rifle, assault rifle, grenade launcher |
| **Huge** | 5 MP | 16F | Sniper rifle, light machine gun, medium machine gun |
| **Heavy** | 6 MP | 20F | Heavy machine gun, rocket launcher, assault cannon |

### B. Mount Concealment & Mechanical Options

- **Blow-Away Panels**:
  - Conceals the weapon until deployed.
  - **Cost**: $25¥ \times \text{Base MP of Mount}$
  - **MP Cost**: $0\text{ MP}$
  - **Note**: One-shot; must be replaced after deployment.
- **Pop-Up / Pop-Out / Pop-Under Mount**:
  - Conceals the weapon and extends/retracts repeatedly.
  - **MP Cost**: $+1\text{ MP}$
  - **Cost**: $100¥ \times \text{MP of Weapon Mount}$

### C. Ammunition Feeds & Capacity Mods

- **Extra Ammo Bin**:
  - Adds a second ammo bin, **doubling** standard ammunition capacity.
  - **Cost**: $1\text{ MP}$ and $50¥$.
- **Belt Feed Conversion**:
  - Replaces magazine feed with a belt feed.
  - Sets weapon ammo code to **`100(belt)`**.
  - **Cost**: $2\text{ MP}$ and $500¥$.
- **Belt Feed + Extra Ammo Bins**:
  - Extra ammo bins can be combined with the belt feed conversion.
  - Each additional ammo bin adds **$+100$ rounds of belt ammo** (e.g. 1 extra bin = 200 rounds belt, 2 extra bins = 300 rounds belt).
  - Each extra bin costs $1\text{ MP}$ and $50¥$.
