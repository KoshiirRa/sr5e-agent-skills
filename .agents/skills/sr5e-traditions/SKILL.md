---
name: sr5e-traditions
description: Dedicated skill for querying, resolving, and applying all Shadowrun 5th Edition magical traditions from traditions.xml, including Drain attributes, spirit alignments, and Forbidden Arcana advanced rules.
---

# Shadowrun 5e Magical Traditions System

This skill provides comprehensive rules, reference data, and programmatic lookup for all 74 magical traditions defined in `data/traditions.xml`, including core traditions from the SR5 Core Rulebook, Street Grimoire (`SG`), and advanced rules from **Forbidden Arcana (`FA`)**.

---

## 1. Drain Attribute Principles

In Shadowrun 5th Edition, every magical tradition determines its Drain resistance test with:
$$\text{Drain Pool} = \text{Willpower} + \text{Tradition Secondary Attribute}$$

The 5 tradition attribute archetypes in SR5 are:
1. **Willpower + Logic (`{WIL} + {LOG}`)**: Hermetic, Psionic, Cosmic, Necro Magic, Olympianism, Pariah, Planar Magic, Tarot.
2. **Willpower + Charisma (`{WIL} + {CHA}`)**: Shamanic, Aztec, Black Magic, Christian Theurgy, Druid (Alt), Green Magic, Missionist, Norse variants (Godi, Berserker, Seidman), Vodou, Wiccan.
3. **Willpower + Intuition (`{WIL} + {INT}`)**: Chaos Magic, Buddhist, Elder God, Red Magic, Shinto, Sioux, Wuxing.
4. **Willpower + Willpower (`{WIL} + {WIL}`)**: Romani, specialized mystic traditions.
5. **Willpower + Magic (`{WIL} + {MAG}`)**: Draconic, Blood Magic.

---

## 2. Spirit Category Alignments

Every tradition assigns specific spirit types to the 5 spell categories:
- **Combat**: Offense, direct/indirect combat spells.
- **Detection**: Sensory enhancement, divination, informational spells.
- **Health**: Healing, stabilization, attribute enhancement.
- **Illusion**: Stealth, deceit, sensory deception.
- **Manipulation**: Environmental manipulation, telekinesis, mind control.

Spirits can only provide Aid Sorcery bonuses for spells matching their aligned category.

---

## 3. Advanced Tradition Rules (*Forbidden Arcana*)

*Forbidden Arcana* introduced specialized sub-traditions, focused archetypes, and theological/philosophical constraints that modify standard character capabilities:

### A. Skill & Skill Group Disablements
Certain traditions forbid or replace standard magical disciplines:
- **`skillgroupdisable`**:
  - `Buddhism [Traditionalist]`: Disables `Enchanting`.
  - `Christian Theurgy [Traditional]`: Disables `Enchanting`.
  - `Druid [Traditional]`: Disables `Enchanting`.
  - `Norse [Seidman]`: Disables `Sorcery` (focuses purely on spirits and enchanting).
- **`skilldisable`**:
  - `Christian Theurgy [Traditional]` / `[Vigila Evangelica]`: Disables `Binding` (viewed as commanding angels/spirits heretically).
  - `Christian Theurgy [Westphalian]`: Disables `Alchemy` and `Artificing`.
  - `Islam [Islamic Alchemist]`: Disables `Spellcasting` and `Ritual Spellcasting` (pure alchemical practitioner).
  - `Pariah`: Disables `Summoning`, `Binding`, `Spellcasting`, `Ritual Spellcasting`, `Alchemy`, `Artificing` (pure Null-Mage counter-magic archetype).

### B. Granted Metamagic
- Some traditions grant immediate, innate access to specific metamagic arts upon initiation or character creation:
  - `Christian Theurgy [Traditional]`, `[Vigila Evangelica]`, and `[Westphalian]` automatically grant **Exorcism** (`<addmetamagic forced="True">Exorcism</addmetamagic>`).

### C. Spell Category Restrictions & Additions
- **Restricted Categories (`limitspellcategory`)**:
  - `Christian Theurgy [Westphalian]`: Caster can only learn/cast spells from **Combat** and **Health** categories.
- **Bonus Spell Categories (`spellcategory`)**:
  - Traditions like `Missionist` receive expanded category affinities.

### D. Innate Drain Modifiers
- `Elder God`: Possesses `<drainresist>-2</drainresist>`, suffering a permanent $-2$ penalty on all Drain resistance rolls due to the corruptive, alien nature of their patron entities.

### E. Unique Spirit Rosters
- `Draconic`: All standard spirit types available across all 5 spell categories.
- `Necro Magic`: Utilizes morbid spirit forms (Corpse Spirit for Combat, Carcass Spirit for Detection, Rot Spirit for Health, Detritus Spirit for Illusion, Palefire Spirit for Manipulation).

---

## 4. Querying Traditions via CLI / Python

Use the included helper script to look up any tradition, spirit alignment, or advanced FA rules:

```bash
# Query by name (exact or partial)
python .agents/skills/sr5e-traditions/scripts/query_tradition.py "Westphalian"
python .agents/skills/sr5e-traditions/scripts/query_tradition.py "Necro Magic"

# Filter by drain attribute
python .agents/skills/sr5e-traditions/scripts/query_tradition.py --drain "LOG"

# Filter by book source (SR5, SG, FA, SAG)
python .agents/skills/sr5e-traditions/scripts/query_tradition.py --source "FA"

# List all 74 traditions
python .agents/skills/sr5e-traditions/scripts/query_tradition.py --list-all
```
