"""Self-consistency and non-regression checker for USG protocol documents.

Usage:
  python3 check_usg.py USG_v0_5.json
  python3 check_usg.py USG_v0_5.json --previous USG_v0_4.json

0.6 additions: governance changelog/history keys; for versions >= 0.6, machine-readable conditions,
inquiry routing, library model, zones, lifecycle, dimension basis, S02 status mapping, evidence
precedence, trigger rules, resolved questions; defaults pending author confirmation are listed.
0.7 additions: delivery routes and bootstrap rule, S00.never classification, no default by silence,
site mode rule, inquiry log, regulatory absence rule, reviewer designation, feasibility stage mapping.
0.8 additions: execution and phase model (coverage, order, commitment points and rule), design hypotheses,
stakeholders, ODVs, affected systems, value ledger, pressured_by, statement model, S00.drivers first,
strain report, loops from any stage (must escalate to the human), also_answerable_by authorities.
0.9 additions: reviewer independence, delivery premises, never evaluable stage, assumption aging, conformance,
failure scenarios and propagation graph, impact by scenario, environmental absorption, consent, novelty
trigger (kept before 'none of the above'), failure precedents and precedent overlay, risk-first resolution.
0.10 additions: alternative options in sync and with rules, program model, need_behind, generation duty,
bootstrap proposes precursors, means separation, S12.context_provision first, closure model, supply basis,
by-product rule, speculation rule (forbidden evidence kinds), strategy-pattern overlay.
0.11 additions: site_envelope schema and statuses, S04.intervention_zone output, sandbox and consistency rules,
design hypothesis levels, uses_answers and deviations, sandbox_first inquiry rule.
0.12 additions: coordinate frame (right-handed), geometric authority hierarchy, encoded envelope geometry,
derived buildable envelope, immutability, export checks, export model and manifest.
"""
import json, re, sys

args = sys.argv[1:]
path = args[0] if args and not args[0].startswith("--") else "USG_v0_5.json"
prev_path = args[args.index("--previous") + 1] if "--previous" in args else None
U = json.load(open(path))
errors, warnings, info = [], [], []

REQUIRED_SECTIONS = ["document", "core_thesis", "answer_authority", "pipeline", "ontology", "relation_vocabulary",
                     "rule_model", "topology_model", "physics", "geometry_model", "controlled_feedback_loops",
                     "conflict_detection", "validation", "schemas", "invariants"]
for s in REQUIRED_SECTIONS:
    if s not in U:
        errors.append(f"missing required section '{s}'")

# ---------------------------------------------------------------- stages and questions
stages = U["pipeline"]
ids = [s["id"] for s in stages]
idx = {s: i for i, s in enumerate(ids)}
if ids != sorted(ids):
    errors.append("stage ids not in order")
auth = set(U["answer_authority"]["authorities"])
review_classes = set(U.get("professional_review_classes", {}))
qids, qpos = set(), {}
for s in stages:
    for i, q in enumerate(s["questions"]):
        qpos[q["id"]] = (s["id"], i)
for s in stages:
    for q in s["questions"]:
        if q["id"] in qids:
            errors.append(f"duplicate question {q['id']}")
        qids.add(q["id"])
        if not q["id"].startswith(s["id"] + "."):
            errors.append(f"{q['id']} not prefixed by {s['id']}")
        if q["authority"] not in auth:
            errors.append(f"{q['id']}: unknown authority {q['authority']}")
        if "review_class" in q and q["review_class"] not in review_classes:
            errors.append(f"{q['id']}: unknown review_class {q['review_class']}")
        if q["authority"] == "professional_review" and review_classes and "review_class" not in q:
            warnings.append(f"{q['id']}: professional_review question without review_class")
        for f in q["feeds"]:
            if "." in f:  # same-stage question feed
                if f not in qpos:
                    errors.append(f"{q['id']}: feeds unknown question {f}")
                elif qpos[f][0] != s["id"]:
                    errors.append(f"{q['id']}: question feed {f} crosses stages")
                elif qpos[f][1] <= qpos[q["id"]][1]:
                    errors.append(f"{q['id']}: question feed {f} is not later in the stage")
            elif f not in idx:
                errors.append(f"{q['id']}: feeds unknown stage {f}")
            elif idx[f] <= idx[s["id"]]:
                errors.append(f"{q['id']}: feeds non-downstream stage {f}")
by_auth = {a: sum(q["authority"] == a for s in stages for q in s["questions"]) for a in sorted(auth)}
info.append(f"{len(stages)} stages, {len(qids)} questions")
info.append(f"by authority: {by_auth}")

# Dotted references to protocol sections (e.g. evidence_model.gate_mapping) must resolve
def resolve(ref):
    node = U
    for part in ref.split("."):
        if not isinstance(node, dict) or part not in node:
            return False
        node = node[part]
    return True
for s in stages:
    for q in s["questions"]:
        for key in ("rule",):
            if key in q and not resolve(q[key]):
                errors.append(f"{q['id']}: {key} '{q[key]}' does not resolve")
        if "constrained_by" in q:
            c = q["constrained_by"]
            if c not in qpos:
                errors.append(f"{q['id']}: constrained_by unknown question {c}")
            elif (idx[qpos[c][0]], qpos[c][1]) >= (idx[s["id"]], qpos[q["id"]][1]):
                errors.append(f"{q['id']}: constrained_by {c} is not answered earlier")
    if "executed_by" in s and s["executed_by"] not in U:
        errors.append(f"{s['id']}: executed_by '{s['executed_by']}' not defined")

# ---------------------------------------------------------------- loops
for lp in U["controlled_feedback_loops"]["loops"]:
    if lp["from"] == "any":
        if lp["to"] not in idx:
            errors.append(f"{lp['id']}: unknown target stage")
        if lp.get("escalation") != "human":
            errors.append(f"{lp['id']}: a loop from any stage must escalate to the human")
        continue
    if lp["from"] not in idx or lp["to"] not in idx:
        errors.append(f"{lp['id']}: unknown stage")
    elif idx[lp["to"]] >= idx[lp["from"]]:
        errors.append(f"{lp['id']}: not a backward loop")
info.append(f"{len(U['controlled_feedback_loops']['loops'])} feedback loops")

# ---------------------------------------------------------------- relations
rv = U["relation_vocabulary"]
rels = rv["relations"]
layers = set(rv.get("layers", {"structure": ""}))
inverses = {}
stage_words = {"strategic", "legal", "semantic", "topology", "geometry", "system", "final"}
for name, r in rels.items():
    missing = [k for k in ("definition", "inverse", "symmetric", "transitive", "earliest_stage") if k not in r]
    if missing:
        errors.append(f"relation {name}: missing {missing}")
        continue
    if r.get("layer", "structure") not in layers:
        errors.append(f"relation {name}: unknown layer {r.get('layer')}")
    if r["symmetric"] and r["inverse"]:
        errors.append(f"relation {name}: symmetric relations need no inverse")
    if r["inverse"]:
        if r["inverse"] in rels:
            errors.append(f"relation {name}: inverse '{r['inverse']}' collides with a base relation")
        if r["inverse"] in inverses:
            errors.append(f"inverse '{r['inverse']}' used twice")
        inverses[r["inverse"]] = name
    if not set(re.findall(r"[a-z]+", r["earliest_stage"])) & stage_words:
        errors.append(f"relation {name}: earliest_stage has no valid stage")
if "mapping_from_0_2" in rv:
    valid_targets = set(rels) | set(inverses) | {"flow", "force"}
    for old, new in rv["mapping_from_0_2"].items():
        if re.match(r"[a-z_]+", new).group(0) not in valid_targets:
            errors.append(f"mapping {old} -> {new}: target not defined")
by_layer = {l: sum(r.get("layer", "structure") == l for r in rels.values()) for l in sorted(layers)}
info.append(f"{len(rels)} relations {by_layer}, {len(inverses)} derived inverses")

# ---------------------------------------------------------------- ontology
onto = U["ontology"]
for c, d in onto.items():
    if "definition" not in d:
        errors.append(f"ontology {c}: no definition")
    if c not in ("rule",) and "required_fields" not in d:
        warnings.append(f"ontology {c}: no required_fields")
info.append(f"{len(onto)} ontology classes")

# ---------------------------------------------------------------- evidence model consistency
if "evidence_model" in U:
    em = U["evidence_model"]
    statuses = set(onto.get("claim", {}).get("status_values", []))
    if set(em["claim_status_rule"]) != statuses or set(em["gate_mapping"]) != statuses:
        errors.append("evidence_model statuses do not match ontology.claim.status_values")
    for st in ("insufficient", "conflicting"):
        if em["gate_mapping"].get(st, "").startswith("pass"):
            errors.append(f"evidence_model: '{st}' must not pass a gate")

# ---------------------------------------------------------------- 0.6 structures (checked when the version has them)
def vtuple(v):
    return tuple(int(x) for x in str(v).split("."))
V = vtuple(U["document"]["version"])
doc = U["document"]
if "supersedes" in doc:
    key = "changelog_from_" + doc["supersedes"].replace(".", "_")
    if key not in U:
        errors.append(f"governance: '{key}' missing for a version superseding {doc['supersedes']}")
    if doc["supersedes"] not in U.get("history", {}):
        warnings.append(f"governance: history has no entry for {doc['supersedes']}")
if V >= (0, 6):
    for s in ("inquiry_model", "library_model"):
        if s not in U:
            errors.append(f"missing required section '{s}' (0.6+)")
    # machine-readable required / when conditions
    cond_vars = {"site_mode", "intensity"}
    cond_re = re.compile(r"^(\w+) (!=|==) (\w+)$")
    for s in stages:
        for q in s["questions"]:
            for key in ("required", "when"):
                v = q.get(key)
                if v is None or isinstance(v, bool):
                    continue
                m = cond_re.match(str(v))
                if not m:
                    errors.append(f"{q['id']}: {key} '{v}' is not a machine-readable condition")
                elif m.group(1) not in cond_vars:
                    errors.append(f"{q['id']}: {key} uses unknown variable '{m.group(1)}'")
    # inquiry routing covers every authority
    routing = set(U.get("inquiry_model", {}).get("routing", {}))
    if routing != auth:
        errors.append(f"inquiry_model.routing {sorted(routing)} != authorities {sorted(auth)}")
    # library model
    lm = U.get("library_model", {})
    for layer in ("protocol", "domain_library", "program_instance"):
        if layer not in lm.get("layers", []):
            errors.append(f"library_model.layers missing '{layer}'")
    if set(lm.get("layers", [])) != set(lm.get("layer_meaning", {})):
        errors.append("library_model.layer_meaning does not match layers")
    lc = onto.get("library_candidate", {})
    if "scope" not in lc.get("required_fields", []):
        errors.append("ontology.library_candidate must require 'scope'")
    if not lm.get("generalization", {}).get("scopes"):
        errors.append("library_model.generalization has no scopes")
    # zones and lifecycle
    if "within" not in onto.get("zone", {}).get("required_fields", []):
        errors.append("ontology.zone must require 'within'")
    if "zone" not in rels["contains"]["object"]:
        errors.append("relation contains cannot hold zones")
    if "beneficiary" not in onto.get("lifecycle_phase", {}).get("required_fields", []):
        errors.append("ontology.lifecycle_phase must require 'beneficiary'")
    if "basis" not in rels["dimension_in_range"].get("params", {}):
        errors.append("dimension_in_range has no 'basis' parameter")
    # S02 status mapping consistent with site_candidate statuses
    s02 = next(s for s in stages if s["id"] == "S02")
    screen = set(onto["site_candidate"]["screen_status_values"])
    mapped = {v for k, v in s02.get("status_mapping", {}).items() if k != "note"}
    if not mapped <= screen:
        errors.append(f"S02.status_mapping targets {sorted(mapped - screen)} not in site_candidate.screen_status_values")
    if set(s02.get("overall_precedence", [])) != mapped:
        errors.append("S02.overall_precedence does not cover exactly the mapped statuses")
    if "scenario_rule" in s02 and "under_scenario" not in screen:
        errors.append("S02.scenario_rule present but 'under_scenario' is not a screen status")
    # evidence model
    if "precedence_rule" not in U.get("evidence_model", {}):
        errors.append("evidence_model.precedence_rule missing")
    for k in ("owner_statement", "professional_confirmation"):
        if k not in onto["evidence"].get("kind_reserved", {}):
            errors.append(f"ontology.evidence.kind_reserved missing '{k}'")
    # feasibility triggers
    levels = set(U["feasibility_module"]["intensity"]["levels"])
    for t in U["feasibility_module"]["intensity"]["triggers"]:
        if t.get("minimum") not in levels:
            errors.append(f"trigger '{t.get('condition')}': minimum not a valid level")
    for k in ("unknown_rule", "trigger_fact_rule"):
        if k not in U["feasibility_module"]["intensity"]:
            errors.append(f"feasibility_module.intensity.{k} missing")
    # resolved questions must carry an answer
    for r in U.get("resolved_questions", []):
        if not r.get("answer"):
            errors.append(f"resolved question without answer: {r.get('question')}")

if V >= (0, 7):
    dr = onto.get("delivery_route", {})
    if "depends_on" not in dr.get("required_fields", []):
        errors.append("ontology.delivery_route must require 'depends_on'")
    if not {"self", "success_condition"} <= set(dr.get("reserved_dependencies", [])):
        errors.append("ontology.delivery_route must reserve 'self' and 'success_condition'")
    if "bootstrap_rule" not in U["conflict_detection"]:
        errors.append("conflict_detection.bootstrap_rule missing")
    if not any("bootstrap" in c for c in U["conflict_detection"]["checks"]):
        errors.append("conflict_detection.checks has no bootstrap check")
    if "S01.delivery" not in qpos:
        errors.append("question S01.delivery missing")
    nv = next(q for s in stages for q in s["questions"] if q["id"] == "S00.never")
    cls = set(nv.get("classification", {}).get("classes", []))
    if cls != {"design_rule", "use_restriction", "vacuous", "unevaluable"}:
        errors.append(f"S00.never classification classes {sorted(cls)} incomplete")
    if cls and set(nv["classification"].get("meaning", {})) != cls:
        errors.append("S00.never classification meanings do not match classes")
    for k in ("no_default_by_silence", "site_mode_rule", "log"):
        if k not in U["inquiry_model"]:
            errors.append(f"inquiry_model.{k} missing")
    if "inquiry_log" not in U["schemas"]:
        errors.append("schemas.inquiry_log missing")
    if "regulatory_absence_rule" not in U["evidence_model"]:
        errors.append("evidence_model.regulatory_absence_rule missing")
    if "reviewer_designation" not in U["professional_review_classes"]:
        errors.append("professional_review_classes.reviewer_designation missing")
    fm = U["feasibility_model"]
    if "stage_questions" in fm and set(fm["stage_questions"]) != set(fm["stages"]):
        errors.append("feasibility_model.stage_questions does not cover exactly the feasibility stages")

if V >= (0, 8):
    for s in ("execution_model", "phase_model", "statement_model", "awareness_model", "driver_rule"):
        if s not in U:
            errors.append(f"missing required section '{s}' (0.8+)")
    pm = U.get("phase_model", {})
    phases = pm.get("phases", [])
    covered = [st for p in phases for st in pm.get("stages", {}).get(p, [])]
    if sorted(covered) != sorted(ids) or len(covered) != len(set(covered)):
        errors.append("phase_model.stages must cover every stage exactly once")
    if covered != [st for st in ids if st in covered]:
        errors.append("phase_model.stages out of pipeline order")
    for cp in pm.get("commitment_points", []):
        if "->" in cp:
            a, b = cp.split("->")
            if a not in phases or b not in phases or phases.index(b) != phases.index(a) + 1:
                errors.append(f"commitment point '{cp}' is not a transition between consecutive phases")
    for k in ("negative", "unresolved", "odv"):
        if k not in pm.get("commitment_rule", {}):
            errors.append(f"phase_model.commitment_rule.{k} missing")
    for c, req in (("design_hypothesis", "presupposes"), ("open_design_variable", "decide_by"),
                   ("affected_system", "baseline"), ("value_perspective", "burden"), ("stakeholder", "role")):
        if req not in onto.get(c, {}).get("required_fields", []):
            errors.append(f"ontology.{c} must require '{req}'")
    pb = rels.get("pressured_by", {})
    if pb.get("layer") != "decision" or pb.get("object") != "stakeholder":
        errors.append("relation pressured_by must be a decision-layer relation onto stakeholder")
    sm_ = U.get("statement_model", {})
    if "open_design_variable" not in sm_.get("statement_types", {}):
        errors.append("statement_model has no open_design_variable type")
    if "stakeholder_choice" not in sm_.get("basis_values", []):
        errors.append("statement_model.basis_values lacks stakeholder_choice")
    first_s00 = stages[0]["questions"][0]["id"]
    if first_s00 != "S00.drivers":
        errors.append(f"S00.drivers must be the first S00 question, found {first_s00}")
    if "S01.affected_systems" not in qpos:
        errors.append("question S01.affected_systems missing")
    if "value_rule" not in U["evidence_model"]:
        errors.append("evidence_model.value_rule missing")
    if "strain_report" not in U["schemas"]:
        errors.append("schemas.strain_report missing")
    if not any(lp["from"] == "any" for lp in U["controlled_feedback_loops"]["loops"]):
        errors.append("no premise-reopened loop from any stage")
    for s in stages:
        for q in s["questions"]:
            for a in q.get("also_answerable_by", []):
                if a not in auth:
                    errors.append(f"{q['id']}: also_answerable_by unknown authority '{a}'")

if V >= (0, 9):
    if "reviewer_independence" not in U["professional_review_classes"]:
        errors.append("professional_review_classes.reviewer_independence missing")
    if "interested" not in U["evidence_model"]["precedence_rule"]:
        errors.append("evidence_model.precedence_rule does not exclude interested reviewers")
    if "premises" not in onto["delivery_route"].get("optional_fields", []):
        errors.append("delivery_route has no 'premises'")
    nvq = next(q for s in stages for q in s["questions"] if q["id"] == "S00.never")
    if "evaluable_stage" not in nvq.get("classification", {}):
        errors.append("S00.never classification has no evaluable_stage")
    if "assumption_aging" not in U["phase_model"]["commitment_rule"]:
        errors.append("phase_model.commitment_rule.assumption_aging missing")
    if "conformance" not in U:
        errors.append("missing required section 'conformance' (0.9+)")
    if "failure" not in onto["scenario"].get("kind_values", []):
        errors.append("scenario kind 'failure' missing")
    if "failure_propagation" not in U["topology_model"]["graph_types"]:
        errors.append("graph type failure_propagation missing")
    if "change_by_scenario" not in onto["affected_system"].get("optional_fields", []):
        errors.append("affected_system has no change_by_scenario")
    if "environmental_absorption" not in U["conflict_detection"]:
        errors.append("conflict_detection.environmental_absorption missing")
    if "consent_values" not in onto["value_perspective"]:
        errors.append("value_perspective has no consent values")
    if not any(t["condition"].startswith("novelty") for t in U["feasibility_module"]["intensity"]["triggers"]):
        errors.append("universal novelty trigger missing")
    if U["feasibility_module"]["intensity"]["triggers"][-1]["condition"] != "none of the above":
        errors.append("'none of the above' must remain the last trigger")
    if "failure_precedent" not in onto["evidence"].get("kind_reserved", {}):
        errors.append("evidence kind failure_precedent missing")
    if "precedent_overlay" not in U["library_model"]["layers"]:
        errors.append("library_model has no precedent_overlay layer")
    if "consequence-reducing" not in U["conflict_detection"]["resolution_order"][0]:
        errors.append("resolution_order must start with a consequence-reducing design change")
    for k in ("interested_review", "environmental_absorption", "imposed_burden"):
        if k not in U["schemas"]["strain_report"]:
            errors.append(f"strain_report.{k} missing")

if V >= (0, 10):
    if set(U["alternatives_to_build"]["options"]) != set(onto["intervention_alternative"]["option_values"]):
        errors.append("alternatives_to_build.options and intervention_alternative.option_values differ")
    for o in ("staged_precursor", "defer_commitment"):
        if o not in onto["intervention_alternative"]["option_values"]:
            errors.append(f"alternative option '{o}' missing")
        if o not in onto["intervention_alternative"].get("option_rules", {}):
            errors.append(f"alternative option '{o}' has no option rule")
    if "program_model" not in U:
        errors.append("missing required section 'program_model' (0.10+)")
    if "S01.need_behind" not in qpos:
        errors.append("question S01.need_behind missing")
    gd = U["alternatives_to_build"].get("generation_duty", {})
    if not set(gd.get("strategy_level_options", [])) <= set(onto["intervention_alternative"]["option_values"]):
        errors.append("generation_duty names unknown strategy-level options")
    if "staged_precursor" not in U["conflict_detection"]["bootstrap_rule"]:
        errors.append("bootstrap_rule does not propose precursor alternatives")
    if "means_separation" not in U["inquiry_model"]:
        errors.append("inquiry_model.means_separation missing")
    s12q = next(s for s in stages if s["id"] == "S12")["questions"][0]["id"]
    if s12q != "S12.context_provision":
        errors.append(f"S12.context_provision must be the first S12 question, found {s12q}")
    cm = U.get("closure_model", {})
    if cm.get("order", [None])[0] != "none" or set(cm.get("order", [])[1:]) != set(cm.get("levels", {})):
        errors.append("closure_model.order must be 'none' followed by exactly the defined levels")
    if "supply_basis_values" not in onto["delivery_route"]:
        errors.append("delivery_route has no supply_basis values")
    if "byproduct_rule" not in U["conflict_detection"]:
        errors.append("conflict_detection.byproduct_rule missing")
    if "speculation_rule" not in U["evidence_model"]:
        errors.append("evidence_model.speculation_rule missing")
    if set(onto["evidence"].get("kind_forbidden", [])) & set(onto["evidence"].get("kind_reserved", {})):
        errors.append("an evidence kind is both reserved and forbidden")
    if "strategy_pattern_overlay" not in U["library_model"]["layers"]:
        errors.append("library_model has no strategy_pattern_overlay layer")

if V >= (0, 11):
    se = U["schemas"].get("site_envelope", {})
    if "undefined" not in se.get("status_values", []):
        errors.append("site_envelope.status_values must include 'undefined'")
    if set(se.get("status_values", [])) != set(se.get("status_meaning", {})):
        errors.append("site_envelope.status_meaning does not match status_values")
    for f in ("setbacks", "protected_zones", "existing_elements", "orientation_datum", "access_points"):
        if f not in se.get("fields", {}):
            errors.append(f"site_envelope has no field '{f}'")
    izq = next(q for s in stages for q in s["questions"] if q["id"] == "S04.intervention_zone")
    if izq.get("output") != "site_envelope":
        errors.append("S04.intervention_zone must output site_envelope")
    for k in ("sandbox_rule", "consistency_rule"):
        if k not in U["execution_model"]:
            errors.append(f"execution_model.{k} missing")
    dh = onto["design_hypothesis"]
    if set(dh.get("level_values", [])) != {"concept", "topological", "geometric"}:
        errors.append("design_hypothesis.level_values must be concept, topological, geometric")
    for f in ("level", "uses_answers", "deviations"):
        if f not in dh.get("optional_fields", []):
            errors.append(f"design_hypothesis has no '{f}'")
    if "resolved_by" not in dh.get("deviation_fields", []):
        errors.append("design_hypothesis.deviation_fields lacks resolved_by")
    if "sandbox_first" not in U["inquiry_model"]:
        errors.append("inquiry_model.sandbox_first missing")

if V >= (0, 12):
    gm_ = U["geometry_model"]
    cf = U["schemas"].get("coordinate_frame", {})
    for f in ("origin", "x_axis", "y_axis", "z_axis", "units", "elevation_datum"):
        if f not in cf:
            errors.append(f"coordinate_frame has no '{f}'")
    for k in ("frame_rule", "authority", "encoding_rule", "immutability_rule"):
        if k not in gm_:
            errors.append(f"geometry_model.{k} missing")
    if "right-handed" not in gm_.get("frame_rule", ""):
        errors.append("geometry_model.frame_rule must require a right-handed frame")
    hier = gm_.get("authority", {}).get("hierarchy", [])
    if not hier or hier[0] != "survey":
        errors.append("geometric authority hierarchy must start with 'survey'")
    se_ = U["schemas"]["site_envelope"]
    if "controlling_geometry_ref" not in se_:
        errors.append("site_envelope has no controlling_geometry_ref")
    if set(se_.get("geometry_types", {})) != {"point", "polygon", "circle", "halfplane"}:
        errors.append("site_envelope.geometry_types must be point, polygon, circle, halfplane")
    if "no_structure" not in se_.get("protected_zone_rules", []):
        errors.append("site_envelope.protected_zone_rules lacks no_structure")
    be = U["schemas"].get("buildable_envelope", {})
    if be.get("authority") != "derived":
        errors.append("buildable_envelope must have derived authority")
    order = re.findall(r"[a-z]+", be.get("status_rule", ""))
    if [s for s in order if s in se_["status_values"]] != ["confirmed", "assumed", "exercise", "range"]:
        errors.append("buildable_envelope.status_rule must order confirmed > assumed > exercise > range")
    if not U["validation"].get("export_checks"):
        errors.append("validation.export_checks missing")
    em_ = U.get("export_model", {})
    if set(em_.get("subjects", [])) != {"design_hypothesis", "geometric_candidate"} or \
            set(em_.get("classes", [])) != {"concept", "construction"}:
        errors.append("export_model subjects/classes incomplete")
    for f in ("subject", "class", "project_status", "coordinate_frame", "checks", "topology_validated"):
        if f not in U["schemas"].get("export_manifest", {}):
            errors.append(f"export_manifest has no '{f}'")
    if not any("adapts to the site envelope" in i for i in U["invariants"]):
        errors.append("immutability invariant missing")

# defaults awaiting the author's decision are listed, never silently final
def find_pending(node, path=""):
    if isinstance(node, dict):
        if node.get("status") == "default pending author confirmation":
            yield path
        for k, v in node.items():
            yield from find_pending(v, f"{path}.{k}" if path else k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from find_pending(v, f"{path}[{i}]")
pending = list(find_pending(U))
if pending:
    info.append(f"defaults pending author confirmation: {pending}")

# ---------------------------------------------------------------- non-regression against previous version
if prev_path:
    P = json.load(open(prev_path))
    removed_note = json.dumps(U.get("changelog_removed", []))
    def accounted(item):
        return item in removed_note
    for sec in P:
        if sec not in U and not sec.startswith("changelog") and not accounted(sec):
            errors.append(f"regression: section '{sec}' removed without changelog_removed entry")
    for c in P.get("ontology", {}):
        if c not in onto and not accounted(c):
            errors.append(f"regression: ontology class '{c}' removed")
    for r in P.get("relation_vocabulary", {}).get("relations", {}):
        if r not in rels and not accounted(r):
            errors.append(f"regression: relation '{r}' removed")
    prev_q = {q["id"] for s in P["pipeline"] for q in s["questions"]}
    for qid in sorted(prev_q - qids):
        if not accounted(qid) and not accounted(qid.split(".")[1]):
            errors.append(f"regression: question '{qid}' removed")
    for r, d in P.get("relation_vocabulary", {}).get("relations", {}).items():
        if r in rels and len(rels[r]) < len(d):
            errors.append(f"regression: relation '{r}' lost fields")
    for c, d in P.get("ontology", {}).items():
        if c in onto and len(onto[c]) < len(d):
            errors.append(f"regression: ontology class '{c}' lost fields")
    info.append(f"compared against {P['document']['version']}: "
                f"{len(qids - prev_q)} questions added, {len(prev_q - qids)} removed (all must be in changelog_removed)")

print(f"USG {U['document']['version']}")
print("INFO"); [print("  " + s) for s in info]
print("ERRORS"); [print("  " + s) for s in errors] or print("  none")
print("WARNINGS"); [print("  " + s) for s in warnings] or print("  none")
sys.exit(1 if errors else 0)
