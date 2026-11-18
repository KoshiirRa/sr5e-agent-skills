---
name: sr5e-explosives-and-chunky-salsa
description: Rules and calculations for Shadowrun 5th Edition explosive blast drop-off, grenade scatter, barrier penetration, and the Chunky Salsa reflected shockwave rule.
---

# Shadowrun 5e Explosives & Chunky Salsa System

This skill covers the mechanics of explosive blast damage, grenade scatter, barrier resistance, and the "Chunky Salsa" reflected shockwave effect in enclosed spaces.

---

## 1. Grenade Attack & Scatter Mechanics

Grenade attacks target an area rather than an individual. Threshold to hit target location is **$3$ hits**.

### Scatter Distance
If the attacker scores fewer than 3 hits on the attack test ($\text{Throwing Weapons}$ or $\text{Heavy Weapons}$):
$$\text{Scatter Distance (meters)} = \max(0, \text{Scatter Dice Roll} - \text{Net Hits})$$

| Delivery Method | Scatter Roll | Scatter Direction | Modifiers |
| :--- | :---: | :---: | :--- |
| **Standard Thrown Grenade** | $2\text{D}6$ meters | $1\text{D}8$ Direction | Prone / bracing: no effect. |
| **Aerodynamic Thrown Grenade** | $1\text{D}6$ meters | $1\text{D}8$ Direction | Aerodynamic design reduces scatter. |
| **Grenade Launcher (Unguided)** | $3\text{D}6$ meters | $1\text{D}8$ Direction | High-velocity ballistic trajectory. |
| **Airburst-Linked Launcher** | $1\text{D}6$ meters | $1\text{D}8$ Direction | Detonates at exact target coordinates. |

---

## 2. Blast Damage Falloff

Explosive blast energy drops off rapidly with distance from the point of detonation:

$$\text{Effective Blast DV} = \text{Base DV} - (\text{Distance from Blast in meters} \times \text{Drop-off Rate})$$

- **Standard Frag / HE Grenades**: Drop-off rate is **$-2\text{ DV}$ per meter**.
- **Concussion Grenades**: Drop-off rate is **$-1\text{ DV}$ per meter** (Stun damage).
- **AP Falloff**: AP is unaffected by distance; full AP applies as long as at least $1\text{ DV}$ reaches the target.

---

## 3. The "Chunky Salsa" Rule (Confined Space Shockwaves)

When an explosion occurs within an enclosed space (such as a corridor, elevator, sealed bunker, or vehicle interior), the shockwave cannot dissipate into the open air and reflects off solid surfaces.

### Step-by-Step Resolution:
1. **Initial Blast**:
   Calculate blast damage from the detonation point to the nearest solid barrier (wall, ceiling, or floor).
2. **Barrier Structural Check**:
   - The barrier resists the incoming blast using:
     $$\text{Barrier Soak} = \text{Barrier Armor} \times 2$$
   - Each hit scored reduces the blast DV.
   - If the remaining DV exceeds the barrier's **Structure Rating**, the barrier is breached/destroyed, creating an opening for the blast to escape.
3. **Shockwave Reflection**:
   - If the barrier **withstands** the blast (is not completely breached):
     $$\text{Reflected Blast DV} = \text{Remaining Blast DV at Barrier Surface}$$
   - The shockwave bounces back into the room toward the center.
   - The reflected damage **adds directly to the current blast DV** affecting anyone caught in its path:
     $$\text{Combined Target DV} = \text{Direct Blast DV} + \sum \text{Reflected Blast DVs}$$
4. **Multiple Walls**:
   In fully enclosed spaces with rigid walls on all sides, the shockwave reflects back and forth continuously until all blast energy dissipates below $1\text{ DV}$ or the walls collapse. Targets inside suffer massive compounded damage.
