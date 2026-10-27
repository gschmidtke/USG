# Source adapters

A source adapter reads one kind of input (an existing model, a drawing set, a scan, a sketch) and hands USG **evidence records**, not conclusions. Adapters sit in front of the stage model, as `docs/proposals/source-neutral-interpretation-handoff.md` describes: they add no stage and change no stage.

| Adapter | Status | Version | Record |
|---|---|---|---|
| [`input-reading/`](input-reading/README.md) | proposal, owner decision pending | 0.3.4 | `CUR-2026-10-27-INPUT-READING` |

`docs/proposals/architectural-sketch-reconstruction.md` is a candidate second adapter. Moving it here is part of its pending promotion decision (LOG-0008).

## Boundary rules

1. **The protocol owns the interface.** The evidence-record fields an adapter emits, and what each field means, are defined by the protocol (`answer_authority`, `evidence_model`, `geometry_model.authority`). An adapter may propose new fields; they become binding only through a protocol patch.
2. **The protocol owns authority.** An adapter supplies the fields that authority rules read; it never decides by itself which authority a value carries. Authority rules an adapter proposes, such as Input Reading's `authority_resolution`, go into the protocol when accepted, not into the adapter.
3. **The adapter owns its method.** How a source is read (passes, repeat proofs, grids, acceptance checks) belongs to the adapter. It is versioned on its own and changes without a protocol version bump.
4. **Declared compatibility.** Each adapter has an `adapter.json` naming its version, status, spec, and the protocol versions it is written against.
5. **Checked at the boundary.** When an adapter is accepted, CI validates its fixture outputs against the evidence schema of the current protocol, so a protocol patch that breaks an adapter fails on the same pull request. Until then, adapter tools run by hand and are not in CI.
6. **Same governance.** Patch, never rewrite; a changelog per version; every change through a curation pass and a `curation/LOG.md` entry.

## Layout

```text
adapters/<name>/
├── README.md      what it is, how it fits, open gaps, owner decisions
├── adapter.json   manifest: version, status, spec, compatible protocol
├── spec.json      the machine-readable method
├── tools/         adapter-specific checks
└── fixtures/      pinned test sources and their expected records
```
