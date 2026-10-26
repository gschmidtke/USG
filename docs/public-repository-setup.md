# Public repository governance setup

USG is designed to be publicly readable and publicly contributable **through the Inbox only**, while canonical knowledge remains curator-controlled.

## Intended authority model

```text
Public human / AI contributor
          ↓
      Pull Request
          ↓
      inbox/** only
          ↓
 inbox-only-path-guard
          ↓
    Curator review
          ↓
 curation record / tests
          ↓
 curator-authored canonical PR
          ↓
 canonical-validation
          ↓
       main
```

## Repository-side controls already implemented

- `.github/CODEOWNERS` assigns repository ownership to `@gschmidtke`.
- `.github/workflows/inbox-only-pr.yml` rejects non-curator PRs that modify anything outside `inbox/**`.
- `.github/workflows/canonical-validation.yml` runs protocol/conformance tests only for curator-authored canonical changes and pushes to `main`.
- `CONTRIBUTING.md` explains the public contribution contract.
- `CURATION.md` defines the curation process.
- `schema/inbox-submission.schema.json` defines optional machine-readable intake metadata.
- `schema/curation-record.schema.json` defines the curation audit record.
- `curation/` stores machine-readable curator decisions.

## GitHub settings that must be enabled manually

The connected GitHub App used by ChatGPT can edit repository contents but cannot currently create or modify repository rulesets/branch protection or repository visibility. Configure the following in the GitHub repository UI after this branch is merged.

### 1. Change visibility to Public

Repository **Settings → General → Danger Zone → Change repository visibility → Public**.

Before doing this, confirm that no private/client/proprietary content exists anywhere in the full Git history, not only the current tree.

### 2. Create a ruleset for `main`

Repository **Settings → Rules → Rulesets → New branch ruleset**.

Target branch:

```text
main
```

Recommended rules:

- Require a pull request before merging.
- Require status checks to pass.
- Require conversation resolution before merging.
- Block force pushes.
- Block branch deletion.
- Require code-owner review where supported/desired.

Required checks:

```text
inbox-only-path-guard
canonical-validation
```

`canonical-validation` is intentionally skipped for ordinary external Inbox PRs; GitHub ruleset configuration should therefore be tested before making it universally required. If GitHub treats a skipped job as non-satisfying in the chosen setup, require only `inbox-only-path-guard` for all PRs and use `canonical-validation` as a curator merge condition for canonical PRs.

### 3. Keep collaborators restricted

Do not grant ordinary contributors repository write access. Public contributors should fork the repository and submit pull requests.

Only the owner/curator (or a future dedicated curator GitHub App/account) should have write authority capable of changing canonical paths.

## Security design

The Inbox guard uses `pull_request_target` only to inspect GitHub's PR file list. It does **not** check out or execute contributor content.

The canonical validation workflow executes repository code only when the PR author is the designated curator (`gschmidtke`) or after content has reached `main`.

This separation is intentional. Public Inbox submissions are data/evidence, not executable authority.

## License decision before public release

No public-use license is selected by this governance setup. Before making the repository public, choose the intended licensing model for protocol text, code, schemas, examples, and contributed material. A public GitHub repository without a license is viewable but does not automatically grant broad reuse rights.

The contribution terms should match the chosen license so that accepted Inbox material can legally be incorporated into USG.
