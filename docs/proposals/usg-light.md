# USG Light — orientation check for any endeavor

Status: PROPOSED (LOG-0030, 2026-11-20). Not canonical. Owner directive 2026-11-20.
Scope note: USG v0.13 is written for built structures. Owner decision D1 (universal scope) is open. This proposal uses only the domain-neutral parts of the engine and no stage of the built-structure pipeline.

## Why

AI agents and people often get caught in operational mode. They finish the visible task correctly and miss the rest of the problem: the wrong goal, the wrong level, or a single option taken as the only one. Full USG (S00–S20) is too heavy to run at every turning point. USG Light is the fast track: four questions that any person or AI can run in minutes, before choosing an approach.

## The four questions (ask in this order)

1. **What am I trying to achieve with this?** (the purpose; the need behind the request)
2. **What makes this endeavor successful, and how would we see it?** (observable success, not a finished sub-task)
3. **Did we set the correct reality frame?** (Are we working at the level where the cause sits, or only where the symptom shows? Start with the smallest frame that is enough, and widen as evidence demands.)
4. **Am I looking too narrowly in my approach?** (Other options, including doing nothing or doing it differently; a named tool or method is a means, not the goal.)

Optional fifth question, to be confirmed by the Owner: **Who decides, and what evidence would show it?**

Purpose comes first because success defined for the wrong goal is worthless. In a live inquiry with a person, ask one question per turn and wait for the answer, as USG does everywhere.

## When to run it

- at the start of a mission or task that is not routine;
- at material transitions (a sub-task finishes, a hand-off, a change of direction);
- when results surprise, or the same uncertainty returns after two attempts;
- before declaring an outcome complete.

Not for routine, mechanical steps. Proportionality matters more than ritual.

## Speak up beyond the role

A role, seat or task constraint limits what an agent may **do**. It does not limit what it may **notice**. Any agent that sees a better reality frame or a blind spot, inside or outside its assigned work, says so. The note is:

- **labelled** as a frame or blind-spot note;
- **brief** and **evidence-based** where possible, with uncertainty stated;
- **sent to whoever owns the decision**, through the normal channel;
- **advisory only**: it creates no authority, does not block work, and is never executed by the agent that raised it.

Silence because "it is not my role" is the failure this rule exists to prevent.

## What it borrows from USG (v0.13)

| Question | USG source |
|---|---|
| 1 purpose | `S00.purpose`; `driver_rule` (a brief is an output of its drivers; trace it backward; never impute motives) |
| 2 success | `S00.success`; `evidence_model` (claim status, observable evidence) |
| 3 reality frame | Orientation from 3XFF, which frames USG from above (README, AGENTS.md). USG imports the question, not 3XFF mechanics or authority |
| 4 narrowness | `alternatives_to_build` (do nothing, reuse, improve operations…); `inquiry_model.means_separation` |
| 5 decider (optional) | `S00.drivers` (decision power); `answer_authority`; `S19` explicit acceptance |

It is the mission-level sibling of `execution_model.entry_check` (purpose and common sense before one operation, LOG-0026).

## Rules

- **Read, don't decide.** An AI may answer the questions from evidence for its own orientation. Purpose, success and decision authority stay with the people who own them; when they are unknown, ask; never invent them.
- **Retrieve before asking.** Check what is already recorded before asking a person again.
- **Wider view, same authority.** Seeing a bigger frame never widens what an agent may change.
- **Escalate to full USG** when the endeavor is a built structure, the answers conflict, the step is hard to reverse, or codes, safety or professional judgement are involved.

## Worked cases (from the TIVERIT environment)

- **Sub-task taken for the mission:** a ten-role research round was completed correctly; the actual goal was a scenario run that never happened. Questions 1 and 2 catch it.
- **Scope artifact:** a request was ruled out of scope because "it is not a building". Question 3 shows the frame was the written scope, not the problem.
- **Wrong decider:** link-state evidence was analysed for the receiving party, while the plausible decision sat with the issuing party. Questions 4 and 5 catch it.
- **Negative control:** a routine mailbox check needs no orientation check.

## Open before promotion

- Owner D1 (universal scope) and the order and fifth question.
- One pilot on a real non-building case, with the questions run at least at start and before completion.
- Placement if promoted: an entry in `execution_model` beside `entry_check`, plus one invariant. No new stage.
