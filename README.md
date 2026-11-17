# Shadowrun 5e Agent Directives & Skills

A structured repository of AI agent directives, rules definitions, and specialized skills for **Shadowrun 5th Edition** (SR5e) tabletop mechanics and calculations.

> **Note**: This repository exclusively houses agent rules, knowledge directives, and skills. Raw Chummer5a XML datasets and generated data exports are kept local and excluded via `.gitignore`.

---

## 📁 Repository Structure

```
├── .agents/
│   └── skills/
│       ├── sr5e-condition-monitors/
│       │   └── SKILL.md             # Condition monitors, damage resistance, and soak pools
│       └── sr5e-drone-customization/
│           └── SKILL.md             # Drone customization rules, mod slots, mounts, formulas
├── AGENTS.md                        # Core workspace agent directives & guidelines
├── .gitattributes                   # LF line-ending normalization
├── .gitignore                       # Ignores data/ XMLs and CSV exports
└── README.md
```

---

## 🤖 Agent Directives (`AGENTS.md`)
The [`AGENTS.md`](./AGENTS.md) file defines the behavioral rules, edge-case math, and rulebook references for agent assistants operating in Shadowrun 5e contexts:
- **Attribute Calculations & Ceilings**: Minimum base-attribute substitutions for zero-value attributes (e.g., Body 0 scaling), $2\times$ attribute caps, free upgrades, and downgrade point gains.
- **Weapon Mount Rules**: MP costs, size categories (Micro to Heavy), ammo conversions (belt feeds, extra bins), and concealment mechanics (pop-up vs. blow-away).
- **Soak & Damage Resistance Pools**: Step-by-step resolution of incoming modified damage, armor penetration (AP), and condition monitor tracking.
- **Source Filtering & Books**: Handling German Pegasus-exclusive source codes (`SAG`, `SOTG`, `HAMG`, `SHB`) and era filtering (excluding legacy 2050 entries).

---

## 🛠️ Specialized Skills (`.agents/skills/`)

### 1. `sr5e-condition-monitors`
Provides deterministic calculation formulas and damage resolution pipelines across all SR5e entity types:
- **Condition Monitor Boxes**:
  - Vehicles (Physical): $12 + \lceil \text{Body} / 2 \rceil$
  - Drones (Physical): $6 + \lceil \text{Body} / 2 \rceil$
  - Sprites (Matrix): $8 + \lceil \text{Level} / 2 \rceil$
  - Characters / Spirits (Physical & Stun): $8 + \lceil (\text{Body} \text{ or } \text{Willpower}) / 2 \rceil$
  - Devices (Matrix): $8 + \lceil \text{Device Rating} / 2 \rceil$
- **Damage Resistance Pools & AP**: Full calculation steps for resisting Physical, Stun, and Matrix biofeedback damage.

### 2. `sr5e-drone-customization`
Provides exhaustive rules for drone tuning according to *Rigger 5.0*:
- **Mod Slots Allocation**: Explicit `<modslots>` fallback to `Body`.
- **Mod Point (MP) Budgeting**: Free upgrades (0 MP, $+1$ attribute or $+3$ armor), downgrades for bonus MP, and Body reduction trade-offs.
- **Cost & Availability Scaling**: Formulas for Handling, Speed, Acceleration, Armor, Sensors, and Pilot upgrades.
- **Weapon Mount Fitting**: Micro through Heavy mounts, pop-up/concealment mechanisms, and ammo bin expansions.
