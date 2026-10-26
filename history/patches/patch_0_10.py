"""Patch USG 0.9 -> 0.10. Loads the previous version and changes only what the changelog lists.

Usage: python3 patch_0_10.py USG_v0_9.json USG_v0_10.json
Source: Mars stress-test delta (author memo 2026-10-11), reviewed against 0.9. Finding: inquiry mostly held;
strategic alternative generation was the gap. Domain patterns (settlement growth, layered logistics) stay out
of the protocol; they belong in the new strategy-pattern overlay.
"""
import json, sys

src, dst = sys.argv[1], sys.argv[2]
U = json.load(open(src))
assert U["document"]["version"] == "0.9", "patch applies to 0.9 only"


def stage(sid):
    return next(s for s in U["pipeline"] if s["id"] == sid)


def question(qid):
    return next(q for q in stage(qid.split(".")[0])["questions"] if q["id"] == qid)


CHANGELOG = [
    "Alternative options staged_precursor (an enabling intervention first, linked by 'enables') and defer_commitment (with a named revisit trigger) added to alternatives_to_build and ontology.intervention_alternative. (Mars A, G)",
    "Added program_model: instances may be linked as precursor_of / enabled_by; a precursor's success is a demonstrated capability, which the enabled instance may presuppose. Recursive capability growth is expressible without a domain pattern. (Mars B)",
    "Added S01.need_behind (required at full depth): the need one level above the stated need. Added alternatives_to_build.generation_duty: alternatives are generated against the need behind the stated need and at strategy level (precursor, defer, means) before the brief's form is accepted; when novelty is true or a delivery route rests on unresolved premises, at least one strategy-level option must be considered (it may be excluded with a reason). Purpose changes still go through FB6 to the human. (Mars J, K)",
    "conflict_detection.bootstrap_rule: on a bootstrap conflict the AI first proposes precursor alternatives, then escalates. (Mars A)",
    "Added inquiry_model.means_separation: a means named in the brief (a form, a technology, a tool) is recorded as a statement concerning means, typed preference unless the human declares it a requirement with a basis. statement_model gained 'concerns' (outcome, means, condition). (Mars F)",
    "Added S12.context_provision as the first S12 question: which required functions can the existing context provide passively, before manufactured systems are selected. (Mars D; universal: natural harbour, earth shelter, shade)",
    "delivery_route gained supply_basis (imported, stocked, locally_produced, locally_reproducible), stock_duration and critical. Added closure_model: survival, maintenance and reproductive autonomy are derived from the supply basis of critical routes, not new schema. (Mars C)",
    "Added conflict_detection check and flow field 'byproduct': every by-product flow (spoil, waste, heat) declares a sink. (Mars E)",
    "Added evidence_model.speculation_rule: fiction and speculation are never evidence; they may only be cited as derived_from of a hypothesis or alternative. (Mars I)",
    "Added a strategy_pattern_overlay layer (declared, empty): cross-domain strategy patterns indexed by problem structure (bootstrap, hostile environment, closure, layered logistics), used by the generator, never normative. (Mars B, H)",
    "Stress test strategy_transformation; invariant; open questions; next steps.",
]

# ------------------------------------------------------------------ document, changelog, history
prev_log = U.pop("changelog_from_0_8")
U["history"] = {"0.9": {"changelog": prev_log, "removed": U["changelog_removed"]}, **U["history"]}
U["document"]["version"] = "0.10"
U["document"]["supersedes"] = "0.9"
new = {}
for k, v in U.items():
    new[k] = v
    if k == "document":
        new["changelog_from_0_9"] = CHANGELOG
U = new
U["changelog_removed"] = []
O = U["ontology"]
atb = U["alternatives_to_build"]

# ------------------------------------------------------------------ 1 options
for opt in ("staged_precursor", "defer_commitment"):
    atb["options"].append(opt)
    O["intervention_alternative"]["option_values"].append(opt)
O["intervention_alternative"]["optional_fields"] = ["enables", "revisit_trigger", "derived_from"]
O["intervention_alternative"]["option_rules"] = {
    "staged_precursor": "must name what it enables (enables: capability or instance)",
    "defer_commitment": "must name a revisit_trigger (a technology, evidence or date); distinct from do_nothing"
}

# ------------------------------------------------------------------ 2 program model
U["program_model"] = {
    "principle": ("An undertaking may be a program of linked instances. A precursor instance exists to create a "
                  "capability another instance needs; its success criterion is that capability, demonstrated."),
    "link_fields": ["precursor_of", "enabled_by"],
    "capability_fields": ["id", "capability", "provided_by", "status"],
    "capability_status_values": ["planned", "demonstrated", "failed"],
    "rule": ("An enabled instance may presuppose a capability by id; until the capability is demonstrated it is an "
             "unresolved premise (awareness and commitment rules apply). Recursion is allowed: a precursor may have "
             "its own precursors.")
}
U["schemas"]["semantic_model"]["program"] = "{precursor_of: list<instance id>, enabled_by: list<capability>}"

# ------------------------------------------------------------------ 3 need behind, generation duty
s01 = stage("S01")
qs = s01["questions"]
pos = next(i for i, q in enumerate(qs) if q["id"] == "S01.need") + 1
qs.insert(pos, {
    "id": "S01.need_behind",
    "q": "Why is this needed: what need lies one level above the stated need?",
    "authority": "human", "required": "intensity == full",
    "rule": "alternatives_to_build.generation_duty",
    "feeds": ["S01.alternatives", "S01.value", "S01.decision"]
})
question("S01.need")["feeds"].insert(0, "S01.need_behind")
question("S01.alternatives")["q"] = ("Could the need, or the need behind it, be met better by doing nothing, reuse, "
                                     "adaptation, expansion, relocation, operational change, a precursor that "
                                     "creates the needed capability first, or deferring commitment?")
atb["generation_duty"] = {
    "rule": ("The AI generates alternatives against the stated need and the need behind it, and at strategy level "
             "(precursor, defer, means), before the brief's form is accepted. The human decides; changing the "
             "purpose goes through FB6."),
    "strategy_level_options": ["staged_precursor", "defer_commitment"],
    "required_when": ("novelty is true, or a delivery route rests on unresolved premises: at least one strategy-level "
                      "option is considered (it may be excluded with a reason)")
}
U["conflict_detection"]["bootstrap_rule"] = U["conflict_detection"]["bootstrap_rule"].replace(
    "the conflict is put back to the human (inquiry_model.conflicts) before S02",
    "the AI first proposes precursor alternatives (staged_precursor), then puts the conflict back to the human "
    "(inquiry_model.conflicts) before S02")
assert "staged_precursor" in U["conflict_detection"]["bootstrap_rule"]

# ------------------------------------------------------------------ 4 means separation
U["inquiry_model"]["means_separation"] = ("A means named in the brief (a form, a technology, a tool, a construction "
                                          "method) is recorded as a statement with concerns = means, typed preference "
                                          "unless the human declares it a requirement and states its basis. A means "
                                          "is a candidate, never a hidden premise.")
U["statement_model"]["fields"].append("concerns")
U["statement_model"]["concerns_values"] = ["outcome", "means", "condition"]

# ------------------------------------------------------------------ 5 context provision
s12 = stage("S12")
s12["questions"].insert(0, {
    "id": "S12.context_provision",
    "q": "Which required functions can the existing context provide passively (structure, shelter, shielding, thermal mass, water, access) before manufactured systems are selected?",
    "authority": "ai_generated", "required": True,
    "confirmation": "professional_review",
    "feeds": ["S12.systems", "S13", "S15"]
})

# ------------------------------------------------------------------ 6 supply basis, closure
dr = O["delivery_route"]
dr["optional_fields"] += ["supply_basis", "stock_duration", "critical"]
dr["supply_basis_values"] = ["imported", "stocked", "locally_produced", "locally_reproducible"]
U["closure_model"] = {
    "principle": "Self-sufficiency is derived from the supply basis of critical routes, never asserted.",
    "levels": {
        "survival": "every critical supply is stocked for at least the interruption scenario, or produced locally",
        "maintenance": "every critical supply, including spare parts, is locally_produced or locally_reproducible",
        "reproductive": "every critical supply and the means of producing it are locally_reproducible"
    },
    "order": ["none", "survival", "maintenance", "reproductive"]
}

# ------------------------------------------------------------------ 7 by-product sinks
O["flow"]["optional_fields"].append("byproduct")
U["conflict_detection"]["checks"].append("by-product flow without a declared sink")
U["conflict_detection"]["byproduct_rule"] = ("Every by-product flow (spoil, waste, heat, water) declares a sink. A sink "
                                             "inside the intervention is a resource loop; a sink outside it is an "
                                             "operational impact on an affected system.")

# ------------------------------------------------------------------ 8 speculation
U["evidence_model"]["speculation_rule"] = ("Fiction and speculation are never evidence and never support or contradict "
                                           "a claim. They may be cited only as derived_from of a design hypothesis or "
                                           "an alternative, as a question generator.")
O["evidence"]["kind_forbidden"] = ["fiction", "speculation", "speculative_precedent"]

# ------------------------------------------------------------------ 9 strategy pattern overlay
lm = U["library_model"]
lm["layers"].insert(lm["layers"].index("domain_library"), "strategy_pattern_overlay")
lm["layer_meaning"]["strategy_pattern_overlay"] = ("cross-domain strategy patterns indexed by problem structure "
                                                   "(bootstrap, hostile environment, closure, layered logistics); "
                                                   "used by the generator to propose alternatives; never normative; "
                                                   "declared in 0.10, no patterns released yet")

# ------------------------------------------------------------------ 10 tests, invariants, questions
U["domain_stress_tests"]["strategy_transformation"] = ("Given a brief for an object (a settlement, a city), does USG "
                                                       "generate strategy-level alternatives (a precursor, deferral, "
                                                       "the need behind the need) before optimizing the object?")
U["invariants"].append("The brief's form is a candidate, not a premise: alternatives are generated against the need behind it.")
U["open_questions_for_review"] += [
    "Who curates the strategy-pattern overlay, and how is a pattern validated before the generator may use it?",
    "Should the generation duty also apply at standard depth?"
]

json.dump(U, open(dst, "w"), indent=2, ensure_ascii=False)
print(f"wrote {dst}: version {U['document']['version']}, {len(CHANGELOG)} changelog entries")
