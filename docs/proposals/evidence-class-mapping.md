# Proposed mapping: sketch source classes ↔ canonical evidence and authority

**Status: proposal — not canonical USG v0.12. Requires owner decision (normative).**

## Problem

USG currently has two vocabularies for how certain a value is:

| Vocabulary | Where | Terms |
| --- | --- | --- |
| Canonical | `USG_v0_12.json`: `answer_authority`, `evidence_model`, `geometry_model.authority` | authority (human, domain_library, ai_generated, derived, professional_review, external_evidence); claim status (confirmed_positive, confirmed_negative, conflicting, insufficient); confidence high / medium / low |
| Proposal | `docs/proposals/architectural-sketch-reconstruction.md`, `schema/usg-output.schema.json` | source classes exact, derived, approximate, observed, ambiguous, unknown; numeric confidence 0–1 |

Nothing maps one onto the other. Read literally, two canonical rules contradict the proposal's "user clarification resolves contradictions":

1. `evidence_model.rules`: *"Evidence of kind owner_statement never exceeds medium confidence"*, and medium confidence never passes a hard gate.
2. `geometry_model.authority.hierarchy`: `owner_sketch` ranks lowest; *"AI-generated drawings are never geometric authority."*

Building 002 shows the gap in practice: the neutral spec labelled user-confirmed values `exact` and "binding", which the canonical model would score as medium-confidence owner statements.

## Proposed resolution: separate design decisions from factual claims

The contradiction disappears once two kinds of value are kept apart:

- **Factual claims about the world** (site boundaries, existing structures, soil, regulation). Here the canonical rules apply unchanged: an owner's statement or sketch of the site is weak evidence, and survey or professional sources outrank it. `geometry_model.authority` governs `site_envelope.controlling_geometry_ref`, the existing-world geometry.
- **Design decisions about the proposed structure** (its form, dimensions, facade, roof). When the human is the designer stating their own intent, the value is not evidence about the world; it is a decision under `answer_authority.human` ("purpose, priorities, preferences, confirmed project goals, acceptance"). It does not need a confidence level to pass a gate. It still remains subject to every factual and regulatory gate (S02, S09, S13, S17).

Rule to add: *A design value stated or confirmed by the human designer is a human-authority decision, not owner_statement evidence. The owner_statement confidence cap and the geometric authority hierarchy apply only to claims about existing conditions.*

## Proposed mapping table

| Source class (proposal) | Canonical authority | Gate behaviour | Notes |
| --- | --- | --- | --- |
| `exact` | human (designer's dimension or explicit statement) | decided value | Must come from the source or an explicit human statement, never from an AI estimate. A `~`, "ca." or similar on the source makes it `approximate`. |
| `derived` | derived | decided value | Deterministic from exact/derived inputs only. |
| `approximate` | ai_generated (proposed assumption) | may be realized only under a declared `labeled` approximate-geometry policy; never passes a hard gate as fact | Carries its derivation (proportion, scale, cross-view). |
| `user_accepted` **(new)** | human, origin ai_generated, with date | decided value for the declared phase | An AI estimate the designer reviewed and accepted (e.g. pier 600 mm accepted on a review view). Records that the number was proposed by AI, not drawn or stated by the human. Re-opens if the source or a factual gate contradicts it. |
| `observed` | ai_generated (reading of the source) | presence/topology decided; geometry open | Cross-view correspondence may raise confidence but never creates an exact dimension. |
| `ambiguous` | none yet: an open question record (`question_record_schema`) | blocks dependent gates until resolved | Keep competing readings with provenance. |
| `unknown` | none | value stays `null`; not built | |

## Related schema changes

- `schema/usg-output.schema.json`: add `user_accepted` to `source_kind`; add an optional `authority` field using the canonical authority names; replace the numeric `confidence` with the canonical `high | medium | low` (or document the conversion).
- A conflict between a source annotation and a later confirmation (Building 002: sketch "~1,5 m" vs a spec value of 1000 mm marked "exact, user-confirmed") is recorded as `ambiguous` and raised to the designer, never resolved silently in either direction.

## Evidence

- Building 001 (`curation/records/2026/2026-10-27-building-001-sketch-review.json`).
- Building 002 (`examples/building-002/`): nine divergences between spec v0.1 and design intent, including a wrong value carried at `exact`, and AI estimates accepted by the designer that had no class to land in.

## Decisions requested from the owner

- [ ] Adopt the design-decision vs factual-claim separation as a v0.13 rule.
- [ ] Adopt the mapping table, including the new `user_accepted` class.
- [ ] Choose the confidence representation for external schemas (canonical high/medium/low, or numeric with a documented conversion).
- [ ] Decide whether the sketch reconstruction proposal can be promoted together with this mapping, now that a second, substantially different sketch (Building 002) has been run.
