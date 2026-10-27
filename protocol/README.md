# Protocol

The canonical USG protocol is versioned and immutable under `versions/`.

- Current source of truth: the file named in `CURRENT` (now `versions/USG_v0_12.json`). Workflows and tools read this pointer; releasing a new version means adding the version file and changing this one line.
- Previous versions are retained for non-regression and rebuild.
- Never rewrite an old protocol version in place. A change becomes a new version produced by a patch.

The current protocol contains the 21-stage pipeline, ontology, evidence model, phase model, geometry authority, schemas, feedback loops, export rules and governance.
