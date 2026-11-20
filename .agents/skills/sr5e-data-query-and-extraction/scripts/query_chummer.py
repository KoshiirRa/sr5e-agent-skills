#!/usr/bin/env python3
"""
Shadowrun 5e Chummer XML Query Utility
Queries raw Chummer5a XML data files (weapons, vehicles, armor, gear, cyberware, bioware, spells, etc.)
with automated era filtering (excludes legacy 2050 gear by default), source resolution, and tabular output.
"""

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[4] / "data"

BOOK_MAP = {
    "SR5": "Core Rulebook",
    "SG": "Street Grimoire",
    "FA": "Forbidden Arcana",
    "R5": "Rigger 5.0",
    "RG": "Run & Gun",
    "CF": "Chrome Flesh",
    "DTR": "Data Trails",
    "HT": "Hard Targets",
    "SSP": "Shadow Spells",
    "KC": "Kill Code",
    "BB": "Better Than Bad",
    "SL": "Stolen Souls",
    "CA": "Cutting Aces",
    "RF": "Run Faster",
    "SAG": "State of the Art ADL (German Pegasus)",
    "SOTG": "Datapuls SOTA 2080 (German Pegasus)",
    "DATG": "Datapuls Verschlusssache (German Pegasus)",
    "HAMG": "Datapuls Hamburg (German Pegasus)",
    "SHB": "Schattenhandbuch (German Pegasus)",
    "2050": "Shadowrun 2050 (Legacy)"
}

FILE_MAP = {
    "weapons": ("weapons.xml", "weapons", "weapon", ["name", "category", "damage", "ap", "mode", "rc", "ammo", "avail", "cost", "source"]),
    "vehicles": ("vehicles.xml", "vehicles", "vehicle", ["name", "category", "handling", "speed", "accel", "body", "armor", "pilot", "sensor", "modslots", "avail", "cost", "source"]),
    "drones": ("vehicles.xml", "vehicles", "vehicle", ["name", "category", "handling", "speed", "accel", "body", "armor", "pilot", "sensor", "modslots", "avail", "cost", "source"]),
    "armor": ("armor.xml", "armors", "armor", ["name", "category", "armor", "avail", "cost", "source"]),
    "gear": ("gear.xml", "gears", "gear", ["name", "category", "rating", "avail", "cost", "source"]),
    "cyberware": ("cyberware.xml", "cyberwares", "cyberware", ["name", "category", "ess", "capacity", "avail", "cost", "source"]),
    "bioware": ("bioware.xml", "biowares", "bioware", ["name", "category", "ess", "capacity", "avail", "cost", "source"]),
    "spells": ("spells.xml", "spells", "spell", ["name", "category", "type", "range", "damage", "duration", "dv", "source"]),
    "qualities": ("qualities.xml", "qualities", "quality", ["name", "category", "karma", "source"]),
}

def get_text_safe(elem, tag, default=""):
    child = elem.find(tag)
    return child.text.strip() if child is not None and child.text else default

def query_dataset(data_type, search_term="", category="", source_filter="", include_2050=False):
    if data_type not in FILE_MAP:
        raise ValueError(f"Unknown data type: {data_type}. Supported: {', '.join(FILE_MAP.keys())}")
        
    xml_filename, parent_tag, item_tag, fields = FILE_MAP[data_type]
    xml_path = DATA_DIR / xml_filename
    
    if not xml_path.exists():
        raise FileNotFoundError(f"XML data file not found at {xml_path}")
        
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    parent_elem = root.find(parent_tag)
    if parent_elem is None:
        # Fallback search
        for child in root:
            if child.tag == parent_tag:
                parent_elem = child
                break
                
    if parent_elem is None:
        items_list = root.findall(f".//{item_tag}")
    else:
        items_list = parent_elem.findall(item_tag)
        
    results = []
    for item in items_list:
        name = get_text_safe(item, "name")
        source = get_text_safe(item, "source")
        cat = get_text_safe(item, "category")
        
        # 2050 legacy era filter
        if not include_2050:
            if source == "2050" or "(2050)" in name:
                continue
                
        # Drone category filter if querying drones
        if data_type == "drones" and not cat.startswith("Drones"):
            continue
            
        # Search term filter
        if search_term and search_term.lower() not in name.lower():
            continue
            
        # Category filter
        if category and category.lower() not in cat.lower():
            continue
            
        # Sourcebook filter
        if source_filter:
            s_filter_upper = source_filter.upper()
            if s_filter_upper == "GERMAN":
                if source not in ["SAG", "SOTG", "DATG", "HAMG", "SHB"]:
                    continue
            elif s_filter_upper not in source.upper():
                continue
                
        entry = {}
        for f in fields:
            entry[f] = get_text_safe(item, f)
            
        # Add human-readable sourcebook
        entry["source_title"] = BOOK_MAP.get(source, source)
        results.append(entry)
        
    return results, fields

def format_table(results, fields):
    if not results:
        print("No matching records found.")
        return
        
    print(f"\nFound {len(results)} matching records:")
    
    # Calculate column widths
    display_fields = [f for f in fields if f not in ["id"]]
    col_widths = {f: len(f.upper()) for f in display_fields}
    for r in results:
        for f in display_fields:
            val = str(r.get(f, ""))
            col_widths[f] = max(col_widths[f], min(len(val), 40))
            
    header = " | ".join(f.upper().ljust(col_widths[f]) for f in display_fields)
    separator = "-+-".join("-" * col_widths[f] for f in display_fields)
    print(header)
    print(separator)
    
    for r in results:
        row_str = " | ".join(str(r.get(f, "")).ljust(col_widths[f])[:col_widths[f]] for f in display_fields)
        print(row_str)
    print()

def main():
    parser = argparse.ArgumentParser(description="Query Shadowrun 5e Chummer XML datasets.")
    parser.add_argument("type", choices=list(FILE_MAP.keys()), help="Data type to query.")
    parser.add_argument("search", nargs="?", default="", help="Name search term (substring, case-insensitive).")
    parser.add_argument("--category", "-c", default="", help="Filter by category.")
    parser.add_argument("--source", "-s", default="", help="Filter by sourcebook code or 'German'.")
    parser.add_argument("--include-2050", action="store_true", help="Include legacy 2050 era items.")
    parser.add_argument("--json", "-j", action="store_true", help="Output results as JSON.")
    args = parser.parse_args()

    results, fields = query_dataset(
        args.type,
        search_term=args.search,
        category=args.category,
        source_filter=args.source,
        include_2050=args.include_2050
    )

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        format_table(results, fields)

if __name__ == "__main__":
    main()
