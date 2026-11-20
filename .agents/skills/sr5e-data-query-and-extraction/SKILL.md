---
name: sr5e-data-query-and-extraction
description: Instructions, schemas, and CLI utilities for querying and extracting data from the 43 Chummer5a XML datasets in the data/ directory.
---

# Shadowrun 5e Chummer XML Data Query & Extraction

This skill provides instructions, data schemas, and CLI utilities for inspecting, querying, and extracting records from the 43 raw Chummer5a XML files located in the `data/` directory.

---

## 1. Quick CLI Query Tool

Use the included utility `scripts/query_chummer.py` to query equipment, weapons, drones, vehicles, cyberware, bioware, armor, gear, spells, and qualities directly:

```bash
# Query weapons
python scripts/query_chummer.py weapons "Predator"
python scripts/query_chummer.py weapons --category "Assault Rifles" --source "RG"

# Query drones & vehicles
python scripts/query_chummer.py drones "Doberman"
python scripts/query_chummer.py vehicles "Americar"

# Query cyberware & bioware
python scripts/query_chummer.py cyberware "Wired Reflexes"
python scripts/query_chummer.py bioware "Muscle Toner"

# Query spells & qualities
python scripts/query_chummer.py spells "Fireball"
python scripts/query_chummer.py qualities "Quick Healer"

# Output clean JSON for programmatic evaluation
python scripts/query_chummer.py weapons "Ares Alpha" --json
```

---

## 2. Core Data Filtering Rules

1. **Era Filtering**:
   - Items tagged with `<source>2050</source>` or containing `(2050)` in the `<name>` represent legacy 2050 gear and are **excluded by default**.
   - Pass `--include-2050` only when historical legacy rules are explicitly requested.
2. **German Pegasus Releases**:
   - Pass `--source German` to automatically match all Pegasus releases (`SAG`, `SOTG`, `DATG`, `HAMG`, `SHB`).
3. **Mod Slots Precedence**:
   - When inspecting vehicles or drones, if `<modslots>` is present and non-empty, use that integer.
   - If `<modslots>` is missing or blank, default Mod Slots to the vehicle's `Body`.
4. **Ammo Codes**:
   - Cylinder/revolver magazines are indicated by `(cy)`.
   - Belt feeds are indicated by `(belt)`.
   - Removable clips/magazines are indicated by `(c)`.
