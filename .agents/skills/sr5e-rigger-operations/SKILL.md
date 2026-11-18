---
name: sr5e-rigger-operations
description: Rules and calculations for Shadowrun 5th Edition rigger control modes, Vehicle Control Rig (VCR) bonuses, Hot-Sim vs Cold-Sim, Gunnery tests, and Ramming/Collision damage.
---

# Shadowrun 5e Rigger Operations & Vehicle Combat

This skill covers the mechanics of rigger control modes, Vehicle Control Rig (VCR) cyberware integration, VR initiative, Gunnery tests, and collision/ramming rules in Shadowrun 5th Edition.

---

## 1. The Three Vehicle Control Modes

### A. Autonomous (Dog Brain)
- The drone/vehicle operates entirely on its own internal Pilot program.
- **Test Pool**: $\text{Pilot} + \text{Autosoft}$ (e.g., Pilot + Maneuvering for piloting, Pilot + Targeting for shooting).
- **Limits**: Vehicle Handling, Speed, or Sensor limits apply.
- **Initiative**: $(\text{Pilot} \times 2) + 4\text{D}6$ (Data Processing + Pilot in Matrix).

### B. Remote Control (Captain's Chair / AR/VR)
- The rigger sends wireless commands via Commlink, Cyberdeck, or RCC (Matrix action: **Control Device**).
- **Test Pool**: Character's own Skill + Physical/Mental Attribute (e.g., Gunnery + Agility or Pilot Ground Craft + Reaction).
- **Control Device Action**:
  - Requires 1 Mark on the vehicle/drone (or ownership).
  - Minor actions / firing takes the rigger's standard action economy.

### C. Jumped In (VR Rigging)
- The rigger interfaces their neural consciousness directly into the vehicle via a **Vehicle Control Rig (VCR)** and a **Rigger Interface**.
- **The "Become the Machine" Principle**:
  - The vehicle replaces the rigger's body.
  - Vehicle limits become the rigger's physical limits.
- **VCR Rating Bonuses**:
  - **Dice Pool Bonus**: Add **$+\text{VCR Rating}$** to all vehicle operational tests (Piloting, Gunnery, Sensor tests, Ramming).
  - **Limit Increase**: Add **$+\text{VCR Rating}$** to all vehicle limits (Handling, Speed, Sensor, Accuracy).
  - **Threshold Reduction**: Subtract **$-\text{VCR Rating}$** from all vehicle test thresholds (minimum threshold 1).

---

## 2. Rigger VR Initiative & Biofeedback

| VR Mode | Initiative Formula | Dice Pool Bonus | Biofeedback Type |
| :--- | :---: | :---: | :--- |
| **Cold-Sim VR** | $\text{Data Processing} + \text{Intuition} + 3\text{D}6$ | $+0$ | **Stun** |
| **Hot-Sim VR** | $\text{Data Processing} + \text{Intuition} + 4\text{D}6$ | $+2$ dice to all actions | **Physical** |

- **Biofeedback**: When a jumped-in vehicle suffers damage or Matrix attacks, the rigger suffers Biofeedback damage (resisted with $\text{Willpower} + \text{Firewall}$).

---

## 3. Gunnery Combat Tests

Vehicle-mounted weapons are resolved through one of three gunnery methods:

1. **Manual / Remote Gunnery (Direct Control)**:
   $$\text{Pool} = \text{Gunnery} + \text{Agility } [\text{Accuracy}]$$
2. **Sensor-Assisted Gunnery (Sensor Targeting)**:
   $$\text{Pool} = \text{Gunnery} + \text{Logic } [\text{Sensor}]$$
   - Target defends with $\text{Reaction} + \text{Intuition}$.
3. **Autonomous Drone Gunnery**:
   $$\text{Pool} = \text{Pilot} + \text{Targeting [Weapon Model] } [\text{Accuracy or Sensor}]$$

---

## 4. Collisions, Ramming & Crash Tests

When vehicles collide with obstacles or each other:

### A. Ramming Attack Test
- **Attacker Test**: $\text{Pilot Skill} + \text{Reaction } [\text{Handling}]$ (jumped-in riggers add VCR rating).
- **Defender Test**: $\text{Pilot Skill} + \text{Reaction } [\text{Handling}]$ to evade.

### B. Collision Damage Formula
$$\text{Base Collision DV} = \left\lceil \frac{\text{Body} \times \text{Speed Margin}}{10} \right\rceil$$
- **Speed Margin**:
  - **Head-on Collision**: $\text{Speed of Vehicle A} + \text{Speed of Vehicle B}$.
  - **Rear-end / Sideswipe**: $|\text{Speed of Vehicle A} - \text{Speed of Vehicle B}|$.
  - **Stationary Obstacle**: Current Speed of the moving vehicle.
- **AP**: $-\text{Speed Margin} / 10$ (round down).

### C. Damage Soak
- Both vehicles (or vehicle and pedestrian/obstacle) suffer collision damage based on the other's Body!
- Each resists with:
  $$\text{Soak Pool} = \text{Body} + \text{Armor} \pm \text{AP}$$
- **Ram Plate Modification**: Adds $+2$ Body for calculating damage inflicted on targets during a ram, and adds $+2$ Armor for resisting ramming damage.
