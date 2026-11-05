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
- none; decisions taken under delegation (LOG-0021, LOG-0023) or by Owner ruling (LOG-0024).

### Decided, implementation pending
- **Branch protection** for `main` ("Protect USG main", as ARPL): owner to apply in repository settings; the curator cannot (LOG-0022).
- Promote sketch reconstruction to `adapters/sketch-reconstruction/` (LOG-0021); unblocked by v0.13 (LOG-0027).
- Input Reading v0.3.5: C-01 to C-10 (C-07 first; C-10 needs its own protocol patch, not in v0.13: LOG-0027), requirements R-ARPL-1/2/3/7, fixtures IR-CC-01/02, candidate IR-CC-03 (LOG-0021).

### Inbox awaiting review
- none (LOG-0020).

### Open design questions carried by examples
- Building 002: which edges carry the 1 m upper-roof overhang; whether the upper box also has a solid facade frame (spec v0.2 U03b, U06b).
- Buildings 001 and 002: should either become a pinned conformance fixture? `examples/building-001/check_building_001.py` could be its core (LOG-0010).
- No conformance instance covers sketch reconstruction yet; current instances cover feasibility, site screening and stress cases (LOG-0010, from Grok's review).
- Building 001 is not yet reproducible from the repository: the source sketch, spec v0.2 and concept profiles v0.3–v0.5 are missing (LOG-0010).
- Building 001 leader text `WARD.` vs `WTRD.` and canopy post count remain ambiguous (LOG-0010).
- Input Reading: gaps C-01 to C-10 to fix in v0.3.5, C-07 (meaning of `observed`) first; C-10 (rank of scans in `geometry_model.authority`) needs a protocol patch; fixtures IR-CC-01 and IR-CC-02 specified but not built, to be built after C-09 (LOG-0013, LOG-0014, LOG-0016). Option 05 is a candidate third fixture, IR-CC-03 (LOG-0020).

### Held for more evidence
- Promotion of legacy-automation purpose recovery to an adapter: needs a qualifying estate (criteria in the proposal) read end to end, plus independent review of the goal records; a firm/catalogue overlay is reconsidered only when two estates need it (LOG-0023).
- Evidence class in natural-language answers, not only in structured output (Gemini observation, Building 001; LOG-0010).

### Deferred work
- Short public guide for contributing a sketch reconstruction; write after the evidence-mapping decision (LOG-0010, from Grok's review).

## Entries

### LOG-0027 · 2026-11-05 · Protocol v0.13 (patch on v0.12)
- **Curator:** Claude, USG curator under DEC-005, on PM dispatch "USG PR25 review and UC04 v0.13" (retry 005). Record `CUR-2026-11-05-PROTOCOL-V0-13`.
- **Input:** decided-but-open item from LOG-0021, the name ruling LOG-0024 and the entry check LOG-0026.
- **Decision:** release v0.13 as a patch; `protocol/CURRENT` points to it. Content: `expanded_name` "Universal Structure Generator"; `answer_authority.design_decision_rule`; `evidence_model.source_class_mapping` (incl. `user_accepted`, `convention`) and `confidence_conversion`; `schemas.evidence` optional `source_class`, `origin`, `accepted_on`; `schemas.handoff` and `export_model.handoff_rule` (incl. optional `specified_products`); `execution_model.entry_check`; two invariants. `schema/usg-output.schema.json` follows (source kinds, authority, confidence enum or converted number, optional `handoff`).
- **Why:** implements decisions already taken; no stage, question, relation or ontology class changed. v0.12 is untouched.
- **How:** `check_usg.py` v0.13 against v0.12: 0 errors, 0 warnings. New 0.13 checks (mapping authorities, output-schema source kinds equal the mapping, hand-off fields, entry check) catch a mutated copy. Mutation suite 97/97; the four pinned instances re-pinned to 0.13 and all match; `build_stages.py --check` and `check_contracts.py` pass.
- **Changed:** `protocol/versions/USG_v0_13.json` (new), `protocol/CURRENT`, `schema/usg-output.schema.json`, `tools/check_usg.py`, `core/stages.json`, `conformance/instances/*.json` (pin), `tests/test_runner.py` (default path), version pointers in README, AGENTS, docs, schema and protocol READMEs, three proposals (status lines), record, this log.
- **Left open:** sketch-reconstruction adapter; Input Reading v0.3.5 (C-10, the rank of scans in `geometry_model.authority`, was not part of the decided v0.13 content and needs its own protocol decision); UC-03 universal-scope wording (Owner go).

### LOG-0026 · 2026-11-05 · Purpose and common-sense entry check (PR #25): accepted with amendments
- **Curator:** Claude, USG curator under DEC-005, on PM dispatch BPL-PM-USG-PR25-20261105-003.
- **Input:** PR #25 (Owner directive; merged by the Owner as a proposal at 21:16 UTC without a curator entry). Record `CUR-2026-11-05-PURPOSE-ENTRY-CHECK`.
- **Decision:** `accept_as_documentation` with four amendments: purpose read from context is a plausibility reading, never a human decision; contradictions are named, not silently fixed; escalation triggers named; placement as `execution_model.entry_check` plus one invariant in v0.13, no new stage, no Standards requirement.
- **Why:** It is the function-first thesis applied to one object or operation. v0.12 covers the purpose of a new structure (S00) and the entry stage, not the moment before an operation inside a partly resolved structure.
- **How:** read PR #25, its checks (both green) and v0.12 core_thesis, S00, driver_rule, consistency_rule; local checks run.
- **Changed:** proposal (status and review section), `AGENTS.md` (entry-check paragraph), record, this log.
- **Left open:** protocol text in v0.13 (added to the v0.13 item under Open items).

### LOG-0025 · 2026-11-05 · Routing correction UC-01: Standards governs, ARPL is precedent
- **Curator:** Claude, USG curator under DEC-005, executing BPL PM priority decision 2026-11-05 (priority 1).
- **Input:** BPL `inbox/usg-curator/2026-11-05-pm-priority-decision-002.md`; bucket list UC-01 (finding I-01). Record `CUR-2026-11-05-UC01-ROUTING`.
- **Decision:** `accept_as_documentation`. `docs/architecture.md`: strata diagram now reads USG → TIVERIT BIM Standards (normative requirements / authority / compliance evidence) → ARPL (operational precedent / production representation / failure memory) → capability → execution, with one explanatory paragraph. `CURATION.md` § Relationship: renamed to include Standards; BIM governance assigned to Standards; ARPL keeps production representation, reuse and failure memory.
- **Why:** README and AGENTS already route this way; these were the last two places that gave governance to ARPL.
- **How:** repository search for ARPL + governance; local checks run.
- **Changed:** `docs/architecture.md`, `CURATION.md`, this log, record.
- **Left open:** none from UC-01. v0.13 patch (LOG-0021, LOG-0024) remains the next version work.

### LOG-0024 · 2026-11-05 · Name ruling: "Universal Structure Generator"
- **Curator:** Claude, USG curator under DEC-005, executing an Owner ruling.
- **Input:** Owner, 2026-11-05 09:26 EST: "GENERATOR for USG". It resolves the conflict between this repository ("Universal Structure Generation", including an earlier Owner confirmation noted at LOG-0018) and BPL DEC-002 ("Universal Structure Generator"). Record `CUR-2026-11-05-USG-NAME-GENERATOR`.
- **Decision:** `accept_as_documentation` (documentation patch). The canonical expansion is **Universal Structure Generator**. The ruling supersedes the earlier confirmation of "Generation".
- **Changed now:** `README.md` (title), `AGENTS.md` (definition line), `LICENSE-DOCS.md` (suggested attribution), `adapters/input-reading/spec.json` (`project` metadata).
- **Not changed (history):** protocol versions v0.5.1–v0.12 keep `expanded_name: "Universal Structure Generation"`, the v0.12 release archive, and earlier log entries. Patch, never rewrite. The **next protocol version (v0.13) carries `expanded_name: "Universal Structure Generator"`.**
- **How:** occurrences found by repository search outside protocol versions, curation history and archive; local checks run.
- **Left open:** `expanded_name` in v0.13; routing fix UC-01 (architecture diagram and CURATION.md), proposed separately.

### LOG-0023 · 2026-11-04 · Purpose recovery from legacy automation: proposal, no protocol change
- **Curator:** Claude, USG curator under DEC-005 (acting for Gottfried Schmidtke), on a PM request made at the Owner's instruction.
- **Input:** LLCO purpose-recovery research (DEVELOPER, Mis) and its PM review; request summary in `curation/archive/CUR-2026-11-04-LEGACY-AUTOMATION-PURPOSE/`. Record `CUR-2026-11-04-LEGACY-AUTOMATION-PURPOSE`.
- **Decision:** `accept_as_documentation`; after the Owner delegated the four open points ("I leave 1-4 to you as USG curator", 2026-11-03 20:36 EST), **adopted as direction**:
  1. Direction approved.
  2. Recovered firm conventions are referenced, not imported; they reach a `domain_library` only through `library_model.generalization`; no new layer.
  3. Criteria set for a qualifying estate; acquiring one is not curation.
  4. Coverage-based readiness default: every choice and required output in a reconciled case, every rule boundary tested, second-runner re-run.

  Basis: the LLCO Goal Record is mapped onto existing concepts:
  - the Input Reading goal;
  - `statement_model.concerns` / `basis` / `relaxable_by`;
  - `evidence_model`;
  - `answer_authority`;
  - the source-neutral hand-off;
  - `pending_user` and materiality.

  It adds three separate claims per kernel (behaviour, purpose, correctness), explicit many-to-many dispositions and a derived readiness rule. It is a candidate source adapter only.
- **Rejected:** a new stage; a canonical USG Goal Record schema; a mandatory single `goal_record` field on rule records; a protocol field for the means classification; a fixed count of reconciled cases as readiness threshold.
- **Why:** USG already carries these meanings. A schema now would duplicate them before any real production estate has been read.
- **How:** Read protocol v0.12 (authority, evidence, statement, rule, review classes, library model), `adapters/README.md`, Input Reading 0.3.4 and the hand-off proposal. Checked open PRs (none) and LLCO PR #1 state (open draft, 817b019; not audited).
- **Changed:** `docs/proposals/legacy-automation-purpose-recovery.md`, record, archive stub, this log.
- **Left open:** locating a qualifying estate (commercial, outside curation); independent review of LLCO goal records; promotion to `adapters/legacy-automation/` after both.

### LOG-0022 · 2026-11-03 · Correction: branch protection not applied by the curator
- **Curator:** Claude, USG curator under DEC-005.
- **Input:** LOG-0021, decision 5.
- **Decision:** LOG-0021 said the ruleset would be applied after merge. The curator's session cannot write repository rulesets (GitHub returned 403 for this API path). The ruleset is therefore **not** in place; the owner applies it in the repository settings.
- **Why:** The log must not claim a protection that does not exist.
- **How:** Attempted `POST /repos/gschmidtke/USG/rulesets` with the ARPL ruleset adapted (required checks `canonical-validation`, `inbox-only-path-guard`); refused by the proxy.
- **Changed:** this log (entry, Open items).
- **Left open:** owner applies "Protect USG main" (Settings → Rules → Rulesets, default branch: block deletion and force push, require a pull request with resolved threads, require the two checks).

### LOG-0021 · 2026-11-03 · Owner decisions taken under delegation; licence; dialogue conformance
- **Curator:** Claude, USG curator under DEC-005. The owner delegated these decisions explicitly: "please go with your own recommendations for these 5 points" (2026-11-03), after the curator's report to PM.
- **Input:** the owner decisions listed in Open items after LOG-0020, and the curator's recommendations in `BPL inbox/pm/2026-11-03-usg-curator-changes-executed-001.md`.
- **Decision:**
  1. Input Reading: **accepted for development**, canonical only after v0.3.5 closes C-01 to C-10 and fixtures pass; goal statement and ARPL requirements R-ARPL-1/2/3/7 adopted into the adapter; partition fields stay local until a second adapter exists.
  2. Inquiry bundling: **no new protocol invariant** (v0.12 already has one question per step; LOG-0017 fixed agent entry); the case becomes dialogue conformance case DLG-01. Revisit if the failure recurs.
  3. Hand-off: optional `specified_products` (basis of design, with authority) distinct from requirements, in the v0.13 schema extension.
  4. Evidence-class mapping **adopted for v0.13** (with confidence high/medium/low and a documented numeric conversion); source-neutral hand-off **adopted as direction** for the same schema extension; sketch reconstruction **to be promoted** to the second adapter after v0.13; licence **CC BY 4.0 for protocol and documents, MIT for code**, as in ARPL.
  5. Branch protection on `main` recommended as in ARPL; applied as a repository ruleset after this pass is merged (repository setting, not a file).
- **Why:** Each decision follows the curator's recommendation as delegated. Protocol changes are decided here but not written here: they go into one v0.13 patch with its own checks, so this pass changes no protocol file.
- **How:** Read all four proposals and the Input Reading adapter; recorded `owner_approval` in records `CUR-2026-10-27-INPUT-READING`, `CUR-2026-11-03-INPUT-READ-GOAL`, `CUR-2026-10-27-SOURCE-NEUTRAL-HANDOFF`, `CUR-2026-11-03-PROGRESSIVE-INQUIRY-BUNDLING`; licence text taken from ARPL; full CI suite run locally.
- **Changed:** `adapters/input-reading/` (README, adapter.json), three proposals (status and decision lines), five records, `conformance/dialogue/` (new), `LICENSE`, `LICENSE-DOCS.md`, `README.md`, `CONTRIBUTING.md`, Open items.
- **Left open:** v0.13 protocol patch; then sketch-reconstruction adapter; Input Reading v0.3.5. Name check for the owner: this repository says "Universal Structure Generation", BPL DEC-002 says "Universal Structure Generator".

### LOG-0020 · 2026-11-03 · Inbox emptied: bundling failure, Input Read goal, Option 05, ARPL hand-over
- **Curator:** Claude, USG curator under DEC-005 (acting for Gottfried Schmidtke, on his instruction to proceed on the curator's assessment).
- **Input:** inbox files merged from PRs #12, #13, #14, #16.
- **Decision:** progressive inquiry bundling → `promote_to_patch_candidate`, owner approval (`CUR-2026-11-03-PROGRESSIVE-INQUIRY-BUNDLING`); Input Read goal → `accept_as_documentation`, proposed with the adapter (`CUR-2026-11-03-INPUT-READ-GOAL`); Option 05 lesson and test case → `accept_as_example` (`CUR-2026-11-03-OPTION05-INPUT-READING`); ARPL hand-over and lessons → `accept_as_documentation` (`CUR-2026-11-03-ARPL-HANDOVER-LESSONS`).
- **Why:** LOG-0017 already fixes the agent-entry side of the bundling failure; an explicit protocol invariant is normative and stays with the owner. The goal statement and Option 05 are the adapter's missing objective and its first real-source evidence. The ARPL hand-over named Zara as curator and is superseded by DEC-005; four of its seven lessons fit the adapter.
- **How:** Read every file in full; compared with `AGENTS.md` (LOG-0017), `adapters/input-reading/` and `schema/usg-output.schema.json` on `main`; archived the files under their record ids; full CI suite run locally. The ARPL hand-over was written by the same AI as ARPL curator; it is curated here as any other submission and recorded as such.
- **Changed:** four records, four archive folders, inbox emptied, Open items.
- **Merge sequence of 2026-11-03:** after triage reported to PM, PRs merged in this order: #10, #11, #18 (renumbered LOG-0017), #17 (renumbered LOG-0018), #15 (LOG-0019), then inbox PRs #16, #13, #12, #14. The number collisions came from parallel passes; rule 2 (claim before you start) is the guard.
- **Left open:** see Open items (bundling invariant, adapter requirements from ARPL, Option 05 fixture, product-vs-requirement in the hand-off).

### LOG-0019 · 2026-11-03 · USG placed in the AEC AI stack; STAR-T-GATE node contract
- **Curator:** Claude, USG curator under DEC-005 (acting for Gottfried Schmidtke, on his instruction to proceed on the curator's assessment). PR #15 was prepared on 2026-10-30/31 without a log entry; this entry records it.
- **Input:** PR #15 (`AGENTS.md`, `README.md`, new `AI-ROUTING-SAFEGUARD.md`, new `STAR-T-GATE.json`).
- **Decision:** accepted as repository documentation; no protocol change. Updated before merge: (1) the API lookup step is named **GPS**, per the owner's ruling of 2026-11-03 (GPS locates capability; it is never authority); (2) 3XFF kept as the frame above the chain, not as a routing step; (3) `STAR-T-GATE.json` lists Claude as primary curator and Zara as acting fallback; (4) contribution channels aligned with ARPL: STAR-T-GATE first, an inbox-only pull request for files, both uncurated evidence. The "If you discover new learning" steps from LOG-0018 now say the same.
- **Why:** The previous chain (`3XFF -> USG -> ARPL -> capability lookup`) skipped TIVERIT BIM Standards and used a superseded name; #15 fixed the first, this pass the second. #15 called the repository inbox non-public while LOG-0018 sent agents to it; one consistent rule avoids agents inventing a third path.
- **How:** Merged `main` (no conflicts); read all four files; checked chain wording against ARPL `AGENTS.md` section 2 and the TIVERIT BIM Standards README; full CI suite run locally.
- **Changed:** `AGENTS.md`, `README.md`, `AI-ROUTING-SAFEGUARD.md`, `STAR-T-GATE.json`, this log.
- **Left open:** the inbox-only workflow still accepts direct PRs to `inbox/**`; branch protection on `main` is not configured (recommended to the owner).

### LOG-0018 · 2026-10-30 · Agent-executable inbox intake
- **Curator:** ChatGPT (Zara) prepared the pass (draft PR #17, titled LOG-0013); completed and merged by Claude, USG curator under DEC-005, on 2026-11-03.
- **Input:** `curation/archive/CUR-2026-10-30-AGENT-EXECUTABLE-INBOX-INTAKE/2026-10-30-agent-executable-inbox-intake.md` (owner observation: an external AI understood the inbox but had to invent the contribution workflow and did not finish).
- **Decision:** `accept_as_documentation` (record `CUR-2026-10-30-AGENT-EXECUTABLE-INBOX-INTAKE`). `AGENTS.md` gains "If you discover new learning": one raw file under `inbox/**`, an inbox-only PR, then stop; if the agent cannot write, it returns the file to the user.
- **Why:** The gap was agent-facing execution, not protocol semantics; the curator, not the contributor, owns normalization and promotion.
- **How (completion, 2026-11-03):** renumbered from the colliding LOG-0013; merged `main` (no conflicts); moved the raw observation from the inbox to the archive as LOG-0007 does; corrected the record, which listed `CONTRIBUTING.md` as changed although the PR did not touch it, and mapped it to the record schema (it failed `check_contracts.py`, which is why the draft PR was blocked); full CI suite run locally.
- **Changed:** `AGENTS.md`, `inbox/README.md`, record, archive, this log.
- **Left open:** how this inbox path and the STAR-T-GATE channel (PR #15) are presented together; settled in LOG-0019.

### LOG-0017 · 2026-10-31 · Execute the canonical inquiry protocol after USG handoff
- **Curator:** ChatGPT (Zara) (acting for Gottfried Schmidtke, on his instruction)
- **Input:** Owner request after a fresh STAR-T-GATE external-AI ADU test showed correct USG routing and concept recognition but a bundled multi-question response instead of canonical one-question inquiry execution. Record `CUR-2026-10-31-USG-EXECUTION-DIRECTIVE`.
- **Decision:** `accept_as_documentation`; strengthen `AGENTS.md` so an arriving AI must resolve `protocol/CURRENT`, load the canonical protocol, and execute its inquiry model literally. No protocol rule, stage, authority model or schema is changed.
- **Why:** The canonical protocol already contains the required one-question-per-step and means-separation behavior. The failure was at the repository execution handoff: the AI treated USG as reference material and substituted its normal conversational workflow.
- **How:** Compared the observed response with v0.12 `inquiry_model`, confirmed the existing source-of-truth delegation in `AGENTS.md`, and added an explicit execution directive without restating USG as a second protocol.
- **Changed:** `AGENTS.md`; `curation/records/2026/2026-10-31-usg-execution-directive.json`; archived owner request.
- **Left open:** none.
- **Note:** prepared as LOG-0016 in PR #18; renumbered LOG-0017 at merge on 2026-11-03 because LOG-0016 was already taken on `main` (USG curator, Claude, under DEC-005).

### LOG-0016 · 2026-10-27 · Mistral's review of the Input Reading series
- **Curator:** Claude (acting for Gottfried Schmidtke, on his request)
- **Input:** Mistral's review of LOG-0013 to LOG-0015 (branch head 85c78ca, spec v0.3.4), pasted by the owner.
- **Decision:** `accept_as_documentation` (record `CUR-2026-10-27-MISTRAL-INPUT-READING-REVIEW`). Its two new findings become C-08 and C-09; a third gap found while assessing it becomes C-10. Its C-07 recommendation is adopted with corrections. The spec is unchanged.
- **Why:** Both findings hold against `spec.json`, but the suggested remapping closes only RA-02, RA-06 and RA-10; RA-11 to RA-13 need new planted failures. The proposed scan rule groups `imported_reference` with scans, although it carries no provenance, and sets confidence "from source quality" although v0.12 gives scans no geometric authority rank. That rank is a protocol decision (C-10), the first case of `adapters/README.md` boundary rule 2.
- **How:** Found both IR-01 actions; tallied the `trips` of all 15 planted failures against RA-01 to RA-13; checked `geometry_model.authority` in v0.12; full CI suite run locally.
- **Changed:** `adapters/input-reading/README.md` (C-08 to C-10, recommended resolution of C-07/C-03/C-01), `adapters/input-reading/adapter.json` (gaps), record and archived review, Open items.
- **Left open:** C-01 to C-10; C-10 needs a protocol patch; the owner's four decisions.

### LOG-0015 · 2026-10-27 · Input Reading moved into its own adapter module
- **Curator:** Claude (acting for Gottfried Schmidtke, on his instruction)
- **Input:** Owner instruction to give Input Reading its own branch and place its files there.
- **Decision:** Create `adapters/` as the home of source adapters and move Input Reading into `adapters/input-reading/`. This is a git branch now and a folder on `main` once merged, not a long-lived branch, which would drift from the protocol. Status, content and owner decisions are unchanged.
- **Why:** Reading a source is method; authority is protocol. A separate module lets the reading method be versioned on its own while the protocol keeps the evidence interface and the authority rules (`adapters/README.md`, boundary rules 1–2).
- **How:** `git mv` for the proposal (now `README.md`), the spec (now `spec.json`, still byte-identical to the archived original) and the coverage walk (now `tools/authority_walk.py`); relative links rewritten; the record's `resulting_files` repointed so `check_contracts.py` still finds them; full CI suite run locally.
- **Changed:** `adapters/README.md`, `adapters/input-reading/` (`README.md`, `adapter.json`, `spec.json`, `tools/authority_walk.py`, `fixtures/README.md`), link in `docs/proposals/source-neutral-interpretation-handoff.md`, record paths, `docs/repository-structure.md`, `AGENTS.md`, Open items.
- **Left open:** whether the sketch-reconstruction proposal becomes the second adapter (part of LOG-0008's promotion decision); an evidence-record schema in `schema/` for CI to check adapter output against, once the owner accepts an adapter.

### LOG-0014 · 2026-10-27 · LOG-0013 pushed; authority coverage walked exhaustively
- **Curator:** Claude (acting for Gottfried Schmidtke, on his request)
- **Input:** The LOG-0013 pass as a patch and zip, prepared by a curator with read-only access; the owner asked for it to be pushed and curated.
- **Decision:** LOG-0013 stands unchanged and goes in as received. Three further gaps (C-05 to C-07) are added to the proposal's known gaps; no change to the spec, record decision or status.
- **Why:** The first pass walked `authority_resolution` by hand. An exhaustive walk shows that its gap list was right but incomplete; C-07 is a vocabulary conflict with the evidence-class mapping and decides how C-01 and C-03 are fixed. All gaps fail closed through the invalid default.
- **How:** Did rule 2's check that LOG-0013 could not: no open pull requests. Confirmed that patch, zip and attachment are byte-identical, that the patch applies cleanly to `main` at LOG-0012, and that the proposal JSON is identical to the archived original. Ran every CI step locally: `check_usg.py` (0 errors, 0 warnings), `build_stages.py --check`, `check_contracts.py` (new record PASS), 97/97 mutation tests, and all four pinned instances. Added `tools/ir_authority_walk.py`, which checks every valid combination of world_relation, design_authority_relation, provenance, source_kind and source_origin under first-match-wins. Result: 1 unreachable rule (C-03) and 180 combinations with no rule (C-01, C-02, C-05 to C-07).
- **Changed:** `docs/proposals/input-reading.md` (C-05 to C-07), `tools/ir_authority_walk.py` (new, not in CI), Open items.
- **Left open:** C-01 to C-07; whether `ir_authority_walk.py` joins CI if Input Reading is accepted.

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