# Input Reading fixtures

Both fixtures are specified in [`../spec.json`](../spec.json) (`conformance_candidates`), with their construction, expected results and the RA checks each planted failure must trip. Neither exists as a source model yet.

| Id | Name | Tests | Status |
|---|---|---|---|
| IR-CC-01 | Two-wing input-reading test | units, context, levels, facade repeats with one exception, mirrored wing with one unmirrored door, identity-less slab, misleading name | specified, not built |
| IR-CC-02 | External-design and existing-world authority test | consultant design model as context, scan of an existing building as target, owner note vs scan conflict, excluded scratch geometry | specified, not built |

Fix C-01 to C-07 (see [`../README.md`](../README.md)) before building IR-CC-02: under the current rules its 2850 mm scan height has no authority rule (C-01).

When built, each fixture goes in its own folder here: the source file(s), the expected evidence records, and the expected RA results.
