---
name: sr5e-magic-drain-and-spirits
description: Rules and calculations for Shadowrun 5th Edition spellcasting drain, summoning, binding, spirit attributes, and Immunity to Normal Weapons (ITNW).
---

# Shadowrun 5e Magic, Drain & Spirits System

This skill covers the mechanics of Spellcasting Drain, Summoning, Binding, Spirit scaling, and spirit combat defenses in Shadowrun 5th Edition.

---

## 1. Spellcasting Drain Mechanics

### A. The Drain Resistance Test
$$\text{Drain Resistance Pool} = \text{Willpower} + \text{Tradition Secondary Attribute} \pm \text{Tradition/Gear Modifiers}$$
*(Refer to `sr5e-traditions` for the secondary attribute of all 74 traditions).*

### B. Stun vs. Physical Drain Threshold
The nature of the drain damage taken depends on the caster's hits on the Spellcasting test compared to their current Magic rating:
$$\text{Drain Damage Type} = \begin{cases} \text{Stun}, & \text{if Spellcasting Hits} \le \text{Magic} \\ \text{Physical}, & \text{if Spellcasting Hits} > \text{Magic} \end{cases}$$

- Each hit on the Drain Resistance test reduces incoming Drain Value (DV) by $1$.
- Any unsoaked Drain is marked on the caster's Condition Monitor.
- **Minimum Drain Floor**: A spell's calculated drain can never drop below **$2\text{ DV}$**.

---

## 2. Spirit Summoning & Binding

### A. Summoning Test
- **Opposed Roll**: $\text{Summoning} + \text{Magic} \text{ [Astral]} \text{ vs. Spirit Force}$
- **Services Granted**: Net hits scored by the summoner.
- **Summoning Drain**:
  $$\text{Drain DV} = 2 \times (\text{Hits rolled by Spirit})$$
  *(Minimum Drain DV is 2).*
  - If the Spirit's hits exceed the summoner's Magic rating, the Drain is **Physical**; otherwise it is **Stun**.

### B. Binding Test
- Requires an existing summoned spirit and an enchanting/binding lodge.
- **Opposed Roll**: $\text{Binding} + \text{Magic} \text{ [Astral]} \text{ vs. Spirit Force} \times 2$
- **Additional Services**: Net hits scored add to existing services.
- **Binding Drain**: $2 \times (\text{Hits rolled by Spirit})$ (minimum 2; Physical if Spirit hits > Magic).

---

## 3. Spirit Attributes & Scaling by Force

Spirit attributes scale directly from their **Force ($F$)**:

| Spirit Type | Body | Agility | Reaction | Strength | Willpower | Logic | Intuition | Charisma | Edge | Essence |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Air** | $F-2$ | $F+3$ | $F+4$ | $F-3$ | $F$ | $F$ | $F$ | $F$ | $\lceil F/2 \rceil$ | $F$ |
| **Beasts** | $F+2$ | $F+1$ | $F$ | $F+2$ | $F$ | $F$ | $F$ | $F$ | $\lceil F/2 \rceil$ | $F$ |
| **Earth** | $F+4$ | $F-2$ | $F-1$ | $F+4$ | $F$ | $F-1$ | $F$ | $F$ | $\lceil F/2 \rceil$ | $F$ |
| **Fire** | $F+1$ | $F+2$ | $F+3$ | $F-2$ | $F$ | $F$ | $F+1$ | $F$ | $\lceil F/2 \rceil$ | $F$ |
| **Man** | $F+1$ | $F$ | $F+2$ | $F-1$ | $F$ | $F$ | $F+1$ | $F$ | $\lceil F/2 \rceil$ | $F$ |
| **Water** | $F$ | $F+1$ | $F+2$ | $F$ | $F$ | $F$ | $F$ | $F$ | $\lceil F/2 \rceil$ | $F$ |

- **Physical Condition Monitor**: $8 + \lceil \text{Body}/2 \rceil$
- **Initiative (Physical)**: $(\text{Reaction} + \text{Intuition}) + 2\text{D}6$
- **Initiative (Astral)**: $(\text{Intuition} \times 2) + 3\text{D}6$

---

## 4. Immunity to Normal Weapons (ITNW)

Materialized spirits possess **Immunity to Normal Weapons** against non-magical, non-elemental attacks (guns, blades, physical impacts, mundane explosions):

### A. Hardened Armor Value
$$\text{Hardened Armor} = 2 \times \text{Force}$$

### B. Modified Damage vs. Hardened Armor
Calculate the incoming modified attack damage:
$$\text{Modified Damage} = \text{Base Weapon DV} + \text{Net Attack Hits}$$

1. **Complete Immunity Threshold**:
   $$\text{If } \text{Modified Damage} \le (\text{Hardened Armor} + \text{AP}), \text{ NO DAMAGE IS DEALT.}$$
   *(The attack completely bounces off; no resistance roll is made).*
   *(Note: AP is typically negative, reducing effective Hardened Armor).*

2. **Penetrating Damage & Automatic Soak**:
   If $\text{Modified Damage} > (\text{Hardened Armor} + \text{AP})$:
   - The spirit rolls damage resistance with:
     $$\text{Soak Pool} = \text{Body} + \max(0, \text{Hardened Armor} + \text{AP})$$
   - In addition to any hits rolled, the spirit receives **automatic hits equal to half the base Hardened Armor**:
     $$\text{Automatic Soak Hits} = \text{Force}$$
   - Net unsoaked damage is marked on the spirit's Physical Condition Monitor.

*Bypassing ITNW: Magical attacks (spells, adept weapon foci, astral combat, and spirit powers) ignore Immunity to Normal Weapons completely.*
