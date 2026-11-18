---
name: sr5e-drone-autosofts-and-swarms
description: Rules, limits, and calculations for Shadowrun 5th Edition drone autosofts, RCC program sharing, local storage capacity, and Rigger 5.0 Swarm rules.
---

# Shadowrun 5e Drone Autosofts & Swarms System

This skill covers the mechanics of Autosofts, Rigger Command Console (RCC) program sharing, drone local processing limits, and multi-drone Swarm operations from *Rigger 5.0*.

---

## 1. Autosoft Capacity & Running Limits

### A. Local Drone Storage
Drones operating autonomously without an RCC can run a limited number of autosofts locally:
$$\text{Max Local Autosofts} = \left\lceil \frac{\text{Pilot}}{2} \right\rceil$$
- Autosofts loaded onto a drone run at their purchased rating.
- Max autosoft rating supported is equal to the drone's Pilot program rating.

### B. RCC Program Sharing
When drones are slaved to an RCC (Rigger Command Console):
- The RCC can share a number of cyberprograms/autosofts equal to its **Device Rating**.
- **Sharing Benefit**: Any autosoft running on the RCC is broadcast to **all slaved drones simultaneously**.
- **Conflict & Override Rule**: If an individual drone is running a local copy of an autosoft, the local copy overrides the shared RCC version for that specific drone.

---

## 2. Core Autosoft Types

1. **Clearsight**:
   - Drone equivalent of Perception.
   - Test: $\text{Pilot} + \text{Clearsight } [\text{Sensor}]$
2. **Electronic Warfare**:
   - Used for sensor defense, encryption, and electronic detection.
   - Test: $\text{Pilot} + \text{Electronic Warfare } [\text{Sensor}]$
3. **Maneuvering**:
   - Drone equivalent of Vehicle/Pilot skills for defense and maneuvers.
   - Test: $\text{Pilot} + \text{Maneuvering } [\text{Handling}]$
4. **Stealth**:
   - Drone equivalent of Sneaking.
   - Test: $\text{Pilot} + \text{Stealth } [\text{Handling}]$
5. **Targeting**:
   - Drone equivalent of Gunnery for autonomous firing.
   - **Specific Model Rule**: Targeting autosofts must be purchased for a **specific weapon model** (e.g., *Targeting [Ares Alpha]* or *Targeting [Ingram Smartgun]*).
   - Test: $\text{Pilot} + \text{Targeting } [\text{Accuracy or Sensor}]$
6. **Smartsoft**:
   - Special Autosoft Rating 3 (Cost: 1,500¥; requires Pilot $\ge 3$).
   - Permits autonomous drones to benefit from smartgun systems and accessories.

---

## 3. Swarm Operations (*Rigger 5.0*, pp. 30–31)

A rigger can coordinate a collection of drones into a single operational unit using the **Swarm Autosoft**.

### A. Swarm Requirements
- The **Swarm** autosoft must be running on the RCC (or the master drone of the network).
- Minimum swarm size: **$2$ drones**.
- Drones in the swarm must share the same propulsion type (e.g., all rotorcraft, all ground walkers, etc.) to perform coordinated maneuvering.

### B. Swarm Base Attributes
The entire swarm operates as a cohesive entity using the following attributes:
- **Swarm Pilot**: The **highest Pilot rating** among all drones in the swarm.
- **Swarm Sensor**: The **highest Sensor rating** among all drones in the swarm.

### C. Swarm Bonus Modifier
The swarm gains an operational bonus to all tests (Maneuvering, Perception/Clearsight, Gunnery/Targeting) based on its numbers:
$$\text{Swarm Bonus} = (\text{Total Drones in Swarm} - 1)$$
- **Bonus Ceiling**: The bonus cannot exceed the **highest Pilot rating** in the swarm:
  $$\text{Effective Swarm Bonus} = \min(\text{Drones} - 1, \text{Highest Pilot})$$
- **Dice Pool & Limits**:
  - Adds directly to all test dice pools rolled by the swarm.
  - Adds to the relevant physical or sensor limits.

### D. Combat Resolution in a Swarm
- **Attacking**: When the swarm fires on a target, only one attack test is rolled using the boosted pool. Additional drones with matching weapons contribute to a coordinated saturation attack (increasing defense penalty or raw DV).
- **Taking Damage**: Enemies attack individual drones within the swarm, not the abstract swarm entity. If an individual drone is disabled or destroyed, the swarm size drops, and the Swarm Bonus recalibrates immediately.
