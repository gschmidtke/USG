# From the ARPL curator to the USG curator — 2026-10-28

**From:** Claude, ARPL curator (acting for Gottfried Schmidtke)
**To:** the USG curator (Zara / ChatGPT, on the owner's decision of 2026-10-28)
**Status:** inbox material, not canonical. Curate under `CURATION.md`.

## How the two repositories work together from now on

Decided by the owner on 2026-10-28:

1. USG is curated by Zara. ARPL is curated by Claude.
2. The ARPL curator does not change canonical USG content. Anything ARPL learns that may belong in USG arrives here, in `inbox/arpl-curator/`, as a pull request that touches only `inbox/**`.
3. The ARPL curator reads the curated USG repository once a week. It checks what changed in the protocol, in `docs/handoff-to-arpl.md` and in `schema/usg-output.schema.json`, and files ARPL-side consequences in ARPL. Questions or contradictions come back through this inbox.

## 1. Open pull requests waiting for a curation decision

These were prepared by Claude as USG curator before the hand-over. They are open and not merged. Please review, merge, change or close them as you see fit; none of them changes the stage model.

| PR | Branch | Content |
|---|---|---|
| #10 | `curator/log-0013-input-reading` | LOG-0013 / LOG-0014: Input Reading adapter as a proposal (v0.3.4), curation gaps C-01 to C-04, an exhaustive walk of the authority rules |
| #11 | `usg-input-reading` | LOG-0015 / LOG-0016: Input Reading as its own adapter module; Mistral's review of the series |
| #12 | `lesson-option05-input-reading` | Owner's inbox lesson: Option 05 Input Reading and a pipeline test case |
| #13 | `inbox-input-read-goal` | Owner's inbox note: Input Read goal and stopping guardrails |

Suggested order: #10 → #11 (it builds on #10), then the two inbox PRs #12 and #13 as their material.

## 2. ARPL lessons from 2026-10-28 that may be tool-agnostic

ARPL is Revit-specific, while USG is not. The lessons below were learned in Revit, but they are stated without Revit terms. Take only what fits USG's function-first scope. The ARPL sources are cited so the evidence can be checked.

1. **Count by identity, never by row.** A listing can show one object several times (a stair that spans levels appears once per level). Every count, completeness score and quantity is taken over unique identities. ARPL: FP55, ARPL-QA-0002 rev 2. USG relevance: Input Reading coverage (RA-04) and source identity (RA-10).
2. **Every input record ends somewhere.** Each input record is either used or listed as a named exception with a reason. A filter that drops records before counting lets totals reconcile while content disappears. ARPL: FP60 (seen twice in one day), ARPL-SCH-0003. USG relevance: the `excluded` participation role already demands this; the lesson is that the check must cover the reader's own filters too.
3. **Names are evidence, categories can lie.** A railing type was used to draw road striping (625 LF of "railing"). The object's declared kind and its function disagreed, and only a quantity view exposed it. ARPL: FP01, ARPL-BOM-0001 lesson 8. USG relevance: supports CLA-03 ("names, tags and groups are evidence, not truth") with a production example.
4. **The unit of an output follows kind + material, never kind alone.** A beam is bought by length (steel) or by volume (concrete). ARPL: ARPL-BOM-0001. USG relevance: if USG ever states quantities in its output, the unit is part of the claim.
5. **Requirements, not products.** A bill of materials states technical requirements. A specific product enters only where an engineer or designer has specified it (basis of design). Owner decision, ARPL-BOM-0001 v1.4. USG relevance: fits "function first, geometry second". The handoff to ARPL may need a field that marks a specified product as distinct from a requirement.
6. **Parts follow the purchase unit.** A part inside an assembly belongs to the assembly (a window's mullions). A part that is bought on its own is its own item (chairs in a table family; curtain-wall mullions). This is the owner's rule. USG relevance: prototype/instance thinking in Input Reading (IR-05 to IR-07). Identity of a nested part is a separate question from whether it counts as its own item.
7. **Silent loss is worse than a reported gap.** An independent AI review lost a whole discipline to a transfer limit and kept reporting "all disciplines". The owner's rule since then: check that every expected input is present before building a report, and treat a missing input as a stop, never as an omission. ARPL: ARPL-PW-0003 rev 7. USG relevance: reading acceptance, an input-presence check before RA-04.

## 3. Owner decisions that touch both repositories

- Reviews of ARPL or USG output by other AIs are a development tool for improving the protocols, not a step in an agent's production routine (ARPL `CURATION.md`, 2026-10-28).
- The owner is building a separate BIM Standards repository. Model-setup conventions (levels and grids from one coordination file, worksets by category) and role scopes will live there, not in USG.

## What the ARPL curator needs back

- Your decision on PRs #10–#13, so that ARPL can follow the Input Reading adapter once it is accepted.
- Any change to `docs/handoff-to-arpl.md` or `schema/usg-output.schema.json`. These are the contract ARPL builds on.
