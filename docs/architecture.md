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

## Stage model

USG v0.12 defines 21 stages in five phases (canonical: the protocol named in `protocol/CURRENT`; summary: `core/stages.json`):

| Phase | Stages |
| --- | --- |
| concept | S00 purpose · S01 strategic_feasibility · S02 constraint_screen · S03 actors · S04 context · S05 scenarios · S06 functions |
| schematic | S07 capacity · S08 relations · S09 physics_and_regulation · S10 performance · S11 semantic_model · S12 topology_generation · S13 topology_validation |
| design_development | S14 geometry_generation · S15 system_sizing · S16 elements |
| technical_design | S17 independent_validation · S18 scoring · S19 human_acceptance · S20 export |

The chain is not a mandatory waterfall. The agent should enter at the lowest stage already sufficiently resolved by the user or source material.

## Design principles

1. Preserve parent purpose while descending.
2. Resolve only as deeply as the requested outcome requires.
3. Keep assumptions explicit.
4. Keep every value's authority and claim status explicit (`answer_authority`, `evidence_model`); for sketches, the proposed source classes exact / derived / approximate / observed / ambiguous / unknown apply (proposal, see `docs/proposals/`).
5. Use proportional reconstruction when design intent is clear but dimensions are absent (proposal).
6. Ask the user only when contradictions or material ambiguity block a coherent resolution.
7. Keep outputs software-neutral until production representation is deliberately chosen downstream.
8. Carry acceptance invariants into the downstream handoff.
9. If downstream evidence contradicts a premise, invalidate only dependent conclusions.

## Intended repository areas

- `protocol/` — the canonical, immutable protocol versions; `protocol/CURRENT` names the current one.
- `core/` — navigation summaries generated from the protocol.
- `schema/` — machine-readable input/output contracts.
- `docs/` — architecture, interfaces and explanatory material.
- `examples/` — worked cases and test inputs/outputs.
- `archive/` — legacy/release bundles retained for provenance.

USG should remain small enough that AI systems can retrieve only the relevant stage knowledge instead of loading an entire domain corpus.
