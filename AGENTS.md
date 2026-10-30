# USG for AI agents

USG means **Universal Structure Generation**. Its job is to resolve a human need into a sufficiently clear, software-neutral specification of a built structure before production representation or API execution is chosen: need first, geometry last.

USG sits between reality-frame reasoning and production logic:

`3XFF -> USG -> ARPL -> capability lookup / typed operation -> execution`

## Source of truth

The canonical protocol is the version named in `protocol/CURRENT` (currently `protocol/versions/USG_v0_12.json`). Everything in this file is a navigation aid. Where this file and the protocol disagree, the protocol wins; report the disagreement to the curator.

## If you are curating

Read `curation/LOG.md` before anything else: it records what has been curated, why and how, and what is still open. Then follow `CURATION.md`, and add your own entry to the log when you finish.

## If you discover new learning

If you are **not** explicitly acting as the USG Curator and you discover a failure, contradiction, missing case, improvement, or other potentially reusable learning:

1. Do not modify canonical USG content.
2. Write the observation as raw evidence under `inbox/<contributor>/<yyyy-mm-dd>-<short-topic>.<ext>`.
3. Preserve enough provenance and context for the observation to be understood or reproduced. A Markdown file is sufficient; sidecar metadata is optional.
4. Open a pull request containing only `inbox/**` material.
5. Stop. Normalization, classification, testing, patch design and canonical promotion belong to the USG Curator.

If you cannot write to the repository or open a pull request, return the prepared Inbox artifact to the user. Do not invent a different contribution workflow.

The minimum valid contribution is one raw file under `inbox/**`. See `CONTRIBUTING.md` for the detailed public contribution guide.

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

The machine-readable contract is `schema/usg-output.schema.json` (integration draft); `docs/handoff-to-arpl.md` explains it with an example that CI validates. Do not restate the fields elsewhere. In short, a USG result carries `schema_version`, `entry_stage` and `resolved_stages` (stage ids S00–S20), `purpose`, `assumptions`, `ambiguities`, `acceptance_invariants`, `handoff_stage` and `handoff_payload`, and may add `parent_frame_reference`, `constraints`, `required_resolution` and `evidence`. The pending proposal `docs/proposals/source-neutral-interpretation-handoff.md`, if approved, extends this same schema rather than adding a second one.

Downstream systems may refine representation but must not silently overwrite USG intent or acceptance invariants.

## Upstream correction

If downstream evidence contradicts a premise USG actually relied on, invalidate only the dependent USG conclusion and resume from the highest invalidated stage. Do not restart the full chain unless the parent purpose itself is no longer valid.
