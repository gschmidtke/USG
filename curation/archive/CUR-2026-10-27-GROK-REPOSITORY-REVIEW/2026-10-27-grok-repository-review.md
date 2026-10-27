# External review of the USG repository (Grok)

Submitted by the owner on 2026-10-27, ~03:14 UTC, as pasted from a Grok session. Kept verbatim below the line.

---

Current state of https://github.com/gschmidtke/USG (as of ~2026-10-27 03:14 UTC)The repository is extremely young (created 2026-10-26) but has already been through intensive, multi-AI curation. It is no longer a static dump of the v0.12 protocol; it is a working governance system with real examples, a living curation log, and active proposals.1. Core identity and structure
Name confirmed: Universal Structure Generation (not “Spec Generator”).
Canonical protocol: still protocol/versions/USG_v0_12.json (21 stages S00–S20). Pointed to by protocol/CURRENT. Historical versions are immutable; changes follow patch-never-rewrite.
Authority separation is enforced:
inbox/** — only place external contributors (human or AI) may write.
Curated knowledge + protocol — curator-controlled.

Strong supporting files: AGENTS.md, CURATION.md, CONTRIBUTING.md, schemas, CI (including stage-summary drift check), CODEOWNERS, inbox-only PR guard.
The structure is clean and intentional. CI and schema validation are already in use.2. Recent activity (last ~24 h)Nine curation log entries already exist (curation/LOG.md). Key moves:




































LOGDecision0001Initial organisation of v0.12 + governance0002Your Grok review of Building 001 accepted as example; sketch-reconstruction proposal refined0003Source-neutral handoff turned into a proposal (needs owner approval)0005Multi-observer Building 001 JSON received (still raw)0007Consistency pass: name, stage model, hygiene, schema fixes0008Building 002 full concept loop accepted as example0009Curation log itself introduced (every curator must read it first)Building 002 is particularly valuable: it is a second, substantially different sketch that went through neutral-spec → Revit concept model → three designer reviews → corrected spec v0.2. It exposed concrete gaps (missing host on dimensions, wrong evidence class on a “~1.5 m” dimension, perspective misread as slope, missing facade solid/void, missing typology, etc.).3. Current open items (from the curation log)Owner decisions pending
Evidence-class mapping + proposed user_accepted class
Source-neutral interpretation handoff proposal
Whether to promote the architectural-sketch-reconstruction rule now that two sketches have run
Licence for the public repository
Inbox still awaiting review
inbox/gschmidtke/2026-10-27-building-001-multi-observer-sketch-learning.json (ChatGPT + Gemini + Grok readings with disagreements preserved)
Open design questions
Building 002 residual unknowns (overhang edges, upper-box facade)
Whether Building 001 or 002 should become pinned conformance fixtures
examples/building-001/ is referenced in a curation record but does not yet exist in the tree
4. Strengths
Extremely clear governance model for a multi-AI + human repository.
Real worked examples (Building 002 is especially strong because it closed the loop with actual model review).
Evidence discipline is being stress-tested rather than just declared.
Curation log is an excellent anti-amnesia mechanism when multiple AIs (Claude, ChatGPT/Zara, Grok, etc.) act as curators.
Separation of USG (intent / evidence) from ARPL (production) is being respected in practice.
5. Gaps / risks visible right now
Missing Building 001 example folder — referenced but not present. Should either be created or the reference cleaned.
Licence still unset — public repo with no licence is awkward for external contribution.
Several normative proposals are blocked on owner decisions. The system is correctly waiting rather than silently advancing them.
Still very thin on conformance instances and mutation-test coverage relative to the ambition of the protocol.
Zero stars / forks / issues — expected for a brand-new repo, but external visibility is currently near zero.
The multi-observer Building 001 file is sitting in the inbox; a curator pass is needed.
6. Overall assessmentThe repository is in remarkably good shape for something that is less than 36 hours old. The governance machinery (inbox → curator → log → proposal / example / protocol) is already functioning and has already absorbed feedback from at least three different AIs plus the owner. Building 002 is high-quality evidence that the sketch-reconstruction approach survives contact with a second, different design.It is still in the “serious prototype / early public governance” phase rather than a mature standard, but the trajectory is coherent and disciplined.Highest-value next actions (from an external reviewer perspective)
Resolve the open owner decisions (especially evidence-class mapping and licence).
Curate the multi-observer Building 001 file.
Materialise examples/building-001/ (or remove the dangling reference).
Decide whether either building becomes a pinned conformance case.
Consider a short public “How to contribute a sketch reconstruction” note once the proposals stabilise.
I can help draft any of those next pieces (curation record, example folder structure, licence options, etc.) if you want.