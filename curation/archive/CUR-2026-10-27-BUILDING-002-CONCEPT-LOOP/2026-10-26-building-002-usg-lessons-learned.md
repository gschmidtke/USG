# USG Lessons Learned — Building 002

Source: session of 2026-10-26 (Gottfried Schmidtke with Claude). Original document: "USG Lessons Learned — Building 002" (Claude Docs). This is the submitted text, kept as the curation source.

## Context

Spec `Building_002_Neutral_Spec_v0.1.json` was reconstructed from one hand sketch (plan + perspective) and user confirmations, handed off at S11 → S14, and used to generate a Revit concept model through the Revit API. It was right on the hard numbers but wrong or silent on nine items that define the design. Corrections came from four review steps: attaching the sketch with its confirmations, then three visual reviews of the model by the designer.

## Divergences

| Item | Spec v0.1 said | Actual design intent | Error type |
| --- | --- | --- | --- |
| Upper box placement | On top of the lower box; footprint null | 10 × 7 m, overlapping the lower box and extending beyond it, on 4 columns ground to roof | Topology lost |
| Upper columns | Coordinates null | Run 0 → roof, not 3000 → roof | Vertical extent not captured |
| Upper roof form | "Sloping roof" (observed) | Flat | Perspective convergence read as slope |
| 1 m overhang | Lower flat roof | Upper flat roof; lower box has no overhang | Dimension bound to the wrong host |
| Glazing module | 1000 mm, exact, user-confirmed | "~1,5 m segments" | Wrong value at the highest evidence class |
| Lower facade | Large glazed openings | Solid frame with recessed floor-to-head glazing | Composition not modelled |
| Railing | Present, height null | Three horizontal rails on sparse posts | Typology not captured |
| Stair | Location only | 1.0 m wide, +x, max 8 risers per flight, then landing | Rule not in the spec |
| "1,0 m" by the stair | Not interpreted | Stair width | Label not anchored |

## Lessons

1. The hard numbers were never the problem; the errors sat in topology, form and composition.
2. A neutral spec must not drop the source.
3. Every dimension needs a host.
4. "Exact" can be wrong: `~` must force approximate; source/confirmation conflicts must be raised.
5. Perspective is not geometry: roof form from a perspective is ambiguous until confirmed.
6. Describe facades as solid and void, not as glazing.
7. Element typology matters as much as presence.
8. Function-first rules (the stair rule) beat geometry.
9. Visual review is the fastest validator; a fixed checklist would find all error classes in one pass.
10. Accepted is its own evidence class (`user_accepted`).

## Proposed changes for v0.2 of the spec format

`user_accepted` class; `~` → approximate; conflict rule; `host` and `edges` on dimensions; plan topology (column markers, volume relations, vertical extent); `source_artifacts`; roof `form` separate from pitch; `facades[*]`; `typology` on guards and stairs; `constraints` on functional elements; `annotations[*]`; a review checklist before acceptance.
