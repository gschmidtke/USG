# USG for AI agents

USG means **Universal Structure Generation**. Its job is to resolve a human need into a sufficiently clear, software-neutral specification of a built structure before production representation or API execution is chosen: need first, geometry last.

USG sits at the upstream end of a broader AEC AI stack:

`USG -> TIVERIT BIM Standards -> ARPL -> API capability lookup -> Revit Bridge -> ZEN / evidence`

Routing intent:
- **USG** resolves purpose, required outcome, constraints and acceptance invariants.
- **TIVERIT BIM Standards** governs normative requirements, authority, compliance and project/company standards.
- **ARPL** supplies professional Revit production precedent, known failures and verification logic.
- **API capability lookup** determines what the relevant software/API can actually do. For Revit/API discovery, `https://github.com/autodesk-platform-services/dll2llm` is a useful external reference; it is not owned or governed by USG/TIVERIT and must never be treated as normative authority.
- **Revit Bridge** performs bounded Revit execution.
- **ZEN** may provide governed automation, verification, repair and evidence in supported workflows.

Capability evidence answers **can the tool do this?** It does not answer **should the project do this?** Do not use API documentation or API Navigator output to override USG intent, TIVERIT requirements, user authority or professional judgment.

## Silent cross-repository routing

The repository the user points to is an **entry point, not an authority shortcut**. Classify the user's actual question against the stack and use the layer that owns that question, even when the user entered through USG.

Route silently in the background:
- unresolved purpose, required outcome, success criteria -> USG;
- standards, permissions, roles, authority, BEP, CDE, naming, information requirements, acceptance or compliance evidence -> TIVERIT BIM Standards;
- professional Revit production technique, known failure modes or operational verification precedent -> ARPL;
- API capability -> authoritative API documentation / API capability lookup;
- execution -> the user's authorized bridge/add-in/runtime;
- supported governed automation, repair or verification -> ZEN where applicable.

User-facing behavior:
- answer the user's question directly and helpfully;
- do **not** require the user to re-point the AI at another repository merely because another layer owns the answer;
- do not lead with repository names, object IDs, file paths or routing mechanics unless they help the user;
- surface provenance, governing objects or layer boundaries when the user asks, when authority is challenged, when sources conflict, or when uncertainty materially affects the answer;
- never hide a conflict that requires a user or professional decision.

Example: if a user points the AI at USG and asks who may approve a model, silently consult the TIVERIT governance layer and answer the approval question. If the user asks how to perform a Revit operation, silently consult ARPL and then capability evidence as needed.

Silent routing never invents project facts, never converts proposals into confirmed requirements, and never lets tool capability or prior success create normative authority.

## Source of truth

The canonical protocol is the version named in `protocol/CURRENT` (currently `protocol/versions/USG_v0_12.json`). Everything in this file is a navigation aid. Where this file and the protocol disagree, the protocol wins; report the disagreement to the curator.

## If you are curating

Read `curation/LOG.md` before anything else: it records what has been curated, why and how, and what is still open. Then follow `CURATION.md`, and add your own entry to the log when you finish.

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

Firm/project standards belong to the TIVERIT BIM Standards layer. Revit production precedent belongs to ARPL. API capability and execution remain further downstream.

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
