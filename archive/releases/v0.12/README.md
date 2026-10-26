# USG – Universal Structure Generation, v0.12

Need first. Function before form. Geometry last.
The pipeline is an order of validity, not an order of work: explore freely, commit only what is valid.

## Contents
| File | Role |
|---|---|
| `USG_v0_12.json` | **Current protocol (source of truth)** |
| `USG_v0_11.json` … `USG_v0_5_1.json` | Previous versions, kept for the non-regression check and rebuild |
| `check_usg.py` | Protocol checker: self-consistency, governance, non-regression |
| `run_usg.py` | Instance runner: walks an instance through the pipeline and applies the gates |
| `usg_geometry.py` | Dependency-free geometry for the export checks (frame handedness, containment, zones, overlaps, distances) |
| `test_runner.py` | Mutation suite (97 tests) for the runner and protocol rules |
| `instances/` | Regression and stress instances (pinned to 0.12) |
| `patches/` | Patch and migration scripts that produced 0.6 to 0.12 |
| `drawings/` | Sandbox site plan, and the numeric site model generated from the encoded envelope (needs matplotlib and shapely) |

## Commands
    python3 check_usg.py USG_v0_12.json --previous USG_v0_11.json
    python3 run_usg.py USG_v0_12.json instances/<instance>.json   # exit 0 = valid and as expected
    python3 test_runner.py USG_v0_12.json
    python3 drawings/numeric_site_model.py instances/instance_adu_backyard.json

Rebuild from history (governance: patch, never rewrite):

    python3 patches/patch_0_6.py USG_v0_5_1.json USG_v0_6.json
    python3 patches/patch_0_7.py USG_v0_6.json USG_v0_7.json
    python3 patches/patch_0_8.py USG_v0_7.json USG_v0_8.json
    python3 patches/patch_0_9.py USG_v0_8.json USG_v0_9.json
    python3 patches/patch_0_10.py USG_v0_9.json USG_v0_10.json
    python3 patches/patch_0_11.py USG_v0_10.json USG_v0_11.json
    python3 patches/patch_0_12.py USG_v0_11.json USG_v0_12.json

## Status at 0.12
- 21 stages in 5 phases, 67 questions, 27 relations (21 structure, 6 decision), 27 ontology classes, 9 feedback loops, 6 universal feasibility triggers.
- Checker: 0 errors, 0 warnings against 0.11.
- Conformance: an implementation is USG-conformant only if it reproduces these instances' expected outcomes and passes the mutation suite.
- Instances:
  - `fail_no_need`: stops at S01, strategic_fail
  - `fail_all_sites_prohibited`: stops at S02, no_candidate_survives, FB7 to the human
  - `instance_adu_backyard`: exploratory; sandbox encoded as geometry in a right-handed frame; buildable envelope ≈ 3,051 sq ft (status: range); H-ADU-2 passes the export checks; stops at S07 (demand not yet asked); 7 library candidates
  - `stress_one_mile_city`: design ran ahead of a prohibited premise. Awareness ranks C-MINING first, strain is reported, the commitment to schematic is blocked, and the run stops at S02 via FB7. It carries 3 documented, expected violations: an incomplete feasibility record, and no strategy-level alternative (precursor or deferral) considered although delivery premise A-R1 is unresolved.
- Mutation tests: 97/97 pass, including a replay of an AI layout drawn outside the sandbox and against recorded answers, including Grok's attacks (the medium-confidence flood holds; self-review is capped).

## Three threads, one state (0.8)
- Design: `design_hypotheses`, each with the premises it presupposes.
- Inquiry: the next question (inquiry_model).
- Awareness: derived from open premises and unanswered questions, ranked dependents x severity, one per design turn.
- Blocking happens only at commitment points (phase transitions, acceptance, export, irreversible acts).

## Defaults pending author confirmation
- `feasibility_module.intensity.own_use_rule`
- `phase_model.commitment_rule.assumption_aging` (0.9)
- `awareness_model.ranking_status` (show-stopper first, 0.9)
- `S01.decision_rules` (proceed against a negative need -> exploratory)
- `S02.scenario_rule` (under_scenario status)

## Version path
- 0.5.1: the last version reviewed only as a document.
- 0.6: inquiry model, library-gap path, jurisdiction overlay, zones, lifecycle phases, trigger facts (from the backyard ADU run).
- 0.7: bootstrap and delivery check, regulatory absence as a claim, classification of "never" statements, no default by silence, enforced inquiry log (from the adversarial run).
- 0.8: validity order and phase model with commitment points; design hypotheses, awareness and strain; driver inquiry; statement types and pressure; open design variables; affected systems and value ledger; FB9 (from One Mile City and the design-agent discussion).

Each version's changelog and history are inside the JSON.
- 0.9: reviewer independence (interested review capped, author decision); evidence-backed delivery routes; deferred-risk never-rules; show-stopper ranking; assumption aging; conformance; failure scenarios and propagation graph; impact by scenario; environmental absorption; consent; novelty trigger and failure precedents; risk as a design generator (from the Grok and Zara reviews).
- 0.10: strategy-level alternatives (staged_precursor, defer_commitment) and the generation duty; need behind the need; program of linked instances with capabilities; means separation; context provision before system selection; closure levels derived from supply basis; by-product sinks; fiction is never evidence; strategy-pattern overlay declared (from the Mars stress-test delta).
- 0.11: the sandbox first. A site envelope (setbacks, separations, protected zones, existing elements, orientation, access, height), every value confirmed, assumed, exercise or range; no dimensioned layout outside it; every layout cites the answers it uses, and deviations go back to the human (from the ADU inquiry, 2026-10-12).
- 0.12: geometry becomes reproducible. A right-handed coordinate frame; a geometric authority hierarchy; envelope values encoded as geometry; a derived buildable envelope; generators never alter the envelope; automatic export checks; every export classified (concept or construction, hypothesis or candidate) with a sidecar manifest.
