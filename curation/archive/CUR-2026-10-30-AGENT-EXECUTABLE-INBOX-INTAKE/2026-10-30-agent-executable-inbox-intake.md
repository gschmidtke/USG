# USG Inbox — Agent-executable contribution path

Date: 2026-10-30
Contributor: Gottfried Schmidtke / curator observation
Status: raw learning intake

## Trigger

An external AI (Mis/Mistral) correctly identified that a repository review/fix should be submitted through the USG Inbox so the curator could review and apply it. It then spent substantial effort designing the mechanics of the submission — contributor naming, sidecar metadata, branch strategy, PR packaging, schema destinations and curator workflow — and did not complete the intended Inbox submission.

## Observation

USG already states the human contribution path in CONTRIBUTING.md and keeps the Inbox deliberately permissive. However, the agent entry document AGENTS.md does not give a deterministic rule for an external AI that discovers reusable learning and wants to submit it.

The contribution mechanism should be executable without requiring the host AI to design a curation workflow.

## Candidate principle

The target repository owns its own contribution mechanics. STAR-T-GATE should only tell an AI to follow the target repository's current contribution instructions.

For USG, the minimum valid external contribution should be one raw file under inbox/**. Metadata, normalization, classification, patch design and canonical promotion are curator responsibilities unless the agent is explicitly acting as curator.

## Candidate agent behavior

When an external AI discovers a failure, contradiction, missing case, improvement or other potentially reusable learning:

1. Do not modify canonical USG content.
2. Write the observation under inbox/<contributor>/<yyyy-mm-dd>-<short-topic>.<ext>.
3. Preserve enough provenance/context to understand or reproduce the observation.
4. Open a pull request containing only Inbox material.
5. Stop. Do not normalize, patch, promote or modify canonical USG unless explicitly acting as curator.
6. If repository write/PR capability is unavailable, return the prepared Inbox artifact to the user rather than inventing a different contribution workflow.

## Suggested disposition

Treat this primarily as agent-facing documentation/usability, not a protocol-version change. Make the existing permissive Inbox contract explicit in AGENTS.md and inbox/README.md, with CONTRIBUTING.md remaining the detailed public contribution guide.
