# Repository structure

"
            "```text
"
            "USG/
"
            "├── README.md
"
            "├── AGENTS.md
"
            "├── core/                  # navigation summaries derived from protocol
"
            "├── protocol/versions/     # immutable protocol versions
"
            "├── schema/                # external/handoff schemas
"
            "├── conformance/instances/ # pinned regression/stress cases
"
            "├── tests/                 # mutation/conformance tests
"
            "├── tools/                 # runner, checker, geometry validator
"
            "├── history/               # patches and migrations
"
            "├── examples/              # generated drawings / worked examples
"
            "├── docs/                  # architecture and explanatory material
"
            "└── archive/               # exact historical release bundles
"
            "```

"
            "## Authority

"
            "`protocol/versions/USG_v0_12.json` is the current machine-readable source of truth. Navigation summaries, docs and external schemas must not silently override it.
