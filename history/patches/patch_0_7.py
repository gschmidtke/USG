"""Patch USG 0.6 -> 0.7. Loads the previous version and changes only what the changelog lists.

Usage: python3 patch_0_7.py USG_v0_6.json USG_v0_7.json
Lessons from the adversarial run (off-world landing structure); no domain content enters the protocol.
"""
import json, sys

src, dst = sys.argv[1], sys.argv[2]
U = json.load(open(src))
assert U["document"]["version"] == "0.6", "patch applies to 0.6 only"


def stage(sid):
    return next(s for s in U["pipeline"] if s["id"] == sid)


def question(qid):
    return next(q for q in stage(qid.split(".")[0])["questions"] if q["id"] == qid)


CHANGELOG = [
    "Added S01.delivery and ontology class delivery_route: how materials, equipment and labour reach the site and how the structure is built, with explicit dependencies. Added the bootstrap-cycle check to conflict_detection and as an S00/S01 gate preview: a route that depends on the intervention itself, or on an event its success condition excludes, is put back to the human as a conflict. (adversarial run: success 'built before any vehicle lands' vs delivery by that vehicle)",
    "Added evidence_model.regulatory_absence_rule: 'no applicable regulation' is a claim that needs evidence like any other; a jurisdiction overlay may rest on a treaty, a licensing regime or an operator standard, not only on a building code. (adversarial run: 'there is no building code' accepted unchallenged)",
    "Added professional_review_classes.reviewer_designation: where no qualified reviewer class exists for a review item, the human designates the reviewer and the designation is recorded; until then the item stays open.",
    "Added S00.never classification: each statement is typed design_rule, use_restriction, vacuous or unevaluable on intake; vacuous and unevaluable statements go back to the human, who keeps, rewrites or drops them. Use restrictions are evaluated against lifecycle phases, not geometry. (adversarial run: a change-of-use prohibition passed unexamined)",
    "Added inquiry_model.no_default_by_silence: the AI never fills a human-authority question with a default the human did not confirm ('unless you say otherwise' is not an answer). Added inquiry_model.site_mode_rule: a named region larger than the intervention implies search_area, to be confirmed by the human. (adversarial run: site mode set by the AI from a 4,000 km region)",
    "Added inquiry_model.log and schemas.inquiry_log: an inquiry run records one question id per step, so granularity is checkable, not only stated. (adversarial run: three questions bundled in one step)",
    "Added stress test bootstrap_dependency and two open questions (stage placement of constructability; reviewer designation for novel domains).",
]

# ------------------------------------------------------------------ document, changelog, history
prev_log = U.pop("changelog_from_0_5_1")
U["history"] = {"0.6": {"changelog": prev_log, "removed": U["changelog_removed"]}, **U["history"]}
U["document"]["version"] = "0.7"
U["document"]["supersedes"] = "0.6"
new = {}
for k, v in U.items():
    new[k] = v
    if k == "document":
        new["changelog_from_0_6"] = CHANGELOG
U = new
U["changelog_removed"] = []

# ------------------------------------------------------------------ A: delivery and bootstrap cycles
s01 = stage("S01")
qs = s01["questions"]
pos = next(i for i, q in enumerate(qs) if q["id"] == "S01.need") + 1
qs.insert(pos, {
    "id": "S01.delivery",
    "q": "How do materials, equipment and labour reach the site, and how is the structure built? Does any route depend on the structure itself, or on an event the success criteria exclude?",
    "authority": "human", "required": True,
    "output": "list<delivery_route>",
    "rule": "conflict_detection.bootstrap_rule",
    "feeds": ["S01.alternatives", "S01.decision", "S04", "S05", "S12"]
})
U["ontology"]["delivery_route"] = {
    "definition": "A way materials, equipment or labour reach the site, with what it depends on. 'self' marks a dependency on the intervention itself; 'success_condition' marks a dependency on an event the success criteria exclude.",
    "required_fields": ["id", "means", "depends_on"],
    "optional_fields": ["evidence_refs", "construction_method", "phase"],
    "reserved_dependencies": ["self", "success_condition"]
}
cd = U["conflict_detection"]
cd["checks"].append("bootstrap cycle: a delivery route depends on the intervention itself or on an event its success criteria exclude")
cd["bootstrap_rule"] = ("If every delivery route depends on 'self' or 'success_condition', the conflict is put back to the "
                        "human (inquiry_model.conflicts) before S02; the AI never resolves it by changing the success "
                        "criteria or inventing a route. If at least one independent route exists, the dependent routes are "
                        "recorded and the run continues. The check runs as a gate preview as soon as S00.success and "
                        "S01.delivery are answered.")
U["feasibility_model"]["stage_questions"] = {
    "strategic_feasibility": "S01 except S01.delivery",
    "constraint_screen": "S02",
    "contextual_feasibility": "S04",
    "physical_feasibility": "S01.delivery (constructability), S09, S15",
    "design_feasibility": "S11-S17"
}

# ------------------------------------------------------------------ B: regulatory absence, reviewer designation
U["evidence_model"]["regulatory_absence_rule"] = (
    "A statement that no regulation, code or standard applies is a claim (gate S02 or S09). It needs evidence like any "
    "other claim and is never assumed. A jurisdiction overlay may rest on a treaty, a licensing regime, an operator "
    "standard or a contractual specification, not only on a building code.")
U["library_model"]["layer_meaning"]["jurisdiction_overlay"] += ("; may rest on a treaty, licensing regime, operator "
                                                                "standard or contract where no building code exists")
U["professional_review_classes"]["reviewer_designation"] = {
    "meaning": ("Where no recognised qualified reviewer class exists for a review item (novel structure type, new "
                "jurisdiction), the human designates the reviewer and the designation is recorded with the item. "
                "Until a reviewer is designated, the item stays open."),
    "default_items": []
}

# ------------------------------------------------------------------ C: never classification
nv = question("S00.never")
nv["output"] = "list<{statement, class, kept_by_human}>"
nv["classification"] = {
    "classes": ["design_rule", "use_restriction", "vacuous", "unevaluable"],
    "meaning": {
        "design_rule": "evaluable on candidates; becomes a hard rule at S09.never",
        "use_restriction": "evaluable on lifecycle phases and permitted uses, not on geometry",
        "vacuous": "no candidate or phase could violate it; adds no constraint",
        "unevaluable": "cannot be expressed with the relation vocabulary or a lifecycle check"
    },
    "rule": ("Each statement is classified on intake (derived, shown to the human). Vacuous and unevaluable statements "
             "go back to the human, who keeps, rewrites or drops them; kept ones are recorded with kept_by_human. The "
             "protocol classifies statements; it never judges them as unreasonable.")
}
question("S09.never")["q"] = ("Translate design_rule statements from S00 into evaluable hard rules and use_restriction "
                              "statements into lifecycle checks; carry kept vacuous or unevaluable statements to provenance.")

# ------------------------------------------------------------------ D: no default by silence, site mode from regions
im = U["inquiry_model"]
im["no_default_by_silence"] = ("The AI never fills a human-authority question with a value the human did not confirm. "
                               "'Unless you say otherwise' is not an answer; the question stays open or becomes a "
                               "visible assumption awaiting confirmation.")
im["site_mode_rule"] = ("A named region larger than the intervention (a valley, district, coastline, corridor) implies "
                        "site_mode search_area, to be confirmed by the human. A site is given only when its boundary is "
                        "identified.")

# ------------------------------------------------------------------ E: inquiry log
im["log"] = ("Every inquiry run records an inquiry_log. Each step asks exactly one question id; a step may record "
             "several question ids only when one human answer is routed to several questions (answer_routing).")
U["schemas"]["inquiry_log"] = {
    "steps": "list<{step, asked: question_id, routed: list<question_id>, authority, answer_ref}>"
}

# ------------------------------------------------------------------ tests, invariants, questions, next steps
U["domain_stress_tests"]["bootstrap_dependency"] = ("Does USG surface, before S02, a delivery route that depends on the "
                                                     "structure itself or on an event its success criteria exclude?")
U["invariants"] += [
    "No human-authority value is set by silence.",
    "Absence of regulation is evidenced, never assumed.",
    "Constructability is tested before design: every structure needs at least one delivery route that does not depend on itself."
]
U["open_questions_for_review"] += [
    "Should constructability (S01.delivery) stay in S01, or become part of a separate physical-feasibility stage?",
    "Reviewer designation: may the human designate any reviewer, or must the jurisdiction overlay or library set minimum qualifications?"
]
U["next_steps"] = [
    "Confirm or replace the three defaults pending author confirmation (own_use_rule, S01.decision_rules, S02.scenario_rule).",
    "Rebuild the residential library and the 160 m2 house instance against v0.7 (light feasibility, given site).",
    "Continue the ADU inquiry (instance_adu_backyard) from S07; first library curation round for residential_adu.",
    "Draft a Florida jurisdiction overlay from the ADU run.",
    "Write a minimal bridge library; test system selection with topology and the deferred 'action' decision.",
    "Extend the checker to validate libraries and instances against schemas.semantic_model.",
    "Only then: topology candidate generation."
]

json.dump(U, open(dst, "w"), indent=2, ensure_ascii=False)
print(f"wrote {dst}: version {U['document']['version']}, {len(CHANGELOG)} changelog entries")
