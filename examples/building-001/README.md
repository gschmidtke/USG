# Building 001: sketch reconstruction with a multi-observer review

The first sketch run through USG. One hand-sketch sheet (plan + perspective) was reconstructed into a neutral interpretation record, read independently by three AI observers (ChatGPT, Gemini, Grok), and realized as concept geometry in several tools. It established the proposed rule *dimensions override proportion, proportion fills the gaps, user clarification resolves contradictions*.

## Files

| File | What it is |
| --- | --- |
| `spec/Building_001_USG_Sketch_Interpretation_v0.3.json` | Interpretation record + neutral spec v0.3, as supplied by the owner, unchanged |
| `check_building_001.py` | Runs the checks the record declares about itself; 20 of them can be decided from the JSON alone |

**Not in the repository yet:** the source sketch (`ChatGPT Image Oct 26, 2026, 03_24_25 PM.jpg`), the earlier `Building_001_Neutral_Spec_v0.2.json` and the v0.3–v0.5 concept profiles named under `provenance`. Add them under `source/` and `spec/` if they should be reproducible from this folder.

## Binding facts

14 000 × 14 000 mm extents · 6 000 mm upper-bar depth · 6 000 mm projecting-wing width (all dimensioned) · 8 000 mm wing depth and re-entrant corner at x = 8 000 · 132.0 m² enclosed footprint (derived). Everything else (heights, thicknesses, roof pitches, partition positions, openings, canopy size, post positions) is observed, approximate, ambiguous or unknown, and the record keeps it that way.

```text
python examples/building-001/check_building_001.py
20/20 decidable checks pass
```

The checker also fails on a deliberately broken copy (moved re-entrant corner, invented wall thickness, post outside the canopy), so it can serve as the core of a conformance fixture if the owner decides to pin one.

## Where the observers disagreed

From the multi-observer submission (`curation/archive/CUR-2026-10-27-BUILDING-001-MULTI-OBSERVER/`). These are kept open on purpose; v0.3 records only one side of the first two.

| Topic | Readings | Evidence state | In v0.3 |
| --- | --- | --- | --- |
| Handwritten leader into the right bedroom | `WARD.` (Gemini) · `WTRD.` (Grok, and the record) | ambiguous | `MARK_01` reads `WTRD.` only; correctly not turned into a room or wardrobe |
| Canopy support count | three posts (concept profile) · about four or five marks (Grok) | presence observed; count and spacing ambiguous | `POST_01..03`, tagged approximate |
| Undimensioned internal layout | one concept realization · several proportional candidates | approximate | one realization (x = 4500, y = 2700), quarantined as non-binding |

All three observers agreed on the binding numbers, on a dominant upper-bar gable with a lower wing roof (not equal cross-gables), and on a covered porch with posts in the re-entrant corner.

## Format notes

v0.3 predates the S00–S20 stage-id rule and the draft `schema/neutral-building-spec.schema.json`, and is kept verbatim. Differences a reader should know:

- `entry_stage` is `S11_semantic_model_sketch_state_reconstruction` (stage id plus label); the current output schema expects `S11`.
- It uses its own source kinds (`dimensioned`, `proportional`, `convention`) with a `legacy_source_kind_map` to the six-class scheme, and numeric confidence. `convention` (a coordinate or adapter choice, never source evidence) is a seventh class not in the proposal; it is noted in `docs/proposals/evidence-class-mapping.md`.

## Compared with Building 002

Building 001 errs on the side of *not building*: unknowns stay null and openings are not cut. Building 002 went further, into a reviewed Revit model, and its errors appeared exactly where v0.1 had committed to a reading without enough evidence (roof form, overhang host, glazing module). Together they support keeping the evidence classes explicit through every downstream step.
