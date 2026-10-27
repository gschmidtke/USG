# USG -> ARPL handoff

USG resolves intent. ARPL resolves production representation.

The handoff should occur only when USG has reduced the problem far enough that ARPL can decide what should exist operationally without changing the user's purpose.

## Minimum handoff fields

```json
{
  "parent_frame_reference": null,
  "entry_stage": "S11",
  "resolved_stages": ["S00", "S06", "S08", "S11", "S12"],
  "purpose": {},
  "constraints": [],
  "assumptions": [],
  "ambiguities": [],
  "acceptance_invariants": [],
  "required_resolution": null,
  "handoff_stage": "S14",
  "handoff_payload": {}
}
```

Stage values are protocol stage ids (S00–S20). `handoff_stage` is the first stage ARPL is expected to carry out (for a concept model typically `S14` geometry_generation).

## Boundary rule

USG may say:
- a wall must exist;
- what it separates;
- required dimensions or approximate proportions;
- required fire/acoustic/thermal performance;
- which relationships must remain intact;
- what must be true for the result to satisfy the purpose.

ARPL decides:
- whether the production object should be a native wall, family, direct shape, assembly, or other representation;
- reuse versus creation;
- production standards and authority;
- representation-specific validation;
- which downstream capability should implement it.

## Premise-gated return

Downstream evidence should return to USG only when it contradicts a premise USG relied on. API failures, transaction failures, or host-specific limitations should normally remain downstream unless they prove the intended function/form cannot be realized as specified.
