# USG for AI agents

USG means **Universal Structure Generator**. Its job is to resolve a human need into a sufficiently clear, software-neutral specification of a built structure before production representation or API execution is chosen: need first, geometry last.

USG sits at the upstream end of a broader AEC AI stack:

`USG -> TIVERIT BIM Standards -> ARPL -> GPS -> Revit Bridge -> ZEN / evidence`

3XFF frames this chain from above (reality frame and orientation); it is not a routing step.

Routing intent:
- **USG** resolves purpose, required outcome, constraints and acceptance invariants.
- **TIVERIT BIM Standards** governs normative requirements, authority, compliance and project/company standards.
- **ARPL** supplies professional Revit production precedent, known failures and verification logic.
- **GPS** (API capability lookup) determines what the relevant software/API can actually do. For Revit/API discovery, `https://github.com/autodesk-platform-services/dll2llm` is a useful external reference; it is not owned or governed by USG/TIVERIT and must never be treated as normative authority.
- **Revit Bridge** performs bounded Revit execution.
- **ZEN** may provide governed automation, verification, repair and evidence in supported workflows.

Capability evidence answers **can the tool do this?** It does not answer **should the project do this?** Do not use API documentation or GPS output to override USG intent, TIVERIT requirements, user authority or professional judgment.

## Silent cross-repository routing

The repository the user points to is an **entry point, not an authority shortcut**. Classify the user's actual question against the stack and use the layer that owns that question, even when the user entered through USG.

Route silently in the background:
- unresolved purpose, required outcome, success criteria -> USG;
- standards, permissions, roles, authority, BEP, CDE, naming, information requirements, acceptance or compliance evidence -> TIVERIT BIM Standards;
- professional Revit production technique, known failure modes or operational verification precedent -> ARPL;
- API capability -> authoritative API documentation / GPS;
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

The canonical protocol is the version named in `protocol/CURRENT` (currently `protocol/versions/USG_v0_13.json`). Everything in this file is a navigation aid. Where this file and the protocol disagree, the protocol wins; report the disagreement to the curator.

## Execution directive for AI agents

When USG owns the current question, **do not use this file as a summary to interpret loosely**. Resolve `protocol/CURRENT`, load the named canonical protocol, and execute that protocol as the governing interaction procedure before doing substantive project work.

In particular:

- Follow the canonical `inquiry_model` literally. Do not substitute the AI's normal conversational workflow for USG's workflow.
- Each inquiry step asks exactly **one question id**. When a human answer can legitimately satisfy several question ids, route that one answer through the canonical `answer_routing` mechanism; do not turn that exception into a bundled questionnaire.
- Ask the single highest-priority unresolved question required by the current stage, then stop and wait for the human answer before asking the next human-authority question.
- Do not bundle related questions, checklists, future-stage questions, or convenience prompts into one turn unless the canonical protocol explicitly permits it.
- Do not compress, reorder, skip, or anticipate required inquiry steps merely because several unknowns are visible at once.
- A form, technology, tool, or construction method named in the brief is a means statement unless the canonical protocol establishes otherwise; do not silently promote a proposed means into the project purpose or a hard requirement.
- Do not jump ahead to external research, regulatory screening, site geometry, layout, production precedent, or downstream execution merely because those activities could be useful. Reach them only when the canonical stage/gate logic makes them the current work.
- Derived previews and awareness items may be surfaced only as allowed by the canonical protocol; they do not authorize replacing the active inquiry step with a multi-question checklist.

### Retrieve before asking

Before asking the human the active question id, check whether it is **already answered on record**. The canonical basis is `inquiry_model.answer_routing`: an answer given before its question is reached is recorded against that question id and is not asked again. Clarification (LOG-0029):

1. **Where to look:** the confirmed answers of the current inquiry, and records the human has pointed to or the project already holds (governing documents, recorded decisions, accepted specifications). Looking up an existing record is not research; external research still waits for its stage and gate.
2. **What counts:** a record satisfies a **human-authority** question only when it states the answer and shows that the human, or the authority the human named, gave it: who, when and where, and it is not superseded. Facts found in records enter as evidence under `evidence_model` (an owner statement stays at most medium confidence); they never become a human decision.
3. **Record it:** route the answer to its question id with its source, mark it `already answered on record`, and move to the next unresolved question id. Do not ask it again.
4. **Ask only what is left:** if no record satisfies the question, ask exactly that one question id and stop (Turn-output constraint below). If records are ambiguous, stale or contradict each other, put the conflict to the human as one conflict question (`inquiry_model.conflicts`, `ambiguity`); the AI never chooses between them. A question about who holds authority goes to the owning authority, not to a guess.
5. **Never:** fabricate a record, treat an AI inference or a silence as an answer (`no_default_by_silence`), skip a stage gate because a later answer is already known, or apply the built-structure stage sequence to another domain and claim conformance.

### Turn-output constraint

For an unresolved human-authority inquiry step, the user-facing turn is constrained as follows:

1. Select exactly one canonical question id: the highest-priority unresolved question permitted by the active stage.
2. Ask only that question.
3. Do not append a second question, sub-question, checklist, alternative prompt, example list that asks for additional information, preview of later questions, or invitation to answer adjacent unknowns.
4. Do not ask for actors, decision authority, functions, success criteria, constraints, site facts, regulation, geometry, budget, schedule, or other information in the same turn unless that information is itself the single selected canonical question id.
5. After asking the selected question, **end the response and wait for the human answer**.

If explanatory context is necessary to make the selected question understandable, keep it declarative and minimal. It must not introduce another request for information.

A compliant turn therefore has this shape:

`<optional minimal context> + <one canonical question> + STOP`

A non-compliant turn includes any of the following after or around the selected question:

- "Who initiated it, who decides, and what does each person want?"
- "What should it provide—for example rental income, family housing, office use, or something else?"
- "Also tell me the budget, schedule, site constraints, and whether the proposed form is fixed."

Those may each correspond to legitimate later inquiries, but they must be asked only when their own canonical question id becomes active.

A correct USG response may therefore be only one short question. Completeness is achieved by executing the sequence faithfully, not by collecting every foreseeable answer in one turn.

## If you are curating

Read `curation/LOG.md` before anything else: it records what has been curated, why and how, and what is still open. Then follow `CURATION.md`, and add your own entry to the log when you finish.

## If you discover new learning

If you are **not** explicitly acting as the USG Curator and you discover a failure, contradiction, missing case, improvement, or other potentially reusable learning:

1. Do not modify canonical USG content.
2. Submit it through **STAR-T-GATE** (`STAR-T-GATE.json` → `public_intake`): POST it to the intake endpoint with target `USG`. Preserve enough provenance and context for the observation to be understood or reproduced.
3. If you have files to hand over and can open a pull request, you may instead write them under `inbox/<contributor>/<yyyy-mm-dd>-<short-topic>.<ext>` (a Markdown file is sufficient; sidecar metadata is optional) and open a pull request containing only `inbox/**` material.
4. Stop. Normalization, classification, testing, patch design and canonical promotion belong to the USG Curator.

If you can neither POST nor open a pull request, return the prepared submission to the user. Do not invent a different contribution workflow.

The minimum valid contribution is one raw file under `inbox/**`. See `CONTRIBUTING.md` for the detailed public contribution guide.

## Core rule

Start at the **lowest already-resolved stage** that still preserves the parent purpose. Do not force every task to restart at S00 when the user has already resolved higher stages. Always name stages by their protocol id (`S11`, `S14`, …), never by a free label.

### Purpose and common-sense entry check

Before a tool operation on an object, ask: **what is its purpose, and does its geometry, position, behaviour and relationships plausibly serve it?** Name an obvious contradiction before choosing the operation. A purpose read from context is a plausibility reading, never a human decision; when it cannot be read, when two readings remain, when the step is hard to reverse, or when codes, structure, life safety or manufacturer instructions are involved, escalate to the full USG reasoning or to the owning authority. Common sense is a plausibility check, never authority. See `docs/proposals/purpose-common-sense-entry-check.md` (accepted, LOG-0026; canonical in v0.13 as `execution_model.entry_check`).

## Stage model (v0.13: 21 stages, 5 phases)

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
- A design value the human designer states or confirms is a human-authority decision, not owner_statement evidence; the confidence cap and the geometric hierarchy apply to existing conditions only (`answer_authority.design_decision_rule`, v0.13). Source classes (exact, derived, approximate, user_accepted, observed, ambiguous, unknown, convention) map to authority and gate behaviour in `evidence_model.source_class_mapping`; numeric confidence only with `evidence_model.confidence_conversion`.

## Sketch reconstruction (proposal, not canonical)

`docs/proposals/architectural-sketch-reconstruction.md` proposes, for reconstructing a design from an architect's own sketch:

**Dimensions override proportion. Proportion fills the gaps. User clarification resolves contradictions.**

with the source classes `exact`, `derived`, `approximate`, `observed`, `ambiguous`, `unknown`. You may use them, labelled as proposal-based, when the user works from a sketch. How they relate to the canonical evidence model is still open: see `docs/proposals/evidence-class-mapping.md`. Do not confuse uncertainty of measurement with uncertainty of intent, and never present an approximate value as exact.

## Source adapters (proposal, not canonical)

`adapters/` holds readers for existing sources (models, drawing sets, scans) that turn them into evidence records before the stage model; see `adapters/README.md`. The first, `adapters/input-reading/`, is a proposal awaiting the owner's decision. An adapter never decides authority: the protocol does.

## Output contract

The machine-readable contract is `schema/usg-output.schema.json` (integration draft); `docs/handoff-to-arpl.md` explains it with an example that CI validates. Do not restate the fields elsewhere. In short, a USG result carries `schema_version`, `entry_stage` and `resolved_stages` (stage ids S00–S20), `purpose`, `assumptions`, `ambiguities`, `acceptance_invariants`, `handoff_stage` and `handoff_payload`, and may add `parent_frame_reference`, `constraints`, `required_resolution` and `evidence`. Since v0.13 a hand-off to a downstream target also carries a `handoff` record (`schemas.handoff`, `export_model.handoff_rule`): descent premises, build policy, approximate policy, pending-user items, target-independent acceptance with read-back, and optional `specified_products`.

Downstream systems may refine representation but must not silently overwrite USG intent or acceptance invariants.

## Upstream correction

If downstream evidence contradicts a premise USG actually relied on, invalidate only the dependent USG conclusion and resume from the highest invalidated stage. Do not restart the full chain unless the parent purpose itself is no longer valid.
