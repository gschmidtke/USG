# USG architecture

USG resolves human intent into a software-neutral specification that can be handed to downstream production systems.

## Position in the strata

```text
3XFF
Reality frame / observer / context
    ↓
USG
Problem / purpose / required resolution
    ↓
ARPL
Production representation / governance
    ↓
Capability lookup / typed operation
    ↓
Execution
```

## Resolution chain

USG uses this chain:

`Purpose -> Actors -> Functions -> Capacity -> Relationships -> Physics -> Context -> Regulation -> Performance -> Form -> Systems -> Elements -> Validation`

The chain is not a mandatory waterfall. The agent should enter at the lowest stage already sufficiently resolved by the user or source material.

## Design principles

1. Preserve parent purpose while descending.
2. Resolve only as deeply as the requested outcome requires.
3. Keep assumptions explicit.
4. Distinguish exact, derived, approximate, observed, ambiguous, and unknown information.
5. Use proportional reconstruction when design intent is clear but dimensions are absent.
6. Ask the user only when contradictions or material ambiguity block a coherent resolution.
7. Keep outputs software-neutral until production representation is deliberately chosen downstream.
8. Carry acceptance invariants into the downstream handoff.
9. If downstream evidence contradicts a premise, invalidate only dependent conclusions.

## Intended repository areas

- `core/` — canonical stage definitions and shared logic.
- `schema/` — machine-readable input/output contracts.
- `docs/` — architecture, interfaces and explanatory material.
- `examples/` — worked cases and test inputs/outputs.
- `archive/` — legacy/release bundles retained for provenance.

USG should remain small enough that AI systems can retrieve only the relevant stage knowledge instead of loading an entire domain corpus.
