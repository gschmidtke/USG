"""Patch USG 0.5.1 -> 0.6. Loads the previous version and changes only what the changelog lists.

Usage: python3 patch_0_6.py USG_v0_5_1.json USG_v0_6.json
"""
import json, sys

src, dst = sys.argv[1], sys.argv[2]
U = json.load(open(src))
assert U["document"]["version"] == "0.5.1", "patch applies to 0.5.1 only"


def stage(sid):
    return next(s for s in U["pipeline"] if s["id"] == sid)


def question(qid):
    return next(q for q in stage(qid.split(".")[0])["questions"] if q["id"] == qid)


CHANGELOG = [
    # structural
    "Added inquiry_model: the pipeline is executed as an inquiry, one question, one authority and one value per step; answers given early are routed to their question and never asked again; derived gate checks run as previews as soon as their inputs exist; conflicting human answers are put back to the human. (ADU run findings 10-12)",
    "Added library_model with a library-gap path: when a domain-library value is missing, the AI may propose it as a visible assumption, the human confirms it for the project, and a generalization question decides its applicability scope (domain, jurisdiction, climate) or keeps it instance-only. Candidates are promoted only by library curation. Any open library gap keeps the project exploratory. (ADU finding 1)",
    "Added a jurisdiction overlay layer between protocol and domain library: code obligations belong to the jurisdiction layer and enter at S09 as code rules; domain libraries hold building-type defaults only. (ADU finding 2)",
    "Added ontology classes library_candidate, zone, lifecycle_phase and trigger_fact. Zones are contained by exactly one functional unit and are governed by fits and not_overlap; this resolves the open question on zones. (ADU findings 2, 3, 5, 6)",
    "Added S00.lifecycle_use: the uses the structure must serve over its life, as phases with a beneficiary each (own_use, third_party_known, market, public). Replaces the separate beneficiary question proposed during the ADU run. (ADU finding 3)",
    "Added S00.triggers: feasibility trigger facts become an explicit question. A trigger may need a fact and a professional classification; an unknown trigger applies conservatively; a library-dependent trigger with no library threshold may be asserted false by the human as a recorded assumption. (failure-run gap 1, ADU finding 5)",
    "Added feasibility_module.intensity.own_use_rule: when the first lifecycle phase is own_use, the human's stated need is the demand evidence at any depth and existing supply means the beneficiary's own assets. Default pending author confirmation.",
    "Added answer_authority.site_fact_rule: site facts stated by the human enter as evidence of kind owner_statement, capped at medium confidence; human authority covers site choice and confirmation, not facts a gate reads. (ADU finding 4)",
    "Added S04.existing: existing structures, utilities, vegetation and access on the site, as context entities feeding the intervention zone, relations and rules. (ADU finding 8)",
    "Added S06.zones: which zones share a functional unit. (ADU finding 6)",
    # wiring
    "S00.never now also feeds S01, so 'never' statements filter alternatives. (ADU finding 7)",
    "dimension_in_range gained a basis parameter (net | gross), required for area and volume. (ADU finding 9)",
    "contains may hold zones; fits may apply to zones.",
    "All conditional 'required' values are machine-readable ('var != value'); S01.supply and S01.demand now read 'intensity != light'. (failure-run gap 6)",
    "evidence_model gained precedence_rule (a professional_confirmation item decides its claim; other items stay visible) and owner_statement confidence cap. (failure-run gap 2)",
    "S02 gained status_mapping and overall_precedence (prohibited > unresolved > conditional > permitted), and scenario_rule: a prohibited site kept under a human-requested rezoning, variance or mitigation scenario continues with screen_status under_scenario, blocked from geometry unless exploratory; the scenario is a blocking review item. Scenario rule is a default pending author confirmation. (failure-run gaps 3, 5)",
    "S01 gained decision_rules: proceeding against a confirmed_negative need claim sets project_status to exploratory. Default pending author confirmation. (failure-run gap 4)",
    "project_status propagation: any open library-gap assumption keeps the project exploratory.",
    "answer_authority.authorities.human text: 'human-confirmed site facts' replaced by site choice and confirmation, per site_fact_rule.",
    "Added stress test small_private_adu, invariants for library content, scope and inquiry granularity; updated next_steps and open questions; zones question moved to resolved_questions.",
]

# ------------------------------------------------------------------ document, changelog, history
prev_log = U.pop("changelog_from_0_5")
U["history"] = {"0.5.1": {"changelog": prev_log, "removed": U["changelog_removed"]}, **U["history"]}
U["document"]["version"] = "0.6"
U["document"]["supersedes"] = "0.5.1"
new = {}
for k, v in U.items():
    new[k] = v
    if k == "document":
        new["changelog_from_0_5_1"] = CHANGELOG
U = new
U["changelog_removed"] = []

# ------------------------------------------------------------------ answer authority
aa = U["answer_authority"]
aa["authorities"]["human"] = aa["authorities"]["human"].replace(
    "and human-confirmed site facts",
    "site choice and confirmation (site facts stated by the human enter as evidence, see site_fact_rule)")
assert "site_fact_rule" not in aa and "site_fact_rule" in aa["authorities"]["human"]
aa["site_fact_rule"] = ("A site fact stated by the human (flood zone, utilities, ground, existing structures) is recorded as "
                        "evidence of kind owner_statement with at most medium confidence. It reaches high confidence only "
                        "through a document or a professional confirmation. Human authority covers choosing and confirming "
                        "the site, not facts that a gate reads.")
aa["library_gap_rule"] = ("When a required domain_library value is missing because the library is absent or incomplete, the "
                          "AI may propose it as a visible assumption of kind library_gap. The human confirms it for the "
                          "project, then answers the generalization question (library_model.generalization). An open "
                          "library_gap assumption keeps project_status exploratory.")

# ------------------------------------------------------------------ feasibility module
inten = U["feasibility_module"]["intensity"]
inten["unknown_rule"] = ("An unknown trigger fact applies conservatively: the floor is never lowered by an unknown. A trigger "
                         "whose threshold only a library can set (size or cost above library threshold) may be asserted "
                         "false by the human when no library threshold exists; the assertion is a recorded assumption in "
                         "the strategic feasibility record.")
inten["trigger_fact_rule"] = ("A trigger may combine a fact (human or external_evidence) with a classification "
                              "(professional_review), e.g. 'care visits occur' and 'this is a regulated occupancy'. Until "
                              "classified, the trigger is unknown and the unknown_rule applies.")
inten["own_use_rule"] = {
    "rule": ("When the first lifecycle phase has beneficiary own_use, the human's stated need (S01.need) is the demand "
             "evidence at any depth, and existing supply means the beneficiary's own assets (stated as owner_statement "
             "evidence). Market evidence is not required."),
    "status": "default pending author confirmation"
}

# ------------------------------------------------------------------ pipeline
s00 = stage("S00")
question("S00.never")["feeds"] = ["S01", "S09"]
s00["questions"].append({
    "id": "S00.lifecycle_use",
    "q": "Which uses must the structure serve over its life, in which phases, and for whom?",
    "authority": "human", "required": True,
    "output": "list<lifecycle_phase>",
    "feeds": ["S01", "S02", "S05", "S10"]
})
s00["questions"].append({
    "id": "S00.triggers",
    "q": "Which feasibility trigger conditions apply to this project, as facts (public funding or ownership, regulated occupancy, size or cost, off-site impact, library triggers)?",
    "authority": "human", "required": True,
    "rule": "feasibility_module.intensity.trigger_fact_rule",
    "output": "list<trigger_fact>",
    "feeds": ["S01"]
})
s00["gate"] = "Purpose, success criteria, site mode, lifecycle use and trigger facts stated; library pinned or declared as a draft."

s01 = stage("S01")
question("S01.supply")["required"] = "intensity != light"
question("S01.demand")["required"] = "intensity != light"
question("S01.demand")["rule"] = "feasibility_module.intensity.own_use_rule"
s01["decision_rules"] = {
    "proceed_against_negative_need": ("If the human decides proceed while a need claim at S01 is confirmed_negative, "
                                      "project_status becomes exploratory and the gate is recorded as passed under "
                                      "exploratory status."),
    "status": "default pending author confirmation"
}

s02 = stage("S02")
question("S02.search_criteria")["required"] = "site_mode != given"
s02["status_mapping"] = {
    "pass_without_conditions": "permitted",
    "pass_with_conditions": "conditional",
    "unresolved": "unresolved",
    "fail": "prohibited",
    "note": "Category status follows evidence_model.gate_mapping of its claims: any confirmed_negative claim -> fail; any conflicting or insufficient claim, or no claim -> unresolved; otherwise pass."
}
s02["overall_precedence"] = ["prohibited", "unresolved", "conditional", "permitted"]
s02["scenario_rule"] = {
    "rule": ("A prohibited candidate kept under a human-requested rezoning, variance or mitigation scenario continues "
             "with screen_status under_scenario. It is blocked from geometry unless project_status is exploratory, and "
             "the scenario is a blocking professional-review item."),
    "status": "default pending author confirmation"
}

s04 = stage("S04")
s04["questions"].insert(0, {
    "id": "S04.existing",
    "q": "What already exists on the site: structures, utilities and connections, vegetation to keep or remove, access routes?",
    "authority": "external_evidence", "required": True,
    "rule": "answer_authority.site_fact_rule",
    "if_unknown": "explicit unknown; blocks the stages that need it",
    "feeds": ["S04.intervention_zone", "S08", "S09", "S12"]
})
question("S04.intervention_zone")["source"] = "S02.site_identity, S02.conditions and S04.existing"

s06 = stage("S06")
s06["questions"].append({
    "id": "S06.zones",
    "q": "Which zones share a functional unit, and which unit contains each zone?",
    "authority": "human", "required": False,
    "default": "domain_library.zone_types",
    "feeds": ["S07", "S08", "S11"]
})
s06["gate"] = "Every referenced unit, zone, role, group, and implicit function is declared; every zone is contained by exactly one unit."

# ------------------------------------------------------------------ ontology
O = U["ontology"]
O["site_candidate"]["screen_status_values"].append("under_scenario")
O["functional_unit"]["optional_fields"].append("zones")
O["evidence"]["kind_reserved"] = {
    "owner_statement": "A fact stated by the owner or client; confidence at most medium.",
    "professional_confirmation": "A confirmation by a qualified professional; decides its claim (evidence_model.precedence_rule)."
}
O["zone"] = {
    "definition": "A region inside a functional unit defined by an activity and its clearances (e.g. kitchen, sleeping and dining zones of a studio). Contained by exactly one functional unit.",
    "required_fields": ["id", "type", "within"],
    "optional_fields": ["equipment", "clearances"],
    "governing_relations": ["contains", "fits", "not_overlap"],
    "examples": ["sleeping_zone", "kitchen_zone", "dining_zone", "entry_zone", "berth_pocket", "loading_bay"],
    "ifc": "IfcSpatialZone"
}
O["lifecycle_phase"] = {
    "definition": "A period of use with its own beneficiary; the first phase justifies the intervention, later phases are retained options.",
    "required_fields": ["id", "use", "beneficiary", "start"],
    "optional_fields": ["end", "retained_option", "conditions"],
    "beneficiary_values": ["own_use", "third_party_known", "market", "public"]
}
O["trigger_fact"] = {
    "definition": "The fact and, where needed, the professional classification that decide one feasibility trigger.",
    "required_fields": ["condition", "value", "authority"],
    "optional_fields": ["classification", "classification_authority", "assumption", "source_ref"],
    "value_values": [True, False, None]
}
O["library_candidate"] = {
    "definition": "A value proposed during a library-gap inquiry that the human declared valid beyond one project. Becomes library content only through library curation.",
    "required_fields": ["id", "library", "path", "value", "scope", "source_instance", "basis", "status"],
    "scope_fields": ["domain", "jurisdiction", "climate"],
    "basis_values": ["single_instance", "multi_instance", "professional"],
    "status_values": ["proposed", "accepted", "rejected"]
}

# ------------------------------------------------------------------ relations
R = U["relation_vocabulary"]["relations"]
R["contains"]["object"] = "unit | zone | element"
R["fits"]["subject"] = "unit | zone"
R["dimension_in_range"]["params"]["basis"] = "net | gross | null (required when measure is area or volume)"

# ------------------------------------------------------------------ evidence model
em = U["evidence_model"]
em["precedence_rule"] = ("An evidence item of kind professional_confirmation decides the status of the claim it supports "
                         "or contradicts (supports -> confirmed_positive, contradicts -> confirmed_negative). All other items "
                         "remain listed and visible. Two professional confirmations in opposite directions leave the claim "
                         "conflicting.")
em["rules"].append("Evidence of kind owner_statement never exceeds medium confidence.")

# ------------------------------------------------------------------ inquiry model (new)
U["inquiry_model"] = {
    "principle": "The pipeline is executed as an inquiry: the engine returns the next applicable, unanswered question in causal order and evaluates each gate as soon as its inputs are complete.",
    "granularity": "One question, one authority, one value per step. A step never bundles questions with different authorities or different decisions.",
    "routing": {
        "human": "ask the human",
        "external_evidence": "collect evidence (search, documents supplied by the human); record kind, source, date and confidence",
        "professional_review": "record a review item stating what must be confirmed and by whom",
        "derived": "compute and show the result",
        "ai_generated": "propose; the human confirms where the question requires confirmation",
        "domain_library": "use the pinned library value; if missing, open a library-gap inquiry (library_model.library_gap)"
    },
    "answer_routing": "An answer given before its question is reached is recorded against its question id with the stage it was received in, and that question is not asked again. It is evaluated when its stage's gate runs.",
    "gate_preview": "A derived check may run as soon as its inputs exist, at the human's request or by the engine. Its result is informational until the owning stage is reached.",
    "conflicts": "Contradictory answers under human authority are put back to the human as a conflict question. The AI never chooses between them.",
    "ambiguity": "An answer that can be read two ways is confirmed with the human before it is recorded."
}

# ------------------------------------------------------------------ library model (new)
U["library_model"] = {
    "layers": ["protocol", "jurisdiction_overlay", "domain_library", "program_instance"],
    "layer_meaning": {
        "protocol": "universal logic; no domain or jurisdiction knowledge",
        "jurisdiction_overlay": "code obligations, editions, design magnitudes and land-use rules for a jurisdiction; read at S02 and S09; reusable across domain libraries",
        "domain_library": "building-type defaults: actor types, unit and zone types, default relations, scenarios, benchmarks",
        "program_instance": "one project's answers, assumptions and evidence"
    },
    "library_gap": {
        "steps": [
            "AI proposes a value for the missing library question as an assumption of kind library_gap",
            "human confirms or changes it for this project",
            "generalization question: valid for this project only, or valid within a scope (domain, jurisdiction, climate)",
            "scoped values become library_candidate records; project-only values stay in the instance"
        ],
        "status_effect": "any open library_gap assumption keeps project_status exploratory"
    },
    "generalization": {
        "question": "Is this value valid only for this project, or for every structure of this type within a scope?",
        "scopes": ["instance_only", "domain", "domain + jurisdiction", "domain + jurisdiction + climate"]
    },
    "code_obligations": "A requirement that comes from a code is never a library default. It enters at S09.codes as a rule with source_class code, edition and clause, scoped to its jurisdiction.",
    "curation": {
        "authority": "library editor (human), with professional_review for code-like or safety content",
        "rule": "Candidates are promoted only in a library release; never automatically. A candidate keeps its basis (single_instance until confirmed by further instances or a professional).",
        "release": "A library release is versioned and pinned by instances at S00.library."
    }
}

# ------------------------------------------------------------------ project status, library requirements, architecture
U["project_status"]["propagation"].append("Any open library_gap assumption keeps project_status exploratory.")
U["domain_library_requirements"]["must_define"].append("zone_types")
U["domain_library_requirements"]["must_not_define"].append("jurisdiction-specific code obligations (they belong in a jurisdiction overlay)")
U["software_architecture"]["jurisdiction_overlay"] = "Code obligations and land-use rules per jurisdiction; shared across domain libraries."
U["software_architecture"]["inquiry_engine"] = "Executes inquiry_model: next question, routing, gate previews, library-gap inquiries."

# ------------------------------------------------------------------ schema updates
sm = U["schemas"]["semantic_model"]
sm["lifecycle"] = "list<lifecycle_phase>"
sm["trigger_facts"] = "list<trigger_fact>"
sm["zones"] = "list<zone>"
sm["library_candidates"] = "list<library_candidate>"
U["schemas"]["strategic_feasibility_record"]["excluded_alternatives"] = "list<{option, reason, excluded_by}>"
U["question_record_schema"]["required"] = "true | false | machine-readable condition 'var != value' or 'var == value'"
for k in ("constrained_by", "source"):
    if k not in U["question_record_schema"]["optional"]:
        U["question_record_schema"]["optional"].append(k)

# ------------------------------------------------------------------ tests, invariants, questions, next steps
U["domain_stress_tests"]["small_private_adu"] = ("Does a backyard ADU with no library reach the design stages as exploratory "
                                                  "through library-gap inquiry, without market evidence?")
U["invariants"] += [
    "Library content is never created silently: every library value comes from a released library or a visible library-gap assumption.",
    "Every library candidate carries an applicability scope; code obligations belong to the jurisdiction layer, not to a domain library.",
    "One question, one authority, one value per inquiry step."
]
oq = U["open_questions_for_review"]
zq = "Should zones be a separate class or functional units with a zone role?"
oq.remove(zq)
U["resolved_questions"] = [{"question": zq, "answer": "Separate class, contained by exactly one functional unit (ontology.zone).",
                            "resolved_in": "0.6", "evidence": "ADU run: studio with kitchen, sleeping and dining zones in one unit"}]
oq += [
    "own_use_rule: is the human's stated need sufficient demand evidence at every depth, or only at light depth? (default: every depth)",
    "S01.decision_rules: should proceeding against a confirmed_negative need force exploratory status, or be allowed as a recorded override? (default: exploratory)",
    "S02.scenario_rule: is under_scenario the right status for a prohibited site kept under a human-requested scenario? (default: yes, blocked from geometry unless exploratory)",
    "Design events: are event types universal for a domain and only their magnitudes jurisdictional?"
]
U["next_steps"] = [
    "Rebuild the residential library and the 160 m2 house instance against v0.6 (light feasibility, given site).",
    "Continue the ADU inquiry (instance_adu_backyard) from S07 with the inquiry engine; first library curation round for residential_adu.",
    "Draft a Florida jurisdiction overlay from the ADU run (landing rule R311.3, heating requirement to confirm, Winter Garden ADU ordinance).",
    "Write a minimal bridge library; test system selection with topology and the deferred 'action' decision.",
    "Extend the checker to validate libraries and instances against schemas.semantic_model.",
    "Only then: topology candidate generation."
]

json.dump(U, open(dst, "w"), indent=2, ensure_ascii=False)
print(f"wrote {dst}: version {U['document']['version']}, {len(CHANGELOG)} changelog entries")
