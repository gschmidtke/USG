# Curation Records

This directory contains the machine-readable audit trail of curator decisions.

Each reviewed Inbox submission should eventually have a curation record conforming to:

```text
schema/curation-record.schema.json
```

Recommended path:

```text
curation/records/<yyyy>/<record-id>.json
```

Curation records explain:

- what was submitted;
- what reusable lesson was identified;
- how it was classified;
- what evidence supported the decision;
- whether tests were added or run;
- whether owner approval was required;
- what canonical files or protocol version resulted.

A curation record is part of the governance/audit layer. It is not itself a protocol rule unless the record points to a canonical change that adopted the lesson.
