---
name: sr5e-cyberware-essence-and-grades
description: Rules, multipliers, and calculations for Shadowrun 5th Edition Cyberware and Bioware grades, Essence loss, the Cyber-Bio essence split, and cyberlimb capacity.
---

# Shadowrun 5e Cyberware, Bioware & Essence System

This skill covers the rules, grade multipliers, essence calculations, and capacity tracking for augmentations in Shadowrun 5th Edition.

---

## 1. Augmentation Grades

Every piece of cyberware and bioware is manufactured to a specific quality grade:

| Grade | Essence Multiplier | Nuyen (¥) Multiplier | Availability Modifier | Installation Requirement |
| :--- | :---: | :---: | :---: | :--- |
| **Used** | **$1.25\times$** | **$0.8\times$** | $-4$ | Street doc / Alley clinic |
| **Standard** | **$1.0\times$** | **$1.0\times$** | $+0$ | Standard clinic |
| **Alphaware** | **$0.8\times$** | **$1.2\times$** | $+2$ | Specialized clinic |
| **Betaware** | **$0.7\times$** | **$1.5\times$** | $+4$ | High-end hospital / Corporate clinic |
| **Deltaware** | **$0.5\times$** | **$2.5\times$** | $+8$ | Delta Clinic (Restricted / In-play only) |

- **Rounding**: Essence costs are rounded to two decimal places ($0.01$).

---

## 2. Cyberware vs. Bioware Essence Loss (The Essence Split)

When a character possesses both Cyberware and Bioware, their body adapts differently to inorganic mechanical parts versus cloned biological grafts.

### The Formula:
$$\text{Total Effective Essence Loss} = \max(\text{Cyberware Loss}, \text{Bioware Loss}) + \left(0.5 \times \min(\text{Cyberware Loss}, \text{Bioware Loss})\right)$$

- **The Primary Category**: The category (Cyberware or Bioware) with the greater total base essence loss is paid in full ($100\%$).
- **The Secondary Category**: The category with the smaller total base essence loss is **halved ($50\%$)**.
- **Current Essence**:
  $$\text{Current Essence} = \max(0.00, 6.00 - \text{Total Effective Essence Loss})$$
  *(If Essence reaches 0.00 or below, the character dies).*

### Essence Holes (Augmentation Removal/Upgrade)
- When a piece of cyberware or bioware is removed, the essence does **not** return.
- Instead, it leaves an **Essence Hole**.
- Any new augmentations installed into that category fill the hole first; no additional Essence is lost until the hole is completely consumed.

---

## 3. Cyberlimb Capacity & Attribute Rules

Cyberlimbs (cyberarms, cyberlegs, cyber skulls, cyber torsos) replace organic limbs and provide dedicated internal **Capacity ($[\dots]$)**:

### A. Base Limb Stats
- Factory standard cyberlimbs start with:
  - **Strength**: 3
  - **Agility**: 3
- Natural physical damage track: Each full cyberlimb adds **$+1$ box** to the character's Physical Condition Monitor (+1 for arm, +1 for leg; torso adds +2).

### B. Customization vs. Enhancement
1. **Customization** (Purchased at limb creation):
   - Increases Strength or Agility up to the character's **natural metatype maximum**.
   - Does **not** consume Capacity.
   - Costs nuyen and increases availability.
2. **Enhancement** (Modular upgrades):
   - Enhances Strength, Agility, or Armor up to **$+3$ above the customized rating**.
   - Consumes **1 Capacity per point** of enhancement.
