# Repository structure

```text
USG/
├── README.md
├── AGENTS.md
├── core/                  # navigation summaries derived from protocol
├── protocol/CURRENT       # pointer to the current protocol version
├── protocol/versions/     # immutable protocol versions
├── schema/                # external/handoff schemas
├── conformance/instances/ # pinned regression/stress cases
├── tests/                 # mutation/conformance tests
├── tools/                 # runner, checker, geometry validator
├── history/               # patches and migrations
├── inbox/                 # unfiltered public learning intake (only public write path)
├── curation/LOG.md        # curation log: read first, append after every pass
├── curation/records/      # machine-readable curator decisions, by year
├── curation/archive/      # curated inbox originals, moved out of inbox/
├── examples/              # generated drawings / worked examples
├── docs/                  # architecture and explanatory material
└── archive/               # exact historical release bundles
```

## Authority

The protocol version named in `protocol/CURRENT` (now `protocol/versions/USG_v0_12.json`) is the current machine-readable source of truth. Navigation summaries, docs and external schemas must not silently override it.
