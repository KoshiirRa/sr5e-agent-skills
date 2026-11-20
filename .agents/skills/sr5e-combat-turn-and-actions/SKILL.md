---
name: sr5e-combat-turn-and-actions
description: Rules and calculations for Shadowrun 5th Edition Combat Turn sequence, initiative passes, action economy, and interrupt actions.
---

# Shadowrun 5e Combat Turn & Action Economy System

This skill covers the mechanics of the Combat Turn sequence, initiative scores, passes, action economies, and interrupt defense actions in Shadowrun 5th Edition.

---

## 1. Initiative Determination

| Plane / Mode | Initiative Score Formula | Base Initiative Dice |
| :--- | :--- | :---: |
| **Physical** | $\text{Reaction} + \text{Intuition}$ | $+1\text{D}6$ (up to $+5\text{D}6$ via cyber/bioware/magic) |
| **Astral** | $\text{Intuition} \times 2$ | $+2\text{D}6$ (total $3\text{D}6$) |
| **Matrix AR** | $\text{Reaction} + \text{Intuition}$ | $+1\text{D}6$ |
| **Matrix VR (Cold-Sim)** | $\text{Data Processing} + \text{Intuition}$ | $+3\text{D}6$ |
| **Matrix VR (Hot-Sim)** | $\text{Data Processing} + \text{Intuition}$ | $+4\text{D}6$ |
| **Rigged Vehicle (Jumped In)** | $\text{Data Processing} + \text{Intuition}$ | $+3\text{D}6$ (Cold) or $+4\text{D}6$ (Hot) |

---

## 2. Combat Turn & Initiative Passes

1. **Initiative Roll**: All combatants roll their initiative score at the start of the Combat Turn.
2. **Action Phase**: Characters act in descending order of initiative score.
3. **Action Economy**: On their Action Phase, a character may take:
   - **One Complex Action**, OR
   - **Two Simple Actions**
   - PLUS **One Free Action** (any time during their phase or out of turn).
4. **Initiative Pass Countdown**:
   - Once all active combatants have acted, subtract **$10$** from everyone's initiative score.
   - Anyone with an initiative score $> 0$ acts again in the next Initiative Pass.
   - Continue until all combatants reach $0$ or below, ending the Combat Turn.

---

## 3. Interrupt Actions (Defensive Actions Out-of-Turn)

Interrupt actions may be taken at any time during a Combat Turn (even before the character's first action phase). They immediately reduce the character's **current initiative score** (or subtract from the next turn if score is 0):

| Interrupt Action | Initiative Cost | Effect | When to Use |
| :--- | :---: | :--- | :--- |
| **Full Defense** | **$-10$** | Adds **$+\text{Willpower}$** to **all** defense tests for the remainder of the Combat Turn. | Facing sustained incoming fire or multiple attackers. |
| **Dodge** | **$-5$** | Adds **$+\text{Gymnastics}$** to defense test against **one** ranged or melee attack. | Single high-threat bullet or blade attack. |
| **Parry** | **$-5$** | Adds **$+\text{Melee Weapon Skill}$** to defense test against **one** melee attack. | Must be wielding a ready melee weapon. |
| **Block** | **$-5$** | Adds **$+\text{Unarmed Combat}$** to defense test against **one** melee attack. | Defending against unarmed/melee strikes empty-handed. |
| **Dive for Cover** | **$-5$** | Move up to $+2$ meters into cover; character drops to **Prone** position. | Escaping line of fire or blast radius. |
| **Run for Your Life** | **$-10$** | Sprint up to full movement speed directly away from an area-of-effect blast. | Avoiding grenades, rockets, or area-effect spells. |
| **Intercept** | **$-5$** | Make an immediate melee attack against a target trying to move past you. | Crowd control / locking down fleeing enemies. |

---

## 4. The 4-Step Combat Resolution Sequence

When an attack occurs:

1. **Step 1: Declare Attack**
   Attacker declares target, weapon, firing mode, and any called shots.
2. **Step 2: Attack Test vs. Defense Test**
   - **Attacker Pool**: $\text{Combat Skill} + \text{Attribute } [\text{Accuracy}] \pm \text{Recoil/Environmental Modifiers}$.
   - **Defender Pool**: $\text{Reaction} + \text{Intuition} \pm \text{Cover/Firing Mode Modifiers}$ (plus any Interrupt bonuses).
   - If Attacker Hits $\le$ Defender Hits, attack misses.
   - If Attacker Hits $>$ Defender Hits, proceed to Step 3 with $\text{Net Hits} = \text{Attacker Hits} - \text{Defender Hits}$.
3. **Step 3: Determine Damage & Stun/Physical Threshold**
   $$\text{Modified DV} = \text{Base Weapon DV} + \text{Net Hits}$$
   $$\text{Effective Armor} = \max(0, \text{Target Armor} + \text{Weapon AP})$$
   - If $\text{Modified DV} \le \text{Effective Armor}$: Damage is **Stun**.
   - If $\text{Modified DV} > \text{Effective Armor}$: Damage is **Physical**.
4. **Step 4: Damage Resistance / Soak Test**
   - **Defender Soak Pool**: $\text{Body} + \text{Effective Armor}$.
   - Each hit reduces incoming Modified DV by $1$.
   - Net unsoaked damage is marked onto the appropriate Condition Monitor (Stun or Physical).
