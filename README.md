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

USG does not choose a Revit API call, a Rhino command, or an IFC entity unless the problem itself requires that target. It should remain software-neutral as long as possible.

## Resolution chain

`Purpose -> Actors -> Functions -> Capacity -> Relationships -> Physics -> Context -> Regulation -> Performance -> Form -> Systems -> Elements -> Validation`

This is not a mandatory waterfall. USG should enter at the **lowest already-resolved stage** that still preserves the parent purpose.

## Architectural sketch rule

When source material is an architectural sketch:

> **Dimensions override proportion. Proportion fills the gaps. User clarification resolves contradictions.**

Approximate geometry is valid temporary design information when intent is clear. Missing exact dimensions do not automatically make visible form unusable.

## Repository structure

```text
USG/
├── AGENTS.md                 AI operating contract
├── README.md                 Project overview
├── core/                     Canonical USG logic
│   └── stages.json
├── schema/                   Machine-readable contracts
│   └── usg-output.schema.json
├── docs/                     Architecture and interfaces
│   └── architecture.md
├── examples/                 Worked resolution cases
│   └── README.md
├── USG_v0_12.zip             Existing v0.12 archive (to be unpacked/reviewed)
├── USG_Article_Need_First_Geometry_Last.docx
└── Inductive vs Deductive Thinking Infographic.png
```

## Current status

This repository is being established as the canonical working home for USG. The existing `USG_v0_12.zip` is retained unchanged until its contents are unpacked and reviewed against this base structure.

The base structure intentionally stays small. Existing v0.12 logic should be preserved where it already works; new structure should clarify and expose that logic rather than replace it prematurely.
