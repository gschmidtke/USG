# USG — Universal Spec Generator

USG is a framework for resolving a human need into a **software-neutral specification** before choosing how that intent will be represented or executed in a particular tool.

Its core premise is simple:

> **Need first. Geometry last.**

USG asks enough questions to determine what must exist, why it must exist, how it must perform, and how success will be judged. It then hands that resolved intent downstream to production logic such as ARPL.

## Position in the reasoning stack

```text
3XFF
Reality frame / context
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

USG remains software-neutral as long as possible.

## Canonical protocol

The current machine-readable source of truth is:

```text
protocol/versions/USG_v0_12.json
```

Historical protocol versions remain immutable. Behavioral changes follow **patch, never rewrite** governance and are verified against conformance cases and mutation tests.

USG v0.12 contains the authoritative 21-stage / five-phase protocol. `core/stages.json` is a navigation summary derived from that protocol, not a replacement for it.

## Learning architecture

USG is designed to improve through curated learning.

```text
Human / AI / production experience
              ↓
           inbox/**
              ↓
            Curator
              ↓
 normalize / deduplicate / test
              ↓
  curation record / proposal / patch
              ↓
       canonical USG knowledge
```

Three authority levels are intentionally separated:

- **Inbox** — writable/unfiltered evidence and learning.
- **Curated knowledge** — reviewed, normalized and traceable learning.
- **Protocol** — governed, versioned behavioral authority.

External contributors should change only `inbox/**`. See `CONTRIBUTING.md`. Curator behavior is defined in `CURATION.md`.

## Architectural sketch proposal

Current work is exploring the rule:

> **Dimensions override proportion. Proportion fills the gaps. User clarification resolves contradictions.**

This remains a proposal until adopted through the governed protocol-patch process. See `docs/proposals/architectural-sketch-reconstruction.md`.

## Repository structure

```text
USG/
├── README.md
├── AGENTS.md                  AI operating contract
├── CURATION.md                curator contract
├── CONTRIBUTING.md            public contribution rules
├── protocol/versions/         immutable protocol versions
├── core/                      derived navigation summaries
├── schema/                    machine-readable integration/intake contracts
├── inbox/                     unfiltered public learning intake
├── curation/                  machine-readable curator decisions
├── conformance/instances/     pinned regression/stress cases
├── tests/                     mutation/conformance tests
├── tools/                     checker, runner, geometry validator
├── history/                   protocol patches and instance migrations
├── examples/                  worked cases and generated artifacts
├── docs/                      architecture, proposals, articles, setup docs
└── archive/                   exact historical release bundles
```

## Public-governance model

The repository is being prepared so humans and AIs may contribute learning through pull requests under `inbox/**`, while canonical paths remain curator-controlled.

Repository controls include:

- CODEOWNERS;
- an Inbox-only external PR guard;
- curator-only canonical validation;
- machine-readable Inbox and curation schemas.

The remaining GitHub visibility/ruleset settings that require repository-admin UI configuration are documented in `docs/public-repository-setup.md`.
