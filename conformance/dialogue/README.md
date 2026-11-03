# Dialogue conformance cases

The cases in `conformance/instances/` test the protocol engine: given a project state, does the pipeline reach the expected gate? They cannot test how an AI **talks** to a human while executing USG.

Dialogue cases fill that gap. Each states a user message, the expected classification, the expected first turn, and what makes a turn nonconforming. They are checked by reading an agent's transcript against the case; they are not run in CI.

The behaviour they check is already canonical in v0.12 (`inquiry_model`: one question, one authority, one value per step) and in `AGENTS.md` (LOG-0017). A case adds no rule; it makes an existing rule testable.

| Case | Checks | Source |
|---|---|---|
| [DLG-01](DLG-01-bridge-first-turn.md) | First turn asks only the current purpose question; no downstream questions bundled | `CUR-2026-11-03-PROGRESSIVE-INQUIRY-BUNDLING` |
