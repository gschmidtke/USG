# Lesson learned: Input Reading must optimize the production outcome

**Date:** 2026-10-27  
**Contributor:** Gottfried Schmidtke with interactive AI review/testing  
**Related test case:** `2026-10-27-option05-input-reading-pipeline-test-case.json`

## Why this submission exists

A real SketchUp hospital-masterplan model (`option 05.skp`) was used to exercise the emerging USG Input Reading proposal end to end. The run was intentionally pushed beyond source inspection into a downstream reconstruction problem: produce a compact, tool-neutral description that Revit or another geometry/BIM tool could use to rebuild the current design.

The exercise validated much of the intake logic, but it also exposed an important optimization rule: **the intake pipeline should be judged by the usability of its production outcome, not by how completely it documents every internal reasoning step.**

## What worked

The source-native read recovered useful structure before any Reading Grid was needed:

- placed vs. unplaced source content;
- current design vs. context/history;
- 48 active Mass Floor definitions;
- 13 vertical mass stacks;
- 22 unique floor-profile prototypes;
- 48 floor placements;
- 26 repeated floor instances eliminated through equivalence compression;
- two recurring vertical systems (primarily 10 ft and 16 ft sequences);
- human-authority resolution for the current design;
- intentional upper-floor profile changes preserved as design, not treated as errors.

The resulting production-oriented rebuild package could therefore be reduced to levels, reusable profiles, placements, stack relationships, and optional exact source envelopes. The full evidence trail remained useful for audit and debugging but was no longer required by the production consumer.

## The key failure

A subsequent grid-generation test exposed a deeper architectural lesson.

The first grid algorithm treated each mass stack as an independent building rectangle, calculated its oriented bounding box, and filled that box with an approximately 32 ft hospital module. The result was mathematically regular but architecturally wrong:

- grids crossed courtyards and exterior voids;
- curved/crescent buildings received Cartesian lattices;
- branching buildings were flooded by one grid system;
- neighboring building grids visually dominated the site plan;
- equal subdivision was optimized instead of structural/planning organization.

This showed that **a mass stack is not automatically a structural grid domain**.

## Revised rule

Grid generation requires an additional architectural decomposition:

```text
Mass Stack
  ↓
Building Recognition
  ↓
Wing / Structural-Zone Decomposition
  ↓
Dominant Axis / Curvature Recognition
  ↓
Grid-System Classification
  ↓
Healthcare / Parking / Utility Module
  ↓
Optimization + Structural Review Flags
  ↓
Revit Grid Output
```

Examples:

- linear clinical bars → local orthogonal grids;
- U/courtyard buildings → separate wing grids, not a filled bounding rectangle;
- branching buildings → one grid domain per wing around a shared node/core;
- curved/crescent buildings → radial grids + concentric arc grids;
- parking → parking-specific module;
- CUP/service masses → independent utility grid;
- podium/tower transitions → separate domains unless continuity is proven.

The approximately 30–35 ft healthcare bay remains a useful planning convention, but it is a **target module after the architecture is understood**, not a universal geometric subdivision rule.

## Pipeline consequence

The production-oriented pipeline should be simplified to:

```text
1. Define the required downstream outcome.
2. Ask only the human questions that materially affect that outcome.
3. Exploit source-native structure.
4. Isolate the active design.
5. Recognize architectural organization.
6. Compress proven repetition/equivalence.
7. Produce the smallest trustworthy rebuild model.
8. Ask: can the downstream task now be performed?
   - Yes → stop intake.
   - No  → read only the missing information.
9. Use a Reading Grid only for unresolved regions that materially block the requested outcome.
```

This suggests three distinct layers:

1. **Internal Reading Process** — potentially detailed, normally invisible.
2. **Audit / Conformance Record** — optional proof/debugging artifact.
3. **Production Result** — compact primary handoff to Revit, Rhino, Archicad, ARPL, or another consumer.

## Proposed general lesson for USG

> Input Reading is successful when it removes work from the downstream tool while preserving enough evidence to explain and re-audit the result.

The protocol should not reward exhaustive interpretation for its own sake. It should optimize for **minimum sufficient verified representation for the requested outcome**.

A Reading Grid should therefore be a fallback observation mechanism rather than a mandatory stage.

Likewise, downstream operations such as structural-grid generation may require architectural semantics (building/wing/grid-domain recognition) that do not follow directly from mass or bounding-box geometry.

## Additional equivalence observation

The source also contained separate SketchUp definition IDs whose normalized geometry/topology/material comparison was exact. These cannot be T1 source-identity matches, but the geometric delta can be proven empty for the declared comparison scope.

A future proposal refinement may therefore distinguish:

```text
T3 match_mode = exact | within_tolerance
```

with `exact` allowing `delta_share = 0` / `proven_empty`, while still preserving different source identities.

## Suggested curator uses

This submission may be useful as one or more of:

- an Input Reading worked example;
- a production-outcome optimization rule;
- a failure-pattern example for premature grid generation;
- a conformance/regression fixture candidate;
- a proposal refinement for Reading Grid optionality;
- a proposal refinement for exact T3 geometric equivalence across different source identities.

The accompanying JSON captures the test-case pipeline, decisions, rules, failure conditions, and next expected artifacts.
