# Purpose & Common-Sense Entry Check
Status: ACCEPTED WITH CURATOR AMENDMENTS (LOG-0026, 2026-11-05). Canonical in v0.13 (LOG-0027): `execution_model.entry_check` and one invariant.
Owner directive: 2026-11-05

Before full USG analysis, ask two questions:

1. **What is its purpose?** Determine the intended function of the object, relationship or action from available context.
2. **How does it align with common sense?** Check whether its geometry, position, behavior and relationships plausibly support that function.

When an obvious contradiction is found, identify it before selecting a tool operation. When purpose and relationships are clear, use the smallest sufficient reasoning path and verify the result. When uncertain or consequential, escalate to fuller USG analysis or authoritative evidence. Common sense is a plausibility check, not a substitute for codes, engineering verification, manufacturer instructions or design authority.

Example: roof-eave blocking intended to receive a sloped soffit must provide a suitable attachment face. Check its relationship to the actual soffit and rafter geometry rather than assuming horizontal placement is correct. Dimensions must describe their intended measured relationship; do not rotate all annotations indiscriminately.

Routing: USG determines functional plausibility; ARPL executes and verifies Revit operations; Standards is consulted only when a relevant governed convention already exists. Do not create a new standard for obvious functional reasoning.

Acceptance: lightweight, generalizable, source-aware, capable of escalating ambiguity and avoiding invented design intent. No canonical protocol promotion until curator review and checks.

## Curator review (LOG-0026)

**What is its purpose?** To stop an agent from executing a tool operation on an object before it has understood what the object is for. The proposal's own example shows the failure: an eave blocking placed horizontally although it has to receive a sloped soffit, and dimensions rotated together with geometry they do not measure.

**How does it align with common sense?** Well. It is USG's core thesis (function first, geometry second) applied at the scale of one object or one operation instead of a whole structure. It adds no stage and no authority.

**Overlap with v0.12:** S00 already asks the purpose of a new structure, and the Core rule already enters at the lowest resolved stage. Neither covers the moment *inside* work on an existing or partly resolved structure, before a single operation. The check fills that gap and nothing else.

**Amendments (applied in v0.13):**
1. **Purpose is read, never decided.** Reading the purpose of an object from context is a plausibility reading by the AI, not a human-authority decision. If the purpose of the structure itself is not stated or recorded, S00 applies as before; drivers and motives are never imputed (`driver_rule`).
2. **A contradiction is reported, not silently fixed.** When the check finds an obvious contradiction between purpose and geometry, position or relationships, the agent names it before choosing an operation. It changes a recorded human answer only through the existing consistency rule (`execution_model.consistency_rule`).
3. **Escalation triggers are named:** the purpose cannot be read from context; two readings remain plausible; the operation is hard to reverse; or the question touches codes, structure, life safety or a manufacturer's instruction (professional review).
4. **Placement:** an entry check in `execution_model`, plus one invariant. Not a stage, not a Standards requirement (as the proposal itself says).
