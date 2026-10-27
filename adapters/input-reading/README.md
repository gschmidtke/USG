# Proposal: USG Input Reading (source adapter)

**Status: proposal, not canonical USG v0.12. Requires owner decision (normative).**
**Module:** `adapters/input-reading/` (see [adapters/README.md](../README.md)); moved here from `docs/proposals/` in LOG-0015.
**Machine-readable version:** [`spec.json`](spec.json) (v0.3.4)
**Origin:** drafted by Gottfried Schmidtke over five review rounds with Claude, Mistral and ChatGPT (v0.1 to v0.3.4, 2026-10-27); the v0.3.4 package and its decision log are archived in `curation/archive/CUR-2026-10-27-INPUT-READING/`. Record: `CUR-2026-10-27-INPUT-READING`.

## What it is

The [source-neutral handoff proposal](../../docs/proposals/source-neutral-interpretation-handoff.md) says source adapters should stay an interpretation boundary in front of the stage model. Input Reading is that boundary for complex existing sources (models, drawing sets, scans): it reads the source and hands USG evidence records, not conclusions. It adds no stage and changes no stage.

> **What are you, what do you already know about yourself, and where do I still need to look?**

```text
human context + source-native information + geometric observation
        ↓
Input Reading  IR-00 … IR-15
        ↓
evidence records (source_kind, authority, confidence, provenance, partition fields)
        ↓
USG stages (entry at the lowest sufficiently resolved stage)
        ↓
USG → ARPL handoff (unchanged; schema/usg-output.schema.json)
```

## The method

1. **IR-00** Ask the human what the object is, what they know, what to recover, which parts are design, existing world or context, and who holds design authority.
2. **IR-01** Read what the source knows about itself: units, coordinates, north, geolocation, components and instances, names, tags, materials. Partition it and classify each partition.
3. **IR-02 to IR-04** Hypothesise what the object is and how it organizes itself; choose a reading strategy.
4. **IR-05 to IR-07** Find repeat candidates, prove each one (tiers T1 to T4), then compress into prototype + transform + delta. Mirrored instances get a handedness review.
5. **IR-08 to IR-11** Build the project frame, assess complexity, create the Reading Grid (`RG-*`) only where complexity remains, and read those cells.
6. **IR-12** Reconcile identity across cells (geometry without source identity becomes one object or an explicit fragmentation record).
7. **IR-13** Put every material assumption and conflict to the human in one list.
8. **IR-14 / IR-15** Assemble the addressable project read and prove the pass with acceptance checks RA-01 to RA-13.

## How it fits the existing proposals

| Existing piece | Relationship |
|---|---|
| v0.12 `answer_authority`, `evidence_model` | Used unchanged: authority values, claim status (computed by USG, not by the reader), high/medium/low confidence, `site_fact_rule` (owner statements about existing conditions are evidence, max medium). |
| [Evidence-class mapping](../../docs/proposals/evidence-class-mapping.md) | Its design-decision vs factual-claim split becomes the partition field `world_relation`. Input Reading extends the mapping with rules for existing-world sources, external design authority and unknown origin (`authority_resolution`, first match wins). Depends on the owner's decision on that proposal, including `user_accepted`. |
| [Source-neutral handoff](../../docs/proposals/source-neutral-interpretation-handoff.md) | Input Reading is a source adapter as that proposal describes it. Its `excluded` / `context_reference` partitions fit the handoff's `record_only` disposition. |
| [Architectural sketch reconstruction](../../docs/proposals/architectural-sketch-reconstruction.md) | One specialization of source reading; its source classes are Input Reading's `source_kind`. |
| `handoff-to-arpl.md` | Unchanged. Representation of prototypes (groups, families, assemblies) stays with ARPL. |

## Key rules

- **Three partition fields, never collapsed:** `world_relation` (proposed_design, existing_world, unknown), `participation_role` (target, context_reference, excluded), `design_authority_relation` (current_human_is_design_authority, external_design_authority, unknown, not_applicable).
- **Authority is resolved, not chosen:** ordered rules over source_kind, world_relation, design_authority_relation, provenance and `source_origin`; a value-bearing record that matches no rule is invalid and high materiality.
- **Similarity is not identity:** each instance records a placement tier and a content tier; T3 needs a declared tolerance, a declared `max_delta_share` with its measure, and only local, classifiable deltas.
- **A mirror is not a copy:** handed content is re-read.
- **Ask when guessing costs more:** materiality from high examples, conflicts and propagation scope first, then a provisional table (dependent_count threshold 5).
- **Unknown stays null; no compass meaning without north.**

## Test cases (proposed, not pinned)

- **IR-CC-01** two-wing test: units, context, levels, facade repeats with one exception, mirrored wing with one unmirrored door, identity-less slab, misleading name.
- **IR-CC-02** authority test: consultant design model as context, scan of an existing building as target, owner note vs scan conflict, excluded scratch geometry.

Neither fixture exists as a model yet. Both are specified with construction, expected results and the RA checks each failure must trip.

## Known gaps found at curation

These do not block a proposal decision; they should be fixed in the next revision, before any fixture is built.

- **C-01 Origins without a rule.** `source_origin` lists `scan`, `imagery`, `terrain`, `imported_reference`, `consultant_design_source` and `human_statement`, but for an existing-world source-native value that is `exact` or `observed`, only the owner and professional origins have rules. Under first-match-wins with the invalid default, a scan dimension, or the geolocation carried by imagery or terrain, is invalid. IR-CC-02's 2850 mm scan height has no stated authority for this reason.
- **C-02 Designer's own annotation.** A proposed-design value with `current_human_is_design_authority`, `source_kind=approximate` and `provenance=source_native` (the designer's "~1,5 m" on their own sketch, Building 002) matches no rule. It should be human authority, approximate, per the evidence-class mapping's design-decision rule.
- **C-03 Unreachable rule.** The rule for existing world + human + observed can never match: the rule before it already covers `[exact, approximate, observed]`.
- **C-04 Duplicate open questions.** `user_accepted` for existing-world evidence and reusing the partition fields each appear twice.

An exhaustive walk of every valid field combination ([`tools/authority_walk.py`](tools/authority_walk.py), LOG-0014) confirms C-01 to C-03 and finds three more. Every gap falls to the invalid, high-materiality default, so a gap costs a question to the human, never a wrong authority.

- **C-05 Design authority unknown, approximate.** The rule for `proposed_design` + `design_authority_relation=unknown` covers only `source_kind=exact`. An approximate value in a design source of unknown authorship ("~3 m" in an unattributed model) matches no rule. It should get the same treatment: external evidence, non-binding until design authority is resolved.
- **C-06 External design value relayed by the human.** `proposed_design` + `external_design_authority` + `provenance=human` + `source_kind=approximate` ("the architect said about 3 m") matches no rule; only the source-native approximate case is covered.
- **C-07 Meaning of `observed`.** The evidence-class mapping defines `observed` as a reader's reading (ai_generated). Rules 4 and 5, C-01 and IR-CC-02 let a human or a source supply an `observed` value. Decide one meaning before fixing C-01 and C-03; under the mapping's meaning, `observed` with `provenance` human or source_native is a category error, and the invalid default is the right result.

## Decisions requested from the owner

- [ ] Accept Input Reading as the source-adapter contract in front of USG (no stage change).
- [ ] Decide the evidence-class mapping proposal first or together: Input Reading's `authority_resolution` extends it.
- [ ] Adopt the three partition fields as reusable fields for every source adapter, or keep them local to Input Reading.
- [ ] Build IR-CC-01 and IR-CC-02 as real fixtures and pin them under [`fixtures/`](fixtures/README.md).
