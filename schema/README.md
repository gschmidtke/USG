# Schemas

This folder is for external integration and handoff schemas. USG v0.12's canonical internal schemas remain embedded in `protocol/versions/USG_v0_12.json` until they can be extracted without breaking non-regression.

- `usg-output.schema.json` — integration draft of the USG result/handoff envelope; stage fields take protocol stage ids S00–S20.
- `neutral-building-spec.schema.json` — integration draft of a software-neutral building handoff reconstructed from source material; worked instance in `examples/building-002/`.
- `inbox-submission.schema.json`, `curation-record.schema.json` — governance contracts.

None of these replaces the protocol's internal schemas.
