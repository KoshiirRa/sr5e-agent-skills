---
name: sr5e-recoil-and-firing-modes
description: Rules and calculations for Shadowrun 5th Edition weapon firing modes, progressive recoil accumulation, recoil compensation (RC), and drone mount recoil.
---

# Shadowrun 5e Recoil & Firing Modes System

This skill covers the mechanics of weapon firing modes, defense modifiers, cumulative recoil accumulation, and recoil compensation (RC) for characters, vehicles, and drones.

---

## 1. Recoil Compensation (RC) Baseline

### A. Character Natural RC
Every character has an innate baseline RC based on their physical mass and stability:
$$\text{Character Natural RC} = 1 + \left\lceil \frac{\text{Strength}}{3} \right\rceil$$

### B. Drone & Vehicle Mount RC
Vehicles and mounted weapons handle recoil through vehicular mass and gyroscopic mounts:
$$\text{Vehicle/Drone Mount RC} = \text{Body} + \text{Mount Specific RC}$$
*(Where a drone's Body is 0, substitute $0.5$ per drone zero-math standards, yielding $\lceil 0.5 \rceil = 1$ baseline RC).*

---

## 2. Firing Modes & Recoil Generation

| Firing Mode | Rounds Fired | Action Type | Recoil Generated | Target Defense Modifier | Notes |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Single Shot (SS)** | 1 | Simple | **0** | $0$ | Does not generate progressive recoil. |
| **Semi-Automatic (SA)** | 1 | Simple | **1** | $0$ | Standard single bullet. |
| **Semi-Auto Burst (SB)** | 3 | Complex | **3** | $-2$ | 3 rapid trigger pulls. |
| **Burst Fire (BF)** | 3 | Simple | **3** | $-2$ | Automatic 3-round burst. |
| **Long Burst (LB)** | 6 | Complex | **6** | $-5$ | Sustained automatic burst. |
| **Full Auto (FA - Simple)** | 6 | Simple | **6** | $-5$ | Compact full-auto burst (or 2 targets). |
| **Full Auto (FA - Complex)** | 10 | Complex | **10** | $-9$ | Heavy full-auto burst (or Suppression Fire). |

---

## 3. Cumulative Recoil & Penalty Formula

Recoil accumulates continuously over consecutive firing actions within the same combat turn until explicitly reset:

$$\text{Cumulative Recoil} = \sum (\text{Rounds Fired in Consecutive Firing Actions})$$
$$\text{Recoil Penalty} = \max(0, \text{Cumulative Recoil} - \text{Total RC})$$

- The penalty directly reduces the shooter's attack dice pool.
- If the penalty exceeds the dice pool, the attacker is reduced to a single die (or unable to fire accurately).

### Resetting Recoil
Cumulative recoil resets to **$0$** whenever:
1. The shooter takes a Simple Action to **Take Aim**.
2. The shooter performs any non-firing Simple or Complex action (reloading, moving, casting a spell, running).
3. The shooter pauses for an entire Action Phase without shooting.

---

## 4. Hardware Recoil Compensation Modifications

| Accessory / Modification | RC Bonus | Mount / Location | Constraints / Notes |
| :--- | :---: | :---: | :--- |
| **Gas-Vent System 1–3** | $+1$ to $+3$ | Barrel | Incompatible with suppressors/silencers. |
| **Shock Pad** | $+1$ | Stock | Attached to rigid or folding stock. |
| **Folding / Fixed Stock** | $+1$ | Stock | Must be extended/braced to provide bonus. |
| **Underbarrel Weight** | $+1$ | Underbarrel | Incompatible with underbarrel weapons/bipods. |
| **Bipod** | $+2$ | Underbarrel | Requires prone position or braced surface. |
| **Tripod** | $+6$ | Underbarrel | Requires stationary setup on ground/surface. |
| **Gyro Mount Harness** | $+6$ | Body Armor / Rig | Heavy torso harness for heavy weapons. |
| **Personalized Grip** | $+1$ | Grip | Only provides RC to the registered owner. |
