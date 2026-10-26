"""Patch USG 0.10 -> 0.11. Loads the previous version and changes only what the changelog lists.

Usage: python3 patch_0_11.py USG_v0_10.json USG_v0_11.json
Source: ADU inquiry 2026-10-12 (Q48-Q67). An AI produced floor plans and a site plan outside any defined limits
and against recorded answers (driveway on the wrong side, laundry moved, pedestrian access from the wrong side).
Author principle: the operating range is defined before any layout.
"""
import json, sys

src, dst = sys.argv[1], sys.argv[2]
U = json.load(open(src))
assert U["document"]["version"] == "0.10", "patch applies to 0.10 only"


def stage(sid):
    return next(s for s in U["pipeline"] if s["id"] == sid)


def question(qid):
    return next(q for q in stage(qid.split(".")[0])["questions"] if q["id"] == qid)


CHANGELOG = [
    "Added schemas.site_envelope: the sandbox in which a structure may be placed (boundary, setbacks, separations, protected zones, existing elements, orientation datum, access points, height limit). Every value carries a status: confirmed, assumed, exercise, range or undefined, with its source. S04.intervention_zone now outputs a site_envelope. (ADU inquiry Q48-Q67)",
    "Added execution_model.sandbox_rule: a geometric design hypothesis presupposes the site envelope and may be created only when every envelope value is defined (confirmed, assumed, exercise value or range). An undefined value forbids geometric layouts; concept and topological exploration stay free (0.8). A layout resting on the favourable end of a range says so. (author principle 2026-10-12: define the operating range before any layout)",
    "design_hypothesis gained 'level' (concept, topological, geometric), 'uses_answers' and 'deviations'. Added execution_model.consistency_rule: a geometric hypothesis cites the recorded answers it uses; any deviation from a recorded human answer is listed and stays a violation until the human resolves it (accepts the deviation, which revises the answer, or rejects it). (Zara's layouts contradicted Q9, Q33 and Q42)",
    "Added inquiry_model.sandbox_first: once a site survives S02, the inquiry asks the envelope values before any layout is proposed; undefined envelope values rank as show-stoppers for geometric work.",
    "Stress test layout_before_sandbox; invariant; open questions.",
]

# ------------------------------------------------------------------ document, changelog, history
prev_log = U.pop("changelog_from_0_9")
U["history"] = {"0.10": {"changelog": prev_log, "removed": U["changelog_removed"]}, **U["history"]}
U["document"]["version"] = "0.11"
U["document"]["supersedes"] = "0.10"
new = {}
for k, v in U.items():
    new[k] = v
    if k == "document":
        new["changelog_from_0_10"] = CHANGELOG
U = new
U["changelog_removed"] = []
O = U["ontology"]

# ------------------------------------------------------------------ site envelope
U["schemas"]["site_envelope"] = {
    "value_record": "{value | min, max, unit, status, source_ref}",
    "status_values": ["confirmed", "assumed", "exercise", "range", "undefined"],
    "status_meaning": {
        "confirmed": "established by its authority (survey, ordinance, professional, or the human for human-authority values)",
        "assumed": "a visible assumption with a value and source, pending confirmation",
        "exercise": "a value set by the human for exploration, pending confirmation",
        "range": "min and max known, the governing value not yet settled",
        "undefined": "no value; forbids geometric layouts"
    },
    "fields": {
        "boundary": "value_record",
        "setbacks": "list<value_record + edge>",
        "separations": "list<value_record + from>",
        "protected_zones": "list<value_record + entity, rule>",
        "existing_elements": "list<value_record + id, keep>",
        "orientation_datum": "value_record",
        "access_points": "value_record",
        "height_limit": "value_record"
    }
}
izq = question("S04.intervention_zone")
izq["output"] = "site_envelope"
izq["rule"] = "execution_model.sandbox_rule"
izq["q"] = ("Within each surviving site, what is the sandbox: setbacks, separations, protected zones, existing elements, "
            "orientation datum, access points and height limit, each confirmed, assumed, an exercise value or a range?")

# ------------------------------------------------------------------ sandbox and consistency rules
em = U["execution_model"]
em["sandbox_rule"] = ("A geometric design hypothesis (any dimensioned layout, plan or placement) presupposes the site "
                      "envelope. It may be created only when every envelope value is defined: confirmed, assumed, an "
                      "exercise value or a range. An undefined value forbids geometric layouts. Concept and topological "
                      "hypotheses remain free. A layout that relies on the favourable end of a range records rests_on = "
                      "favourable; otherwise it must fit the worst case.")
em["consistency_rule"] = ("A geometric design hypothesis lists the recorded answers it uses (uses_answers). Any element "
                          "that departs from a recorded human answer is listed under deviations. A deviation stays a "
                          "violation until the human resolves it: accepting it revises the recorded answer; rejecting it "
                          "changes the hypothesis. The AI never resolves a deviation itself.")
dh = O["design_hypothesis"]
dh["optional_fields"] = sorted(set(dh.get("optional_fields", []) + ["level", "uses_answers", "deviations", "rests_on"]))
dh["level_values"] = ["concept", "topological", "geometric"]
dh["deviation_fields"] = ["question", "recorded", "proposed", "resolved_by", "resolution"]

U["inquiry_model"]["sandbox_first"] = ("Once a site survives S02, the inquiry asks the envelope values (setbacks, "
                                       "separations, protected zones, existing elements, orientation, access) before any "
                                       "layout is proposed. For geometric work, undefined envelope values rank as "
                                       "show-stoppers in awareness.")

# ------------------------------------------------------------------ tests, invariants, questions
U["domain_stress_tests"]["layout_before_sandbox"] = ("Does USG refuse a dimensioned layout until the sandbox is "
                                                     "defined, and catch a layout that contradicts recorded answers?")
U["invariants"].append("No layout outside a defined sandbox; no layout that silently departs from a recorded answer.")
U["open_questions_for_review"] += [
    "Should the sandbox rule also apply to topological hypotheses when they fix adjacency to existing site elements?",
    "Should envelope values carry an expiry (e.g. an exercise value must be confirmed before schematic)?"
]

json.dump(U, open(dst, "w"), indent=2, ensure_ascii=False)
print(f"wrote {dst}: version {U['document']['version']}, {len(CHANGELOG)} changelog entries")
