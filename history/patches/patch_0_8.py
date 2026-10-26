"""Patch USG 0.7 -> 0.8. Loads the previous version and changes only what the changelog lists.

Usage: python3 patch_0_8.py USG_v0_7.json USG_v0_8.json
Source: One Mile City stress test and the post-0.7 design-agent discussion. Central decision (author, 2026-10-11):
the pipeline is an order of validity, not an order of work; blocking happens only at commitment points.
"""
import json, sys

src, dst = sys.argv[1], sys.argv[2]
U = json.load(open(src))
assert U["document"]["version"] == "0.7", "patch applies to 0.7 only"


def stage(sid):
    return next(s for s in U["pipeline"] if s["id"] == sid)


def question(qid):
    return next(q for q in stage(qid.split(".")[0])["questions"] if q["id"] == qid)


CHANGELOG = [
    "Added execution_model: the pipeline is an order of validity, not an order of work. Design may explore at any time; gates decide what may be committed. (author decision 2026-10-11)",
    "Added phase_model: concept, schematic, design_development, technical_design, operation, mapped onto the stages, with commitment points (phase transitions, acceptance, export, irreversible acts in the world) and a commitment rule: a committed design hypothesis is blocked if any premise is negative; unknown premises pass a phase transition only under exploratory status and never pass export or an irreversible act.",
    "Added ontology class design_hypothesis: a design idea at any stage with the question ids, claims, assumptions and affected systems it presupposes. The Design thread is the set of hypotheses.",
    "Added awareness_model: the Awareness thread is derived from open premises of current hypotheses and unanswered questions of the current and earlier phases; ranked by dependents x severity; at most one awareness question per design turn, surfaced at a natural pause, queued and never dropped.",
    "Added S00.drivers as the first S00 question: what triggered the project, who initiated it, who holds decision power, what each party wants. Depth follows feasibility intensity. The AI asks about drivers; it never imputes motives. Added ontology class stakeholder (parties with interests or decision power, distinct from actors who use the structure).",
    "Added statement_model: every requirement-like statement has a statement_type (constraint, requirement, preference, assumption, open_design_variable), a basis (physical, legal, verified_site_condition, stakeholder_choice) and relaxable_by. A statement relaxable by a stakeholder is not a constraint. Added decision-layer relation pressured_by(statement, stakeholder, toward).",
    "Added ontology class open_design_variable with owner, decide_by phase and candidate range, and the spanning rule: generators must span an open ODV, not fix it; committing a value before decide_by is a violation. Unknowns block; ODVs are protected.",
    "Added S01.affected_systems and ontology class affected_system: baseline (evidence, confidence), change (magnitude, persistence, reversibility), beneficiaries, burden bearers, mitigation, compensation, residual. Rule: no baseline, no impact claim. Kinds include dependency and future_public_burden, the two universal questions from the settlement discussion.",
    "Added ontology class value_perspective and evidence_model.value_rule: value is recorded as a ledger of perspectives (benefit, burden, horizon, reversibility); perspectives are shown side by side, never aggregated by the AI; weights come only from the human. S01.value now outputs the ledger.",
    "Added schemas.strain_report: structural strain is a derived collection of open conflicts (hypothesis on a negative claim, pressure against a constraint, burden without compensation, assumption carried past its phase, ODV collapsed early). Not a status, not a score.",
    "Added feedback loop FB9 (premise reopened): from any stage to S00 when a premise of committed work changes; escalation to the human. Inquiry stays open after commitment.",
    "S02.site_candidates may also be answered by the human (also_answerable_by): a human-named candidate in search_area or open mode was not representable. (found while encoding the One Mile City instance)",
    "Added stress test design_ahead_of_premise; invariants for validity order, ledger and ODV protection; open questions; next steps.",
]

# ------------------------------------------------------------------ document, changelog, history
prev_log = U.pop("changelog_from_0_6")
U["history"] = {"0.7": {"changelog": prev_log, "removed": U["changelog_removed"]}, **U["history"]}
U["document"]["version"] = "0.8"
U["document"]["supersedes"] = "0.7"
new = {}
for k, v in U.items():
    new[k] = v
    if k == "document":
        new["changelog_from_0_7"] = CHANGELOG
U = new
U["changelog_removed"] = []
U["core_thesis"]["execution"] = "The pipeline is an order of validity, not an order of work: explore freely, commit only what is valid."

# ------------------------------------------------------------------ execution and phase model
U["execution_model"] = {
    "principle": ("The stage order defines what a value or design decision depends on, not when it may be thought of. "
                  "Design hypotheses may be created at any time; gates decide what may be committed."),
    "threads": {
        "design": "the set of design_hypothesis records: what is being explored or shaped",
        "inquiry": "inquiry_model: the next question needed to continue",
        "awareness": "awareness_model: derived from open premises and unvisited dimensions"
    },
    "single_state": "The three threads are views over one project state, not separate engines."
}
U["phase_model"] = {
    "phases": ["concept", "schematic", "design_development", "technical_design", "operation"],
    "stages": {
        "concept": ["S00", "S01", "S02", "S03", "S04", "S05", "S06"],
        "schematic": ["S07", "S08", "S09", "S10", "S11", "S12", "S13"],
        "design_development": ["S14", "S15", "S16"],
        "technical_design": ["S17", "S18", "S19", "S20"],
        "operation": []
    },
    "operation_note": "Operation follows export: verification, adaptation and lifecycle feedback into library curation and FB9.",
    "commitment_points": ["concept->schematic", "schematic->design_development", "design_development->technical_design",
                          "acceptance", "export", "irreversible_act"],
    "irreversible_act": "An act in the world that is costly to undo (land purchase, permit filing, procurement, construction start), declared by the human.",
    "commitment_rule": {
        "negative": "A committed hypothesis with any premise confirmed_negative, failed or prohibited is blocked, unless the premise is held under a human-requested scenario.",
        "unresolved": "A premise that is unknown, insufficient or conflicting passes a phase transition only under exploratory status, recorded with the reason; it never passes acceptance, export or an irreversible act.",
        "odv": "Committing a value for an open design variable before its decide_by phase is a violation."
    }
}

# ------------------------------------------------------------------ ontology additions
O = U["ontology"]
O["design_hypothesis"] = {
    "definition": "A design idea at any level of definition (a section, a system concept, a layout), recorded with what it presupposes.",
    "required_fields": ["id", "description", "phase", "presupposes", "status", "author"],
    "optional_fields": ["fixes", "derived_from"],
    "status_values": ["exploring", "committed", "retired"],
    "author_values": ["human", "ai_generated"],
    "presupposes_note": "question ids, claim ids, assumption ids, affected_system ids or ODV ids"
}
O["stakeholder"] = {
    "definition": "A party with interests in or decision power over the project (initiator, financier, operator, authority, community). Distinct from actors, who use or load the structure.",
    "required_fields": ["id", "role"],
    "optional_fields": ["decision_power", "interests"]
}
O["open_design_variable"] = {
    "definition": "A question intentionally left open to preserve exploration. Unlike an unknown it does not block; it is protected until its decide_by phase.",
    "required_fields": ["id", "question", "owner", "decide_by", "status"],
    "optional_fields": ["candidate_range", "decided_value"],
    "status_values": ["open", "decided"]
}
O["affected_system"] = {
    "definition": "A system outside the intervention that it changes: ecology, water, ground, ice, atmosphere, climate, community, infrastructure, economy, labour, a dependency it creates, or a burden it shifts to the future.",
    "required_fields": ["id", "kind", "baseline", "change"],
    "optional_fields": ["beneficiaries", "burden_bearers", "mitigation", "compensation", "residual"],
    "kind_values": ["ecology", "water", "ground", "ice", "atmosphere", "climate", "community", "infrastructure",
                    "economy", "labour", "dependency", "future_public_burden"],
    "baseline_fields": ["evidence_refs", "confidence"],
    "change_fields": ["magnitude", "persistence", "reversibility"],
    "persistence_values": ["temporary", "persistent", "cumulative", "unresolved"],
    "rule": "No baseline, no impact claim: with no baseline evidence, change.magnitude is 'unresolved', never zero or a value."
}
O["value_perspective"] = {
    "definition": "One row of the value ledger: what the intervention means for one stakeholder, actor or affected system.",
    "required_fields": ["id", "perspective", "benefit", "burden", "horizon"],
    "optional_fields": ["reversibility", "necessity", "compensation", "evidence_refs"]
}

# ------------------------------------------------------------------ relation: pressured_by
U["relation_vocabulary"]["relations"]["pressured_by"] = {
    "definition": "statement a is being pushed by stakeholder b toward a stronger statement type (usually preference -> requirement).",
    "params": {"toward": "requirement | constraint", "source": "financing | schedule | politics | reputation | other"},
    "subject": "statement | rule",
    "object": "stakeholder",
    "inverse": "pressures",
    "symmetric": False,
    "transitive": False,
    "earliest_stage": "strategic",
    "layer": "decision"
}

# ------------------------------------------------------------------ statement model
U["statement_model"] = {
    "statement_types": {
        "constraint": "cannot reasonably be violated: physics, hard legal limit, verified site condition",
        "requirement": "an outcome the project is expected to satisfy",
        "preference": "a desired outcome that may be traded against other goals",
        "assumption": "a provisional belief used while evidence is incomplete",
        "open_design_variable": "intentionally unresolved to preserve exploration"
    },
    "basis_values": ["physical", "legal", "verified_site_condition", "stakeholder_choice"],
    "fields": ["id", "text", "statement_type", "basis", "relaxable_by"],
    "rule": ("Test: who could relax this? A statement relaxable_by a stakeholder has basis stakeholder_choice and is not "
             "a constraint. Pressure toward a stronger type is recorded with pressured_by, never silently applied.")
}
U["rule_model"]["fields"]["statement_type"] = "constraint | requirement | preference | assumption | open_design_variable"
U["rule_model"]["fields"]["relaxable_by"] = "stakeholder id | null"

# ------------------------------------------------------------------ pipeline questions
s00 = stage("S00")
s00["questions"].insert(0, {
    "id": "S00.drivers",
    "q": "What triggered this project, who initiated it, who holds decision power, and what does each party want?",
    "authority": "human", "required": True,
    "output": "list<stakeholder>",
    "rule": "driver_rule",
    "feeds": ["S00.purpose", "S01", "S10"]
})
U["driver_rule"] = ("Depth follows feasibility intensity: at light depth, trigger and initiator suffice; standard and full "
                    "add decision power, interests and pressures. Drivers are asked, never imputed: the AI may not "
                    "attribute a motive to a party. A received brief is an output of its drivers; the inquiry may "
                    "trace it backward before moving forward.")
s01 = stage("S01")
qs = s01["questions"]
pos = next(i for i, q in enumerate(qs) if q["id"] == "S01.delivery") + 1
qs.insert(pos, {
    "id": "S01.affected_systems",
    "q": "Which systems outside the intervention does it change, what is their baseline, and who benefits or bears the burden?",
    "authority": "external_evidence", "required": "intensity != light",
    "output": "list<affected_system>",
    "rule": "ontology.affected_system.rule",
    "feeds": ["S01.alternatives", "S01.value", "S01.decision", "S02", "S09", "S10"]
})
question("S01.value")["output"] = "list<value_perspective>"
question("S01.value")["rule"] = "evidence_model.value_rule"
sc = question("S02.site_candidates")
sc["also_answerable_by"] = ["human"]
sc["q"] = sc["q"] + " The human may also name candidates."

# ------------------------------------------------------------------ value, awareness, strain
U["evidence_model"]["value_rule"] = ("Value is a ledger of perspectives. Perspectives are shown side by side and never "
                                     "aggregated, ranked or netted by the AI. Weights come only from the human "
                                     "(S10.priorities). The ledger reveals; it does not judge.")
U["awareness_model"] = {
    "sources": [
        "premises of current design hypotheses that are not resolved positively",
        "required questions of the current or an earlier phase that are unanswered",
        "strain_report entries"
    ],
    "ranking": "dependents x severity; severity 3 for negative or conflicting premises, 2 for unknown or insufficient, 1 for unanswered questions",
    "budget": "at most one awareness question per design turn",
    "timing": "surfaced at a natural pause (end of a design move), never mid-thought",
    "queue": "awareness items are queued and re-ranked; never dropped",
    "blocking": "awareness never blocks exploration; it blocks only through phase_model.commitment_rule"
}
U["schemas"]["strain_report"] = {
    "hypothesis_on_negative_claim": "list<{hypothesis, premise}>",
    "pressure_vs_constraint": "list<{statement, stakeholder}>",
    "burden_without_compensation": "list<{perspective or affected_system}>",
    "assumption_past_phase": "list<assumption id>",
    "odv_collapsed": "list<{odv, hypothesis}>",
    "note": "Derived, never stored; counted per category, never collapsed into one number."
}
U["schemas"]["semantic_model"]["design_hypotheses"] = "list<design_hypothesis>"
U["schemas"]["semantic_model"]["stakeholders"] = "list<stakeholder>"
U["schemas"]["semantic_model"]["statements"] = "list<statement>"
U["schemas"]["semantic_model"]["open_design_variables"] = "list<open_design_variable>"
U["schemas"]["semantic_model"]["affected_systems"] = "list<affected_system>"
U["schemas"]["semantic_model"]["value_ledger"] = "list<value_perspective>"
U["schemas"]["semantic_model"]["current_phase"] = "phase_model.phases"
U["topology_model"]["candidate_strategy"]["odv_spanning"] = ("Topology candidates must differ along every open design "
                                                            "variable until its decide_by phase.")
U["question_record_schema"]["optional"].append("also_answerable_by")

# ------------------------------------------------------------------ FB9
U["controlled_feedback_loops"]["loops"].append({
    "id": "FB9", "from": "any", "to": "S00",
    "reason": "A premise of committed work has changed or been reopened (new evidence, changed driver, changed affected-system baseline).",
    "may_change": [],
    "must_not_change": ["purpose_without_human_confirmation", "committed work without human confirmation"],
    "escalation": "human"
})

# ------------------------------------------------------------------ tests, invariants, questions, next steps
U["domain_stress_tests"]["design_ahead_of_premise"] = ("When design runs ahead of a show-stopping premise, does USG let "
                                                        "exploration continue, rank the premise first, report strain, and "
                                                        "block commitment?")
U["invariants"] += [
    "The pipeline is an order of validity: exploration is free, commitment is gated.",
    "Value perspectives are shown side by side, never aggregated by the AI.",
    "Open design variables are protected, not defaulted.",
    "Drivers are asked, never imputed."
]
U["open_questions_for_review"] += [
    "Awareness ranking: is dependents x severity sufficient, or does irreversibility need its own factor?",
    "Should the operation phase get its own stages (verification, adaptation), or stay a feedback channel?",
    "Driver depth: are trigger and initiator enough at light depth?"
]
U["next_steps"] = [
    "Confirm or replace the three defaults pending author confirmation (own_use_rule, S01.decision_rules, S02.scenario_rule).",
    "Rebuild the residential library and the 160 m2 house instance against v0.8.",
    "Continue the ADU inquiry (instance_adu_backyard) from S07; first library curation round for residential_adu.",
    "Draft a Florida jurisdiction overlay from the ADU run.",
    "Write a minimal bridge library; test system selection with topology and the deferred 'action' decision.",
    "Extend the checker to validate libraries and instances against schemas.semantic_model.",
    "Only then: topology candidate generation, with ODV spanning."
]

json.dump(U, open(dst, "w"), indent=2, ensure_ascii=False)
print(f"wrote {dst}: version {U['document']['version']}, {len(CHANGELOG)} changelog entries")
