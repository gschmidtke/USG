# USG Curation Log

**Every curator reads this file first** — Claude, ChatGPT (Zara), any other AI, or a human — before reviewing the inbox or changing anything canonical. It says what has already been curated, why, how, and what is still open, so no pass repeats or silently undoes an earlier one.

Rules:

1. **Read before you act.** Read *Open items* and at least the last five entries. If you disagree with an earlier decision, record the disagreement in a new entry; never edit or delete an old one.
2. **Claim before you start.** Check open pull requests for a curation pass in progress. If one exists, wait or coordinate with its author. Otherwise open your pull request (draft is fine) titled `Curation pass LOG-NNNN: …` as soon as you start, which also reserves the number.
3. **Write when you finish.** Every curation pass adds one entry at the top of *Entries*, in the same pull request as its changes.
4. **One entry per pass**, numbered `LOG-NNNN` in sequence. Dates are UTC (`YYYY-MM-DD`), matching curation record ids.
5. **Link, don't copy.** Per-submission detail lives in `curation/records/<yyyy>/`; the log names the record and gives the reason in one or two sentences.
6. **Update Open items** in the same change: add what your pass left open, remove what it closed.

Entry template:

```markdown
### LOG-NNNN · YYYY-MM-DD · <short title>
- **Curator:** <who> (acting for <owner>)
- **Input:** <inbox files, PR, owner request>
- **Decision:** <what was decided>
- **Why:** <one or two sentences>
- **How:** <checks run, tests, files read>
- **Changed:** <files / PR / record ids>
- **Left open:** <questions, owner decisions> (also listed under Open items)
```

## Open items

### Owner decisions pending
- Evidence-class mapping and the `user_accepted` class: `docs/proposals/evidence-class-mapping.md`, four checkboxes (LOG-0008).
- Source-neutral interpretation handoff proposal: `docs/proposals/source-neutral-interpretation-handoff.md`, `requires_owner_approval: true` (LOG-0003). If approved, extend `schema/usg-output.schema.json`; do not add a second hand-off schema (LOG-0011).
- Promotion of the sketch-reconstruction proposal now that a second sketch has run (LOG-0008).
- Input Reading adapter: `docs/proposals/input-reading.md`, four checkboxes; decide with or after the evidence-class mapping (LOG-0013).
- Licence for the public repository (protocol text, code, schemas, contributions); none chosen yet (LOG-0007).

### Inbox awaiting review
- none (LOG-0010).

### Open design questions carried by examples
- Building 002: which edges carry the 1 m upper-roof overhang; whether the upper box also has a solid facade frame (spec v0.2 U03b, U06b).
- Buildings 001 and 002: should either become a pinned conformance fixture? `examples/building-001/check_building_001.py` could be its core (LOG-0010).
- No conformance instance covers sketch reconstruction yet; current instances cover feasibility, site screening and stress cases (LOG-0010, from Grok's review).
- Building 001 is not yet reproducible from the repository: the source sketch, spec v0.2 and concept profiles v0.3–v0.5 are missing (LOG-0010).
- Building 001 leader text `WARD.` vs `WTRD.` and canopy post count remain ambiguous (LOG-0010).
- Input Reading: gaps C-01 to C-04 to fix in the next revision; fixtures IR-CC-01 and IR-CC-02 specified but not built (LOG-0013).

### Held for more evidence
- Evidence class in natural-language answers, not only in structured output (Gemini observation, Building 001; LOG-0010).

### Deferred work
- Short public guide for contributing a sketch reconstruction; write after the evidence-mapping decision (LOG-0010, from Grok's review).

## Entries

### LOG-0013 · 2026-10-27 · Input Reading adapter turned into a proposal
- **Curator:** Claude (acting for Gottfried Schmidtke, on his request)
- **Input:** USG Input Reading v0.3.4 review package (spec, decision log), supplied by the owner after five review rounds (v0.1 to v0.3.4, reviewers Claude, Mistral, ChatGPT/Zara).
- **Decision:** `accept_as_documentation`, status `proposed`, owner approval required. Record: `CUR-2026-10-27-INPUT-READING`.
- **Why:** It is the source adapter that the source-neutral proposal (LOG-0003) keeps outside the stage model, so no stage changes. Its authority rules extend the evidence-class mapping (LOG-0008) to existing-world and external-design sources, which is normative; nothing has run on a real source or fixture yet.
- **How:** Read the log, all three proposals and v0.12 `answer_authority` / `evidence_model`; walked `authority_resolution` under first-match-wins and found four gaps (C-01 to C-04, listed in the proposal); ran the CI checks locally. Could not check open pull requests for a pass in progress (rule 2): the curator had read-only access to this repository.
- **Changed:** `docs/proposals/input-reading.md` (new), `docs/proposals/input-reading.json` (v0.3.4 as received), one link line in `docs/proposals/source-neutral-interpretation-handoff.md`, record and archived package, Open items.
- **Left open:** owner decision; C-01 to C-04; fixtures IR-CC-01 and IR-CC-02; calibration of tolerance, `max_delta_share` and the materiality threshold.

### LOG-0012 · 2026-10-27 · Credit corrected: source-neutral workflow drafted by Mistral
- **Curator:** Claude (acting for Gottfried Schmidtke, on his instruction)
- **Input:** Open item from LOG-0011; the owner confirmed that the LOG-0003 submission was drafted by Mistral.
- **Decision:** Credit Mistral as the drafter and the owner as the submitter, in record `CUR-2026-10-27-SOURCE-NEUTRAL-HANDOFF` and in the proposal it produced. The archived original is left as received; it correctly names the owner as submitter.
- **Why:** The record and proposal named no author, so the idea read as the curator's or the owner's own. Credit should follow the source.
- **How:** Found every place the submission is credited (record provenance, proposal header, archived original); one-line edits only, so the diff shows exactly what changed. LOG-0003 stays as written, per rule 1; this entry corrects it.
- **Changed:** record provenance line; *Origin* line in `docs/proposals/source-neutral-interpretation-handoff.md`; Open items.
- **Left open:** none.

### LOG-0011 · 2026-10-27 · Mistral's repository review; one hand-off contract
- **Curator:** Claude (acting for Gottfried Schmidtke, on his request)
- **Input:** Mistral's review of the repository, pasted by the owner; written against commit 0dcfd7d, before LOG-0010.
- **Decision:** `accept_as_documentation` (record `CUR-2026-10-27-MISTRAL-REPOSITORY-REVIEW`). Acted on its two new points; the rest were already resolved or already in Open items.
- **Why:** The hand-off was described in three places and the documented example did not validate against the schema, which proves the drift Mistral predicted. Two of its claims did not hold on checking: the sketch proposal has no leftover artefacts, and the protocol has no `sketch_or_reference` source type.
- **How:** Validated the hand-off example against `usg-output.schema.json` (failed: `schema_version` missing); grepped the sketch proposal and the protocol; added `tools/check_contracts.py` to CI (hand-off example, all curation records and the files they name, Building 002 spec, Building 001 self-checks): all pass after the fix.
- **Changed:** `docs/handoff-to-arpl.md` and `AGENTS.md` name the schema as the single machine contract; example fixed; `tools/check_contracts.py` + CI step; log rule 2 *Claim before you start* (rules renumbered); record and archived review.
- **Left open:** provenance of the LOG-0003 submission; hand-off schema extension waits on the source-neutral proposal decision.

### LOG-0010 · 2026-10-27 · Building 001 example, multi-observer file and Grok's repository review
- **Curator:** Claude (acting for Gottfried Schmidtke, on his request)
- **Input:** `inbox/gschmidtke/2026-10-27-building-001-multi-observer-sketch-learning.json` (PR #4); `Building_001_USG_Sketch_Interpretation_v0.3.json` supplied by the owner; Grok's review of the repository, pasted by the owner.
- **Decision:** Multi-observer file `accept_as_example` (record `CUR-2026-10-27-BUILDING-001-MULTI-OBSERVER`). Grok review `accept_as_documentation` (record `CUR-2026-10-27-GROK-REPOSITORY-REVIEW`). Created `examples/building-001/`.
- **Why:** The multi-observer lessons are already in the sketch-reconstruction proposal, so they are not repeated as rules; their case-specific value, the three open disagreements, now sits next to the v0.3 record, which shows only one side of two of them (kept verbatim to show that). Grok's review was accurate; most of its gaps were already in Open items, two were new and are added.
- **How:** Duplicate check against the sketch proposal and Open items; wrote `check_building_001.py`, which decides 20 of the record's own checks (20/20 pass) and fails a deliberately broken copy on 4; compared each disagreement with v0.3. Noted that v0.3 uses a seventh source class, `convention`, and added it to the evidence-mapping proposal.
- **Changed:** `examples/building-001/` (README, v0.3 spec, checker); two records and their archived sources; inbox emptied; `docs/proposals/evidence-class-mapping.md` (convention row, Building 001 evidence); `examples/README.md`; Open items.
- **Left open:** missing Building 001 source files; WARD./WTRD. and post count; conformance coverage of sketch reconstruction; held Gemini observation; deferred contributor guide.

### LOG-0009 · 2026-10-27 · Curation log introduced
- **Curator:** Claude (acting for Gottfried Schmidtke, on his request)
- **Input:** Owner request: a log every curator reads first, to see why and how things were curated.
- **Decision:** Add this file; make reading it step 0 in `CURATION.md` and `AGENTS.md`; reconstruct LOG-0001…0008 from git history and existing records.
- **Why:** Two AI curators (Claude, ChatGPT/Zara) work on the same repository; without a shared log each pass starts blind.
- **How:** Read `git log` of `main`, all records in `curation/records/`, and ARPL ledger entry IN-0011. While validating records, found that `schema/curation-record.schema.json` required `source_submission` to start with `inbox/`, which the archive move in LOG-0007 broke; the pattern now accepts `curation/archive/` as well, and all four records validate.
- **Changed:** `curation/LOG.md`, `CURATION.md`, `AGENTS.md`, `curation/README.md`, `schema/curation-record.schema.json`.
- **Left open:** none new.

### LOG-0008 · 2026-10-27 · Building 002 concept loop accepted as example
- **Curator:** Claude (acting for Gottfried Schmidtke)
- **Input:** Building 002 session: sketch, spec v0.1, Revit concept model, three designer reviews, USG lessons-learned document.
- **Decision:** `accept_as_example`; the evidence gaps are routed to a new proposal, not a protocol change. Record: `CUR-2026-10-27-BUILDING-002-CONCEPT-LOOP`.
- **Why:** It answers Building 001's open question (test on a substantially different sketch) and shows two gaps: no class for AI estimates the designer accepted, and a literal conflict between "user clarification resolves contradictions" and v0.12's owner_statement cap and geometric authority hierarchy. Both are normative, so they need the owner.
- **How:** v0.2 spec validated against the new draft schema; v0.1 fails it (10 errors) as expected; duplicate check against `evidence_model`, `answer_authority`, `geometry_model.authority` and the sketch proposal; protocol checks unchanged. Revit-side lessons went to ARPL (gschmidtke/ARPL PR #1), not here.
- **Changed:** `examples/building-002/`, `schema/neutral-building-spec.schema.json`, `docs/proposals/evidence-class-mapping.md` (PR #5); record and archived source (PR #6).
- **Left open:** owner decision on the mapping proposal; Building 002 U03b and U06b.

### LOG-0007 · 2026-10-27 · Consistency pass (PR #5)
- **Curator:** Claude (acting for Gottfried Schmidtke, on his request to review the repository and fix what was found)
- **Input:** Owner request; repository review.
- **Decision:** Make the agent-facing documents match the canonical protocol; no protocol change.
- **Why:** README/AGENTS named USG "Universal Spec Generator" while the protocol says "Universal Structure Generation" (owner confirmed the latter); AGENTS.md taught a 13-step chain while v0.12 has 21 stages S00–S20; the sketch rule was presented as canonical although its proposal says it is not.
- **How:** Read the protocol (`pipeline`, `phase_model`, `answer_authority`, `evidence_model`, `geometry_model`); ran the checker, 97 mutation tests and 4 conformance instances before and after; confirmed the new `tools/build_stages.py` reproduces `core/stages.json` byte for byte. CI passed on the PR and on `main`.
- **Changed:** name; S00–S20 model in AGENTS/architecture/handoff docs; `protocol/CURRENT` pointer read by CI; stage-summary generator with a CI drift check; stage ids enforced in `usg-output.schema.json`; six broken READMEs fixed; `.gitignore`; committed bytecode and a duplicate inbox file removed; records moved to `curation/records/2026/`, curated originals to `curation/archive/<record_id>/`.
- **Left open:** licence; `handoff_stage` now means the first stage the downstream system carries out (e.g. `S14`), not the word "ARPL".

### LOG-0006 · 2026-10-27 · ARPL redirected Building 001 sketch material to USG
- **Curator:** Claude as ARPL curator (cross-repository; recorded here for traceability)
- **Input:** ARPL intake IN-0011: neutral building definition for Building 001 and the proportional reconstruction rule.
- **Decision:** Redirected to USG; no ARPL pack. No new USG inbox file was created.
- **Why:** USG already owns this stratum: same evidence classes, same sketch rule (proposal), Building 001 review already in USG. ARPL keeps only the downstream handoff side.
- **How:** Duplicate check against USG AGENTS.md, the sketch proposal and the USG inbox.
- **Changed:** nothing in USG; ARPL `ledger/intake-ledger.json` IN-0011.
- **Left open:** none.

### LOG-0005 · 2026-10-27 · Building 001 multi-observer observations received (not curated)
- **Curator:** none yet; owner merged PR #4 into the inbox
- **Input:** `inbox/gschmidtke/2026-10-27-building-001-multi-observer-sketch-learning.json` (ChatGPT, Gemini and Grok readings, disagreements preserved).
- **Decision:** none; status `raw`.
- **Why:** Waiting for a curator pass.
- **How:** —
- **Changed:** inbox only.
- **Left open:** review it (listed under Inbox awaiting review).

### LOG-0004 · 2026-10-27 · Architect-freedom illustration accepted as documentation
- **Curator:** ChatGPT (acting for Gottfried Schmidtke)
- **Input:** `2026-10-27-usg-architect-freedom-concept.json` + `.svg`.
- **Decision:** `accept_as_documentation`. Record: `CUR-2026-10-27-USG-ARCHITECT-FREEDOM-CONCEPT`.
- **Why:** Useful positioning image; rhetorical, not technical evidence, so it must not influence protocol behaviour.
- **How:** See record.
- **Changed:** record; originals later moved to `curation/archive/` (LOG-0007).
- **Left open:** none.

### LOG-0003 · 2026-10-27 · Source-neutral handoff turned into a proposal
- **Curator:** ChatGPT (acting for Gottfried Schmidtke)
- **Input:** `2026-10-27-source-neutral-interpretation-reconstruction-workflow.json`.
- **Decision:** `accept_as_documentation`, status `proposed`. Record: `CUR-2026-10-27-SOURCE-NEUTRAL-HANDOFF`.
- **Why:** Generalizes beyond Building 001 (descent premises, mapper preservation duties, approximate-geometry policy, read-back acceptance), but the evidence base is too narrow to change the stage model. Export classification parts duplicate v0.12.
- **How:** See record.
- **Changed:** `docs/proposals/source-neutral-interpretation-handoff.md`.
- **Left open:** owner approval (listed under Owner decisions pending).

### LOG-0002 · 2026-10-27 · Building 001 sketch review accepted as example
- **Curator:** ChatGPT (acting for Gottfried Schmidtke)
- **Input:** `2026-10-26-sketch-reconstruction-review-and-comparison.md` (Grok review, Gemini comparison), uploaded twice: to `inbox/` via PR #3 and to `inbox/gschmidtke/`; the duplicate was removed in LOG-0007.
- **Decision:** `accept_as_example`. Record: `CUR-2026-10-27-BUILDING-001-SKETCH-REVIEW`.
- **Why:** Disciplined evidence classes, cross-view correspondence and separation of interpretation from realization; consistent with v0.12, no protocol change needed.
- **How:** See record.
- **Changed:** `docs/proposals/architectural-sketch-reconstruction.md` refined.
- **Left open:** test on a substantially different sketch (answered by LOG-0008); Building 001 as conformance fixture (still open).

### LOG-0001 · 2026-10-26 · Repository organized and governance set up (PR #1)
- **Curator:** owner, with ChatGPT via the GitHub App
- **Input:** USG v0.12 release bundle.
- **Decision:** Organize v0.12 into the canonical structure (protocol, core, schema, conformance, tests, tools, history, archive); add inbox-only contribution, CODEOWNERS, curation contract and schemas, and the two CI workflows.
- **Why:** Public, learnable repository where canonical knowledge stays curator-controlled.
- **How:** One-time importer/organizer workflows, removed after use.
- **Changed:** repository structure; `CURATION.md`, `CONTRIBUTING.md`, `inbox/`, `schema/`, `.github/`.
- **Left open:** GitHub ruleset settings documented in `docs/public-repository-setup.md`; licence.
