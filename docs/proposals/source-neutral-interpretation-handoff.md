# Proposed source-neutral interpretation and reconstruction handoff

**Status: proposal — not canonical USG v0.12.**

## Principle

The neutral interpretation record is the contract between source interpretation and downstream reconstruction.

A source may be a hand sketch, a SketchUp model, a point cloud, a BIM model, a drawing set, a text brief or another representation. The source type determines where interpretation effort is required, but not the structure of the downstream contract.

The proposed workflow is:

```text
SOURCE
  ↓
USG interpretation
  ↓
neutral handoff JSON
  ↓
target mapper
  ↓
read-back validation
```

The target mapper may be Revit/ARPL, Blender, IFC, Rhino, another API, or another reconstruction engine.

## Core invariant

A downstream target may change representation, but it may not silently change evidence state or intent.

The mapper must preserve, where applicable:

- stable identifiers;
- evidence classes;
- declared units and coordinate frame;
- relationships;
- null/unknown values;
- assumptions and hypothesis provenance;
- target-independent acceptance invariants.

A value left null by USG remains unresolved downstream unless a new authorized decision updates it.

## Source asymmetry

Different sources carry different kinds of certainty.

### Hand sketch

Typical strengths:

- explicit dimensions;
- annotations;
- relationships;
- design intent;
- cross-view clues.

Typical weaknesses:

- incomplete coordinates;
- approximate proportions;
- ambiguous marks;
- missing construction detail.

Interpretation effort is mainly evidence classification and intent reconstruction.

### Surface/mesh model such as SketchUp

Typical strengths:

- exact vertex coordinates in the model frame;
- group/component topology;
- component occurrences and reuse clues;
- tags/layers;
- material names.

Typical weaknesses:

- missing building semantics;
- walls may be single surfaces with no thickness;
- z coordinates do not necessarily define semantic levels;
- parametric intent is usually absent;
- tags do not necessarily define building roles.

Interpretation effort is mainly semantic recovery rather than measurement.

## Proposed handoff essentials

### 1. Descent premises

Record the premises USG relied on when moving into downstream representation.

If downstream evidence contradicts one of those premises, reopen the owning upstream decision. Other failures stay local to the downstream mapping or production layer.

### 2. Build policy

Each handoff declares how non-binding information may be represented.

Minimum proposed states:

- `build` — may become target geometry or native objects;
- `record_only` — preserve semantics/metadata but do not realize geometry;
- `ignore` — deliberately excluded from this target output.

Approximate values additionally declare an `approximate_policy`:

- `excluded` — do not build approximate values;
- `labeled` — approximate values may be realized in concept geometry, but retain their status and provenance.

The curator currently recommends keeping `approximate_policy` a per-handoff declaration rather than adopting one global default.

### 3. Pending-user gate

A material ambiguity or unresolved human-authority decision may be marked `pending_user`.

`pending_user` blocks binding downstream output that depends on the unresolved value, while still permitting non-binding exploration where the active project/export rules allow it.

### 4. Target-independent acceptance

Acceptance criteria should describe the intended result, not a particular software command.

Examples:

- footprint area preserved;
- controlling dimensions preserved;
- no invented binding values;
- nulls remain unresolved;
- identifiers and evidence states survive mapping;
- required adjacency/containment relationships survive mapping.

Completion requires read-back evidence and a per-invariant pass/fail result. API success alone is not completion.

## Relationship to canonical v0.12

USG v0.12 already requires export checks, export classification, and a sidecar export manifest. This proposal should extend or align with those mechanisms rather than duplicate them.

The new proposal-level learning is primarily:

- source-neutral interpretation as a reusable contract;
- explicit preservation of evidence/nulls across target mappers;
- declared build policy for approximate information;
- thin upstream reopening through recorded descent premises;
- target-independent acceptance with read-back evidence.

## Stage placement

The curator does **not** recommend adding a new canonical USG stage yet.

For now, source adapters should remain an interpretation boundary before or around stage-state reconstruction. The adapter maps source evidence into already-existing USG records/stages, and the pipeline enters at the lowest sufficiently resolved stage that still preserves purpose and authority.

This avoids expanding the canonical stage model before enough cross-domain adapter evidence exists.

## Worked evidence

Building 001 provides one end-to-end example:

```text
hand sketch
  ↓
neutral interpretation JSON
  ↓
concept geometry
  ↓
non-BIM target
  ↓
acceptance checks against the same source-neutral invariants
```

That example supports the proposal but is not sufficient by itself to make the rule canonical.

## Open curator questions

1. After testing more source types, should `approximate_policy` remain per-handoff or become a protocol-level default?
2. What minimum fields belong in a future handoff schema beyond the current `usg-output` schema?
3. Which source adapters deserve dedicated conformance cases first: sketch, SketchUp/surface model, IFC/BIM, or point cloud?
4. How should a mapper prove preservation of semantic evidence when the target format cannot store all metadata natively?
