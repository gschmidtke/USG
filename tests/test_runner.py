"""Mutation tests for run_usg.py: each mutation must produce the violation or outcome it targets.

Usage: python3 test_runner.py USG_v0_5_1.json
"""
import copy, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from run_usg import Run

protocol_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "protocol/versions/USG_v0_12.json"
U = json.load(open(protocol_path, encoding="utf-8"))
FIX = ROOT / "conformance/instances"
A = json.load(open(FIX / "fail_no_need.json", encoding="utf-8"))
B = json.load(open(FIX / "fail_all_sites_prohibited.json", encoding="utf-8"))
C = json.load(open(FIX / "instance_adu_backyard.json", encoding="utf-8"))
M = json.load(open(FIX / "stress_one_mile_city.json", encoding="utf-8"))


def run(base, mutate):
    I = copy.deepcopy(base)
    mutate(I)
    return Run(U, I).run()


def ev(I, eid):
    return next(e for e in I["evidence"] if e["id"] == eid)


def cl(I, cid):
    return next(c for c in I["claims"] if c["id"] == cid)


def downgrade_b_env(I):
    ev(I, "E-B-ENV")["confidence"] = "medium"
    cl(I, "C-B-ENV")["status"] = "insufficient"
    rec = I["screen_records"][1]
    rec["categories"]["environmental"]["status"] = "unresolved"
    rec["overall_status"] = "unresolved"


def variance_a(I):
    I["screen_records"][0]["human_requested_scenario"] = {"kind": "variance", "authority": "human", "ref": "client 2026-10-01"}
    I["screen_records"][0]["overall_status"] = "under_scenario"


def confirm_c(I):
    I["site_candidates"][2]["confirmed_by"] = {"authority": "human", "decision": "confirmed"}


def manifest(I, hid):
    """A complete, honest concept-export manifest for a hypothesis (schemas.export_manifest)."""
    return {"protocol_version": U["document"]["version"], "instance": I["instance"]["id"],
            "subject": {"type": "design_hypothesis", "id": hid}, "class": "concept", "project_status": "exploratory",
            "coordinate_frame": I.get("coordinate_frame"), "controlling_geometry_ref": "owner_sketch",
            "envelope_inputs": [], "assumptions": [], "unresolved": [], "reviews_required": [],
            "checks": [{"check": c, "result": "pass"} for c in U["validation"]["export_checks"][:4]],
            "topology_validated": False, "statement": "Exploratory concept geometry. Not for construction."}


def has(r, text):
    return any(text in v for v in r.violations)


tests = [
    # --- A: strategic gate
    ("A1 exploratory decision passes S01 and carries status",
     A, lambda I: (I["strategic_feasibility_record"].update(decision="exploratory"),
                   I["answers"]["S01.decision"].update(value="exploratory")),
     lambda r: r.stop["stage"] != "S01" and r.project_status == "exploratory" and not r.reaches_geometry),
    ("A2 intensity below trigger floor is a violation",
     A, lambda I: (I["strategic_feasibility_record"].update(intensity="light"),
                   I["answers"]["S01.intensity"].update(value="light")),
     lambda r: has(r, "below the derived floor 'full'")),
    ("A3 recorded claim status is recomputed, not trusted",
     A, lambda I: cl(I, "C-NEED").update(status="confirmed_positive"),
     lambda r: has(r, "C-NEED: recorded status 'confirmed_positive' but evidence gives 'confirmed_negative'")),
    ("A4 unexpired 2019 study turns C-NEED conflicting",
     A, lambda I: ev(I, "E-DEM-3").pop("valid_until"),
     lambda r: r.claim_status["C-NEED"] == "conflicting"),
    ("A5 omitted comparison dimension is a violation",
     A, lambda I: I["strategic_feasibility_record"]["alternatives_decision_record"]["ALT-3"].pop("carbon"),
     lambda r: has(r, "ALT-3 omits ['carbon']")),
    ("A6 automatic winner in decision record is a violation",
     A, lambda I: I["strategic_feasibility_record"]["alternatives_decision_record"].update(winner="ALT-1"),
     lambda r: has(r, "automatic winner")),
    ("A7 human decision answered by AI is a violation",
     A, lambda I: I["answers"]["S01.decision"].update(authority="ai_generated"),
     lambda r: has(r, "S01.decision: answered by 'ai_generated'")),
    ("A8 only-build alternatives is a violation",
     A, lambda I: I["strategic_feasibility_record"].update(alternatives=[{"id": "ALT-3", "option": "new_build", "description": "x"}]),
     lambda r: has(r, "no non-build alternative")),
    # --- B: constraint screen
    ("B1 confirming SITE-C without a screen record is a violation",
     B, confirm_c,
     lambda r: has(r, "no constraint_screen_record for confirmed candidate SITE-C")),
    ("B2 professional status answered by AI is a violation",
     B, lambda I: I["answers"]["S02.status"].update(authority="ai_generated"),
     lambda r: has(r, "S02.status: answered by 'ai_generated'")),
    ("B3 medium-confidence wetland survey: SITE-B unresolved, blocked not dropped, run continues past S02",
     B, downgrade_b_env,
     lambda r: r.stop["stage"] != "S02" and ("SITE-B", "blocked") in r.ctx["survivors"] and not r.reaches_geometry),
    ("B4 same, exploratory: SITE-B continues as exploratory",
     B, lambda I: (downgrade_b_env(I), I.update(project_status="exploratory")),
     lambda r: ("SITE-B", "unresolved") in r.ctx["survivors"]),
    ("B5 human-requested variance: SITE-A under_scenario, blocked from geometry (real project)",
     B, variance_a,
     lambda r: ("SITE-A", "blocked") in r.ctx["survivors"] and r.stop["stage"] != "S02" and not r.violations),
    ("B6 recorded category status that contradicts claims is a violation",
     B, lambda I: I["screen_records"][1]["categories"]["heritage"].update(status="permitted"),
     lambda r: has(r, "heritage: recorded 'permitted' but claims give 'unresolved'")),
    ("B7 AI site outside search criteria is a violation",
     B, lambda I: I["site_candidates"][0].update(within_search_criteria=False),
     lambda r: has(r, "not declared within S02.search_criteria")),
    ("B8 search criteria answered when site_mode=given is a violation",
     B, lambda I: I["answers"]["S00.site_mode"].update(value="given"),
     lambda r: has(r, "answered although not applicable")),
    # --- 0.6 rules
    ("A9 proceed against confirmed_negative need forces exploratory (S01.decision_rules)",
     A, lambda I: (I["strategic_feasibility_record"].update(decision="proceed"),
                   I["answers"]["S01.decision"].update(value="proceed")),
     lambda r: r.project_status == "exploratory" and r.stop["stage"] != "S01"),
    ("B9 professional confirmation decides the conflicting heritage claim (precedence_rule)",
     B, lambda I: I["evidence"].append({"id": "E-B-HER3", "kind": "professional_confirmation", "source": "county archaeologist", "date": "2026-10-01",
                                        "confidence": "high", "supports": ["C-B-HER"], "contradicts": []}),
     lambda r: r.claim_status["C-B-HER"] == "confirmed_positive"),
    ("C1 ADU instance: draft library derives exploratory status",
     C, lambda I: None,
     lambda r: r.project_status == "exploratory" and r.stop["stage"] == "S07" and not r.violations),
    ("C2 library-gap value without human confirmation is a violation",
     C, lambda I: I["answers"]["S05.operating"].pop("confirmed_by"),
     lambda r: has(r, "S05.operating: library-gap value not confirmed by the human")),
    ("C3 owner_statement recorded as high confidence is a violation",
     C, lambda I: ev(I, "E-OWN-FLOOD").update(confidence="high"),
     lambda r: has(r, "owner_statement recorded as high")),
    ("C4 without own_use, standard depth needs demand evidence",
     C, lambda I: I["answers"]["S00.lifecycle_use"]["value"][0].update(beneficiary="market"),
     lambda r: r.stop["stage"] == "S01" and r.stop["reason"] == "required_answer_missing"),
    ("C5 library candidate without domain scope is a violation",
     C, lambda I: I["library_candidates"][0].update(scope={"jurisdiction": "Florida"}),
     lambda r: has(r, "LC-1: library_candidate scope has no domain")),
    ("C6 instance cannot accept its own library candidate",
     C, lambda I: I["library_candidates"][0].update(status="accepted"),
     lambda r: has(r, "acceptance is library curation")),
    ("C7 only library-dependent triggers may be asserted false as an assumption",
     C, lambda I: I["answers"]["S00.triggers"]["value"]["public assembly, regulated or high-risk occupancy"].update(value=False, assumption=True),
     lambda r: has(r, "only library-dependent triggers")),
    ("C8 explicit unknown that blocks its own stage stops the run there",
     C, lambda I: I["answers"]["S04.intervention_zone"].update(status="unknown", blocks_stage="S04"),
     lambda r: r.stop["stage"] == "S04"),
    ("C9 FEMA map (high) does not override the cap on the owner statement but confirms the claim",
     C, lambda I: I["evidence"].append({"id": "E-FEMA", "kind": "flood_map", "source": "FEMA NFHL", "date": "2026-10-10",
                                        "confidence": "high", "supports": ["C-FLOOD"], "contradicts": []}),
     lambda r: r.claim_status["C-FLOOD"] == "confirmed_positive"),
    # --- 0.7 rules (lessons from the adversarial run)
    ("D1 every delivery route self-dependent: bootstrap conflict back to the human at S01",
     C, lambda I: I["answers"]["S01.delivery"].update(value=[{"id": "R1", "means": "the vehicle the structure is built to receive", "depends_on": ["success_condition"]}]),
     lambda r: r.stop["stage"] == "S01" and r.stop["reason"] == "bootstrap_conflict" and r.stop["escalation"] == "human"),
    ("D2 one self-dependent and one independent route: run continues, dependency recorded",
     C, lambda I: I["answers"]["S01.delivery"]["value"].append({"id": "R2", "means": "delivered by the structure's own crane", "depends_on": ["self"]}),
     lambda r: r.stop["stage"] == "S07" and any("self-dependent" in n for n in r.notes)),
    ("D3 unclassified never statement is a violation",
     C, lambda I: I["answers"]["S00.never"]["value"].append("must never be loud"),
     lambda r: has(r, "unclassified statement")),
    ("D4 vacuous never statement not returned to the human is a violation",
     C, lambda I: I["answers"]["S00.never"]["value"].append({"statement": "must never become a restaurant", "class": "vacuous", "kept_by_human": False}),
     lambda r: has(r, "is vacuous and was not returned to the human")),
    ("D5 use restriction is accepted and routed to lifecycle checks",
     C, lambda I: I["answers"]["S00.never"]["value"].append({"statement": "must never become a short-term rental", "class": "use_restriction"}),
     lambda r: not r.violations and any("use restriction" in n for n in r.notes)),
    ("D6 human-authority value set by silence is a violation",
     C, lambda I: I["answers"]["S00.site_mode"].update(status="default_by_silence"),
     lambda r: has(r, "set by silence")),
    ("D7 inquiry step asking two questions is a violation",
     C, lambda I: I.update(inquiry_log=[{"step": 1, "asked": "S00.purpose"}, {"step": 2, "asked": ["S00.success", "S00.never"]}]),
     lambda r: has(r, "exactly one question id per step")),
    ("D8 one answer routed to several questions is allowed",
     C, lambda I: I.update(inquiry_log=[{"step": 1, "asked": "S00.purpose", "routed": ["S00.lifecycle_use"]}]),
     lambda r: not r.violations),
    ("D9 'no applicable regulation' without an evidenced claim is a violation",
     C, lambda I: I.update(jurisdiction_overlay={"basis": "none"}),
     lambda r: has(r, "absence of regulation asserted without an evidenced claim")),
    # --- 0.8 rules (One Mile City / design-agent model)
    ("E1 One Mile City as encoded: mining premise first, strain reported, schematic commitment blocked",
     M, lambda I: None,
     lambda r: r.awareness[0]["item"] == "C-MINING" and r.commit_results[0]["blocked"] and r.stop["stage"] == "S02"),
    ("E2 human-requested variance holds the negative premise: run continues, commitment passes as exploratory",
     M, lambda I: (I["screen_records"][0].update(human_requested_scenario={"kind": "treaty review scenario", "authority": "human"}, overall_status="under_scenario")),
     lambda r: r.stop["stage"] != "S02" and not r.commit_results[0]["blocked"]),
    ("E3 unresolved premise never passes export, even exploratory",
     M, lambda I: I.update(commitments=[{"point": "export", "hypotheses": ["H5"]}]),
     lambda r: r.commit_results[0]["blocked"]),
    ("E4 real project: unresolved premise blocks a phase transition",
     M, lambda I: (I.update(project_status="real", commitments=[{"point": "concept->schematic", "hypotheses": ["H5"]}]),
                   I["strategic_feasibility_record"].update(decision="proceed"), I["answers"]["S01.decision"].update(value="proceed"),
                   I["answers"]["S00.library"]["value"].update(status="released")),
     lambda r: r.project_status == "real" and r.commit_results[0]["blocked"]),
    ("E5 committing an ODV value before its decide_by phase is a violation",
     M, lambda I: I["commitments"][0]["hypotheses"].append("H2"),
     lambda r: has(r, "commits ODV-TAPER at 'concept->schematic' before its decide_by phase")),
    ("E6 a committed hypothesis fixing an open ODV early appears as strain",
     M, lambda I: next(h for h in I["design_hypotheses"] if h["id"] == "H2").update(status="committed"),
     lambda r: "odv_collapsed" in r.strain and has(r, "H2: commits ODV-TAPER")),
    ("E7 impact magnitude without baseline is a violation",
     M, lambda I: I["affected_systems"][0]["change"].update(magnitude="high"),
     lambda r: has(r, "AS-SEABED: impact claim without baseline")),
    ("E8 an aggregated value score is a violation",
     M, lambda I: I["value_ledger"][0].update(score=0.7),
     lambda r: has(r, "carries an aggregate 'score'")),
    ("E9 a constraint relaxable by a stakeholder is a violation",
     M, lambda I: I["statements"][0].update(statement_type="constraint"),
     lambda r: has(r, "ST-1: typed constraint but relaxable by SH-1")),
    ("E10 interests imputed by the AI are a violation",
     M, lambda I: I["answers"]["S00.drivers"]["value"][0].update(interests_source="ai_generated"),
     lambda r: has(r, "interests imputed by the AI")),
    ("E11 a premise that names nothing declared is a violation",
     M, lambda I: I["design_hypotheses"][0]["presupposes"].append("C-NOWHERE"),
     lambda r: has(r, "premise 'C-NOWHERE' is not a declared")),
    ("E12 retiring the mining hypotheses removes that strain and changes the awareness order",
     M, lambda I: [h.update(status="retired") for h in I["design_hypotheses"] if h["id"] in ("H1", "H3", "H4")],
     lambda r: "hypothesis_on_negative_claim" not in r.strain and r.awareness[0]["item"] != "C-MINING"),
    ("E13 an assumption carried past its phase appears as strain",
     M, lambda I: I.update(current_phase="schematic"),
     lambda r: "A-R1" in r.strain.get("assumption_past_phase", [])),
    ("E14 human-named site candidate in search_area is accepted (also_answerable_by)",
     M, lambda I: None,
     lambda r: not has(r, "S02.site_candidates: answered by")),
    # --- 0.9: Grok's attacks and Zara's failure/frontier rules
    ("F1 Grok attack: 20 medium-confidence items cannot pass a hard gate by volume",
     B, lambda I: I["evidence"].extend({"id": f"E-FL-{i}", "kind": "stakeholder_statement", "source": "x", "date": "2026-10-01",
                                        "confidence": "medium", "supports": ["C-A-LU"], "contradicts": []} for i in range(20)),
     lambda r: r.claim_status["C-A-LU"] == "confirmed_negative" and r.stop["reason"] == "no_candidate_survives"),
    ("F2 Grok attack: owner's self-review is capped and cannot confirm land use",
     C, lambda I: I["evidence"].append({"id": "E-SELF", "kind": "professional_confirmation", "source": "owner", "reviewer": "SH-1",
                                        "date": "2026-10-11", "confidence": "high", "supports": ["C-LU"], "contradicts": []}),
     lambda r: r.claim_status["C-LU"] == "insufficient" and r.strain.get("interested_review") == ["E-SELF"]),
    ("F3 an independent professional confirmation still decides the claim",
     C, lambda I: I["evidence"].append({"id": "E-PRO", "kind": "professional_confirmation", "source": "land-use attorney", "reviewer": "external",
                                        "date": "2026-10-11", "confidence": "high", "supports": ["C-LU"], "contradicts": []}),
     lambda r: r.claim_status["C-LU"] == "confirmed_positive"),
    ("F4 Grok attack: unverified 'independent' delivery route ranks as a show-stopper",
     M, lambda I: None,
     lambda r: [a["item"] for a in r.awareness[:2]] == ["C-MINING", "A-R1"] and r.awareness[1]["show_stopper"]),
    ("F5 unverified delivery premise blocks export",
     M, lambda I: I.update(commitments=[{"point": "export", "hypotheses": []}]),
     lambda r: r.commit_results[0]["blocked"] and "delivery premise A-R1 unresolved" in r.commit_results[0]["reasons"]),
    ("F6 design_rule never-statement without evaluable stage is a violation",
     C, lambda I: I["answers"]["S00.never"]["value"][0].pop("evaluable_stage"),
     lambda r: has(r, "design_rule without a valid evaluable_stage")),
    ("F7 late-evaluable never-rules surface as deferred risk",
     C, lambda I: None,
     lambda r: sum(a["state"].startswith("deferred_risk") for a in r.awareness) == 3),
    ("F8 an assumption past its until_phase blocks the phase transition, even exploratory",
     M, lambda I: I.update(commitments=[{"point": "concept->schematic", "hypotheses": ["H5"]}]),
     lambda r: r.commit_results[0]["blocked"] and any("assumption_aging" in x for x in r.commit_results[0]["reasons"])),
    ("F9 engineered containment removes the environmental-absorption strain",
     M, lambda I: I["flows"][0].update(containment="engineered"),
     lambda r: "environmental_absorption" not in r.strain),
    ("F10 an imposed burden appears as strain",
     M, lambda I: I["value_ledger"][2].update(consent="imposed"),
     lambda r: r.strain.get("imposed_burden") == ["V-SEABED"]),
    ("F11 novelty true without failure precedents is a violation",
     M, lambda I: I["answers"]["S00.triggers"]["value"][next(k for k in I["answers"]["S00.triggers"]["value"] if k.startswith("novelty"))].update(value=True),
     lambda r: has(r, "no failure precedents")),
    ("F12 novelty true with a failure precedent passes",
     M, lambda I: (I["answers"]["S00.triggers"]["value"][next(k for k in I["answers"]["S00.triggers"]["value"] if k.startswith("novelty"))].update(value=True),
                   I["evidence"].append({"id": "E-PREC-1", "kind": "failure_precedent", "source": "closed-loop habitat failure record",
                                         "date": "2026-10-11", "confidence": "medium", "supports": [], "contradicts": []}),
                   I["strategic_feasibility_record"].update(failure_precedents=["E-PREC-1"])),
     lambda r: not has(r, "no failure precedents")),
    ("F13 impact by scenario without baseline is a violation",
     M, lambda I: I["affected_systems"][2].update(change_by_scenario=[{"scenario": "SC-FAIL-1", "magnitude": "high"}]),
     lambda r: has(r, "AS-OCEAN: impact claim without baseline in scenario SC-FAIL-1")),
    ("F14 an unknown novelty trigger never lowers depth (ADU stays standard, no violation)",
     C, lambda I: None,
     lambda r: r.ctx.get("intensity") == "standard" and not r.violations),
    # --- 0.10: Mars stress-test delta
    ("G1 considering a precursor satisfies the generation duty",
     M, lambda I: I["strategic_feasibility_record"]["excluded_alternatives"].append(
         {"option": "staged_precursor", "reason": "not explored in the exercise; to be studied", "excluded_by": "human"}),
     lambda r: not has(r, "generation_duty")),
    ("G2 staged_precursor without 'enables' is a violation",
     M, lambda I: I["strategic_feasibility_record"]["alternatives"].append({"id": "ALT-3", "option": "staged_precursor", "description": "autonomous seed"}),
     lambda r: has(r, "ALT-3: staged_precursor must name what it enables")),
    ("G3 defer_commitment without a revisit trigger is a violation",
     M, lambda I: I["strategic_feasibility_record"]["alternatives"].append({"id": "ALT-4", "option": "defer_commitment", "description": "wait"}),
     lambda r: has(r, "ALT-4: defer_commitment must name a revisit_trigger")),
    ("G4 a planned precursor capability is an unresolved premise; demonstrated, it resolves",
     M, lambda I: (I.update(program={"enabled_by": [{"id": "CAP-SEED", "capability": "autonomous excavation and power", "provided_by": "seed instance", "status": "planned"}]}),
                   I["design_hypotheses"][0]["presupposes"].append("CAP-SEED")),
     lambda r: any(a["item"] == "CAP-SEED" and a["state"] == "unresolved" for a in r.awareness)),
    ("G5 a failed precursor capability is a negative premise that blocks commitment",
     M, lambda I: (I.update(program={"enabled_by": [{"id": "CAP-SEED", "capability": "x", "provided_by": "seed", "status": "failed"}]}),
                   I["design_hypotheses"][0]["presupposes"].append("CAP-SEED")),
     lambda r: r.commit_results[0]["blocked"] and any(h["premise"] == "CAP-SEED" for h in r.strain.get("hypothesis_on_negative_claim", []))),
    ("G6 a means typed as requirement without the human's declaration is a violation",
     M, lambda I: I["statements"].append({"id": "ST-4", "text": "build the city with drones", "statement_type": "requirement",
                                          "basis": "stakeholder_choice", "relaxable_by": None, "concerns": "means"}),
     lambda r: has(r, "ST-4: a means is typed preference")),
    ("G7 a means declared a requirement by the human is accepted",
     M, lambda I: I["statements"].append({"id": "ST-4", "text": "build the city with drones", "statement_type": "requirement",
                                          "basis": "stakeholder_choice", "relaxable_by": None, "concerns": "means", "declared_by": "human"}),
     lambda r: not has(r, "ST-4")),
    ("G8 a by-product flow without a sink is a violation",
     M, lambda I: I["flows"].append({"id": "F-SPOIL", "medium": "goods", "source": "excavation", "byproduct": True}),
     lambda r: has(r, "F-SPOIL: by-product flow without a declared sink")),
    ("G9 fiction recorded as evidence is a violation",
     M, lambda I: I["evidence"].append({"id": "E-FIC", "kind": "fiction", "source": "a novel", "date": "2011-06-15",
                                        "confidence": "low", "supports": [], "contradicts": []}),
     lambda r: has(r, "E-FIC: kind 'fiction' is never evidence")),
    ("G10 closure level is derived: stocked 40 days vs 28-day target and a locally produced route give survival",
     M, lambda I: (I.update(autonomy_target_days=28),
                   I["answers"]["S01.delivery"]["value"][0].update(critical=True, supply_basis="stocked", stock_duration_days=40),
                   I["answers"]["S01.delivery"]["value"][1].update(critical=True, supply_basis="locally_produced")),
     lambda r: r.closure_level == "survival"),
    ("G11 closure level reproductive only when every critical route is locally reproducible",
     M, lambda I: [rt.update(critical=True, supply_basis="locally_reproducible") for rt in I["answers"]["S01.delivery"]["value"]],
     lambda r: r.closure_level == "reproductive"),
    # --- 0.11: sandbox and consistency (ADU inquiry Q48-Q67)
    ("K1 replay of Zara's site plan: driveway east, path from the east, W/D moved, no human resolution",
     C, lambda I: I["design_hypotheses"].append({
         "id": "H-ZARA-1", "description": "Zara site plan (example)", "phase": "concept", "level": "geometric", "status": "exploring",
         "author": "ai_generated", "presupposes": [], "uses_answers": ["S04.access", "S06.zones"],
         "deviations": [{"question": "S04.access", "recorded": "vehicles via rear lane (west)", "proposed": "driveway east"},
                        {"question": "S04.access", "recorded": "pedestrians from the rear lane", "proposed": "path from the east driveway"},
                        {"question": "S06.zones", "recorded": "W/D in the kitchen (Q42)", "proposed": "W/D beside the closet"}]}),
     lambda r: sum("H-ZARA-1: deviates from" in v for v in r.violations) == 3),
    ("K2 a deviation resolved by the human is accepted",
     C, lambda I: I["design_hypotheses"][0]["deviations"].append(
         {"question": "S06.zones", "recorded": "W/D in the kitchen", "proposed": "W/D beside the closet", "resolved_by": "human", "resolution": "accepted (Q52)"}),
     lambda r: not r.violations),
    ("K3 an undefined envelope value forbids the layout and becomes a show-stopper",
     C, lambda I: I["site_envelope"]["setbacks"][1].update(status="undefined"),
     lambda r: has(r, "H-ADU-2: geometric hypothesis outside a defined sandbox: undefined ['setbacks']")
               and r.awareness[0]["item"] == "site_envelope.setbacks"),
    ("K4 a missing envelope field counts as undefined",
     C, lambda I: I["site_envelope"].pop("protected_zones"),
     lambda r: has(r, "undefined ['protected_zones']")),
    ("K5 a geometric hypothesis without a site envelope is a violation",
     C, lambda I: I.pop("site_envelope"),
     lambda r: has(r, "geometric hypothesis without a site envelope")),
    ("K6 concept-level hypotheses need no sandbox (One Mile City)",
     M, lambda I: None,
     lambda r: not has(r, "sandbox_rule")),
    ("K7 a geometric hypothesis citing no recorded answers is a violation",
     C, lambda I: I["design_hypotheses"][0].update(uses_answers=[]),
     lambda r: has(r, "cites no recorded answers")),
    ("K8 citing an answer that was never given is a violation",
     C, lambda I: I["design_hypotheses"][0]["uses_answers"].append("S07.demand"),
     lambda r: has(r, "uses S07.demand, which has no recorded answer")),
    ("K9 a range without min and max is a violation",
     C, lambda I: I["site_envelope"]["setbacks"][1].update(status="range", min=None) and None or I["site_envelope"]["setbacks"][1].pop("max"),
     lambda r: has(r, "a range needs min and max")),
    ("K10 resting on the favourable end of a range is reported",
     C, lambda I: None,
     lambda r: any("H-ADU-2: rests on the favourable end" in n for n in r.notes)),
    # --- 0.12: frame, encoding, buildable checks, exports
    ("L1 a left-handed frame (y = south) is a violation",
     C, lambda I: I["coordinate_frame"].update(y_axis="south"),
     lambda r: has(r, "frame is left-handed")),
    ("L2 geometric work without a declared frame is a violation",
     C, lambda I: I.pop("coordinate_frame"),
     lambda r: has(r, "no coordinate frame is declared")),
    ("L3 an envelope value without geometry does not bind and is a violation",
     C, lambda I: I["site_envelope"]["setbacks"][0].pop("geometry"),
     lambda r: has(r, "is not encoded as geometry")),
    ("L4 an AI drawing cannot be the controlling geometry",
     C, lambda I: I["site_envelope"].update(controlling_geometry_ref="ai_drawing"),
     lambda r: has(r, "not in the authority hierarchy")),
    ("L5 a valid concept export of the hypothesis passes",
     C, lambda I: I.update(exports=[{"file": "H-ADU-2.stl", "manifest": manifest(I, "H-ADU-2")}]),
     lambda r: not r.violations),
    ("L6 a hypothesis exported as construction geometry is a violation",
     C, lambda I: I.update(exports=[{"file": "x.stl", "manifest": dict(manifest(I, "H-ADU-2"), **{"class": "construction"})}]),
     lambda r: has(r, "a hypothesis export must be concept geometry") and has(r, "construction geometry requires")),
    ("L7 a footprint moved into the rear setback fails, and exporting it is a violation",
     C, lambda I: (I["design_hypotheses"][0].update(footprint=[[7, 54], [32.75, 54], [32.75, 69], [7, 69]]),
                   I.update(exports=[{"file": "x.stl", "manifest": manifest(I, "H-ADU-2")}])),
     lambda r: has(r, "exported although check failed: footprint inside the buildable envelope")
               and has(r, "manifest claims pass for 'footprint inside the buildable envelope'")),
    ("L8 a footprint over the trunk fails the no_structure check",
     C, lambda I: I["design_hypotheses"][0].update(footprint=[[15, 38], [40.75, 38], [40.75, 53], [15, 53]]),
     lambda r: any(x["check"].startswith("no intersection") and x["result"] == "fail" for x in r.export_results["H-ADU-2"])),
    ("L9 a footprint overlapping the main house fails",
     C, lambda I: I["design_hypotheses"][0].update(footprint=[[40, 40], [65.75, 40], [65.75, 55], [40, 55]]),
     lambda r: any(x["check"] == "no overlap with fixed existing elements" and x["result"] == "fail" for x in r.export_results["H-ADU-2"])),
    ("L10 a footprint on the parking reservation fails",
     C, lambda I: I["design_hypotheses"][0].update(footprint=[[5, 30], [30.75, 30], [30.75, 45], [5, 45]]),
     lambda r: any(x["check"].startswith("footprint inside") and "reserved area P1" in x["detail"] for x in r.export_results["H-ADU-2"])),
    ("L11 a manifest with the wrong project status is a violation",
     C, lambda I: I.update(exports=[{"file": "x.stl", "manifest": dict(manifest(I, "H-ADU-2"), project_status="real")}]),
     lambda r: has(r, "manifest says project_status 'real'")),
    ("G12 at full depth the need behind the need is required",
     A, lambda I: I["answers"].pop("S01.need_behind"),
     lambda r: r.stop["stage"] == "S01" and "S01.need_behind" in r.stop["detail"]),
]

fails = 0
for name, base, mut, ok in tests:
    r = run(base, mut)
    passed = bool(ok(r))
    fails += not passed
    st = r.stop or {}
    print(f"{'PASS' if passed else 'FAIL'}  {name}   [stop {st.get('stage')}:{st.get('reason')}, {len(r.violations)} violations]")
    if not passed:
        for v in r.violations:
            print("        " + v)
print(f"\n{len(tests) - fails}/{len(tests)} mutation tests pass")
sys.exit(1 if fails else 0)
