# USG Lessons Learned — Building 002

**Date:** 2026-10-26/27  
**Contributor:** Gottfried Schmidtke via Claude/Revit reconstruction session  
**Type:** downstream reconstruction review + neutral-spec failure analysis

## Context

The spec `Building_002_Neutral_Spec_v0.1.json` was right on the hard numbers but wrong or silent on nine items that define the design. A second AI rebuilding from the JSON alone would have produced a recognisably different building.

The spec was reconstructed from one hand sketch (plan + perspective on one sheet) and user confirmations, and handed off at stage S11 → S14. It was then used to generate a Revit concept model. Each correction below came from one of four review steps: attaching the sketch with its confirmations, then three visual reviews of the model by the author.

## Where the spec diverged from design intent

| Item | Spec v0.1 said | Actual design intent | Error type |
|---|---|---|---|
| Upper box placement | On top of the lower box; footprint null, approximate | 10 × 7 m, overlapping the lower box and extending beyond it to the right, on 4 columns from ground to roof | Topology lost: plan column markers were seen but not encoded |
| Upper columns | Upper-box corners, coordinates null | Run 0 → roof, not 3000 → roof | Vertical extent not captured |
| Upper roof form | Sloping roof (observed) | Flat | Perspective convergence read as slope |
| 1 m overhang | `ROOF_LOWER_01`, flat roof | Belongs to the upper flat roof; the lower box has no overhang | Dimension bound to the wrong host |
| Glazing module | 1000 mm, exact, user-confirmed | ~1.5 m segments as written on the sketch | Wrong value carried at the highest evidence class |
| Lower facade | Large ground-level glazed openings | Solid frame (corner piers, head band) with recessed, floor-to-head glazing | Composition (solid vs void) not modelled |
| Railing | Present, height null | Three horizontal rails on sparse posts | Typology not captured |
| Stair | Location only; width, run, direction null | 1.0 m wide, rising in +x along the top edge, max 8 risers per flight, then landing | Rule existed in the author's head, not in the spec |
| "1.0 m" by the stair | Not interpreted | Stair width | Label not anchored to an element |

## Lessons for the protocol

1. **The hard numbers were never the problem.** Lower box 10 × 8 m, level 3000, roof top 6000 and 300 × 300 columns all survived unchanged. The errors sat in topology, form and composition, which is where the design intent lives.
2. **A neutral spec must not drop the source.** Without the sketch the generator placed the upper box on top of the lower box. The sketch fixed it at once. Either the source image travels with the spec, or plan topology must be encoded explicitly.
3. **Every dimension needs a host.** "Flat roof overhang 1000" was right as a value and wrong as an attribution. A value without a binding to an element (and an edge) is ambiguous.
4. **"Exact" can be wrong.** The glazing module was carried as exact and user-confirmed at 1000, while the sketch says ~1.5. A `~` on the source should force the approximate class, and a conflict between source and confirmation should be raised, never resolved silently.
5. **Perspective is not geometry.** Converging lines were read as a sloping roof by the spec author and again by the generator. Roof form from a perspective should be classed ambiguous until confirmed.
6. **Describe facades as solid and void, not as glazing.** "Glazing present, 1 m modules" lost the frame, the piers, the head band and the recess, which define the building's character.
7. **Element typology matters as much as presence.** "Railing present" produced a baluster railing; the design is a horizontal-rail railing.
8. **Function-first rules beat geometry.** The stair rule (1.0 m wide, max 8 risers per flight, then landing) was enough for the generator to derive the whole stair. USG should capture such rules as constraints.
9. **Visual review is the fastest validator.** Each review of the 3D model exposed one class of error within a minute. A structured review checklist would have found them in one pass.
10. **Accepted is its own evidence class.** Proportional estimates (600 mm piers, 2400 head, rail heights) were accepted by the author without becoming source facts. The spec needs a class for that.

## Proposed changes for curator consideration

| Change | Candidate location | Fixes |
|---|---|---|
| Add evidence class `user_accepted` (value proposed by AI, accepted by author, with date) | evidence model / schema | Lesson 10 |
| Map `~`, `ca.` and similar source notation to `approximate`, whatever the confirmation | source interpretation rule | Lesson 4 |
| Conflict between source annotation and confirmation remains unresolved and is raised to the author | source interpretation rule | Lesson 4 |
| Every dimension carries `host` and, where relevant, `edges` | dimension/value record | Lesson 3 |
| Encode plan topology: column markers with approximate coordinates, relation to other volumes, vertical extent | topology / relationships | Lessons 1–2 |
| `source_artifacts`: source image or resolvable hash/location travels with the spec | handoff/project | Lesson 2 |
| Roof `form` separate from pitch; form from perspective-only evidence defaults to ambiguous | roof semantics | Lesson 5 |
| Facade block per face: composition, piers, head band, sill, recess, glazing layout | new facade semantics | Lesson 6 |
| `typology` on railings, stairs and similar elements | element semantics | Lesson 7 |
| Functional constraints on elements, e.g. stair width/max risers/landing | element constraints | Lesson 8 |
| Annotation anchors: sketch label tied to element ID with interpretation | annotations | Stair 1.0 m label |
| Review checklist before acceptance: massing/placement → roof form → overhangs → facade composition → railings → stair | acceptance/review | Lesson 9 |

## Corrected Building 002 facts

The corrected facts belong in `Building_002_Neutral_Spec_v0.2.json`:

- upper roof is flat;
- the 1 m overhang belongs to the upper roof;
- the lower box has no overhang;
- upper box is 10 × 7 m;
- upper box overlaps the lower box and extends to the right;
- upper-box corner columns run from ground to roof;
- glazing is approximately 1.5 m in equal panels;
- lower facade is a solid frame with recessed floor-to-head glazing;
- railing is three horizontal rails on sparse posts;
- stair is 1.0 m wide, rises in +x along the top edge, maximum 8 risers per flight, then landing.

No claim is made here that the proposed schema changes are canonical. They are submitted for curator review against current USG.
