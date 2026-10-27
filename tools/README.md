# Tools

- `check_usg.py` — protocol self-consistency, governance and non-regression checker.
- `run_usg.py` — executes pinned instances through implemented stage gates.
- `usg_geometry.py` — dependency-free geometry checks used by the runner.
- `build_stages.py` — regenerates `core/stages.json` from the current protocol; `--check` fails if the committed summary has drifted (run in CI).

These tools implement/check the protocol; they are not protocol authority.
