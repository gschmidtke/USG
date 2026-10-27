# USG for AI agents

USG means **Universal Structure Generation**. Its job is to resolve a human need into a sufficiently clear, software-neutral specification of a built structure before production representation or API execution is chosen: need first, geometry last.

USG sits between reality-frame reasoning and production logic:

`3XFF -> USG -> ARPL -> capability lookup / typed operation -> execution`

## Source of truth

The canonical protocol is the version named in `protocol/CURRENT` (currently `protocol/versions/USG_v0_12.json`). Everything in this file is a navigation aid. Where this file and the protocol disagree, the protocol wins; report the disagreement to the curator.

## Core rule

Start at the **lowest already-resolved stage** that still preserves the parent purpose. Do not force every task to restart at S00 when the user has already resolved higher stages. Always name stages by their protocol id (`S11`, `S14`, …), never by a free label.

## Stage model (v0.12: 21 stages, 5 phases)

| Phase | Stages |
| --- | --- |
| concept | S00 purpose · S01 strategic_feasibility · S02 constraint_screen · S03 actors · S04 context · S05 scenarios · S06 functions |
| schematic | S07 capacity · S08 relations · S09 physics_and_regulation · S10 performance · S11 semantic_model · S12 topology_generation · S13 topology_validation |
| design_development | S14 geometry_generation · S15 system_sizing · S16 elements |
| technical_design | S17 independent_validation · S18 scoring · S19 human_acceptance · S20 export |

Each stage's purpose, output and gate are summarized in `core/stages.json` (generated from the protocol by `tools/build_stages.py`). Moving downward reduces the problem space. Each stage should resolve only what is needed to hand a sufficiently constrained problem to the next stage.

## What USG owns

USG owns:
- what problem is being solved and why it matters;
- who/what participates;
- what functions are required;
- required capacities and relationships;
- physical, context and regulatory constraints;
- required performance;
- enough topology/geometry/system/element definition to express the intended outcome;
- acceptance invariants for downstream production.

USG does **not** own:
- which Revit family, system family or API call should be used;
- firm/project production standards once the intent is resolved;
- runtime transaction safety;
- tool-specific execution.

Those belong downstream (ARPL).

## Evidence and authority (canonical)

- Every value has exactly one authority (`answer_authority`): human, domain_library, ai_generated, derived, professional_review, external_evidence. AI may propose assumptions but may not silently replace human or professional authority.
- Gates read claim status (`evidence_model`), never raw evidence: `confirmed_positive`, `confirmed_negative`, `conflicting`, `insufficient`. Low-confidence evidence never passes a hard gate; conflicting evidence is shown side by side, never averaged.
- Geometric authority (`geometry_model.authority`): survey > approved_site_plan > professional_drawing > owner_statement > owner_sketch. AI-generated drawings are never geometric authority.

## Sketch reconstruction (proposal, not canonical)

`docs/proposals/architectural-sketch-reconstruction.md` proposes, for reconstructing a design from an architect's own sketch:

**Dimensions override proportion. Proportion fills the gaps. User clarification resolves contradictions.**

with the source classes `exact`, `derived`, `approximate`, `observed`, `ambiguous`, `unknown`. You may use them, labelled as proposal-based, when the user works from a sketch. How they relate to the canonical evidence model is still open: see `docs/proposals/evidence-class-mapping.md`. Do not confuse uncertainty of measurement with uncertainty of intent, and never present an approximate value as exact.

## Output contract

A USG result should carry at least (integration draft: `schema/usg-output.schema.json`):
- `parent_frame_reference`
- `entry_stage` (a stage id S00–S20)
- `resolved_stages` (stage ids)
- `purpose`
- `constraints`
- `assumptions`
- `ambiguities`
- `acceptance_invariants`
- `required_resolution`
- `handoff_stage`
- `handoff_payload`

Downstream systems may refine representation but must not silently overwrite USG intent or acceptance invariants.

## Upstream correction

If downstream evidence contradicts a premise USG actually relied on, invalidate only the dependent USG conclusion and resume from the highest invalidated stage. Do not restart the full chain unless the parent purpose itself is no longer valid.
