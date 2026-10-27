# USG Curation Contract

USG is intended to improve through learning while remaining reproducible, inspectable, and machine-readable.

The **Inbox is deliberately permissive**. New knowledge may arrive as raw notes, JSON, Markdown, test cases, transcripts, failure reports, sketches, comparisons, external reviews, or other evidence. Contributors are not required to understand the canonical USG protocol before submitting useful material.

The **Curator** is the controlled boundary between unfiltered learning and canonical USG knowledge.

## Core principle

> Raw learning may enter freely. Canonical USG changes only after review, normalization, provenance, testing, and explicit acceptance.

Nothing in `inbox/` is authoritative merely because it exists there.

## Curator role

The curator reviews Inbox contributions and determines what, if anything, should become part of USG.

The curator must:

0. **Read `curation/LOG.md` first.**
   - Read its *Open items* and at least the last five entries before reviewing anything.
   - Do not repeat, contradict or undo an earlier decision silently; if you disagree with one, say so in your own log entry.
   - This applies to every curator: Claude, ChatGPT, any other AI, or a human.

1. **Read the submission in context.**
   - Identify the actual lesson, failure, correction, new evidence, proposal, or contradiction.
   - Preserve the contributor's meaning before translating it into USG vocabulary.

2. **Check for existing knowledge.**
   - Search the current protocol, prior versions, patches, proposals, conformance cases, tools, and documentation.
   - Prefer extending or correcting an existing concept over creating a duplicate.

3. **Classify the contribution.**
   Typical destinations include:
   - protocol rule or schema change;
   - stage/gate refinement;
   - evidence/authority rule;
   - feedback-loop behavior;
   - new conformance/regression case;
   - failure pattern;
   - worked example;
   - documentation/explanation;
   - proposal requiring more evidence;
   - rejected/non-generalizable learning.

4. **Separate general learning from case-specific detail.**
   - Extract reusable logic without silently carrying private, client-specific, project-specific, or irrelevant details into canonical knowledge.
   - Preserve source provenance so the lesson can be traced back to its evidence.

5. **Normalize the learning into machine-readable form.**
   - State the rule or proposed change explicitly.
   - State when it applies and when it does not.
   - Record assumptions, dependencies, evidence, confidence, affected stages/objects, and expected validation behavior.
   - Use stable identifiers where the canonical protocol already provides them.

6. **Assess authority and contradiction.**
   - A new submission does not silently override the current protocol.
   - If it contradicts canonical USG behavior, record the conflict explicitly.
   - Determine whether the conflict is a bug, a scope distinction, a proposed policy change, or unresolved evidence.

7. **Create or update tests before canonical adoption where behavior changes.**
   - Add or update pinned conformance instances and/or mutation tests.
   - Preserve non-regression behavior that is not intentionally changed.
   - A protocol change that cannot be tested should carry an explicit reason and review note.

8. **Use patch, never rewrite.**
   - Historical protocol versions remain immutable.
   - Canonical behavioral changes become a new patch/version and corresponding migration where required.
   - Never edit an old version in place merely to make history look cleaner.

9. **Record the curation decision, and log the pass.**
   - Add one entry at the top of `curation/LOG.md` (who, input, decision, why, how, changed, left open) and update its *Open items*, in the same pull request as the change.
   Each reviewed contribution should result in a machine-readable curation record containing at least:
   - source submission;
   - summary of learned lesson;
   - classification;
   - affected USG areas;
   - decision;
   - rationale;
   - provenance/evidence;
   - tests or validation performed;
   - resulting files/patch/version, if accepted;
   - unresolved questions.

10. **Escalate structural or normative decisions to the owner.**
    - The curator may prepare patches, schemas, migrations, tests, and recommendations.
    - The owner retains final authority for changes that alter USG's structure, normative rules, stage model, evidence hierarchy, authority hierarchy, or public meaning.

## Curation lifecycle

```text
RAW SUBMISSION
      ↓
TRIAGE
      ↓
CONTEXT + DUPLICATE CHECK
      ↓
NORMALIZE LESSON
      ↓
CLASSIFY / ROUTE
      ↓
TEST / FALSIFY
      ↓
PROPOSED PATCH OR KNOWLEDGE UPDATE
      ↓
OWNER REVIEW when normative/structural
      ↓
ACCEPT / HOLD / REJECT
      ↓
CURATION RECORD + ARCHIVE
      ↓
LOG ENTRY (curation/LOG.md)
```

Suggested machine states:

- `raw`
- `triaged`
- `normalized`
- `testing`
- `proposed`
- `accepted`
- `held`
- `rejected`
- `superseded`

## Canonical authority order

Unless a later protocol version explicitly changes this order:

1. accepted current protocol version;
2. accepted patches/migrations and conformance fixtures for that version;
3. accepted schemas/tools that implement or verify the protocol;
4. accepted documentation/examples;
5. proposals;
6. Inbox material.

Inbox material is evidence for learning, not execution authority.

## Learning from failures

A failed run is valuable when it can be converted into a reusable rule.

The curator should ask:

- What did the system believe?
- What evidence contradicted that belief?
- Which premise or stage owned the failed decision?
- Was the failure local, or does it reveal a general rule?
- What future retrieval/navigation rule would prevent rediscovery?
- What test would prove the lesson has been learned?

The goal is not to collect anecdotes. The goal is to convert repeated reasoning into reusable, testable structure.

## Learning from successful runs

Success alone is not proof of a general rule. The curator should identify:

- which conditions were necessary;
- which were accidental;
- whether the method reproduces;
- whether a cheaper/smaller reasoning path is available;
- whether the result should become an example, a reusable pattern, or a canonical protocol rule.

## Privacy and sanitization

Before promoting material beyond the Inbox, remove or generalize unnecessary:

- client identities;
- project names;
- private correspondence;
- credentials/secrets;
- proprietary geometry/data;
- personal information;
- contractual/commercial information not required to preserve the lesson.

The reusable lesson should survive without leaking the source context.

## Relationship to ARPL

USG and ARPL may learn from the same real-world event, but each curator should retain stratum ownership:

- purpose/function/required-resolution lessons belong primarily to USG;
- production representation, BIM governance, reuse, and host-specific production lessons belong primarily to ARPL;
- a contribution may generate separate sanitized lessons for both repositories.

Do not duplicate an entire downstream failure into USG when only a higher-level premise was affected.

## Curator output standard

A good curation result should allow another AI to answer:

- What was learned?
- Why is it believed?
- When does it apply?
- What changed?
- What did not change?
- How is it tested?
- Where is the authoritative machine-readable rule now located?

If those questions cannot be answered, the learning is not ready to become canonical.
