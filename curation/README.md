# Curation Records

**Start with [`LOG.md`](LOG.md)**: the chronological log of every curation pass (who, why, how, what is still open). Every curator reads it before acting and adds an entry when done.

This directory contains the machine-readable audit trail of curator decisions.

Each reviewed Inbox submission should eventually have a curation record conforming to:

```text
schema/curation-record.schema.json
```

Path:

```text
curation/records/<yyyy>/<yyyy-mm-dd>-<topic>.json
```

Once a submission has a record, its original files move out of `inbox/` to:

```text
curation/archive/<record-id>/
```

and the record's `source_submission` / `resulting_files` point to the archived copy. `inbox/` then holds only material still waiting for review.

Curation records explain:

- what was submitted;
- what reusable lesson was identified;
- how it was classified;
- what evidence supported the decision;
- whether tests were added or run;
- whether owner approval was required;
- what canonical files or protocol version resulted.

A curation record is part of the governance/audit layer. It is not itself a protocol rule unless the record points to a canonical change that adopted the lesson.
