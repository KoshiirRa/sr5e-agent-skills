---
name: sr5e-matrix-and-pan-defense
description: Rules and calculations for Shadowrun 5th Edition Personal Area Network (PAN) defense, device slaving, Marks, Matrix actions, and Noise calculations.
---

# Shadowrun 5e Matrix & PAN Defense System

This skill covers the rules and calculations for device slaving, Personal Area Network (PAN) defense, Matrix Marks, and environmental Noise in Shadowrun 5th Edition.

---

## 1. PAN Slaving & Mutual Defense

Personal devices (smartguns, cyberware, goggles, commlinks, medkits) can be slaved to a central Master device (a high-rating Commlink, Cyberdeck, or RCC):

### A. Slaving Capacity
$$\text{Max Slaved Devices} = \text{Master's Device Rating} \times 3$$

### B. Wireless Defense Test
When a slaved device is attacked wirelessly in the Matrix:
$$\text{Defense Pool} = \max(\text{Device Rating}, \text{Master's Logic/Willpower}) + \max(\text{Device Firewall}, \text{Master's Firewall})$$
- The slaved device defends using the **Master's superior stats**.
- If a slaved device is marked or compromised wirelessly, the Master is **not** automatically marked.

### C. Direct Connection (Bypassing PAN)
- If an attacker gains a direct physical connection (using a universal data cable, wire tap, or fiber tap) to a slaved device:
  - The device must defend using **its own native Device Rating and Firewall** (the Master cannot help).
  - If the attacker successfully places a mark on the slaved device via direct connection, **that mark also automatically replicates onto the Master device**!

---

## 2. Matrix Marks & Privilege Levels

| Marks Required | Privilege Level | Permitted Actions |
| :---: | :--- | :--- |
| **1 Mark** | **User Access** | Control Device (Simple actions), Edit File, Trace Icon, Enter/Exit Host. |
| **2 Marks** | **Security Access**| Control Device (Complex actions), Disarm Data Bomb. |
| **3 Marks** | **Admin Access** | Format Device, Reboot Device, Jump Into Rigged Vehicle. |
| **Owner (4)** | **Ownership** | Full ownership control, transferring ownership, clearing all marks. |

---

## 3. Core Matrix Actions

1. **Brute Force (Loud Attack)**:
   - **Test**: $\text{Cybercombat} + \text{Logic } [\text{Attack}] \text{ vs. } \text{Willpower} + \text{Firewall}$
   - **Success**: Places $1$ Mark ($+1$ additional mark for every $2$ net hits). Deals Matrix damage equal to net hits. Target is immediately aware of an attack.
2. **Hack on the Fly (Stealth Sleaze)**:
   - **Test**: $\text{Hacking} + \text{Logic } [\text{Sleaze}] \text{ vs. } \text{Intuition} + \text{Firewall}$
   - **Success**: Places $1$ Mark ($+1$ additional mark for every $2$ net hits) silently without alerting the target.
   - **Glitch/Failure**: Target places $1$ mark on the hacker and sounds the alert.
3. **Control Device**:
   - **Test**: $\text{Electronic Warfare} + \text{Logic } [\text{Data Processing}] \text{ vs. } \text{Intuition} + \text{Firewall}$ (or $\text{Pilot} + \text{Firewall}$ for drones).

---

## 4. Environmental Noise Calculations

Noise reduces all Matrix test dice pools:
$$\text{Net Noise Penalty} = \max(0, \text{Total Environmental Noise} - \text{Total Noise Reduction})$$

### A. Distance Noise
| Distance to Target | Noise Penalty |
| :--- | :---: |
| $0 \text{ to } 100 \text{ meters}$ | $0$ |
| $101 \text{ meters to } 1 \text{ km}$ | $-1$ |
| $1 \text{ km to } 10 \text{ km}$ | $-3$ |
| $10 \text{ km to } 100 \text{ km}$ | $-5$ |
| Greater than $100 \text{ km}$ | $-8$ |

### B. Situational Noise Modifiers
- **Cross-Grid Penalty**: $-2$ dice if hacking from a Public/Local Grid onto a Global Grid.
- **Spam Zone** (dense comm traffic / commercial ads): $-1$ to $-4$.
- **Static Zone** (abandoned barrens / underground tunnels): $-1$ to $-4$.
- **Faraday Cage / Negating Paint**: $-1$ to $-20$ (blocks wireless signals entirely if rating exceeds signal strength).

### C. Noise Reduction Gear
- **Datajack**: $+1$ Noise Reduction.
- **Antennae** (installed in headware or armor): $+1$ to $+3$ Noise Reduction.
- **RCC Noise Reduction**: Rigger can allocate RCC processing points between Program Sharing and Noise Reduction.
