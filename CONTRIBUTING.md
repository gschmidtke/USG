# Contributing to USG

USG is designed to learn from outside observations while keeping the canonical protocol governed and reproducible.

## Public contribution rule

External contributors — human or AI — should add material only under:

```text
inbox/**
```

Do not edit canonical repository content directly.

That includes, among other paths:

- `protocol/**`
- `core/**`
- `schema/**`
- `conformance/**`
- `tests/**`
- `tools/**`
- `history/**`
- `curation/**`
- `docs/**`
- `.github/**`
- `AGENTS.md`
- `CURATION.md`
- `README.md`

A repository guard checks pull requests and rejects external PRs that modify anything outside `inbox/**`.

## How to contribute

1. Fork the repository.
2. Add one or more files under:

```text
inbox/<contributor>/<yyyy-mm-dd>-<short-topic>.<ext>
```

3. Open a pull request.
4. The USG Curator reviews, classifies, normalizes, tests, and routes useful learning.

You do **not** need to understand the USG protocol schema before contributing.

Useful submissions include:

- observations;
- failed runs;
- successful patterns;
- contradictions;
- proposed rules;
- JSON experiments;
- external AI reviews;
- sketches and references;
- examples that expose missing cases;
- regulatory or physical constraints not currently represented;
- evidence that an existing rule is wrong, incomplete, or too broad.

## What happens after submission

Inbox material is not authoritative merely because it has been merged.

The curator follows `CURATION.md` and may classify the submission as:

- accepted example;
- conformance case;
- failure pattern;
- documentation improvement;
- proposal;
- protocol patch candidate;
- duplicate;
- held for more evidence;
- rejected/non-generalizable.

Canonical changes are made separately by the curator and, where normative or structural, require owner approval.

## Optional machine-readable metadata

You may accompany a submission with metadata conforming to:

```text
schema/inbox-submission.schema.json
```

This is optional. Raw material is welcome.

## Safety and privacy

Do not submit:

- credentials or secrets;
- private client data you are not authorized to disclose;
- personal information not necessary to preserve the learning;
- proprietary content you do not have permission to share;
- malicious payloads or material intended to compromise reviewers or automation.

The Inbox is an evidence intake channel, not a code-execution channel.
