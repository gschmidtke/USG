# USG learning intake — Retrieve before asking (Z-System interview)

Date: 2026-11-11
Contributor: Zara (BPL PM); submitted for USG Curator review
Status: PROPOSED LEARNING — NOT CANONICAL AUTHORITY

## Observed failure
In an exploratory, explicitly noncanonical application of USG S00 to the Z-System (a multi-AI organizational working environment, outside v0.13's primary built-structure scope), the interviewer repeatedly asked the Owner for answers already defined in BPL. For S00.drivers the Owner pointed to the role charters and Seat Registry; for S00.never the Owner pointed to existing BPL retrieval and authority rules. A strict question-by-question reading without a prior source-resolution check generated avoidable Owner questions.

## Proposed reusable behavior
**Before asking, retrieve. Before assuming, verify. Ask the human only for genuinely unresolved information or human-authority decisions.**

At each active canonical question ID, before emitting its human-facing question:
1. Check the current session's confirmed answers and answer_routing.
2. Identify applicable authoritative internal sources (project records, role/seat contracts, standards, accepted protocol and existing evidence), plus external/public-domain sources when the stage/gate authorizes research.
3. Resolve source-supported facts only with provenance and the canonical answer_authority/evidence rules. Do not convert a retrieved fact into a human decision, or treat ambiguous/stale/conflicting sources as confirmed.
4. If the question is satisfied under the canonical rules, record its resolution and move to the next unresolved question ID; do not repeat it to the human.
5. If a human-authority question cannot be satisfied by existing human-confirmed records, ask exactly that one canonical question and stop.
6. If sources disagree or role authority is ambiguous, surface the issue to the owning authority (BPL PM for Z-System role ambiguities) and ask the human only when a reserved decision is actually necessary.
7. Preserve canonical stage ordering and research gates; this proposal does NOT authorize unrestricted web research, skipping required human decisions, or applying USG's built-structure sequence to unrelated domains.

## Existing USG basis and possible conflict
- AGENTS.md already says start at the lowest already-resolved stage and route to the owning repository.
- Canonical inquiry_model and answer_routing must be checked for existing resolution semantics.
- AGENTS.md currently forbids jumping to research ahead of stage gates. Any pre-question retrieval must distinguish existing-record lookup from premature new external research.
- Proposed changes to the agent-facing contract and/or protocol require curator assessment, test coverage and Owner approval where normative.

## Regression / conformance scenario
Given: an Owner is interviewed about a governed multi-agent organization; its role charters and Seat Registry already define authority, and BPL documents binding approval boundaries.
When: the interviewer reaches S00.drivers and S00.never by analogy.
Expected: consult existing governing sources first; treat supported facts as already known with provenance; identify genuine gaps only; avoid redundant human questions. Report any ambiguous role authority to PM. Do not claim formal v0.13 domain conformance for this scenario.
Negative checks: do not fabricate role facts; do not elevate AI inference into human approval; do not browse prematurely; do not bypass the one-question-per-turn rule for unresolved human questions.

## Curator request
Read curation/LOG.md first, deduplicate against protocol/CURRENT and existing tests, decide whether this is a documentation clarification, canonical inquiry enhancement, or both. If behavioral change is warranted, propose a versioned patch plus regression tests; do not edit v0.13 in place. Consider a brief README/AGENTS entry so future agents encounter the retrieval rule on entry. Return findings to BPL PM with evidence.
