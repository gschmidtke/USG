# Proposed: purpose recovery from legacy automation sources

**Status: adopted as direction (owner decisions delegated to the USG curator, 2026-11-04, LOG-0023). Not canonical protocol: no protocol, schema or stage change.**
**Record:** `CUR-2026-11-04-LEGACY-AUTOMATION-PURPOSE`
**Origin:** DEVELOPER research (Mis) for LLCO, PM review (Zara), curated by Claude as USG curator under DEC-005. Sources are pinned in the record.

## What this is

Most USG sources describe a structure: a sketch, a model, a drawing set. A legacy automation estate (AutoLISP routines, scripts, block libraries, extraction tables) is different: it describes **how a firm produced** structures. Recovering its purpose means separating what the production process needed from what the old platform made convenient, before choosing a successor.

This fits the Input Reading goal unchanged (`CUR-2026-11-03-INPUT-READ-GOAL`): *convert an arbitrary source into the smallest verified, tool-neutral representation sufficient to continue the intended production process.* For this kind of source, the "intended production process" is the thing to recover.

## Placement: a candidate source adapter, not a stage or schema

- Position: a candidate **source adapter** ("legacy automation"), under `adapters/README.md` rules 1–6.
  - Its method (reading layers L1–L7, goal records, dispositions) belongs to the adapter and to its owning technical project, LLCO.
  - The protocol is not touched.
- Status: it stays a proposal until a rights-cleared real production estate has been read end to end. Today there is no such estate; the corpus holds only utility libraries.
- Interface: it reuses existing USG concepts for everything it hands over (table below). New fields stay adapter-local, as decided for Input Reading's partition fields (LOG-0021): local until a second adapter needs them.

## Mapping to existing USG concepts (no duplication)

| Goal Record field (LLCO proposal) | Existing USG concept it maps to | Note |
|---|---|---|
| candidate `purpose` | `statement_model` statement, type `assumption`, authority `ai_generated` until confirmed (`answer_authority.assumption_rule`) | A purpose is confirmed only by human authority (§Authority) |
| essential logic / platform mechanism / era constraint | `statement_model.concerns`: `outcome` / `condition` vs `means` | Adapter-local refinement for `means` only: `means_reason: platform_mechanism \| era_constraint \| unknown` |
| firm convention, client requirement, external standard, drafting habit | `statement_model.basis` + `relaxable_by` | firm convention → `stakeholder_choice`, relaxable by the firm; client requirement → `stakeholder_choice`, relaxable by the client; code → `legal`; drafting habit → `preference` or `assumption`; unknown → open |
| observed behaviour | `evidence_model` items on a **behaviour claim** | LLCO evidence kinds map to evidence items with source and confidence |
| `choices` / `compatibility` | `rule_model` (`strength`, `source_ref`, `statement_type`) | Two scopes kept apart: object rules inside a document vs catalogue availability rules |
| `cross_output_consistency`, `acceptance_criteria` | source-neutral hand-off, *target-independent acceptance* (adopted as direction, LOG-0021) | Stated as invariants with read-back evidence, never as tool commands |
| `exceptions`, `required_human_confirmation` | `pending_user` gate + Input Reading `materiality` table | High-materiality open items block binding output |
| `provenance` | evidence `source_ref`, pinned `repo@commit` | |

## Three claims per kernel, never one status

For each recovered kernel, three separate USG claims are evaluated by `evidence_model.claim_status_rule`:

1. **Behaviour:** "routine R gives output Y for input X." Recorded runs in the original environment can make it `confirmed_positive` for the tested inputs only. A substitute runtime counts only where it is calibrated.
2. **Purpose:** "R exists to achieve P for beneficiary B." Matching historical outputs, structure and comments are supporting evidence, never deciding. **Only the authorized process owner** (human authority: purpose, acceptance) confirms it. Statements from practitioners are capped at medium confidence (owner_statement rule), and so are interested parties (reviewer_independence).
3. **Correctness:** "Y is what the process should produce." It is decided by governing documents (specifications, contracts, option catalogues, QA records) and by the process owner. Regulated content (structural, life safety) goes to `professional_review`. A long-used defect is a behaviour fact; it is not evidence of why it was tolerated.

## Disposition per goal (many-to-many, explicit)

Each goal lists its coverage items. Each item has one disposition, an authority and evidence:

| Disposition | Meaning |
|---|---|
| `native_coverage` | Covered by a target platform feature. Needs versioned primary-source evidence and must say native, configured, scripted or product extension |
| `external_system` | Covered by another system (configurator, estimating, ERP) |
| `retained_legacy` | The legacy routine stays, with the reason |
| `reimplement` | Becomes a rule in a library (ARPL / USG domain library), through that repository's adoption |
| `retire` | No longer needed, with reason and authority |
| `uncovered_gap` | Known and not covered: never silent |
| `undecided` | Open; it blocks binding output that depends on it |

A goal may need several items and a rule may serve several goals. No new rule is required where `native_coverage` or `external_system` suffices.

## Readiness before successor design

Derived, not a fixed count. A successor design may start when:

1. every required output is listed;
2. every choice and compatibility rule has a status (confirmed, assumed or open), and every open one is `pending_user`;
3. the acceptance basis is declared (reference outputs with their element scope);
4. the cross-output consistency pairs are written as invariants;
5. every goal has a disposition, `undecided` included.

**Default reconciliation basis (curator decision, LOG-0023):** coverage, not a count. A reconciled historical case is a past released output reproduced with read-back evidence. Before successor design:

- every **choice** in the option space appears in at least one reconciled historical case;
- every **required output** appears in at least one reconciled historical case;
- every **boundary** of a compatibility or quantity rule has a test case;
- the reconciliation is **re-run by a second runner**.

The authorized owner of an engagement may raise this basis. Lowering it is recorded as an accepted unresolved item under the materiality rule. It is not a protocol constant.

## Explicitly not proposed

- No new USG stage; no canonical Goal Record schema in USG.
- No mandatory single `goal_record` field on rule records. The link is many-to-many and lives on the goal side, with an optional derived back-reference.
- No protocol field for the means classification. `concerns` already carries it.
- No general claims about all LISP estates, about transition durations, or about Revit capability without versioned sources.

## Decisions (LOG-0023, delegated by the Owner)

1. **Direction adopted.** This document is the agreed direction for purpose recovery. Its fields stay adapter-local in LLCO.
2. **Placement of recovered firm conventions.**
   - A recovered firm convention belongs to the estate owner. It stays in that estate's records (LLCO, client-owned deliverable) and is **referenced, not imported**.
   - Content enters a USG `domain_library` only by answering `library_model.generalization`, i.e. as a generalized, owner-released pattern.
   - **No new library layer.** A firm/catalogue overlay is reconsidered only when two estates show the same need.
3. **A qualifying estate, required for promotion to `adapters/legacy-automation/`.** It must:
   - be rights-cleared for study and for publishing derived records;
   - contain at least one option-to-documents or option-to-BOM chain;
   - come with released historical outputs for reconciliation;
   - have a named process owner available for purpose rulings.

   Finding and acquiring such an estate is commercial and outside curation; the curator only sets the criteria.
4. **Readiness threshold:** the coverage-based default above.

Promotion to an adapter additionally needs an independent review of the goal records; the author's self-review does not count.
