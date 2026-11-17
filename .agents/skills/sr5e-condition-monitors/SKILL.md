---
name: sr5e-condition-monitors
description: Rules and calculation formulas for Shadowrun 5th Edition Condition Monitors, damage resistance, and soak pools across Characters, Spirits, Vehicles, Drones, Sprites, and Devices.
---

# Shadowrun 5e Condition Monitors & Damage Resistance

This skill details the formulas and calculations for determining Condition Monitors (Physical, Stun, and Matrix) and resolving damage resistance/soak pools across all entity types in Shadowrun 5th Edition (SR5).

---

## 1. General Rounding Principle

All Condition Monitor attribute divisions are **rounded up** ($\lceil \dots \rceil$):
$$\text{Bonus Boxes} = \left\lceil \frac{\text{Attribute}}{2} \right\rceil$$

---

## 2. Condition Monitor Formulas

### A. Physical Condition Monitors
- **Characters & Spirits**:
  $$\text{Physical CM} = 8 + \left\lceil \frac{\text{Body}}{2} \right\rceil$$
- **Drones**:
  $$\text{Physical CM} = 6 + \left\lceil \frac{\text{Body}}{2} \right\rceil$$
  *(Note: If Body is 0, such as on certain microdrones, applying the $0.5$ zero-rule gives $6 + \lceil 0.5 / 2 \rceil = 7$ boxes).*
- **Vehicles (Manned / Non-Drone)**:
  $$\text{Physical CM} = 12 + \left\lceil \frac{\text{Body}}{2} \right\rceil$$

### B. Stun Condition Monitors
- **Characters & Spirits**:
  $$\text{Stun CM} = 8 + \left\lceil \frac{\text{Willpower}}{2} \right\rceil$$
- *(Vehicles, Drones, Devices, and Sprites do not have Stun condition monitors; non-biological targets are immune to Stun damage unless specified by electricity/matrix attack rules).*

### C. Matrix Condition Monitors
- **Devices**:
  $$\text{Matrix CM} = 8 + \left\lceil \frac{\text{Device Rating}}{2} \right\rceil$$
  *(Used for Commlinks, Cyberdecks, RCCs, vehicle/drone internal electronics, and standalone electronic gear).*
- **Sprites**:
  $$\text{Matrix CM} = 8 + \left\lceil \frac{\text{Level}}{2} \right\rceil$$

---

## 3. Damage Resistance & Soak Pools

### Physical Damage Resistance
- **Standard Pool**:
  $$\text{Resistance Pool} = \text{Body} + \max(0, \text{Armor} + \text{AP})$$
  *(Armor Penetration / AP is applied as a modifier to effective Armor; AP cannot reduce effective Armor below 0).*
- **Resolution**:
  - Each hit rolled on the resistance test reduces incoming Modified Damage by $1$.
  - Any remaining unsoaked damage marks boxes on the target's Physical Condition Monitor.

---

## 4. Quick Reference Summary Table

| Entity Type | Monitor Type | Formula | Base | Divisor / Resistance Attributes |
| :--- | :--- | :--- | :---: | :--- |
| **Characters / Spirits** | **Physical** | $8 + \lceil \text{Body} / 2 \rceil$ | $8$ | Body (Resists: Body + Armor + AP) |
| **Characters / Spirits** | **Stun** | $8 + \lceil \text{Willpower} / 2 \rceil$ | $8$ | Willpower (Resists: Body) |
| **Drones** | **Physical** | $6 + \lceil \text{Body} / 2 \rceil$ | $6$ | Body (min $0.5$) (Resists: Body + Armor + AP) |
| **Vehicles** | **Physical** | $12 + \lceil \text{Body} / 2 \rceil$ | $12$ | Body (Resists: Body + Armor + AP) |
| **Sprites** | **Matrix** | $8 + \lceil \text{Level} / 2 \rceil$ | $8$ | Level |
| **Devices** | **Matrix** | $8 + \lceil \text{Device Rating} / 2 \rceil$ | $8$ | Device Rating (Resists: Device Rating + Firewall) |
