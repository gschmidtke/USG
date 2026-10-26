"""Patch USG 0.8 -> 0.9. Loads the previous version and changes only what the changelog lists.

Usage: python3 patch_0_9.py USG_v0_8.json USG_v0_9.json
Sources: Grok review of 0.8 (attacks verified against the runner) and Zara's failure/frontier-risk discoveries,
mapped onto existing structures (no new ontology classes). Author decision 2026-10-11: interested review is capped.
"""
import json, sys

src, dst = sys.argv[1], sys.argv[2]
U = json.load(open(src))
assert U["document"]["version"] == "0.8", "patch applies to 0.8 only"


def stage(sid):
    return next(s for s in U["pipeline"] if s["id"] == sid)


def question(qid):
    return next(q for q in stage(qid.split(".")[0])["questions"] if q["id"] == qid)


CHANGELOG = [
    # Grok
    "Added professional_review_classes.reviewer_independence: a review by a stakeholder whose interest the item decides (including self-designation) is recorded as a conflict and capped at medium confidence; it can never decide a claim or close a gate. evidence_model.precedence_rule amended accordingly. (Grok attack 'initiator is the only reviewer', verified: in 0.8 an owner's self-review confirmed three land-use claims; author decision 2026-10-11: cap, not forbid)",
    "delivery_route gained 'premises'; bootstrap_rule amended: a route with no self-dependency counts as verified only when its premises are resolved. Unverified routes do not halt the run but are show-stopper awareness items and block acceptance, export and irreversible acts. (Grok point 7, verified on One Mile City)",
    "S00.never classification: design_rule statements carry evaluable_stage; a hard rule evaluable after the current phase is surfaced as deferred risk. (Grok point 6)",
    "awareness_model.ranking: show-stopper premises (claims at S01 or S02 gates, delivery premises) always rank before all other items; within each class, dependents x severity. Default pending author confirmation. (Grok point 8)",
    "phase_model.commitment_rule.assumption_aging: an unconfirmed assumption presupposed by committed work blocks a phase transition once its until_phase has ended, even under exploratory status. Default pending author confirmation. (Grok point 1)",
    "Added conformance: an implementation is conformant to a version only if it reproduces the reference instances' expected outcomes and passes the reference mutation suite; no interface may bypass a commitment point. (Grok: enforcement at the protocol/product boundary)",
    # Zara
    "Scenario kind 'failure' added (what fails, its initiating event and consequence scope), alongside operating, design_event and phase. (Zara 1, 6)",
    "Topology graph type 'failure_propagation' added: single points of failure, shared dependencies, common-cause failures, cascade paths, isolation, degradation and recovery paths. (Zara 6)",
    "affected_system gained change_by_scenario and recoverability; impact_classes operational, failure, catastrophic, externalized. The no-baseline rule applies per scenario. (Zara 2)",
    "Added conflict_detection.environmental_absorption: a flow in a failure scenario whose sink is an affected system or context outside the intervention means the environment is acting as containment; it is reported as strain until containment is engineered or the absorption is explicitly accepted by the human with professional review. (Zara 3)",
    "value_perspective gained 'consent' (accepted, imposed, unresolved) for burdens; imposed burdens are reported as strain. Accepted risk is not unexamined risk. (Zara 5)",
    "Universal feasibility trigger added: novelty in environment, scale, technology, materials, system combination, autonomy or operating regime (minimum standard); when the trigger is true, the feasibility record must include failure precedents. (Zara 4; minimum chosen as standard so an unknown does not force full depth on small projects)",
    "Evidence kind failure_precedent and a precedent overlay layer, indexed by mechanism, not by project type; precedents themselves stay out of the protocol. (Zara 1)",
    "conflict_detection.resolution_order gained a first step: propose a consequence-reducing design change that preserves the purpose (AI-generated design hypothesis; the human decides). Risk generates design before anything escalates. (Zara 7)",
    "project_status: 'experimental progression' is named as the product term for exploratory status with irreversible acts blocked; no new state. (Zara 8)",
    "strain_report gained interested_review, environmental_absorption and imposed_burden.",
    "Invariant added: USG protects ambitious design from unexamined risk, not from risk. Stress tests, open questions and next steps updated.",
]

# ------------------------------------------------------------------ document, changelog, history
prev_log = U.pop("changelog_from_0_7")
U["history"] = {"0.8": {"changelog": prev_log, "removed": U["changelog_removed"]}, **U["history"]}
U["document"]["version"] = "0.9"
U["document"]["supersedes"] = "0.8"
new = {}
for k, v in U.items():
    new[k] = v
    if k == "document":
        new["changelog_from_0_8"] = CHANGELOG
U = new
U["changelog_removed"] = []
O = U["ontology"]

# ------------------------------------------------------------------ G1 reviewer independence
U["professional_review_classes"]["reviewer_independence"] = {
    "meaning": ("A review by a stakeholder whose interest the item decides, including a self-designated reviewer, is "
                "recorded as a conflict. Its evidence is capped at medium confidence: it is shown, but it can never "
                "decide a claim or close a gate."),
    "decided": "author 2026-10-11 (cap, not forbid)",
    "default_items": []
}
O["evidence"]["optional_fields"] += ["reviewer", "interested"]
U["evidence_model"]["precedence_rule"] += (" A professional_confirmation by an interested reviewer "
                                           "(professional_review_classes.reviewer_independence) does not decide; it "
                                           "counts as medium-confidence evidence.")
U["evidence_model"]["rules"].append("A review by an interested party never exceeds medium confidence.")

# ------------------------------------------------------------------ G2 delivery premises
O["delivery_route"]["optional_fields"].append("premises")
U["conflict_detection"]["bootstrap_rule"] += (" A route without self-dependency counts as verified only when its "
                                              "premises are resolved. Unverified routes do not halt the run; they are "
                                              "show-stopper awareness items and block acceptance, export and "
                                              "irreversible acts.")

# ------------------------------------------------------------------ G3 never evaluable stage
nv = question("S00.never")
nv["classification"]["evaluable_stage"] = ("Each design_rule records the stage at which it can first be evaluated. A "
                                           "hard rule evaluable after the current phase is surfaced as deferred risk, "
                                           "so constraints are not parked where they fire only after expensive work.")
nv["output"] = "list<{statement, class, evaluable_stage, kept_by_human}>"

# ------------------------------------------------------------------ G4 ranking, G5 aging
am = U["awareness_model"]
am["ranking"] = ("Show-stopper premises (claims decided at S01 or S02, delivery route premises) rank before all other "
                 "items. Within each class: dependents x severity; severity 3 for negative or conflicting, 2 for "
                 "unknown, insufficient or deferred risk, 1 for unanswered questions.")
am["ranking_status"] = {"rule": "show-stopper first", "status": "default pending author confirmation"}
U["phase_model"]["commitment_rule"]["assumption_aging"] = {
    "rule": ("An unconfirmed assumption presupposed by committed work blocks a phase transition once its until_phase "
             "has ended, even under exploratory status."),
    "status": "default pending author confirmation"
}
O["assumption"]["optional_fields"] = ["until_phase", "kind"]

# ------------------------------------------------------------------ G6 conformance
U["conformance"] = {
    "rule": ("An implementation is conformant to a USG version only if it reproduces the expected outcomes of that "
             "version's reference instances and passes its reference mutation suite."),
    "gates": "No interface may bypass a commitment point; an exploratory result can never be exported as buildable.",
    "reference": "run_usg.py and test_runner.py of the same release"
}

# ------------------------------------------------------------------ Z1 failure scenarios
O["scenario"]["kind_values"].append("failure")
O["scenario"]["optional_fields"] = ["initiating_event", "consequence_scope", "probability_class"]
O["scenario"]["examples"].append("pipe_rupture")

# ------------------------------------------------------------------ Z2 failure propagation graph
U["topology_model"]["graph_types"]["failure_propagation"] = ("systems and units as nodes, dependency edges along which "
                                                            "a failure propagates; shows single points of failure, "
                                                            "shared dependencies, common-cause failures, cascade "
                                                            "paths, isolation, degradation and recovery paths")
U["topology_model"]["library_declares"] += (" Any library whose structures carry life, hazardous media or critical "
                                            "service declares failure_propagation.")

# ------------------------------------------------------------------ Z3 impact by scenario
asys = O["affected_system"]
asys["optional_fields"] += ["change_by_scenario", "recoverability"]
asys["impact_classes"] = ["operational", "failure", "catastrophic", "externalized"]
asys["recoverability_values"] = ["full", "partial", "none", "unresolved"]
asys["rule"] += " The same rule applies to every entry of change_by_scenario."

# ------------------------------------------------------------------ Z4 environmental absorption
cd = U["conflict_detection"]
cd["checks"].append("environmental absorption: a failure-scenario flow whose sink lies outside the intervention")
cd["environmental_absorption"] = ("A flow in a failure scenario whose sink is an affected system or a context entity "
                                  "outside the intervention boundary means the environment is acting as containment. "
                                  "It is reported as strain until containment is engineered, or until the human "
                                  "explicitly accepts the absorption with professional review.")

# ------------------------------------------------------------------ Z5 consent
O["value_perspective"]["optional_fields"].append("consent")
O["value_perspective"]["consent_values"] = ["accepted", "imposed", "unresolved"]

# ------------------------------------------------------------------ Z6 novelty trigger
trig = U["feasibility_module"]["intensity"]["triggers"]
none_idx = next(i for i, t in enumerate(trig) if t["condition"] == "none of the above")
trig.insert(none_idx, {"condition": "novelty in environment, scale, technology, materials, system combination, autonomy or operating regime",
                       "minimum": "standard"})
U["feasibility_module"]["intensity"]["novelty_rule"] = ("When the novelty trigger is true, the strategic feasibility "
                                                       "record must include failure precedents (evidence of kind "
                                                       "failure_precedent), found by mechanism across structure types.")
U["schemas"]["strategic_feasibility_record"]["failure_precedents"] = "list<evidence_ref> (required when novelty is true)"

# ------------------------------------------------------------------ Z7 precedents
O["evidence"]["kind_reserved"]["failure_precedent"] = ("A documented failure of a comparable system: what failed, the "
                                                       "missed assumption, the cascade, and the lesson. Comparable "
                                                       "means sharing a mechanism, not a project type.")
lm = U["library_model"]
lm["layers"].insert(lm["layers"].index("domain_library"), "precedent_overlay")
lm["layer_meaning"]["precedent_overlay"] = ("failure precedents indexed by mechanism (containment loss, power loss, "
                                            "closed-loop life support, collapse, ...); read at S01 and S09; shared "
                                            "across domain libraries")

# ------------------------------------------------------------------ Z8 risk as design generator
cd["resolution_order"].insert(0, ("propose a consequence-reducing design change that preserves the purpose "
                                  "(redundancy, compartmentation, staging, refuge, passive fail-safe, alternative "
                                  "siting); recorded as an ai_generated design hypothesis; the human decides"))

# ------------------------------------------------------------------ Z9 experimental progression
U["project_status"]["product_terms"] = {"experimental progression": ("exploratory status with irreversible acts "
                                                                     "blocked; work advances by simulation, "
                                                                     "prototypes, staged deployment or bounded "
                                                                     "experiments")}

# ------------------------------------------------------------------ strain, invariants, tests, questions
sr = U["schemas"]["strain_report"]
note = sr.pop("note")
sr["interested_review"] = "list<evidence id>"
sr["environmental_absorption"] = "list<{flow, sink, scenario}>"
sr["imposed_burden"] = "list<value_perspective id>"
sr["note"] = note
U["invariants"].append("USG protects ambitious design from unexamined risk, not from risk.")
U["invariants"].append("No party certifies its own interest: interested review never closes a gate.")
U["domain_stress_tests"]["frontier_failure"] = ("Does USG surface failure precedents, cascades and environmental "
                                                "absorption for a novel structure, and generate consequence-reducing "
                                                "design before escalating?")
U["open_questions_for_review"] += [
    "Should the novelty trigger require full depth instead of standard?",
    "Failure precedents: who curates the precedent overlay, and with what minimum evidence per precedent?"
]
U["open_questions_for_review"] = [q for q in U["open_questions_for_review"]
                                  if not q.startswith("Awareness ranking: is dependents x severity sufficient")]
U["resolved_questions"].append({"question": "Awareness ranking: is dependents x severity sufficient, or does irreversibility need its own factor?",
                                "answer": "Show-stopper premises rank first; dependents x severity within each class (default pending author confirmation).",
                                "resolved_in": "0.9", "evidence": "Grok review of 0.8, point 8"})

json.dump(U, open(dst, "w"), indent=2, ensure_ascii=False)
print(f"wrote {dst}: version {U['document']['version']}, {len(CHANGELOG)} changelog entries")
