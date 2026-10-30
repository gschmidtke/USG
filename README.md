# USG — Universal Structure Generation

USG is a framework for resolving a human need into a **software-neutral specification of a built structure** before choosing how that intent will be represented or executed in a particular tool.

Its core premise is simple:

> **Need first. Geometry last.**

USG asks enough questions to determine what must exist, why it must exist, how it must perform, and how success will be judged. It then hands that resolved intent downstream to governed production.

## Start here — route the question first

If you are a human or AI arriving here, do **not** assume this repository owns the whole task. Start at the highest unresolved layer:

1. **What are we trying to achieve, and why?** → **USG** — stay here.
2. **What is required or permitted, who has authority, what must a BEP/company/project standard contain, or what evidence proves compliance?** → **TIVERIT BIM Standards** — https://github.com/gschmidtke/TIVERIT-BIM-STANDARDS
3. **How has this been done successfully in Revit, what failed before, and how should the result be verified?** → **ARPL** — https://github.com/gschmidtke/ARPL
4. **Can the current Revit/API implementation perform the required operation?** → **API capability lookup** — authoritative API documentation or the external Autodesk Platform Services `dll2llm` / API Navigator: https://github.com/autodesk-platform-services/dll2llm
5. **Execute the resolved operation in Revit.** → the user's authorized **Revit Bridge / executor**.
6. **Automate, verify, repair, or produce governed evidence in supported workflows.** → **ZEN** where applicable.

This is a **navigation route, not a requirement to invoke every layer**. Start at the highest materially unresolved question and continue downstream only as far as the task requires. A downstream capability or successful execution must never overwrite upstream intent, standards, user authority, or professional acceptance.

## Position in the AEC AI stack

USG is the upstream intent-resolution layer in a broader AI-driven AEC workflow:

```text
USG
purpose / intent / required outcome
    ↓
TIVERIT BIM Standards
normative requirements / authority / compliance evidence
    ↓
ARPL
professional Revit production precedent / failure memory
    ↓
API capability lookup
    ↓
Revit Bridge
bounded Revit execution
    ↓
ZEN
productized governed automation / verification / repair / evidence
```

Public repositories owned by Gottfried Schmidtke:

- TIVERIT BIM Standards — https://github.com/gschmidtke/TIVERIT-BIM-STANDARDS
- ARPL — https://github.com/gschmidtke/ARPL

For AI-driven Revit work, capability discovery should occur **after** intent, standards and production logic are resolved and **before** execution. A useful external reference is Autodesk Platform Services `dll2llm` / API Navigator:

https://github.com/autodesk-platform-services/dll2llm

That external project is not owned or governed by this repository. Treat capability lookup as evidence of what an API can do, never as authority for what the project should do.

Revit Bridge and ZEN are downstream TIVERIT implementation/product layers; they are referenced here by role rather than presented as public repositories.

USG remains software-neutral as long as possible.

## Canonical protocol

The current machine-readable source of truth is the version named in `protocol/CURRENT`:

```text
protocol/versions/USG_v0_12.json
```

Historical protocol versions remain immutable. Behavioral changes follow **patch, never rewrite** governance and are verified against conformance cases and mutation tests.

USG v0.12 contains the authoritative 21-stage / five-phase protocol (S00–S20). `core/stages.json` is a navigation summary generated from that protocol by `tools/build_stages.py`, not a replacement for it; CI fails if the two drift apart.

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

External contributors should change only `inbox/**`. See `CONTRIBUTING.md`. Curator behavior is defined in `CURATION.md`; every curation pass is logged in `curation/LOG.md`, which each curator reads first.

## Architectural sketch proposal

Current work is exploring the rule:

> **Dimensions override proportion. Proportion fills the gaps. User clarification resolves contradictions.**

This remains a proposal until adopted through the governed protocol-patch process. See `docs/proposals/architectural-sketch-reconstruction.md`, how its evidence classes would map onto the canonical evidence model in `docs/proposals/evidence-class-mapping.md`, and the worked loop in `examples/building-002/`.

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
