# USG Input Reading v0.3.4 — Review Decision Log

Carries forward all prior review decisions and adds the Claude v0.3.3 review patch.

## MIS-01 — Mistral

**Proposal:** Treat USG Input Reading as a process contract with addressable project records and an acceptance step.

**Decision:** `adopted`

**Why:** Moves the concept from philosophy to a testable, inspectable input process without changing canonical USG stages.

## MIS-02 — Mistral

**Proposal:** Use exact/derived/approximate/observed/ambiguous/unknown as 'the USG protocol evidence model' with no parallel taxonomy.

**Decision:** `rejected_as_stated; reframed`

**Why:** Current USG v0.12 canonical evidence uses separate authority and claim-status axes. The six classes remain proposal-level source classes. v0.3 therefore records source_kind + canonical authority + canonical claim_status + provenance.

## MIS-03 — Mistral

**Proposal:** Every interpretation output carries evidence state and provenance.

**Decision:** `adopted_with_modification`

**Why:** Retained, but evidence is represented as multiple independent fields rather than one overloaded class.

## MIS-04 — Mistral

**Proposal:** Tiered prototype equivalence and delta-verification obligations.

**Decision:** `adopted_with_modification`

**Why:** The tier concept is essential. v0.3 prevents a tolerance-based geometry match from becoming 'exact'; it is verified within tolerance and remains approximate/provisional until its delta obligation is satisfied.

## MIS-05 — Mistral

**Proposal:** Mechanically triggered human escalation based on uncertainty and bindingness.

**Decision:** `adopted`

**Why:** Makes 'ask instead of guess' operational. v0.3 also includes dependent_count and propagation scope.

## MIS-06 — Mistral

**Proposal:** Record context rather than discard it; map it to record_only downstream.

**Decision:** `adopted_with_modification`

**Why:** Context remains separate and preserved. record_only is described as a proposed downstream disposition because the source-neutral handoff proposal is not yet canonical.

## MIS-07 — Mistral

**Proposal:** Organizational model as descent premise; local contradiction causes local re-entry.

**Decision:** `adopted`

**Why:** Prevents a wrong assumption in one region from forcing a complete reread.

## MIS-08 — Mistral

**Proposal:** Starter quantitative complexity metrics.

**Decision:** `adopted_as_provisional`

**Why:** Useful for relative ranking, but calibration and weights remain open questions.

## MIS-09 — Mistral

**Proposal:** Reading Acceptance contract with pass/fail checks.

**Decision:** `adopted_and_expanded`

**Why:** Acceptance is central to proving the pass. v0.3 adds explicit checks for units, north reference and mirror handedness.

## MIS-10 — Mistral

**Proposal:** Manifest-style project structure with selective loading.

**Decision:** `adopted`

**Why:** Directly supports large-model reading and avoids a monolithic JSON.

## MIS-11 — Mistral

**Proposal:** Use RG as the Reading Grid short name.

**Decision:** `adopted_with_naming_refinement`

**Why:** The formal concept is 'USG Reading Grid'; individual region identifiers use RG-*. 'Adaptive' describes behavior rather than becoming a second formal name.

## CLA-01 — Claude

**Proposal:** Position USG Input Reading explicitly as an input adapter in front of USG.

**Decision:** `adopted`

**Why:** Preserves the current stage model and clarifies that existing-source reading is evidence intake, not need resolution.

## CLA-02 — Claude

**Proposal:** Read units, coordinates, north reference and context before repetition analysis.

**Decision:** `adopted`

**Why:** These can invalidate every later transform or compass interpretation if wrong.

## CLA-03 — Claude

**Proposal:** Names, tags and groups are evidence, not truth.

**Decision:** `adopted`

**Why:** A recorded source label may be exact as a token while its semantic interpretation remains only observed.

## CLA-04 — Claude

**Proposal:** Every repetition is tested before compression.

**Decision:** `adopted`

**Why:** This is the correct gate between candidate similarity and prototype compression.

## CLA-05 — Claude

**Proposal:** A mirror is not a copy; re-read handed content.

**Decision:** `adopted`

**Why:** Geometric mirror symmetry does not preserve door swings, stair direction, handed equipment, text or asymmetric clearances.

## CLA-06 — Claude

**Proposal:** A prototype change revalidates every instance delta; instance overrides stay local.

**Decision:** `adopted`

**Why:** Prevents hidden propagation errors and matches shared-type lessons already seen downstream.

## CLA-07 — Claude

**Proposal:** Cross-cell reconciliation is only for geometry without source identity.

**Decision:** `adopted_with_modification`

**Why:** Identity reconstruction is mandatory for geometry without native identity, but source-identified objects still need cross-cell consistency checks.

## CLA-08 — Claude

**Proposal:** Use dependent_count to decide assumption materiality.

**Decision:** `adopted_with_modification`

**Why:** Dependency count is useful but insufficient alone. v0.3 combines bindingness, dependent_count, propagation scope, evidence state and conflicts.

## CLA-09 — Claude

**Proposal:** Create synthetic conformance case IR-CC-01.

**Decision:** `adopted`

**Why:** A compact deliberately adversarial fixture can test units, context separation, repetition, mirror handedness, identity, nulls and north-reference behavior.

## CLA-10 — Claude

**Proposal:** Treat exact/derived/approximate/observed/ambiguous/unknown as 'USG's classes, unchanged'.

**Decision:** `rejected_as_stated; reframed`

**Why:** The current repository explicitly marks those as proposal source classes, not canonical v0.12 evidence. v0.3 preserves them as source_kind while carrying canonical authority and claim_status separately.

## CLA-11 — Claude

**Proposal:** geometry_match within tolerance => exact.

**Decision:** `rejected`

**Why:** Tolerance proves equivalence only within the declared tolerance. It does not make independent geometry exact.

## CLA-12 — Claude

**Proposal:** Numeric confidence 0-1 accompanies records.

**Decision:** `adopted_as_optional_diagnostic`

**Why:** Useful for ranking or review, but it must never promote source_kind, authority or claim_status.

## CLA-13 — Claude

**Proposal:** Worked example should be anonymized.

**Decision:** `adopted`

**Why:** The general proposal should not depend on client/project identity; case specifics can remain in separate evidence/example files.

## CLA-14 — Claude

**Proposal:** Refer to USG as Universal Spec Generator.

**Decision:** `rejected`

**Why:** The repository currently defines USG as Universal Structure Generation.

## CLA-15 — Claude

**Proposal:** No compass meaning without a north reference.

**Decision:** `adopted`

**Why:** Prevents invented orientation semantics from entering the project read.

## CL2-01 — Claude (review of v0.3)

**Proposal:** Declare source_role (design_intent, existing_conditions, context) per source partition.

**Decision:** `superseded_by_ZAR-01_and_CL3-02`

**Why:** The single source_role model was replaced by orthogonal world_relation / participation_role plus design_authority_relation.

## CL2-02 — Claude (review of v0.3)

**Proposal:** Align evidence fields with evidence-class-mapping.md: add 'convention', derive authority from source_kind and source_role, use canonical high/medium/low confidence.

**Decision:** `superseded_by_ZAR-02_and_CL3-03`

**Why:** Authority is no longer derived from a context column or source_kind alone; it is resolved from world relation, actual design authority, provenance and source kind.

## CL2-03 — Claude (review of v0.3)

**Proposal:** Remove claim_status from the record; link records to claims instead.

**Decision:** `applied_in_0.3.1_pending_owner_review`

**Why:** v0.12 computes claim status per claim from all evidence items; a single reading record cannot carry it.

## CL2-04 — Claude (review of v0.3)

**Proposal:** T2 proves placement only; compression needs a content tier.

**Decision:** `applied_in_0.3.1_pending_owner_review`

**Why:** An exact array of independent copies proves where they are, not that they are equal.

## CL2-05 — Claude (review of v0.3)

**Proposal:** Define 'instance override' for T1; reserve acceptance of unresolved high-materiality items to human authority.

**Decision:** `applied_in_0.3.1_pending_owner_review`

**Why:** Both were undefined terms an autonomous reader would fill in itself.

## CL2-06 — Claude (review of v0.3)

**Proposal:** Give every reading acceptance check a pass condition and a result value.

**Decision:** `applied_in_0.3.1_pending_owner_review`

**Why:** Check names alone cannot prove a pass.

## CL2-07 — Claude (review of v0.3)

**Proposal:** Restore the IR-CC-01 construction and expected results.

**Decision:** `applied_in_0.3.1_pending_owner_review`

**Why:** A fixture needs expected outputs, not only failure signatures; the wing B construction decides which tier it must pass.

## CL2-08 — Claude (review of v0.3)

**Proposal:** Ask about context and existing conditions in the initial questions.

**Decision:** `applied_in_0.3.1_pending_owner_review`

**Why:** Context classification is high materiality; the human can answer it in seconds.

## ZAR-01 — ChatGPT/Zara review of Claude v0.3.1

**Proposal:** Use one source_role enum: design_intent | existing_conditions | context.

**Decision:** `adopted_with_structural_modification`

**Why:** Context is orthogonal to design-vs-existing-world. Terrain can be existing-world context; a scan can be existing-world target; an external conceptual model can be proposed-design context.

## ZAR-02 — ChatGPT/Zara review of Claude v0.3.1

**Proposal:** Derive authority mechanically from source_kind + source_role.

**Decision:** `adopted_with_structural_modification`

**Why:** Authority also depends on provenance and whether the current human actually holds design authority. The patch now validates authority from multiple fields rather than assuming every design source is human-authority.

## ZAR-03 — ChatGPT/Zara review of Claude v0.3.1

**Proposal:** Context must not participate in the design read.

**Decision:** `adopted_with_scope_refinement`

**Why:** Context must stay outside target design reconstruction/compression, but can legitimately anchor geolocation, north and site relationships and may have its own compact representation.

## ZAR-04 — ChatGPT/Zara review of Claude v0.3.1

**Proposal:** Wing B may be T3 within tolerance except one door delta.

**Decision:** `adopted_after_t3_definition_fix`

**Why:** The previous T3 definition required a whole-geometry match and therefore contradicted the fixture. T3 now permits explicit detected deltas only when residual/base geometry matches within tolerance.

## ZAR-05 — ChatGPT/Zara review of Claude v0.3.1

**Proposal:** Every record has authority/confidence matching authority_mapping.

**Decision:** `modified`

**Why:** convention, ambiguous and unknown records can be non-evidence/open records. Requiring a canonical authority for them contradicted the mapping's own 'none' entries.

## CL3-01 — Claude v0.3.2 review

**Proposal:** Remove leftover source_role and stale authority_mapping terminology.

**Decision:** `adopted`

**Why:** Stale fields contradicted the orthogonal partition model and would fail curator consistency checks.

## CL3-02 — Claude v0.3.2 review

**Proposal:** Make design_authority_relation use four values consistently, including not_applicable.

**Decision:** `adopted`

**Why:** Every partition now has a deterministic value; existing_world cannot silently omit the field.

## CL3-03 — Claude v0.3.2 review

**Proposal:** Fill authority-resolution gaps for existing-world evidence, unknown design authority, human approximations and derived confidence.

**Decision:** `adopted`

**Why:** These are common reading cases and were otherwise under-specified.

## CL3-04 — Claude v0.3.2 review

**Proposal:** Prevent T3 from absorbing unlimited difference as deltas.

**Decision:** `adopted`

**Why:** T3 now allows only classifiable local deltas and requires a predeclared max_delta_share.

## CL3-05 — Claude v0.3.2 review

**Proposal:** Add participation_role=excluded for scratch/history content.

**Decision:** `adopted`

**Why:** Keeps source inventory and coverage honest without forcing scratch geometry into target/context reading.

## CL3-06 — Claude v0.3.2 review

**Proposal:** Add IR-CC-02 covering consultant design context and existing-world target.

**Decision:** `adopted`

**Why:** The new orthogonal source model needs a fixture beyond the simplest human-authored design case.

## MIS3-01 — Mistral v0.3.2 review

**Proposal:** Use target rather than design-only wording in IR-08/RA-04 and exercise existing-world target coverage.

**Decision:** `adopted`

**Why:** A renovation scan can be existing_world and still be the primary read target.

## MIS3-02 — Mistral v0.3.2 review

**Proposal:** Re-key authority by world_relation × design_authority_relation (+ provenance); participation_role must not change authority.

**Decision:** `adopted`

**Why:** Context/target is a reading-role axis, not an evidence-authority axis.

## MIS3-03 — Mistral v0.3.2 review

**Proposal:** State claim_link timing explicitly.

**Decision:** `adopted`

**Why:** Input Reading creates evidence items; USG claims and claim_status exist only when those records are consumed downstream.

## MIS3-04 — Mistral v0.3.2 review

**Proposal:** Map each conformance failure to the RA checks it should trip and add a provisional materiality table.

**Decision:** `adopted`

**Why:** Makes IR-13 and the conformance fixtures machine-checkable rather than narrative.

## CL4-01 — Claude v0.3.3 review

**Proposal:** Existing-world human statements must use external_evidence rather than human authority.

**Decision:** `adopted`

**Why:** This aligns with canonical v0.12: human authority covers project/design decisions, while factual existing-world statements enter as evidence.

## CL4-02 — Claude v0.3.3 review

**Proposal:** Define source_origin and add unknown-origin handling.

**Decision:** `adopted`

**Why:** Authority rules referenced source_origin without a schema field; unknown origin must not inherit professional authority.

## CL4-03 — Claude v0.3.3 review

**Proposal:** Give authority rules fixed order, first-match semantics, and invalid default; fill common gaps.

**Decision:** `adopted`

**Why:** Prevents overlapping rules from assigning conflicting authorities and prevents unmatched records from silently choosing authority.

## CL4-04 — Claude v0.3.3 review

**Proposal:** Define the measure behind delta_share.

**Decision:** `adopted`

**Why:** A percentage is meaningless unless the denominator/measure is declared.

## CL4-05 — Claude v0.3.3 review

**Proposal:** Complete materiality table and define override precedence.

**Decision:** `adopted`

**Why:** Makes high_examples and conflict propagation operational rather than advisory.

## CL4-06 — Claude v0.3.3 review

**Proposal:** Remove duplicate conformance_candidate and merge duplicate claim_link definition.

**Decision:** `adopted`

**Why:** Duplicate structures would drift and undermine the curator's single-source checks.

## CL4-07 — Claude v0.3.3 review

**Proposal:** Make IR-CC-02 ceiling conflict deterministic with explicit scan value and tolerance.

**Decision:** `adopted`

**Why:** A conformance fixture must have one expected outcome rather than depend on reader-chosen tolerance.
