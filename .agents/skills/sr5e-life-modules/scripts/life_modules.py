#!/usr/bin/env python3
"""
Shadowrun 5e Life Modules Query, Step-by-Step Character Builder,
Markdown Sheet Generator & Recommendation Engine.
Reads dedicated JSON datasets under data/life_modules/ (standard library only).
"""

import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
DATA_DIR = REPO_ROOT / "data" / "life_modules"

STAGE_FILES = {
    "metatypes": "metatypes.json",
    "nationalities": "nationalities.json",
    "formative_years": "formative_years.json",
    "teen_years": "teen_years.json",
    "further_education": "further_education.json",
    "real_life": "real_life.json",
}

STAGE_ALIASES = {
    "meta": "metatypes",
    "metatype": "metatypes",
    "metatypes": "metatypes",
    "nat": "nationalities",
    "nationality": "nationalities",
    "nationalities": "nationalities",
    "formative": "formative_years",
    "formative_years": "formative_years",
    "teen": "teen_years",
    "teen_years": "teen_years",
    "fe": "further_education",
    "education": "further_education",
    "further_education": "further_education",
    "rl": "real_life",
    "real": "real_life",
    "real_life": "real_life",
}


def load_json(filename: str) -> dict:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def load_all_data() -> dict:
    sa = load_json("skill_attributes.json")
    data = {
        "rules": load_json("rules.json"),
        "skill_groups": load_json("skill_groups.json")["skill_groups"],
        "skill_attributes": sa["active_skill_attributes"],
        "focus_presets": sa["focus_presets"],
        "stages": {},
    }
    for key, fname in STAGE_FILES.items():
        raw = load_json(fname)
        items = raw.get("metatypes") if key == "metatypes" else raw.get("modules", [])
        data["stages"][key] = {
            "meta": raw,
            "items": items,
            "by_name": {item["name"].lower(): item for item in items},
        }
    return data


def resolve_module(data: dict, stage: str, name: str) -> dict | None:
    by_name = data["stages"][stage]["by_name"]
    q = name.strip().lower()
    if q in by_name:
        return by_name[q]
    matches = [item for k, item in by_name.items() if q in k]
    if len(matches) == 1:
        return matches[0]
    return None


def triangular_raise_cost(start: int, delta: int, multiplier: int) -> int:
    """Cost to raise a rating from `start` to `start + delta` at `New Rating * multiplier`."""
    if delta <= 0:
        return 0
    end = start + delta
    return multiplier * ((end * (end + 1) // 2) - (start * (start + 1) // 2))


def resolve_focus(build: dict, data: dict) -> tuple[list[str], list[str]]:
    """Return (core_attributes, core_skills) from focus_areas presets + explicit core_skills (unless core_skills_override is true)."""
    core_attrs = []
    core_skills = []
    presets = data["focus_presets"]
    exclude_set = {s.lower() for s in build.get("exclude_core_skills", [])}
    for f in build.get("focus_areas", []):
        key = f.strip().lower().replace(" ", "_")
        if key in presets:
            for a in presets[key]["core_attributes"]:
                if a not in core_attrs:
                    core_attrs.append(a)
            if not build.get("core_skills_override"):
                for s in presets[key]["core_skills"]:
                    if s not in core_skills and s.lower() not in exclude_set:
                        core_skills.append(s)
    for s in build.get("core_skills", []):
        if s not in core_skills and s.lower() not in exclude_set:
            core_skills.append(s)
    return core_attrs, core_skills


def validate_further_education(fe_modules: list[dict]) -> list[str]:
    errors = []
    if not fe_modules:
        return errors

    athletes = [m for m in fe_modules if m.get("category") == "StudentAthlete"]
    non_athletes = [m for m in fe_modules if m.get("category") != "StudentAthlete"]

    if len(athletes) > 1:
        errors.append(
            f"Further Education: at most 1 Student Athlete module may be taken (found {len(athletes)})."
        )

    if len(non_athletes) > 2:
        errors.append(
            f"Further Education: too many non-Student-Athlete modules ({len(non_athletes)}). "
            "Max is 1, or 2 via Community College / Trade School -> State University / Ivy League."
        )
    elif len(non_athletes) == 2:
        prereq_cats = {"CommunityCollege", "TradeTechnicalSchool", "Trade School Shop"}
        followup_cats = {"StateUniversity", "IvyLeague"}
        cats = [m.get("category") for m in non_athletes]
        valid_pair = (
            (cats[0] in prereq_cats and cats[1] in followup_cats)
            or (cats[1] in prereq_cats and cats[0] in followup_cats)
        )
        if not valid_pair:
            errors.append(
                f"Further Education: invalid 2-module combination ({cats[0]} + {cats[1]}). "
                "Two non-Student-Athlete modules are only allowed when combining a Community College "
                "or Trade School module with a State University or Ivy League module."
            )
    return errors


def min_karma_to_reach_pool(
    current_attr: int,
    max_attr: int,
    current_skill: int,
    max_skill: int,
    target_pool: int = 12,
    has_spec: bool = False,
) -> int | None:
    """Minimum Karma required to raise Attr and/or Skill so Attr + Skill (+2 if spec) >= target_pool."""
    effective_target = target_pool - (2 if has_spec else 0)
    if current_attr + current_skill >= effective_target:
        return 0
    if max_attr + max_skill < effective_target:
        return None
    best = None
    for a in range(current_attr, max_attr + 1):
        needed_s = max(current_skill, effective_target - a)
        if needed_s <= max_skill:
            cost = triangular_raise_cost(current_attr, a - current_attr, 5) + triangular_raise_cost(
                current_skill, needed_s - current_skill, 2
            )
            if best is None or cost < best:
                best = cost
    return best


def evaluate_build(build: dict, data: dict) -> dict:
    rules = data["rules"]
    skill_groups_map = data["skill_groups"]
    skill_attrs = data["skill_attributes"]

    errors = []
    warnings = []
    advisories = []
    notes = []
    pending_choices = []

    playstyle = (build.get("playstyle") or "story").strip().lower()
    core_attrs, core_skills = resolve_focus(build, data)

    # 1. Resolve Metatype
    meta_name = build.get("metatype")
    metatype = resolve_module(data, "metatypes", meta_name) if meta_name else None
    if not metatype:
        errors.append(f"Metatype '{meta_name}' not found or missing.")

    # 2. Single-choice stages
    nat_name = build.get("nationality")
    nationality = resolve_module(data, "nationalities", nat_name) if nat_name else None
    if nat_name and not nationality:
        errors.append(f"Nationality '{nat_name}' not found.")

    fy_name = build.get("formative_years")
    formative = resolve_module(data, "formative_years", fy_name) if fy_name else None
    if fy_name and not formative:
        errors.append(f"Formative Years module '{fy_name}' not found.")

    ty_name = build.get("teen_years")
    teen = resolve_module(data, "teen_years", ty_name) if ty_name else None
    if ty_name and not teen:
        errors.append(f"Teen Years module '{ty_name}' not found.")

    # 3. Further Education
    fe_names = build.get("further_education", [])
    if isinstance(fe_names, str):
        fe_names = [fe_names]
    fe_modules = []
    for n in fe_names:
        m = resolve_module(data, "further_education", n)
        if not m:
            errors.append(f"Further Education module '{n}' not found.")
        else:
            fe_modules.append(m)
    errors.extend(validate_further_education(fe_modules))

    # 4. Real Life (chronological order)
    rl_names = build.get("real_life", [])
    if isinstance(rl_names, str):
        rl_names = [rl_names]
    rl_modules = []
    for n in rl_names:
        m = resolve_module(data, "real_life", n)
        if not m:
            errors.append(f"Real Life module '{n}' not found.")
        else:
            rl_modules.append(m)

    # 5. Awakened / Emerged quality cost
    awakened = build.get("awakened_quality")
    awakened_cost = 0
    if awakened:
        costs = {**rules["awakened_and_emerged_costs"]}
        fa_costs = costs.pop("forbidden_arcana_aspected_variants", {})
        all_aw_costs = {**costs, **fa_costs}
        if awakened in all_aw_costs:
            awakened_cost = all_aw_costs[awakened]
        else:
            errors.append(f"Unknown awakened_quality '{awakened}'. Valid: {', '.join(all_aw_costs.keys())}")

    selected_modules = []
    for st, mod in [
        ("nationalities", nationality),
        ("formative_years", formative),
        ("teen_years", teen),
    ]:
        if mod:
            selected_modules.append((st, mod))
    for mod in fe_modules:
        selected_modules.append(("further_education", mod))
    for mod in rl_modules:
        selected_modules.append(("real_life", mod))

    # 6. Validate prerequisites & post-requisites
    fe_vocations = {m.get("vocation") for m in fe_modules if m.get("vocation")}
    rl_categories = [m.get("category") for m in rl_modules]
    resolved_choices_by_mod = {
        rc["module"].lower(): rc for rc in build.get("resolved_choices", []) if rc.get("module")
    }

    for st, mod in selected_modules:
        req = mod.get("requires")
        if req:
            if "qualities_any" in req and awakened not in req["qualities_any"]:
                errors.append(
                    f"Prerequisite failed for '{mod['name']}': requires one of {req['qualities_any']} "
                    f"(character has {awakened or 'Mundane'})."
                )
            if "metatypes_any" in req and metatype and metatype["metatype"] not in req["metatypes_any"]:
                errors.append(
                    f"Prerequisite failed for '{mod['name']}': requires metatype in {req['metatypes_any']} "
                    f"(character is {metatype['metatype']})."
                )
            if "exclude_formative_years" in req and formative and formative["name"] in req["exclude_formative_years"]:
                errors.append(
                    f"Prerequisite failed for '{mod['name']}': cannot be taken with Formative Years '{formative['name']}'."
                )
            if "further_education_vocation_any" in req and not (fe_vocations & set(req["further_education_vocation_any"])):
                errors.append(
                    f"Prerequisite failed for '{mod['name']}': requires Further Education vocation in "
                    f"{req['further_education_vocation_any']}."
                )
            if "prior_real_life_categories_any" in req and st == "real_life":
                idx = rl_modules.index(mod)
                prior_cats = set(rl_categories[:idx])
                if not (prior_cats & set(req["prior_real_life_categories_any"])):
                    errors.append(
                        f"Prerequisite failed for '{mod['name']}': must first complete a Real Life module in "
                        f"{req['prior_real_life_categories_any']}."
                    )

        post = mod.get("post_requires")
        if post and "real_life_categories_any" in post:
            if not (set(rl_categories) & set(post["real_life_categories_any"])):
                # Only hard error if Real Life stage has already been entered or build is marked finalized
                msg = f"Post-requisite for '{mod['name']}': {post.get('description', 'missing required Real Life module')}"
                if rl_modules or build.get("finalized"):
                    errors.append(msg)
                else:
                    warnings.append(f"[Upcoming] {msg}")

        if mod.get("note"):
            notes.append({"module": mod["name"], "note": mod["note"]})
        if mod.get("choices") and mod["name"].lower() not in resolved_choices_by_mod:
            pending_choices.append({"module": mod["name"], "choices": mod["choices"]})

    # 7. Aggregate Module Totals
    module_karma = (metatype["cost"] if metatype else 0) + awakened_cost
    for _, mod in selected_modules:
        module_karma += mod.get("cost") or 0

    base_attributes = dict(metatype["attributes"]) if metatype else {}
    mod_attributes = Counter()
    attr_max = {k: v + 5 for k, v in base_attributes.items() if k not in ("EDGE", "INI")}
    if "EDGE" in base_attributes:
        attr_max["EDGE"] = base_attributes["EDGE"] + 5
    if awakened:
        base_attributes["MAG/RES"] = base_attributes.get("MAG/RES", 1)
        attr_max["MAG/RES"] = 6

    skill_groups = Counter()
    active_skills = Counter()
    specializations = {}
    knowledge_skills = Counter()
    unresolved_placeholders = []

    pos_qualities = []
    neg_qualities = []
    pos_mod_karma = 0
    neg_mod_karma = 0
    best_sinner = None

    # Build lookup for resolved placeholders: (module_lower, placeholder_lower) -> list of resolutions
    res_ph_map = {}
    for rp in build.get("resolved_placeholders", []):
        key = (rp.get("module", "").lower(), rp.get("placeholder", "").lower())
        res_ph_map.setdefault(key, []).append(rp)

    for _, mod in selected_modules:
        for attr, val in mod.get("attributes", {}).items():
            mod_attributes[attr] += val

        for sg, val in mod.get("skill_groups", {}).items():
            skill_groups[sg] += val
            for member in skill_groups_map.get(sg, []):
                active_skills[member] += val

        for sk, val in mod.get("active_skills", {}).items():
            active_skills[sk] += val

        for sk, spec in mod.get("skill_specializations", {}).items():
            specializations.setdefault(sk, []).append(f"{spec} ({mod['name']})")

        for ks in mod.get("knowledge_skills", []):
            kname = ks["name"]
            key = (mod["name"].lower(), kname.lower())
            if key in res_ph_map and res_ph_map[key]:
                chosen_entry = res_ph_map[key].pop(0)
                if "split" in chosen_entry and isinstance(chosen_entry["split"], dict):
                    for sp_name, sp_ranks in chosen_entry["split"].items():
                        knowledge_skills[sp_name] += sp_ranks
                else:
                    chosen_name = chosen_entry["chosen"]
                    knowledge_skills[chosen_name] += chosen_entry.get("ranks", ks["ranks"])
            elif ks.get("is_placeholder"):
                if nationality and mod["name"] == nationality["name"] and kname == "[Language]" and build.get("secondary_language"):
                    knowledge_skills[build["secondary_language"]] += ks["ranks"]
                else:
                    unresolved_placeholders.append({
                        "module": mod["name"],
                        "placeholder": kname,
                        "description": ks.get("placeholder_description"),
                        "ranks": ks["ranks"],
                        "options": ks.get("options"),
                    })
            else:
                knowledge_skills[kname] += ks["ranks"]

        quals = mod.get("qualities", {})
        sinner = quals.get("sinner")
        if sinner:
            s_val = sinner.get("karma_value") or 0
            if best_sinner is None or s_val > (best_sinner.get("karma_value") or 0):
                best_sinner = sinner
        pos_mod_karma += quals.get("positive_total") or 0
        neg_mod_karma += quals.get("negative_total") or 0
        pos_qualities.extend(quals.get("positive", []))
        neg_qualities.extend(quals.get("negative", []))

    # 8. Apply resolved module choices (Regular Job, Postgraduate Studies, Celebrity, Drifter, etc.)
    choice_contacts = []
    for rc in build.get("resolved_choices", []):
        mname = rc.get("module", "")
        for attr, val in rc.get("attributes", {}).items():
            mod_attributes[attr] += val
        for sg, val in rc.get("skill_groups", {}).items():
            skill_groups[sg] += val
            for member in skill_groups_map.get(sg, []):
                active_skills[member] += val
        for sk, val in rc.get("active_skills", {}).items():
            active_skills[sk] += val
        for sk, spec in rc.get("specializations", {}).items():
            specializations.setdefault(sk, []).append(f"{spec} ({mname})")
        for ks, val in rc.get("knowledge_skills", {}).items():
            knowledge_skills[ks] += val
        for ct in rc.get("contacts", []):
            choice_contacts.append({**ct, "free": True, "source": mname})

    # Post-module baseline attributes
    post_mod_attributes = {}
    for k in sorted(set(base_attributes.keys()) | set(mod_attributes.keys())):
        post_mod_attributes[k] = base_attributes.get(k, 0) + mod_attributes.get(k, 0)

    # 9. Apply post-module Karma raises (Attributes, Active Skills, Specializations, Knowledge Skills)
    attr_raises = build.get("attribute_raises", {})
    attr_raise_karma = 0
    final_attributes = dict(post_mod_attributes)
    for attr, delta in attr_raises.items():
        if delta > 0:
            start = final_attributes.get(attr, 1)
            attr_raise_karma += triangular_raise_cost(start, delta, 5)
            final_attributes[attr] = start + delta

    active_cap = rules["skills"]["active_skill_cap"]
    skill_to_group = {}
    for sg_name, members in skill_groups_map.items():
        for m in members:
            skill_to_group[m] = sg_name

    # Apply explicit skill_rollovers from build JSON first
    skill_rollovers_applied = []
    for sr in build.get("skill_rollovers", []):
        src_sk = sr.get("from")
        dst_sk = sr.get("to")
        r_pts = int(sr.get("ranks", 0) or 0)
        if src_sk and dst_sk and r_pts > 0 and active_skills.get(src_sk, 0) > active_cap:
            actual_move = min(r_pts, active_skills[src_sk] - active_cap)
            if actual_move > 0:
                src_grp = skill_to_group.get(src_sk)
                valid_group_targets = [
                    m for m in skill_groups_map.get(src_grp, []) if m != src_sk and active_skills.get(m, 0) < active_cap
                ] if src_grp else []
                if valid_group_targets and dst_sk not in skill_groups_map.get(src_grp, []):
                    errors.append(
                        f"Skill rollover from '{src_sk}' to '{dst_sk}' is invalid: '{src_sk}' belongs to skill group '{src_grp}', "
                        f"so excess ranks must roll over into {valid_group_targets}."
                    )
                elif not valid_group_targets and skill_attrs.get(src_sk) != skill_attrs.get(dst_sk):
                    errors.append(
                        f"Skill rollover from '{src_sk}' ({skill_attrs.get(src_sk)}) to '{dst_sk}' ({skill_attrs.get(dst_sk)}) is invalid: "
                        f"must share the same linked attribute ({skill_attrs.get(src_sk)})."
                    )
                active_skills[src_sk] -= actual_move
                active_skills[dst_sk] += actual_move
                skill_rollovers_applied.append({
                    "from": src_sk,
                    "to": dst_sk,
                    "ranks": actual_move,
                    "mode": "manual",
                })

    # Automatically roll over any remaining module active skills > active_cap (7)
    for sk in sorted(list(active_skills.keys())):
        while active_skills[sk] > active_cap:
            src_grp = skill_to_group.get(sk)
            group_candidates = [
                m for m in skill_groups_map.get(src_grp, []) if m != sk and active_skills.get(m, 0) < active_cap
            ] if src_grp else []
            if group_candidates:
                # Pick group member with lowest current rank (or core skill preference)
                group_candidates.sort(key=lambda m: (m not in core_skills, active_skills.get(m, 0), m))
                target = group_candidates[0]
                reason = f"same skill group ({src_grp})"
            else:
                linked_a = skill_attrs.get(sk, "INT")
                attr_candidates = [
                    m for m, a in skill_attrs.items() if a == linked_a and m != sk and active_skills.get(m, 0) < active_cap
                ]
                if not attr_candidates:
                    break
                attr_candidates.sort(key=lambda m: (m not in core_skills, -active_skills.get(m, 0), m))
                target = attr_candidates[0]
                reason = f"same linked attribute ({linked_a})"
            active_skills[sk] -= 1
            active_skills[target] += 1
            skill_rollovers_applied.append({
                "from": sk,
                "to": target,
                "ranks": 1,
                "mode": f"auto ({reason})",
            })
            notes.append({
                "module": "Skill Cap Rollover",
                "note": f"'{sk}' exceeded cap {active_cap} -> rolled +1 rank into '{target}' ({reason}; override via 'skill_rollovers' in JSON).",
            })

    active_raises = build.get("active_skill_raises", {})
    active_raise_karma = 0
    final_active_skills = Counter(active_skills)
    for sk, delta in active_raises.items():
        if delta > 0:
            start = final_active_skills.get(sk, 0)
            active_raise_karma += triangular_raise_cost(start, delta, 2)
            final_active_skills[sk] = start + delta

    manual_specs = build.get("specializations", {})
    spec_karma = 0
    for sk, sp_list in manual_specs.items():
        if isinstance(sp_list, str):
            sp_list = [sp_list]
        for sp in sp_list:
            specializations.setdefault(sk, []).append(sp)
            spec_karma += rules["skills"]["specialization_cost"]

    # Free knowledge points = (final INT + final LOG) * 2
    free_ks_points = (final_attributes.get("INT", 1) + final_attributes.get("LOG", 1)) * 2
    ks_raises = build.get("knowledge_skill_raises", {})
    ks_free_used = 0
    ks_raise_karma = 0
    final_knowledge_skills = Counter(knowledge_skills)
    # Apply free points first (greedy: highest-rank raises benefit most from free 1-pt-per-rank)
    ks_steps = []
    for ks_name, delta in ks_raises.items():
        start = final_knowledge_skills.get(ks_name, 0)
        for step in range(1, delta + 1):
            ks_steps.append((start + step, ks_name))
        final_knowledge_skills[ks_name] = start + delta
    # Sort descending by new rating so free points cover the most expensive ranks first
    for new_rating, _ in sorted(ks_steps, reverse=True):
        if ks_free_used < free_ks_points:
            ks_free_used += 1
        else:
            ks_raise_karma += new_rating * 1

    # Track Primary & Secondary Languages from Nationality (and Bilingual quality)
    primary_lang_opts = nationality.get("primary_language_options", []) if nationality else []
    secondary_lang_opts = nationality.get("secondary_language_options", []) if nationality else []
    chosen_primary_lang = build.get("primary_language")
    if not chosen_primary_lang and len(primary_lang_opts) == 1:
        chosen_primary_lang = primary_lang_opts[0]

    chosen_secondary_lang = build.get("secondary_language")
    if not chosen_secondary_lang:
        if len(secondary_lang_opts) == 1:
            chosen_secondary_lang = secondary_lang_opts[0]
        else:
            # Check if resolved via nationality [Language] placeholder
            for rp in build.get("resolved_placeholders", []):
                if nationality and rp.get("module", "").lower() == nationality["name"].lower() and rp.get("placeholder", "").lower() == "[language]":
                    chosen_secondary_lang = rp.get("chosen")
                    break

    secondary_lang_ranks = 0
    if chosen_secondary_lang and chosen_secondary_lang in final_knowledge_skills:
        secondary_lang_ranks = final_knowledge_skills[chosen_secondary_lang]
    elif nationality:
        for ks in nationality.get("knowledge_skills", []):
            if ks["name"] == "[Language]" or (chosen_secondary_lang and ks["name"].lower() == chosen_secondary_lang.lower()):
                secondary_lang_ranks = ks["ranks"]
                break

    has_bilingual = any("bilingual" in q.lower() for q in (list(pos_qualities) + [mq.get("name", "") for mq in build.get("manual_positive_qualities", [])]))
    bilingual_lang = build.get("bilingual_language")
    sinner_karma = best_sinner["karma_value"] if best_sinner else 0
    total_neg_mod_karma = neg_mod_karma + sinner_karma

    manual_pos_list = build.get("manual_positive_qualities", [])
    manual_pos_karma_total = 0
    manual_pos_counted_toward_cap = 0
    for q in manual_pos_list:
        k = q.get("karma", 0)
        manual_pos_karma_total += k
        if not q.get("is_mastery") and not q.get("from_tradition"):
            manual_pos_counted_toward_cap += k
    if manual_pos_counted_toward_cap > rules["qualities"]["positive_karma_limit"]:
        errors.append(
            f"Manual non-Mastery/non-Tradition positive qualities ({manual_pos_counted_toward_cap} Karma) "
            f"exceed the {rules['qualities']['positive_karma_limit']} Karma limit."
        )

    manual_neg_allowance = max(0, rules["qualities"]["negative_karma_limit"] - total_neg_mod_karma)
    manual_neg_list = build.get("manual_negative_qualities", [])
    manual_neg_karma_gain = 0
    manual_neg_counted = 0
    for q in manual_neg_list:
        k = q.get("karma", 0)
        manual_neg_karma_gain += k
        if not q.get("from_tradition"):
            manual_neg_counted += k
    if manual_neg_counted > manual_neg_allowance:
        errors.append(
            f"Manual negative qualities ({manual_neg_counted} Karma) exceed remaining negative quality allowance "
            f"({manual_neg_allowance} Karma; module negative qualities already total {total_neg_mod_karma} Karma)."
        )

    buyoffs = build.get("negative_quality_buyoffs", [])
    buyoff_karma = sum(b.get("karma", 0) for b in buyoffs)
    bought_off_names = {b["name"].lower() for b in buyoffs if b.get("name")}
    active_mod_neg_qualities = [q for q in neg_qualities if q.lower() not in bought_off_names]

    # Check duplicate module qualities (unless replaced)
    replaced_names = {r["replaced"].lower() for r in build.get("duplicate_quality_replacements", []) if r.get("replaced")}
    dup_pos = [q for q, cnt in Counter(pos_qualities).items() if cnt > 1 and q.lower() not in replaced_names]
    dup_neg = [q for q, cnt in Counter(active_mod_neg_qualities).items() if cnt > 1 and q.lower() not in replaced_names]
    if dup_pos:
        warnings.append(
            f"Duplicate positive qualities from modules ({dup_pos}): if unable to advance tier, replace with another quality of the same Karma cost."
        )
    if dup_neg:
        warnings.append(
            f"Duplicate negative qualities from modules ({dup_neg}): if unable to advance tier, replace with another quality of the same Karma cost (or buy off)."
        )

    # 11. Spells, Complex Forms, Contacts, Nuyen
    spells = build.get("spells", [])
    complex_forms = build.get("complex_forms", [])
    magic_purchase_karma = (len(spells) + len(complex_forms)) * 5

    # Gather all active qualities (from modules + manual) to detect contact-modifying qualities
    all_active_pos_qualities = list(pos_qualities) + [q.get("name", "") for q in manual_pos_list if q.get("name")]
    all_active_neg_qualities = list(active_mod_neg_qualities) + [q.get("name", "") for q in manual_neg_list if q.get("name")]
    all_active_qualities = all_active_pos_qualities + all_active_neg_qualities
    active_qual_lower = [q.lower() for q in all_active_qualities]

    cha_final = final_attributes.get("CHA", 1)
    contact_rules = rules.get("contacts", {})
    quality_effects_map = contact_rules.get("quality_effects", {})

    # Base pool + extra pools + bonus contact points
    base_free_contact_karma = cha_final * 3
    extra_contact_points = int(build.get("extra_contact_points", 0) or 0)
    contact_notes = list(build.get("contact_notes", []))
    contact_cost_delta = 0
    contact_min_cost = 2  # Default minimum Contact cost (Conn 1 + Loy 1 = 2)

    contact_pools = {
        "standard": {
            "id": "standard",
            "label": "Standard Contact Pool (CHA × 3)",
            "capacity": base_free_contact_karma + extra_contact_points,
            "base_from_cha": base_free_contact_karma,
            "bonus_points": extra_contact_points,
            "spent": 0,
            "remaining": base_free_contact_karma + extra_contact_points,
            "overflow_karma": 0,
            "allows_karma_overflow": True,
        }
    }

    # Check quality effects from rules.json
    quality_granted_contacts = []
    global_loyalty_bonus = 0
    global_loyalty_source = None
    has_ex_con = False
    ex_con_min_map = {}
    code_of_honor_broken = bool(build.get("code_of_honor_broken", False))

    for q_key, q_eff in quality_effects_map.items():
        if any(q_key.lower() in aql for aql in active_qual_lower):
            if q_eff.get("note"):
                contact_notes.append(f"**{q_key}**: {q_eff['note']}")
            if "requires_negative_quality_substring" in q_eff:
                req_neg = q_eff["requires_negative_quality_substring"].lower()
                if not any(req_neg in nq.lower() for nq in all_active_neg_qualities):
                    errors.append(
                        f"Quality '{q_key}' requires a '{q_eff['requires_negative_quality_substring']}' negative quality."
                    )
            if "global_loyalty_modifier_when_upheld" in q_eff:
                if code_of_honor_broken:
                    global_loyalty_bonus += int(q_eff.get("global_loyalty_modifier_when_broken", -1))
                    global_loyalty_source = f"{q_key} (Code of Honor broken: -1 Loyalty)"
                else:
                    global_loyalty_bonus += int(q_eff["global_loyalty_modifier_when_upheld"])
                    global_loyalty_source = f"{q_key} (Code of Honor upheld: +2 Loyalty)"
            if "min_loyalty_by_archetype" in q_eff:
                has_ex_con = True
                ex_con_min_map = {k.lower(): v for k, v in q_eff["min_loyalty_by_archetype"].items()}
            if "cost_delta_per_contact" in q_eff:
                contact_cost_delta += q_eff["cost_delta_per_contact"]
                contact_min_cost = min(contact_min_cost, q_eff.get("min_cost_per_contact", 1))
            if "extra_pool" in q_eff:
                ep = q_eff["extra_pool"]
                cap = cha_final * 4 if ep.get("formula") == "CHA * 4" else int(ep.get("points", 0))
                pid = ep["id"]
                contact_pools[pid] = {
                    "id": pid,
                    "label": ep.get("label", q_key),
                    "source": q_key,
                    "capacity": cap,
                    "spent": 0,
                    "remaining": cap,
                    "overflow_karma": 0,
                    "min_connection": ep.get("min_connection"),
                    "max_connection": ep.get("max_connection"),
                    "allows_karma_overflow": not ep.get("no_karma_overflow", False),
                }
            if "granted_contact" in q_eff:
                gc = dict(q_eff["granted_contact"])
                gc["source"] = q_key
                quality_granted_contacts.append(gc)

    # Check if Mr. Johnson module was selected without resolved_choices contacts yet
    for _, mod in selected_modules:
        if mod["name"] == "Mr. Johnson":
            contact_notes.append(
                "**Mr. Johnson (Life Module)**: Grants 3 free Contacts, each with 7 points to spend between Connection and Loyalty."
            )
        if any("dealer connection" in pq.lower() for pq in mod.get("qualities", {}).get("positive", [])):
            contact_notes.append(
                f"**Dealer Connection ({mod['name']})**: -10% cost and +2 Availability dice for chosen vehicle/drone category; doubles as a vehicle/drone dealer network."
            )

    # Custom extra contact pools from build JSON
    for cep in build.get("extra_contact_pools", []):
        pid = cep.get("id") or cep.get("name", "custom").lower().replace(" ", "_")
        cap = int(cep.get("points", 0))
        contact_pools[pid] = {
            "id": pid,
            "label": cep.get("label") or cep.get("name", pid),
            "source": cep.get("source", "Custom"),
            "capacity": cap,
            "spent": 0,
            "remaining": cap,
            "overflow_karma": 0,
            "min_connection": cep.get("min_connection"),
            "max_connection": cep.get("max_connection"),
            "allows_karma_overflow": cep.get("allows_karma_overflow", False),
        }

    # Global or quality-driven contact loyalty/connection modifiers from build JSON
    loyalty_modifiers = list(build.get("contact_loyalty_modifiers", []))
    for lm in loyalty_modifiers:
        if isinstance(lm, dict):
            contact_notes.append(
                f"**{lm.get('source', 'Modifier')}**: {lm.get('effect', '')} ({lm.get('condition', 'all contacts')})"
            )
        elif isinstance(lm, str):
            contact_notes.append(lm)

    # Merge quality-granted contacts (unless user already defined an overriding contact with same name/source)
    user_contacts = list(choice_contacts) + list(build.get("contacts", []))
    existing_contact_names = {c.get("name", "").lower() for c in user_contacts}
    all_contacts_raw = [
        gc for gc in quality_granted_contacts if gc["name"].lower() not in existing_contact_names
    ] + user_contacts

    has_fihp = "high_places" in contact_pools
    max_single_pts = contact_rules.get("chargen_max_single_contact_points", 7)
    max_conn_std = contact_rules.get("chargen_max_connection", 6)
    max_loy_std = contact_rules.get("chargen_max_loyalty", 6)

    evaluated_contacts = []
    for c in all_contacts_raw:
        cname = c.get("name") or "Unnamed Contact"
        archetype = c.get("archetype") or c.get("type") or ""
        conn = int(c.get("connection", 1))
        loy = int(c.get("loyalty", 1))
        conn_mod = int(c.get("connection_modifier", 0) or 0)
        loy_mod = int(c.get("loyalty_modifier", 0) or 0)
        forced_loy = c.get("forced_loyalty")
        eff_conn = conn + conn_mod
        base_eff_loy = forced_loy if forced_loy is not None else (loy + loy_mod)
        eff_loy = max(1, base_eff_loy + global_loyalty_bonus)
        is_free = bool(c.get("free", False))
        is_group = bool(c.get("is_group", False))
        c_notes = list(c.get("notes", [])) if isinstance(c.get("notes"), list) else ([c["notes"]] if c.get("notes") else [])
        if c.get("blackmail") or c.get("chip_leverage"):
            c_notes.append("Blackmail/Chip leverage (+2 Loyalty for coerced favors; cannot voluntarily betray)")
        if forced_loy is not None and forced_loy != loy:
            c_notes.append(f"Effective Loyalty {forced_loy} via {c.get('source', 'quality')}")
        if global_loyalty_bonus != 0 and global_loyalty_source:
            c_notes.append(global_loyalty_source)

        # Ex-Con minimum Loyalty check for Corporate (4+) and Law Enforcement (5+) contacts
        if has_ex_con:
            arch_blob = f"{cname} {archetype} {c.get('faction', '')}".lower()
            if c.get("is_law_enforcement") or any(k in arch_blob for k in ("law enforcement", "police", "lone star", "knight errant", "detective", "cop")):
                if loy < 5:
                    errors.append(
                        f"Ex-Con restriction: Law Enforcement contact '{cname}' ({archetype or 'Law Enforcement'}) requires Loyalty 5 or 6 (got Loyalty {loy})."
                    )
            elif c.get("is_corporate") or any(k in arch_blob for k in ("corporate", "corp", "mr. johnson")):
                if loy < 4:
                    errors.append(
                        f"Ex-Con restriction: Corporate contact '{cname}' ({archetype or 'Corporate'}) requires Loyalty 4+ (got Loyalty {loy})."
                    )

        # Determine which pool this contact draws from
        pool_id = c.get("pool")
        if not pool_id:
            if has_fihp and conn >= 8:
                pool_id = "high_places"
            else:
                pool_id = "standard"
        if pool_id not in contact_pools:
            warnings.append(f"Contact '{cname}' references unknown pool '{pool_id}'; defaulting to 'standard'.")
            pool_id = "standard"

        raw_pts = conn + loy
        if is_free:
            eff_cost = 0
        else:
            eff_cost = max(contact_min_cost, raw_pts + contact_cost_delta)
            contact_pools[pool_id]["spent"] += eff_cost

        # Chargen cap validation for non-free contacts
        if not is_free:
            if pool_id == "high_places":
                if conn < 8 or conn > 12:
                    errors.append(
                        f"Contact '{cname}' in Friends in High Places pool must have Connection 8–12 (got Connection {conn})."
                    )
                if loy < 1 or loy > max_loy_std:
                    warnings.append(
                        f"Contact '{cname}' Loyalty ({loy}) exceeds standard chargen maximum ({max_loy_std})."
                    )
            else:
                if conn > max_conn_std:
                    warnings.append(
                        f"Contact '{cname}' Connection ({conn}) exceeds standard chargen max ({max_conn_std})"
                        + (" — set pool='high_places' and Connection 8–12 to use Friends in High Places." if has_fihp else " (requires Friends in High Places for Connection 8–12).")
                    )
                if loy > max_loy_std:
                    warnings.append(
                        f"Contact '{cname}' Loyalty ({loy}) exceeds standard chargen max ({max_loy_std})."
                    )
                if raw_pts > max_single_pts:
                    warnings.append(
                        f"Contact '{cname}' total Connection + Loyalty ({raw_pts}) exceeds standard single-contact chargen cap ({max_single_pts} points)."
                    )

        evaluated_contacts.append({
            "name": cname,
            "archetype": archetype,
            "connection": conn,
            "effective_connection": eff_conn,
            "loyalty": loy,
            "effective_loyalty": eff_loy,
            "raw_points": raw_pts,
            "effective_cost": eff_cost,
            "pool": pool_id,
            "free": is_free,
            "is_group": is_group,
            "source": c.get("source"),
            "notes": c_notes,
        })

    # Compute remaining & overflow across pools
    contact_karma_overflow = 0
    for pid, pinfo in contact_pools.items():
        rem = pinfo["capacity"] - pinfo["spent"]
        if rem >= 0:
            pinfo["remaining"] = rem
            pinfo["overflow_karma"] = 0
        else:
            pinfo["remaining"] = 0
            overflow = -rem
            pinfo["overflow_karma"] = overflow
            if pinfo.get("allows_karma_overflow", True):
                contact_karma_overflow += overflow
            else:
                errors.append(
                    f"Contact pool '{pinfo['label']}' exceeded by {overflow} points ({pinfo['spent']}/{pinfo['capacity']}), "
                    "and this pool does not allow spending general Karma on overflow."
                )

    free_contact_karma = contact_pools["standard"]["capacity"]
    contact_points_paid = contact_pools["standard"]["spent"]

    karma_for_nuyen = build.get("karma_for_nuyen", 0)
    if karma_for_nuyen > rules["karma_to_nuyen"]["max_karma"]:
        errors.append(
            f"karma_for_nuyen ({karma_for_nuyen}) exceeds maximum allowed ({rules['karma_to_nuyen']['max_karma']})."
        )
    starting_nuyen = karma_for_nuyen * rules["karma_to_nuyen"]["nuyen_per_karma"]

    # Total Karma accounting
    total_karma_spent = (
        module_karma
        + attr_raise_karma
        + active_raise_karma
        + spec_karma
        + ks_raise_karma
        + manual_pos_karma_total
        - manual_neg_karma_gain
        + buyoff_karma
        + magic_purchase_karma
        + contact_karma_overflow
        + karma_for_nuyen
    )
    starting_karma = rules["starting_karma"]
    remaining_karma = starting_karma - total_karma_spent
    if remaining_karma < 0:
        errors.append(f"Over Karma budget by {-remaining_karma} Karma ({total_karma_spent}/{starting_karma}).")

    # 12. Check Caps
    for attr, val in final_attributes.items():
        if attr in attr_max and val > attr_max[attr]:
            warnings.append(f"Attribute {attr}={val} exceeds metatype natural max ({attr_max[attr]}).")

    active_cap = rules["skills"]["active_skill_cap"]
    for sk, val in final_active_skills.items():
        if val > active_cap:
            warnings.append(f"Active skill '{sk}'={val} exceeds Life Modules chargen cap ({active_cap}).")

    ks_cap = rules["skills"]["knowledge_skill_cap"]
    for ks, val in final_knowledge_skills.items():
        if val > ks_cap:
            warnings.append(f"Knowledge skill '{ks}'={val} exceeds Life Modules chargen cap ({ks_cap}).")

    # 13. Compute Dice Pools for every Active Skill
    active_skill_details = {}
    for sk, rating in sorted(final_active_skills.items()):
        linked = skill_attrs.get(sk, "INT")
        attr_val = final_attributes.get(linked, 1)
        pool = attr_val + rating
        specs = specializations.get(sk, [])
        active_skill_details[sk] = {
            "linked_attribute": linked,
            "rating": rating,
            "dice_pool": pool,
            "specializations": specs,
            "spec_dice_pool": pool + 2 if specs else None,
        }

    # 14. Core Skill Readiness & Story vs Munchkin Advisory
    core_skill_targets = {k: int(v) for k, v in (build.get("core_skill_targets") or {}).items()}
    core_skill_report = []
    total_karma_needed_for_12 = 0
    for sk in core_skills:
        target_pool = core_skill_targets.get(sk, 12)
        linked = skill_attrs.get(sk, "INT")
        cur_attr = final_attributes.get(linked, 1)
        max_a = attr_max.get(linked, 6)
        cur_sk = final_active_skills.get(sk, 0)
        specs = specializations.get(sk, [])
        cur_pool = cur_attr + cur_sk
        effective_pool = cur_pool + (2 if specs else 0)
        needed_k = min_karma_to_reach_pool(cur_attr, max_a, cur_sk, active_cap, target_pool, bool(specs))
        if needed_k is not None:
            total_karma_needed_for_12 += needed_k
        core_skill_report.append({
            "skill": sk,
            "linked_attribute": linked,
            "rating": cur_sk,
            "dice_pool": cur_pool,
            "spec_dice_pool": cur_pool + 2 if specs else None,
            "target_pool": target_pool,
            "meets_12": effective_pool >= target_pool,
            "min_karma_to_12": needed_k,
        })

    if core_skills:
        below_12 = [c for c in core_skill_report if not c["meets_12"]]
        if playstyle == "story":
            # In story mode, ONLY advise when core skills are estimated < target at end of chargen
            if build.get("finalized") or remaining_karma < total_karma_needed_for_12:
                for c in below_12:
                    t_p = c.get("target_pool", 12)
                    if build.get("finalized"):
                        advisories.append(
                            f"[Story Readiness] Core skill '{c['skill']}' finishes at {c['dice_pool']} dice "
                            f"(below the {t_p}-dice benchmark)."
                        )
                    elif c["min_karma_to_12"] is None or c["min_karma_to_12"] > remaining_karma:
                        advisories.append(
                            f"[Story Readiness] Core skill '{c['skill']}' is currently {c['dice_pool']} dice "
                            f"and cannot reach {t_p} with remaining {remaining_karma} Karma "
                            f"(needs at least {c['min_karma_to_12']} Karma)."
                        )
                if not build.get("finalized") and below_12 and total_karma_needed_for_12 > remaining_karma:
                    advisories.append(
                        f"[Story Readiness] Bringing all {len(below_12)} sub-target core skills to benchmark requires "
                        f"~{total_karma_needed_for_12} Karma total, but only {remaining_karma} Karma remains."
                    )
        else:
            # Munchkin mode: always report sub-target core skills and Karma needed
            for c in below_12:
                t_p = c.get("target_pool", 12)
                advisories.append(
                    f"[Optimization] Core skill '{c['skill']}': {c['dice_pool']} dice "
                    f"(min {c['min_karma_to_12']} Karma to reach {t_p})."
                )

    # 15. Age & Derived Stats (RAW SR5)
    age = 0
    if nationality or formative:
        age = 10
    if teen:
        age = 17
    fe_age_map = rules["age_progression"]["further_education_years_added"]
    for m in fe_modules:
        age += fe_age_map.get(m.get("category"), 4)
    age += len(rl_modules) * rules["age_progression"]["real_life_years_added_per_module"]

    bod = final_attributes.get("BOD", 1)
    rea = final_attributes.get("REA", 1)
    str_ = final_attributes.get("STR", 1)
    cha = final_attributes.get("CHA", 1)
    int_ = final_attributes.get("INT", 1)
    log = final_attributes.get("LOG", 1)
    wil = final_attributes.get("WIL", 1)
    essence = build.get("essence", 6.0)

    derived = {
        "age": age,
        "essence": essence,
        "initiative": f"{rea + int_} + 1d6",
        "free_knowledge_points": free_ks_points,
        "free_knowledge_points_used": ks_free_used,
        "free_contact_karma": free_contact_karma,
        "free_contact_karma_used": min(contact_points_paid, free_contact_karma),
        "physical_limit": math.ceil((str_ * 2 + bod + rea) / 3),
        "mental_limit": math.ceil((log * 2 + int_ + wil) / 3),
        "social_limit": math.ceil((cha * 2 + wil + math.ceil(essence)) / 3),
        "physical_condition_monitor": 8 + math.ceil(bod / 2),
        "stun_condition_monitor": 8 + math.ceil(wil / 2),
        "composure": cha + wil,
        "judge_intentions": cha + int_,
        "lifting_carrying": bod + str_,
        "memory": log + wil,
    }

    return {
        "character": {
            "name": build.get("name") or "Unnamed Runner",
            "concept": build.get("concept") or "",
            "playstyle": playstyle,
            "focus_areas": build.get("focus_areas", []),
            "metatype": metatype["name"] if metatype else None,
            "awakened_quality": awakened or "Mundane",
        },
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "advisories": advisories,
        "selected_modules": [{"stage": st, "name": m["name"], "cost": m.get("cost")} for st, m in selected_modules],
        "karma": {
            "budget": starting_karma,
            "spent_total": total_karma_spent,
            "remaining": remaining_karma,
            "breakdown": {
                "metatype_and_modules_and_awakened": module_karma,
                "attribute_raises": attr_raise_karma,
                "active_skill_raises": active_raise_karma,
                "specializations": spec_karma,
                "knowledge_skill_raises": ks_raise_karma,
                "manual_positive_qualities": manual_pos_karma_total,
                "manual_negative_qualities_gain": -manual_neg_karma_gain,
                "negative_quality_buyoffs": buyoff_karma,
                "spells_and_complex_forms": magic_purchase_karma,
                "contact_karma_overflow": contact_karma_overflow,
                "karma_for_nuyen": karma_for_nuyen,
            },
            "starting_nuyen": starting_nuyen,
        },
        "derived": derived,
        "attributes": {
            "base": base_attributes,
            "module_bonus": dict(mod_attributes),
            "raises": attr_raises,
            "final": final_attributes,
            "max": attr_max,
        },
        "qualities": {
            "sinner": best_sinner,
            "module_positive": pos_qualities,
            "module_positive_karma_exempt": pos_mod_karma,
            "manual_positive": manual_pos_list,
            "manual_positive_counted": manual_pos_counted_toward_cap,
            "manual_positive_cap": rules["qualities"]["positive_karma_limit"],
            "module_negative_active": active_mod_neg_qualities,
            "module_negative_karma_total": total_neg_mod_karma,
            "manual_negative": manual_neg_list,
            "manual_negative_allowance_remaining": max(0, manual_neg_allowance - manual_neg_counted),
            "negative_buyoffs": buyoffs,
        },
        "skill_groups": dict(sorted(skill_groups.items())),
        "active_skills": active_skill_details,
        "skill_rollovers": skill_rollovers_applied,
        "core_skill_readiness": core_skill_report,
        "languages": {
            "primary_language": chosen_primary_lang,
            "primary_language_options": primary_lang_opts,
            "secondary_language": chosen_secondary_lang,
            "secondary_language_ranks": secondary_lang_ranks,
            "secondary_language_options": secondary_lang_opts,
            "has_bilingual": has_bilingual,
            "bilingual_language": bilingual_lang,
        },
        "knowledge_skills": dict(sorted(final_knowledge_skills.items())),
        "unresolved_placeholders": unresolved_placeholders,
        "spells": spells,
        "complex_forms": complex_forms,
        "contacts": {
            "pools": list(contact_pools.values()),
            "total_free_points": sum(p["capacity"] for p in contact_pools.values()),
            "total_points_spent": sum(p["spent"] for p in contact_pools.values()),
            "total_unspent_points": sum(p["remaining"] for p in contact_pools.values()),
            "karma_overflow_spent": contact_karma_overflow,
            "cost_delta_per_contact": contact_cost_delta,
            "min_cost_per_contact": contact_min_cost,
            "list": evaluated_contacts,
            "modifiers_and_notes": contact_notes,
        },
        "module_notes": notes,
        "pending_choices": pending_choices,
    }


def render_markdown_sheet(report: dict) -> str:
    ch = report["character"]
    k = report["karma"]
    d = report["derived"]
    attrs = report["attributes"]
    quals = report["qualities"]

    lines = [
        f"# {ch['name']} — Shadowrun 5e Life Modules Sheet",
        "",
        f"- **Concept**: {ch['concept'] or '_TBD_'}",
        f"- **Metatype**: {ch['metatype'] or '_Unselected_'} | **Awakened/Emerged**: {ch['awakened_quality']} | **Age**: {d['age']} | **Essence**: {d['essence']}",
        f"- **Mode**: `{ch['playstyle']}` | **Focus Areas**: {', '.join(ch['focus_areas']) or '_None_'}",
        f"- **Karma**: **{k['spent_total']} / {k['budget']}** spent (**{k['remaining']} remaining**) | **Starting Nuyen**: {k['starting_nuyen']:,}¥ ({k['breakdown']['karma_for_nuyen']} Karma)",
        "",
    ]

    if report["errors"]:
        lines.append("## Validation Errors")
        for e in report["errors"]:
            lines.append(f"- **ERROR**: {e}")
        lines.append("")

    if report["warnings"]:
        lines.append("## Warnings")
        for w in report["warnings"]:
            lines.append(f"- **WARN**: {w}")
        lines.append("")

    if report["advisories"]:
        lines.append("## Core Skill Readiness & Advisories")
        for a in report["advisories"]:
            lines.append(f"- {a}")
        lines.append("")

    # Life Modules Timeline
    lines.append("## Life Modules Timeline")
    lines.append("| Stage | Module | Karma |")
    lines.append("| :--- | :--- | ---: |")
    for m in report["selected_modules"]:
        lines.append(f"| {m['stage']} | {m['name']} | {m['cost']} |")
    lines.append("")

    # Attributes
    lines.append("## Attributes")
    lines.append("| Attribute | Base | Modules | Raises | Final | Max |")
    lines.append("| :--- | ---: | ---: | ---: | ---: | ---: |")
    order = ["BOD", "AGI", "REA", "STR", "CHA", "INT", "LOG", "WIL", "EDGE", "MAG/RES"]
    for a in order:
        if a in attrs["final"]:
            lines.append(
                f"| **{a}** | {attrs['base'].get(a, 0)} | +{attrs['module_bonus'].get(a, 0)} | "
                f"+{attrs['raises'].get(a, 0)} | **{attrs['final'][a]}** | {attrs['max'].get(a, '-')} |"
            )
    lines.append("")

    # Derived Stats
    lines.append("## Derived Stats & Limits")
    lines.append(
        f"- **Initiative**: {d['initiative']} | **Physical Limit**: {d['physical_limit']} | "
        f"**Mental Limit**: {d['mental_limit']} | **Social Limit**: {d['social_limit']}"
    )
    lines.append(
        f"- **Condition Monitors**: Physical {d['physical_condition_monitor']} / Stun {d['stun_condition_monitor']}"
    )
    lines.append(
        f"- **Composure**: {d['composure']} | **Judge Intentions**: {d['judge_intentions']} | "
        f"**Lifting/Carrying**: {d['lifting_carrying']} | **Memory**: {d['memory']}"
    )
    lines.append(
        f"- **Free Knowledge Points**: {d['free_knowledge_points_used']} / {d['free_knowledge_points']} used | "
        f"**Free Contact Karma**: {d['free_contact_karma_used']} / {d['free_contact_karma']} used"
    )
    lines.append("")

    # Core Skills Readiness Table (if focus set)
    if report["core_skill_readiness"]:
        lines.append("## Core Skills (Target Benchmarks)")
        lines.append("| Core Skill | Linked Attr | Rating | Dice Pool | Target | Status |")
        lines.append("| :--- | :---: | ---: | ---: | ---: | :--- |")
        for c in report["core_skill_readiness"]:
            t_p = c.get("target_pool", 12)
            pool_str = f"{c['dice_pool']} ({c['spec_dice_pool']} spec)" if c["spec_dice_pool"] else str(c["dice_pool"])
            status = f"OK (>={t_p})" if c["meets_12"] else f"Needs {c['min_karma_to_12']} Karma for {t_p}"
            lines.append(f"| {c['skill']} | {c['linked_attribute']} | {c['rating']} | **{pool_str}** | {t_p} | {status} |")
        lines.append("")

    # Active Skills
    lines.append("## Active Skills & Dice Pools")
    lines.append("| Skill | Attr | Rating | Dice Pool | Specializations |")
    lines.append("| :--- | :---: | ---: | ---: | :--- |")
    for sk, info in report["active_skills"].items():
        pool_str = f"**{info['dice_pool']}**" + (f" ({info['spec_dice_pool']} spec)" if info["spec_dice_pool"] else "")
        specs = ", ".join(info["specializations"]) if info["specializations"] else "—"
        lines.append(f"| {sk} | {info['linked_attribute']} | {info['rating']} | {pool_str} | {specs} |")
    lines.append("")

    # Knowledge & Language Skills
    langs = report.get("languages", {})
    lines.append("## Knowledge & Language Skills")
    prim_lang = langs.get("primary_language")
    prim_opts = langs.get("primary_language_options") or []
    sec_lang = langs.get("secondary_language")
    sec_ranks = langs.get("secondary_language_ranks") or 0
    sec_opts = langs.get("secondary_language_options") or []
    if prim_lang:
        lines.append(f"- **Primary (Native) Language**: **{prim_lang}** (`N`)")
    elif prim_opts:
        lines.append(f"- **Primary (Native) Language**: _Unselected_ (`N` — Options: {', '.join(prim_opts)})")
    if langs.get("has_bilingual"):
        b_lang = langs.get("bilingual_language") or "_Choose 2nd Native Language_"
        lines.append(f"- **Second Native Language (Bilingual)**: **{b_lang}** (`N`)")
    if sec_lang:
        int_v = attrs["final"].get("INT", 1)
        log_v = attrs["final"].get("LOG", 1)
        lines.append(
            f"- **Secondary Language (Nationality)**: **{sec_lang}** (Rating {sec_ranks} — {int_v + sec_ranks}d INT / {log_v + sec_ranks}d LOG)"
        )
    elif sec_opts:
        lines.append(f"- **Secondary Language (Nationality)**: _Unselected_ (Rating {sec_ranks} — Options: {', '.join(sec_opts)})")
    if prim_lang or prim_opts or sec_lang or sec_opts or langs.get("has_bilingual"):
        lines.append("")

    if report["knowledge_skills"]:
        lines.append("| Knowledge / Language | Rating | Dice Pool (INT / LOG) |")
        lines.append("| :--- | ---: | :--- |")
        int_v = attrs["final"].get("INT", 1)
        log_v = attrs["final"].get("LOG", 1)
        for ks, r in report["knowledge_skills"].items():
            ks_clean = " ".join(ks.split())
            lines.append(f"| {ks_clean} | {r} | {int_v + r} (INT) / {log_v + r} (LOG) |")
    else:
        lines.append("_None resolved yet._")
    if report["unresolved_placeholders"]:
        lines.append("")
        lines.append("### Unresolved Placeholder Knowledge Skills")
        for ph in report["unresolved_placeholders"]:
            opts_str = f" _(Options: {', '.join(ph['options'])})_" if ph.get("options") else ""
            lines.append(f"- **{ph['placeholder']}** (Rating {ph['ranks']}){opts_str} — from _{ph['module']}_")
    lines.append("")

    # Qualities
    lines.append("## Qualities")
    if quals["sinner"]:
        lines.append(f"- **SINner (Active)**: {quals['sinner']['type']} ({quals['sinner']['karma_value']} Karma)")
    pos_all = quals["module_positive"] + [
        f"{q['name']} ({q['karma']}K{' [Mastery]' if q.get('is_mastery') else ''})" for q in quals["manual_positive"]
    ]
    neg_all = quals["module_negative_active"] + [
        f"{q['name']} ({q['karma']}K)" for q in quals["manual_negative"]
    ]
    lines.append(
        f"- **Positive**: {', '.join(pos_all) or 'None'} "
        f"_(Manual cap: {quals['manual_positive_counted']}/{quals['manual_positive_cap']} Karma; module/tradition/Mastery exempt)_"
    )
    lines.append(
        f"- **Negative**: {', '.join(neg_all) or 'None'} "
        f"_(Module negative total: {quals['module_negative_karma_total']}K; manual allowance remaining: {quals['manual_negative_allowance_remaining']}K)_"
    )
    if quals["negative_buyoffs"]:
        lines.append(
            "- **Bought-Off Negatives**: "
            + ", ".join(f"{b['name']} ({b['karma']}K)" for b in quals["negative_buyoffs"])
        )
    lines.append("")

    # Contacts Section (Always rendered)
    c_sec = report["contacts"]
    lines.append("## Contacts & Network")
    lines.append("### Contact Point Pools")
    lines.append("| Pool | Capacity | Spent | Unspent | Karma Overflow |")
    lines.append("| :--- | ---: | ---: | ---: | ---: |")
    for p in c_sec["pools"]:
        ov_str = f"{p['overflow_karma']} Karma" if p.get("allows_karma_overflow", True) else "N/A (Use-or-Lose)"
        lines.append(
            f"| **{p['label']}** | {p['capacity']} | {p['spent']} | **{p['remaining']}** | {ov_str} |"
        )
    if c_sec["cost_delta_per_contact"] != 0:
        lines.append(
            f"- **Contact Cost Modifier**: `{c_sec['cost_delta_per_contact']:+d}` point(s) per Contact "
            f"(minimum `{c_sec['min_cost_per_contact']}` pt/Contact)"
        )
    lines.append("")

    if c_sec["list"]:
        lines.append("### Current Contacts")
        lines.append("| Name | Archetype / Role | Conn | Loy | Cost / Pool | Notes |")
        lines.append("| :--- | :--- | :---: | :---: | :--- | :--- |")
        for c in c_sec["list"]:
            conn_str = (
                f"{c['connection']} ({c['effective_connection']} eff)"
                if c["effective_connection"] != c["connection"]
                else str(c["connection"])
            )
            loy_str = (
                f"{c['loyalty']} ({c['effective_loyalty']} eff)"
                if c["effective_loyalty"] != c["loyalty"]
                else str(c["loyalty"])
            )
            if c.get("free"):
                cost_str = f"0 (Free via {c.get('source') or 'Quality/Module'})"
            else:
                cost_str = f"{c['effective_cost']} pts (`{c['pool']}`)"
            grp_tag = ["Group Contact"] if c.get("is_group") else []
            note_str = "; ".join(grp_tag + (c.get("notes") or [])) or "—"
            lines.append(
                f"| **{c['name']}** | {c.get('archetype') or '—'} | {conn_str} | {loy_str} | {cost_str} | {note_str} |"
            )
    else:
        lines.append(f"_No contacts selected yet ({c_sec['total_unspent_points']} unspent contact points available)._")
    lines.append("")

    if c_sec["modifiers_and_notes"]:
        lines.append("### Contact & Loyalty Modifiers / Notes")
        for cn in c_sec["modifiers_and_notes"]:
            lines.append(f"- {cn}")
        lines.append("")

    if report["spells"] or report["complex_forms"]:
        lines.append("## Spells & Complex Forms")
        if report["spells"]:
            lines.append(f"- **Spells**: {', '.join(report['spells'])}")
        if report["complex_forms"]:
            lines.append(f"- **Complex Forms**: {', '.join(report['complex_forms'])}")
        lines.append("")

    if report["module_notes"] or report["pending_choices"]:
        lines.append("## Module Notes & Pending Choices")
        for n in report["module_notes"]:
            lines.append(f"- **{n['module']}**: {n['note']}")
        for pc in report["pending_choices"]:
            lines.append(f"- **PENDING CHOICE — {pc['module']}**: `{json.dumps(pc['choices'])}`")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def module_karma_value(mod: dict, skill_groups_map: dict, core_attrs: list[str], core_skills: list[str]) -> tuple[float, float]:
    """Return (raw_karma_equivalent, focus_weighted_score) for munchkin ranking."""
    # Approximate raw Karma value: Attr ~15K avg, Active skill ~4K avg, Group ~12K, PosQual 1:1
    raw_val = 0.0
    focus_val = 0.0
    for a, v in mod.get("attributes", {}).items():
        raw_val += v * 15
        if a in core_attrs:
            focus_val += v * 35
    expanded = Counter(mod.get("active_skills", {}))
    for sg, v in mod.get("skill_groups", {}).items():
        for m in skill_groups_map.get(sg, []):
            expanded[m] += v
    for sk, v in expanded.items():
        raw_val += v * 4
        if sk in core_skills:
            focus_val += v * 14
    pos_k = mod.get("qualities", {}).get("positive_total") or 0
    neg_k = mod.get("qualities", {}).get("negative_total") or 0
    raw_val += pos_k - (neg_k * 0.25)
    cost = max(1, mod.get("cost") or 1)
    return raw_val / cost, (focus_val + raw_val * 0.35) / cost


def cmd_recommend(args, data: dict) -> int:
    stage = STAGE_ALIASES.get(args.stage.lower())
    if not stage or stage == "metatypes":
        print("Specify a module stage: nationalities, formative_years, teen_years, further_education, real_life", file=sys.stderr)
        return 1

    build = json.loads(Path(args.build_file).read_text(encoding="utf-8")) if args.build_file else {}
    if args.focus:
        build["focus_areas"] = args.focus
    mode = (args.mode or build.get("playstyle") or "story").lower()
    core_attrs, core_skills = resolve_focus(build, data)
    theme = (args.theme or "").lower()

    # Determine current build state for legality filtering
    awakened = build.get("awakened_quality")
    meta = resolve_module(data, "metatypes", build["metatype"]) if build.get("metatype") else None
    formative_name = build.get("formative_years")
    fe_mods = [
        resolve_module(data, "further_education", x)
        for x in (build.get("further_education") or [])
    ]
    fe_mods = [m for m in fe_mods if m]
    fe_vocs = {m.get("vocation") for m in fe_mods if m.get("vocation")}
    rl_mods = [resolve_module(data, "real_life", x) for x in (build.get("real_life") or [])]
    rl_cats = {m.get("category") for m in rl_mods if m}

    candidates = []
    for mod in data["stages"][stage]["items"]:
        # Check prerequisites
        req = mod.get("requires") or {}
        if "qualities_any" in req and awakened not in req["qualities_any"]:
            continue
        if "metatypes_any" in req and meta and meta["metatype"] not in req["metatypes_any"]:
            continue
        if "exclude_formative_years" in req and formative_name in req["exclude_formative_years"]:
            continue
        if "further_education_vocation_any" in req and not (fe_vocs & set(req["further_education_vocation_any"])):
            continue
        if "prior_real_life_categories_any" in req and not (rl_cats & set(req["prior_real_life_categories_any"])):
            continue
        if stage == "further_education" and validate_further_education(fe_mods + [mod]):
            continue

        if theme:
            blob = json.dumps(mod, ensure_ascii=False).lower()
            if theme not in blob:
                continue

        eff, fscore = module_karma_value(mod, data["skill_groups"], core_attrs, core_skills)
        candidates.append((fscore, eff, mod))

    if mode == "munchkin":
        candidates.sort(key=lambda x: (x[0], x[1]), reverse=True)
    else:
        # Story mode: prioritize theme/focus fit gently without hyper-optimizing
        candidates.sort(key=lambda x: (x[0] > 0, x[0]), reverse=True)

    print(f"Top {min(args.limit, len(candidates))} legal '{stage}' recommendations (mode={mode}, focus={build.get('focus_areas', [])}):")
    for fscore, eff, mod in candidates[: args.limit]:
        attrs = ", ".join(f"{k}+{v}" for k, v in mod.get("attributes", {}).items())
        sk_hits = []
        expanded = Counter(mod.get("active_skills", {}))
        for sg, v in mod.get("skill_groups", {}).items():
            for m in data["skill_groups"].get(sg, []):
                expanded[m] += v
        for sk in core_skills:
            if expanded.get(sk):
                sk_hits.append(f"{sk}+{expanded[sk]}")
        extra = f" | Core: {', '.join(sk_hits)}" if sk_hits else ""
        note = f" | Note: {mod['note']}" if mod.get("note") else ""
        score_tag = f" [FocusScore={fscore:.2f}, RawEff={eff:.2f}]" if mode == "munchkin" else ""
        print(f"  - {mod['name']} ({mod.get('cost')}K) | {attrs}{extra}{score_tag}{note}")
    return 0


def cmd_search(args, data: dict) -> int:
    stages = (
        [STAGE_ALIASES[args.stage.lower()]]
        if args.stage and args.stage.lower() in STAGE_ALIASES
        else list(STAGE_FILES.keys())
    )
    if args.stage and args.stage.lower() not in STAGE_ALIASES:
        print(f"Unknown stage: {args.stage}. Valid: {', '.join(STAGE_FILES.keys())}", file=sys.stderr)
        return 1

    results = []
    q = (args.query or "").lower()
    attr_filter = args.attr.upper() if args.attr else None
    skill_filter = args.skill.lower() if args.skill else None
    qual_filter = args.quality.lower() if args.quality else None

    for st in stages:
        for item in data["stages"][st]["items"]:
            if q and q not in item["name"].lower() and q not in (item.get("note") or "").lower():
                continue
            if args.max_cost is not None and (item.get("cost") is None or item["cost"] > args.max_cost):
                continue
            if attr_filter and attr_filter not in item.get("attributes", {}):
                continue
            if skill_filter:
                all_sk = (
                    list(item.get("active_skills", {}).keys())
                    + list(item.get("skill_groups", {}).keys())
                    + [k["name"] for k in item.get("knowledge_skills", [])]
                )
                if not any(skill_filter in s.lower() for s in all_sk):
                    continue
            if qual_filter:
                quals = item.get("qualities", {})
                qlist = list(quals.get("positive", [])) + list(quals.get("negative", []))
                if quals.get("sinner"):
                    qlist.append(f"SINner ({quals['sinner'].get('type', '')})")
                if not any(qual_filter in x.lower() for x in qlist):
                    continue
            results.append({"stage": st, **item})

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return 0

    print(f"Found {len(results)} matching entries:")
    for r in results[: args.limit]:
        attrs = ", ".join(f"{k}+{v}" for k, v in r.get("attributes", {}).items())
        note_tag = " [NOTE]" if r.get("note") else ""
        req_tag = " [REQ]" if r.get("requires") or r.get("post_requires") else ""
        print(f"  [{r['stage']}] {r['name']} ({r.get('cost')} Karma) | {attrs}{note_tag}{req_tag}")
    if len(results) > args.limit:
        print(f"  ... ({len(results) - args.limit} more; use --limit or --json to see all)")
    return 0


def cmd_show(args, data: dict) -> int:
    stages = (
        [STAGE_ALIASES[args.stage.lower()]]
        if args.stage and args.stage.lower() in STAGE_ALIASES
        else list(STAGE_FILES.keys())
    )
    q = args.name.strip().lower()
    matches = []
    for st in stages:
        for item in data["stages"][st]["items"]:
            if item["name"].lower() == q:
                matches = [(st, item)]
                break
            if q in item["name"].lower():
                matches.append((st, item))
        if len(matches) == 1 and matches[0][1]["name"].lower() == q:
            break

    if not matches:
        print(f"No module found matching '{args.name}'.", file=sys.stderr)
        return 1
    if len(matches) > 1 and not args.all:
        print(f"Multiple matches for '{args.name}':")
        for st, item in matches[:15]:
            print(f"  [{st}] {item['name']} ({item.get('cost')} Karma)")
        print("Pass an exact name or --stage to narrow, or --all to dump all.")
        return 0

    out = [{"stage": st, **item} for st, item in matches]
    print(json.dumps(out[0] if len(out) == 1 else out, indent=2, ensure_ascii=False))
    return 0


def cmd_evaluate(args, data: dict) -> int:
    if args.build_file:
        build = json.loads(Path(args.build_file).read_text(encoding="utf-8"))
    else:
        build = {
            "name": args.name,
            "playstyle": args.mode,
            "focus_areas": args.focus or [],
            "metatype": args.metatype,
            "nationality": args.nationality,
            "formative_years": args.formative_years,
            "teen_years": args.teen_years,
            "further_education": args.further_education or [],
            "real_life": args.real_life or [],
            "awakened_quality": args.awakened,
            "karma_for_nuyen": args.nuyen_karma,
        }

    report = evaluate_build(build, data)

    if args.sheet_out:
        md = render_markdown_sheet(report)
        Path(args.sheet_out).write_bytes(md.encode("utf-8"))
        print(f"Wrote Markdown character sheet to {args.sheet_out}")

    if args.markdown:
        print(render_markdown_sheet(report))
    elif not args.sheet_out:
        print(json.dumps(report, indent=2, ensure_ascii=False))

    return 0 if report["valid"] else 2


def main():
    parser = argparse.ArgumentParser(description="Shadowrun 5e Life Modules Query, Builder & Validator")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_search = sub.add_parser("search", help="Search life modules across stages")
    p_search.add_argument("query", nargs="?", default="", help="Substring to match module name or note")
    p_search.add_argument("--stage", help="Stage filter")
    p_search.add_argument("--attr", help="Filter by attribute granted (e.g., BOD, LOG, CHA)")
    p_search.add_argument("--skill", help="Filter by active skill, skill group, or knowledge skill")
    p_search.add_argument("--quality", help="Filter by quality name")
    p_search.add_argument("--max-cost", type=int, help="Maximum Karma cost")
    p_search.add_argument("--limit", type=int, default=25, help="Max results to print in text mode")
    p_search.add_argument("--json", action="store_true", help="Output raw JSON")

    p_show = sub.add_parser("show", help="Show full details of a module")
    p_show.add_argument("name", help="Module name (exact or substring)")
    p_show.add_argument("--stage", help="Optional stage to narrow lookup")
    p_show.add_argument("--all", action="store_true", help="Dump all matches if multiple")

    p_rec = sub.add_parser("recommend", help="Recommend legal modules for the next stage (story or munchkin mode)")
    p_rec.add_argument("--stage", required=True, help="Target stage to recommend from")
    p_rec.add_argument("--build-file", help="Current in-progress character JSON")
    p_rec.add_argument("--focus", action="append", help="Focus preset (e.g. face, street_samurai, decker, mage, medic)")
    p_rec.add_argument("--mode", choices=["story", "munchkin"], help="Recommendation mode")
    p_rec.add_argument("--theme", help="Optional story keyword filter (e.g. corp, gang, magic, military)")
    p_rec.add_argument("--limit", type=int, default=10, help="Number of recommendations to display")

    p_eval = sub.add_parser("evaluate", help="Validate, price, and render a Life Modules character build")
    p_eval.add_argument("--build-file", help="Path to JSON build specification")
    p_eval.add_argument("--name", help="Character name")
    p_eval.add_argument("--mode", choices=["story", "munchkin"], default="story", help="Advisory mode")
    p_eval.add_argument("--focus", action="append", help="Focus preset (repeatable)")
    p_eval.add_argument("--metatype", help="Metatype name")
    p_eval.add_argument("--nationality", help="Nationality module name")
    p_eval.add_argument("--formative-years", help="Formative Years module name")
    p_eval.add_argument("--teen-years", help="Teen Years module name")
    p_eval.add_argument("--further-education", action="append", help="Further Education module name (repeatable)")
    p_eval.add_argument("--real-life", action="append", help="Real Life module name (repeatable, chronological)")
    p_eval.add_argument("--awakened", help="Awakened/Emerged quality")
    p_eval.add_argument("--nuyen-karma", type=int, default=0, help="Karma converted to Nuyen (max 200)")
    p_eval.add_argument("--markdown", action="store_true", help="Print running Markdown character sheet to stdout")
    p_eval.add_argument("--sheet-out", help="Write running Markdown character sheet to a .md file")

    args = parser.parse_args()
    data = load_all_data()

    if args.cmd == "search":
        sys.exit(cmd_search(args, data))
    elif args.cmd == "show":
        sys.exit(cmd_show(args, data))
    elif args.cmd == "recommend":
        sys.exit(cmd_recommend(args, data))
    elif args.cmd == "evaluate":
        sys.exit(cmd_evaluate(args, data))


if __name__ == "__main__":
    main()
