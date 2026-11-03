# Owner-requested USG execution clarification

Date: 2026-10-31 UTC
Curator: ChatGPT (Zara), acting for Gottfried Schmidtke

## Trigger

A fresh external-AI STAR-T-GATE test correctly routed an ADU project request into USG and recognized USG concepts including S00 purpose, means-vs-outcome separation, and evidence authority. However, the AI still responded with a bundled questionnaire covering purpose, decision authority, success criteria, means classification, site facts, and later-stage matters instead of executing the canonical inquiry model one question at a time.

The owner concluded that once STAR-T-GATE routes an AI into USG, the AI must follow USG's own instructions directly rather than merely using USG as reference material.

## Owner instruction

Update USG's AI-facing repository instructions so that an arriving AI resolves `protocol/CURRENT`, loads the canonical protocol, and executes its inquiry rules literally. The clarification must not duplicate or change the canonical protocol itself; it must make clear that the repository instructions are a handoff into the canonical execution procedure, not a loose summary.

## Expected behavior

- execute the canonical `inquiry_model` rather than the AI's default conversational workflow;
- one question id per inquiry step, with canonical `answer_routing` as the limited exception;
- ask the highest-priority unresolved question, then wait for the human answer;
- do not bundle future-stage questions or convenience checklists;
- do not silently promote means named in the brief into purpose or hard requirements;
- do not jump ahead into external research, regulatory screening, geometry, production precedent, or execution until canonical stage/gate logic reaches those activities.
