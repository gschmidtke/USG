# Proposed architectural sketch reconstruction rule

**Status: proposal — not yet canonical USG v0.12 protocol.**

Architectural sketches communicate through explicit dimensions, topology, proportion, annotation and perspective. A reconstruction system should not treat every undimensioned feature as unusable, and it should not silently promote an interpretation or realization choice into source truth.

## Core rule

**Dimensions override proportion. Proportion fills the gaps. User clarification resolves material contradictions.**

Suggested evidence states:

- `exact` — explicitly dimensioned or stated; build exactly.
- `derived` — calculated from exact information without adding unsupported intent.
- `approximate` — intent is clear but value or geometry is inferred proportionally; reconstruct only under an explicit policy and keep it labelled approximate.
- `observed` — presence, topology or relationship is visible but usable geometry is not reliable.
- `ambiguous` — multiple materially different readings remain; preserve the competing readings and ask the user when the ambiguity affects the design.
- `unknown` — no useful information exists; leave unresolved.

Do not confuse uncertainty of measurement with uncertainty of design intent. Ask the user when explicit evidence conflicts or ambiguity materially changes the design, not for every missing dimension.

## Source-first interpretation

The raw sketch remains the evidence source. A prior JSON interpretation is a derived record and may be re-audited against the source.

Recommended sequence:

1. read the source;
2. create or re-validate an evidence ledger;
3. map evidence into the lowest already-resolved USG stages that preserve purpose;
4. identify contradictions, ambiguities and unresolved values;
5. generate a realization only after the evidence state is stable enough for the chosen build mode.

For a sketch that already contains spaces, relationships and partial geometry, USG should reconstruct the resolved state rather than restart design from S00.

## Cross-view correspondence

Plan, section, elevation and perspective views should constrain one another when they plausibly describe the same object.

Example pattern from Building 001:

- small square marks in plan alone were weak evidence;
- vertical supports under a low roof in perspective were also incomplete evidence;
- together they strongly supported the semantic interpretation `canopy_support_post`.

Cross-view correspondence may strengthen the confidence of an `observed` relationship, but it does not create an exact dimension unless exact evidence exists.

## Interpretation is not realization

Keep these layers distinct:

1. **source evidence** — what the sketch actually shows or states;
2. **interpretation** — the semantic/topological reading of that evidence;
3. **realization hypothesis** — one possible geometric completion of approximate or unresolved values;
4. **accepted output** — a realization that has passed the required human and validation gates.

For example, `posts exist along the canopy edge` may be observed while `three posts at x = 1200, 3900, 6500 mm` is only one realization hypothesis.

## Multi-observer disagreement

Independent readers may disagree about the same mark. Do not silently replace one reading with the newest one.

Store materially different candidate readings with provenance and classify the source item as `ambiguous` until resolved. Building 001 produced a useful example where one observer read a handwritten mark as `WARD.` while two others read `WTRD.`.

The disagreement itself is evidence about interpretation uncertainty.

## Approximate-geometry policy

Approximate geometry must never be promoted silently into binding geometry.

A handoff should declare one of at least these policies:

- `excluded` — approximate values remain record-only and are not built;
- `labeled` — approximate values may be used in concept geometry, but every resulting object/value retains its approximate status and assumption provenance.

This proposal does not yet require one global policy. The curator currently recommends keeping the policy explicit per handoff until more cross-domain evidence exists.

## Multiple proportional realizations

When the source establishes intent but not one unique dimension, a generator may preserve several plausible proportional realizations instead of collapsing the design to a single arbitrary default.

Examples include:

- undimensioned room splits;
- canopy depth;
- post count and spacing;
- roof pitch;
- opening placement.

Candidate diversity should not alter exact or derived evidence.

## Export and downstream behavior

USG v0.12 already requires export classification and a sidecar manifest for geometry exports. Sketch reconstruction should use that canonical mechanism rather than invent a separate export rule.

A concept export should make clear:

- which exact and derived facts were used;
- which approximate assumptions were realized;
- which observed items were represented only semantically;
- which ambiguous or unknown items were deliberately not built;
- the export class and subject required by the current protocol.

The downstream target must not erase evidence status merely because the geometry was successfully created.

## Building 001 status

Building 001 is considered a strong worked example for this proposal, not yet proof of a universal protocol rule. The repeated observations from ChatGPT, Gemini and Grok support the evidence discipline, cross-view correspondence, separation of interpretation from realization, and source-first audit behavior.

Further testing on substantially different sketches is recommended before promotion into canonical protocol behavior.
