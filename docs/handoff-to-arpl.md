# USG -> ARPL handoff

USG resolves intent. ARPL resolves production representation.

The handoff should occur only when USG has reduced the problem far enough that ARPL can decide what should exist operationally without changing the user's purpose.

## Minimum handoff fields

```json
{
  "parent_frame_reference": null,
  "entry_stage": "form",
  "resolved_stages": ["purpose", "functions", "relationships", "form", "validation"],
  "purpose": {},
  "constraints": [],
  "assumptions": [],
  "ambiguities": [],
  "acceptance_invariants": [],
  "required_resolution": null,
  "handoff_stage": "ARPL",
  "handoff_payload": {}
}
```

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
