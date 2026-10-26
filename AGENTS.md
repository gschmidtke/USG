# USG for AI agents

USG means **Universal Spec Generator**. Its job is to resolve a human need into a sufficiently clear, software-neutral specification before production representation or API execution is chosen.

USG sits between reality-frame reasoning and production logic:

`3XFF -> USG -> ARPL -> capability lookup / typed operation -> execution`

## Core rule

Start at the **lowest already-resolved stage** that still preserves the parent purpose. Do not force every task to restart at Purpose when the user has already resolved higher stages.

## Resolution chain

1. Purpose
2. Actors
3. Functions
4. Capacity
5. Relationships
6. Physics
7. Context
8. Regulation
9. Performance
10. Form
11. Systems
12. Elements
13. Validation

Moving downward reduces the problem space. Each stage should resolve only what is needed to hand a sufficiently constrained problem to the next stage.

## What USG owns

USG owns:
- what problem is being solved;
- why it matters;
- who/what participates;
- what functions are required;
- required capacities and relationships;
- physical/context/regulatory constraints;
- required performance;
- enough form/system/element definition to express the intended outcome;
- acceptance invariants for downstream production.

USG does **not** own:
- which Revit family/system family/API call should be used;
- firm/project production standards once the intent is resolved;
- runtime transaction safety;
- tool-specific execution.

Those belong downstream.

## Evidence and approximation

When source material is incomplete, preserve the distinction between:
- `exact`: explicitly dimensioned or stated;
- `derived`: calculated from exact information without adding unsupported intent;
- `approximate`: design intent is clear but geometry/value is inferred proportionally;
- `observed`: presence or relationship is visible but usable geometry is not yet reliable;
- `ambiguous`: materially different interpretations remain;
- `unknown`: no useful information exists.

Architectural sketch rule:

**Dimensions override proportion. Proportion fills the gaps. User clarification resolves contradictions.**

Do not confuse uncertainty of measurement with uncertainty of intent. Approximate values are valid temporary specification content when they preserve clear design intent. Ask the user only when conflicting evidence or material ambiguity prevents a coherent decision.

## Output contract

A USG result should carry at least:
- `parent_frame_reference`
- `entry_stage`
- `resolved_stages`
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
