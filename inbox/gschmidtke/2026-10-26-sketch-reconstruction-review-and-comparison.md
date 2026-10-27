# External review: Building 001 sketch reconstruction, USG evidence discipline, and comparison with contemporary Sketch-to-BIM agents

**Suggested inbox path:** `inbox/<your-github-username>/2026-10-26-sketch-reconstruction-review-and-comparison.md`

**Date:** 2026-10-26  
**Contributor:** Grok (xAI) via interactive session with repository owner / user  
**Related material:**  
- Building_001_USG_Sketch_Interpretation_v0.3.json  
- Source sketch: ChatGPT Image Oct 26, 2026, 03_24_25 PM.jpg (plan + perspective on one sheet)  
- USG protocol v0.12  
- docs/proposals/architectural-sketch-reconstruction.md  
- ARPL inbox item on proportional reconstruction rule (same day)

**Type of contribution:** external AI review + comparative observation + proposed refinements for curator consideration

---

## 1. Purpose of this note

This note records conclusions from a working session that:

1. Inspected the hand sketch of Building 001.
2. Examined the existing USG-style interpretation record (v0.3).
3. Generated a concept-mass STL under the declared concept_build_profile.
4. Compared the USG approach with other contemporary AI / multi-agent sketch-interpretation systems (2025–2026 literature and prototypes).

The goal is to feed usable learning into the USG inbox so the curator can decide whether any of it should become a conformance case, a documentation improvement, a proposal refinement, or a protocol-patch candidate.

---

## 2. Summary judgment on the Building 001 interpretation record

The v0.3 JSON is already a high-quality, disciplined application of the emerging architectural-sketch rule:

> Dimensions override proportion. Proportion fills the gaps. User clarification resolves contradictions.

**Strengths observed**

- Clear separation of evidence classes (`exact`, `derived`, `observed`, `approximate`, `ambiguous`, `unknown`).
- Binding geometry limited to what the sketch actually supports (14 m × 14 m, 6 m upper-bar depth, 6 m projecting-wing width, derived re-entrant at x = 8000 mm, 132 m² footprint).
- Correct rejection of the earlier equal cross-gable reading; perspective supports a dominant upper-bar gable + lower wing roof.
- Cross-view correspondence used productively for the canopy/posts (plan squares ↔ perspective vertical supports).
- Proportional room splits and opening sizes correctly quarantined or left null.
- Explicit concept_build_profile with assumption IDs, plus a stricter authoritative-only mode.
- Validation and enhanced_validation sections that protect the binding numbers.

**Minor observations / possible tightenings**

- Canopy depth and post spacing in the concept profile are reasonable but somewhat arbitrary relative to the visible plan marks and perspective. A more tightly proportional reading of the marks would still remain approximate, yet closer to the source.
- The number of posts is treated as three; the plan marks suggest a possible fourth or a slightly different rhythm. This remains approximate either way.
- IP_PROP_01 / IP_PROP_02 positions are correctly non-binding; a pure concept mass could optionally omit them or show them only as guide geometry.
- The “WTRD.” annotation and the unlabelled kitchen rectangle are correctly left unresolved.

None of these points overturn the major decisions in the record. They are refinements of proportional choices, not challenges to the evidence classification.

---

## 3. What would change with direct sketch access + full USG protocol

If an agent starts from the raw sketch image and the USG protocol rather than from a pre-digested JSON:

1. Produce (or re-validate) the evidence ledger first.
2. Enter at the lowest already-resolved stage that still preserves purpose (here approximately S11 / S14).
3. Keep the authoritative layer strictly limited to exact + derived geometry and observed topology.
4. Generate concept geometry only after evidence classification is stable, and always under an explicit build mode with tagged assumptions.
5. Export any mesh/STL/IFC with a sidecar manifest that declares export class (concept), subject (design_hypothesis), and the assumption IDs used.
6. Ask the human only for material ambiguity or conflicting evidence, not for every missing dimension.

This is already largely what the v0.3 record enables; the difference is mainly procedural strictness and packaging of the downstream export.

---

## 4. Comparative landscape (2025–2026)

Contemporary systems that convert hand sketches into 3-D or BIM fall into a few recurring patterns:

| Family | Examples | Typical intermediate | Evidence discipline | Downstream coupling | Human role |
|--------|----------|----------------------|---------------------|---------------------|------------|
| Multi-agent Sketch-to-BIM | Sketch2BIM (Automation in Construction 2026), related MLLM + script pipelines | Tool-oriented JSON (walls, openings with host links) | Best-guess geometry; accuracy improved by iteration | Usually hard-wired to Revit / Blender | Feedback loop to raise detection metrics |
| Commercial residential | Higharc AI | Internal room/wall detection | Domain-tuned, proprietary | Native 3-D BIM inside the product | Light review |
| Generative / diffusion | Sketch → multi-scheme 2-D → mesh pipelines | Image or mesh | Low; optimised for visual plausibility | Mesh / Grasshopper | Optional selection among schemes |
| Constraint-triggered agents | BlueprintAgent-style | Entity extraction + validators | Local re-inspection on rule violation | Simulation-ready frames | Correction of flagged conflicts |
| Review-oriented tools | Esquisse-kun and similar | Explicit / readable / estimated / unknown | Strong separation of value classes | Review notes, not full models | Primary user of the classification |
| USG-style | Building 001 record + protocol | Software-neutral, multi-stage, provenance-rich specification | Explicit evidence classes + staged hand-off | Delayed; ARPL or other production logic later | Clarification only on material ambiguity |

**Distinctive USG characteristics**

- Persistent, versioned, software-neutral intermediate that can be handed to any downstream system.
- Explicit governance of when approximate values may be used.
- Sketch treated as one evidence source inside an authority hierarchy, not the sole input.
- Coupling to a staged protocol (S00–S20 style) with acceptance invariants.
- Learning path (inbox → curator → protocol) so failures become shared knowledge.

Most Sketch-to-BIM agents optimise for speed-to-usable-geometry. USG optimises for fidelity of intent and long-term governability. The two are complementary: a USG record can later feed a Sketch2BIM-style or ARPL production step once the human has accepted the evidence classification.

---

## 5. Suggested curator actions (non-binding)

The following are offered only as options for the curator; they are not protocol changes by themselves.

1. **Accept as example / conformance case**  
   The Building 001 v0.3 record (or a cleaned derivative) is a strong worked example of the architectural-sketch reconstruction rule applied to a real plan + perspective sheet.

2. **Documentation improvement**  
   Add a short “Sketch reconstruction” note under docs or examples that points to:
   - the priority order (exact → derived → proportional → perspective → user clarification),
   - the requirement to tag approximate geometry,
   - the recommendation to export concept geometry with a manifest.

3. **Proposal refinement**  
   Consider whether the canopy/posts cross-view pattern and the treatment of unresolved annotations (“WTRD.”, kitchen rectangle) should be mentioned as recurring patterns in the architectural-sketch proposal.

4. **No immediate protocol patch required**  
   The existing v0.12 evidence and export rules already support the observed behaviour. The main value is illustrative and comparative.

---

## 6. Practical artefacts produced in the session

- Concept-mass STL generated under the declared concept_build_profile (walls, slab, derived + approximate partitions, primary + wing gables, canopy, three posts).
- Explicit recognition that the STL is concept geometry only and must not promote approximate values into the authoritative layer.

These artefacts are session-local; the durable learning is the evidence discipline and the comparison above.

---

## 7. Closing

USG’s insistence on “Need first. Geometry last.” and on labelled evidence classes remains a useful counterweight to the dominant Sketch-to-BIM pattern of rapid, best-guess geometry generation. The Building 001 record shows that the approach is already practical for a realistic hand sketch. The comparative landscape confirms that few other systems maintain an equally strict, software-neutral intermediate.

This note is submitted to the inbox for curator triage. No claim is made that any part of it is already canonical.

---

*End of submission.*
