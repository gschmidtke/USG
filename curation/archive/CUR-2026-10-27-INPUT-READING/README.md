# USG Input Reading v0.3.4

This patch applies Claude's review of v0.3.3.

Key changes:
- existing-world human statements use `external_evidence` + canonical `owner_statement`, max medium confidence;
- `source_origin` is defined, including `unknown`;
- authority resolution is ordered (`first_match_wins`) with an invalid/high-materiality default;
- missing authority cases are covered, including external approximate design values and unknown-origin existing-world records;
- derived confidence inherits the weakest input;
- T3 `delta_share` now declares its measurement basis;
- the materiality table is complete and high-example/conflict/propagation overrides are explicit;
- duplicate `conformance_candidate` and duplicate claim-link structures are removed;
- IR-CC-02 has a deterministic ceiling conflict: ~3000 mm owner note vs 2850 mm scan, ±50 mm tolerance.

Status: discussion draft / candidate USG inbox submission. Not canonical.

Repository:
https://github.com/gschmidtke/USG
