# Building 002: sketch → neutral spec → concept model → corrections

A complete loop on a second, substantially different hand sketch (after Building 001). A neutral spec (v0.1) was reconstructed from the sketch, used to generate a Revit concept model through the API, and corrected over three designer reviews of that model. The corrected spec is v0.2.

The hard numbers survived every review unchanged: lower box 10 × 8 m, level 3000, roof top 6000 and 300 × 300 columns. The errors were in topology, form and composition, where the design intent lives.

## Files

| File | What it is |
| --- | --- |
| `source/sketch.jpg` | Designer's hand sketch: plan and perspective on one sheet |
| `spec/Building_002_Neutral_Spec_v0.1.json` | Spec as handed off, unchanged |
| `spec/Building_002_Neutral_Spec_v0.2.json` | Spec after review; adds hosts, facades, guards typology, stair constraints, annotation anchors, source artifacts and the proposed `user_accepted` class |

## Where v0.1 diverged from design intent

| Item | v0.1 | Design intent (v0.2) | Error type |
| --- | --- | --- | --- |
| Upper box placement | On top of the lower box; footprint null | 10 × 7 m, overlapping the lower box and extending beyond it, on 4 columns from ground to roof | Topology lost: plan column markers seen but not encoded |
| Upper columns | Coordinates null | Run L1 → roof underside, not L2 → roof | Vertical extent not captured |
| Upper roof form | "Sloping roof" (observed) | Flat | Perspective convergence read as slope |
| 1 m overhang | Bound to the lower flat roof | Belongs to the upper roof; lower box has no overhang | Dimension bound to the wrong host |
| Glazing module | 1000 mm, "exact", user-confirmed | "~1,5 m segments" as written on the sketch | Wrong value carried at the highest evidence class |
| Lower facade | "Large glazed openings" | Solid frame (corner piers, head band) with recessed floor-to-head glazing | Solid/void composition not modelled |
| Railing | Present, height null | Three horizontal rails on sparse posts | Typology not captured |
| Stair | Location only | 1.0 m wide, rising +x along the top edge, max 8 risers per flight, then landing | Functional rule not in the spec |
| "1,0 m" by the stair | Not interpreted | Stair width | Label not anchored to an element |

## Lessons for USG

1. A neutral spec must travel with its source (`source_artifacts`) or encode plan topology explicitly.
2. Every dimension needs a host element and, where relevant, the edges it applies to.
3. "Exact" can be wrong: `~` on the source must force `approximate`, and a conflict between source and confirmation must be raised.
4. Roof form read from a perspective alone is `ambiguous` until confirmed.
5. Describe facades as solid and void (`facades[*].composition`), not as "glazing present".
6. Record element typology (railing, stair), not only presence.
7. Function-first constraints (the stair rule) let a generator derive the whole element; capture them as `constraints`.
8. Visual review of a generated model found one error class per review; a fixed checklist would find them in one pass: placement → roof form → overhangs → facade composition → guards → stair.
9. AI estimates accepted by the designer need their own class (`user_accepted`); see `docs/proposals/evidence-class-mapping.md`.

Production-side lessons (Revit API, timeouts, type semantics, dependent heights) were filed with ARPL, not here.

## Status

Example and evidence for the proposals in `docs/proposals/`. Not canonical protocol. The v0.2 spec format is described by the draft `schema/neutral-building-spec.schema.json`.
