# USG Inbox

The Inbox is the **unfiltered learning intake** for USG.

Useful material may be added here before it has been normalized into the canonical protocol structure.

Accepted intake can include:

- raw notes;
- JSON experiments;
- Markdown discussions;
- failure reports;
- successful workflow reports;
- external model reviews;
- comparisons between interpretations;
- proposed rules;
- conformance examples;
- sketches and references;
- migration ideas;
- contradictions discovered during use.

## Important

Nothing in this folder is canonical merely because it is present.

Inbox material must be reviewed under `CURATION.md` before it may alter USG behavior.

**Minimum valid submission: one raw file under `inbox/**`.**

A contributor does not need to normalize the observation, classify it, design a patch, create metadata, or understand the USG protocol schema. Those are curator responsibilities. Preserve the learning and enough provenance/context to understand it; complexity belongs with the curator.

## Recommended naming

Use a stable, descriptive path when possible:

```text
inbox/<contributor>/<yyyy-mm-dd>-<short-topic>.<ext>
```

Examples:

```text
inbox/gschmidtke/2026-10-26-architectural-sketch-proportions.json
inbox/reviewer-a/2026-11-02-stage-s07-contradiction.md
```

Raw uploads that do not follow the naming recommendation are still valid submissions.

## Optional sidecar metadata

For material that benefits from machine-readable intake metadata, add a JSON record conforming to:

`schema/inbox-submission.schema.json`

The metadata is optional. The curator may create it during triage if the contributor supplied only raw material.

## Lifecycle

```text
Inbox
  ↓
Curator review
  ↓
Normalize / deduplicate / test
  ↓
Proposal or canonical patch
  ↓
Curation record
  ↓
Archive / accepted destination
```

The Inbox should stay easy to contribute to. Complexity belongs with the curator, not the contributor.
