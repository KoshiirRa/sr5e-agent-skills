import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[4] / "data" / "traditions.xml"

BOOK_MAP = {
    "SR5": "Shadowrun 5th Edition Core",
    "SG": "Street Grimoire",
    "FA": "Forbidden Arcana",
    "HT": "Hard Targets",
    "SSP": "Shadow Spells",
    "DTR": "Data Trails",
    "SAG": "State of the Art ADL (German Pegasus)",
    "SOTG": "Datapuls SOTA 2080 (German Pegasus)",
    "DATG": "Datapuls Verschlusssache (German Pegasus)",
    "HAMG": "Datapuls Hamburg (German Pegasus)",
    "SHB": "Schattenhandbuch (German Pegasus)",
    "SFME": "Shadowrun Missions Exclusive",
    "GE": "Grimoire Exclusive"
}

GERMAN_SOURCES = {"SAG", "SOTG", "DATG", "HAMG", "SHB"}

def get_text_safe(elem, tag, default=""):
    child = elem.find(tag)
    return child.text.strip() if child is not None and child.text else default

def parse_traditions(xml_file=DATA_PATH):
    if not xml_file.exists():
        print(f"Error: traditions XML file not found at {xml_file}")
        sys.exit(1)
        
    tree = ET.parse(xml_file)
    root = tree.getroot()
    traditions_elem = root.find("traditions")
    if traditions_elem is None:
        print("Error: <traditions> element not found in XML.")
        sys.exit(1)
        
    traditions = []
    for t in traditions_elem.findall("tradition"):
        name = get_text_safe(t, "name")
        drain = get_text_safe(t, "drain")
        source = get_text_safe(t, "source")
        page = get_text_safe(t, "page")
        
        # Spirit mappings
        spirits = {}
        for cat in ["combat", "detection", "health", "illusion", "manipulation"]:
            val = get_text_safe(t, cat)
            if val:
                spirits[cat.capitalize()] = val
                
        spirits_node = t.find("spirits")
        if spirits_node is not None:
            for s_child in spirits_node:
                tag_name = s_child.tag.lower()
                for cat in ["combat", "detection", "health", "illusion", "manipulation"]:
                    if cat in tag_name and s_child.text:
                        spirits[cat.capitalize()] = s_child.text.strip()
                        
        spiritform = get_text_safe(t, "spiritform", "Materialization")
        bonuses = {
            "disabled_skills": [],
            "disabled_skillgroups": [],
            "forced_metamagic": [],
            "limited_categories": [],
            "bonus_categories": [],
            "added_qualities": [],
            "drain_mod": None,
            "special_notes": []
        }
        
        bonus_node = t.find("bonus")
        if bonus_node is not None:
            for b in bonus_node:
                btag = b.tag.lower()
                btext = b.text.strip() if b.text else ""
                
                if btag == "skilldisable" and btext:
                    bonuses["disabled_skills"].append(btext)
                elif btag == "skillgroupdisable" and btext:
                    bonuses["disabled_skillgroups"].append(btext)
                elif btag == "addmetamagic" and btext:
                    bonuses["forced_metamagic"].append(btext)
                elif btag == "limitspellcategory" and btext:
                    bonuses["limited_categories"].append(btext)
                elif btag == "spellcategory" and btext:
                    bonuses["bonus_categories"].append(btext)
                elif btag == "addquality":
                    sel = b.attrib.get("select")
                    qname = f"{btext} ({sel})" if (btext and sel) else (sel or btext)
                    if qname:
                        bonuses["added_qualities"].append(qname)
                elif btag == "addqualities":
                    for aq in b.findall("addquality"):
                        aq_text = aq.text.strip() if aq.text else ""
                        sel = aq.attrib.get("select")
                        qname = f"{aq_text} ({sel})" if (aq_text and sel) else (sel or aq_text)
                        if qname:
                            bonuses["added_qualities"].append(qname)
                elif btag == "drainresist" and btext:
                    bonuses["drain_mod"] = btext
                elif btag in ["specificpower", "specificskill"]:
                    bonuses["special_notes"].append(f"{btag}: {b.attrib}")
                    
        traditions.append({
            "name": name,
            "drain": drain,
            "source": source,
            "source_full": BOOK_MAP.get(source, source),
            "page": page,
            "spiritform": spiritform,
            "spirits": spirits,
            "bonuses": bonuses
        })
        
    return traditions

def display_tradition(t):
    print(f"\n==================================================")
    print(f"Tradition: {t['name']}  [{t['source_full']} p.{t['page']}]")
    print(f"Drain Pool: {t['drain']}  |  Spirit Form: {t['spiritform']}")
    print(f"--------------------------------------------------")
    print("Spirit Alignments:")
    for cat in ["Combat", "Detection", "Health", "Illusion", "Manipulation"]:
        s_name = t["spirits"].get(cat, "None / Custom")
        print(f"  • {cat:<13}: {s_name}")
        
    b = t["bonuses"]
    has_adv = any([
        b["disabled_skills"], b["disabled_skillgroups"], b["forced_metamagic"],
        b["limited_categories"], b["bonus_categories"], b["added_qualities"],
        b["drain_mod"] is not None
    ])
    
    if has_adv:
        print(f"--------------------------------------------------")
        print("Advanced Rules & Restrictions:")
        if b["drain_mod"]:
            print(f"  • Drain Resistance Mod: {b['drain_mod']}")
        if b["disabled_skillgroups"]:
            print(f"  • Disabled Skill Groups: {', '.join(b['disabled_skillgroups'])}")
        if b["disabled_skills"]:
            print(f"  • Disabled Skills: {', '.join(b['disabled_skills'])}")
        if b["forced_metamagic"]:
            print(f"  • Granted Metamagic: {', '.join(b['forced_metamagic'])}")
        if b["limited_categories"]:
            print(f"  • Restricted Spell Categories: {', '.join(b['limited_categories'])}")
        if b["bonus_categories"]:
            print(f"  • Bonus Spell Categories: {', '.join(b['bonus_categories'])}")
        if b["added_qualities"]:
            print(f"  • Mandatory Qualities: {', '.join(b['added_qualities'])}")
    print(f"==================================================")

def main():
    parser = argparse.ArgumentParser(description="Query Shadowrun 5e traditions from Core, SG, FA, HT, SSP, and German Pegasus books.")
    parser.add_argument("name", nargs="?", default=None, help="Name or partial name of tradition.")
    parser.add_argument("--drain", "-d", help="Filter by secondary drain attribute (e.g. LOG, CHA, INT, WIL, MAG).")
    parser.add_argument("--source", "-s", help="Filter by book code or alias (e.g. SR5, SG, FA, HT, SSP, German, SAG, SOTG).")
    parser.add_argument("--list-all", "-l", action="store_true", help="List all tradition names.")
    args = parser.parse_args()

    traditions = parse_traditions()

    if args.list_all:
        print(f"\nAll Traditions ({len(traditions)} total):")
        for t in sorted(traditions, key=lambda x: x["name"]):
            print(f"  - {t['name']:<38} | {t['drain']:<15} | [{t['source_full']}]")
        return

    filtered = traditions
    if args.drain:
        d_upper = args.drain.upper()
        filtered = [t for t in filtered if d_upper in t["drain"].upper()]
        
    if args.source:
        s_query = args.source.strip().upper()
        if s_query in ["GERMAN", "PEGASUS", "DE"]:
            filtered = [t for t in filtered if t["source"] in GERMAN_SOURCES]
        elif s_query in ["HARD TARGETS", "HARDTARGETS"]:
            filtered = [t for t in filtered if t["source"] == "HT"]
        elif s_query in ["SHADOW SPELLS", "SHADOWSPELLS"]:
            filtered = [t for t in filtered if t["source"] == "SSP"]
        elif s_query in ["FORBIDDEN ARCANA", "FORBIDDENARCANA"]:
            filtered = [t for t in filtered if t["source"] == "FA"]
        elif s_query in ["STREET GRIMOIRE", "STREETGRIMOIRE"]:
            filtered = [t for t in filtered if t["source"] == "SG"]
        else:
            filtered = [t for t in filtered if s_query in t["source"].upper() or s_query in t["source_full"].upper()]
        
    if args.name:
        q = args.name.lower()
        filtered = [t for t in filtered if q in t["name"].lower()]

    if not filtered:
        print("No matching traditions found.")
        return

    for t in filtered:
        display_tradition(t)

if __name__ == "__main__":
    main()
