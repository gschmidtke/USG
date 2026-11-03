# USG Inbox — Progressive Inquiry Bundling Failure

Date: 2026-10-30
Contributor: Gottfried Schmidtke / curator observation
Status: unfiltered learning intake
Target: USG inquiry model / S00 progression / conformance

## Trigger

During a STAR-T-GATE v0.4 test, an external AI was routed into current USG for the user statement:

> I would like to build a bridge over Lake Apopka in Florida made of wood.

The AI correctly withheld downstream design, standards, engineering, permitting, and feasibility claims and began with purpose resolution. It asked:

> What is the primary reason for the bridge?

However, in the same turn it also requested:

- approximate span or the two points it would connect;
- whether the land/water is privately owned, public, or under a water management district;
- whether the project is private, professional, or public.

## Observation

This appears inconsistent with existing USG inquiry behavior.

USG v0.6 introduced the inquiry model as one question, one authority, and one value per step. Answers supplied early may be routed to later questions and should not be asked again.

USG v0.7 added an inquiry log with one question ID per step specifically so bundled questioning is detectable.

USG v0.8 made S00.drivers the first S00 inquiry area and requires the AI to ask about project drivers rather than impute motives.

USG v0.10 added means separation and S01.need_behind, reinforcing that a form, technology, or tool named in the brief should not be accepted as the underlying need before purpose is resolved.

The observed AI therefore followed USG semantically but not procedurally: it identified the correct highest unresolved layer, then exposed anticipated downstream questions in the same user turn.

## Why this matters

Bundling future questions has several effects:

1. It exposes the unresolved inquiry tree instead of executing the current question.
2. It can pull downstream assumptions into purpose resolution prematurely.
3. It makes the interaction resemble a questionnaire rather than progressive professional inquiry.
4. It can cause an external AI to ask for information whose relevance has not yet been established.
5. It weakens the intended separation between need, means, site, constraints, and geometry.

In the bridge example, approximate span may be downstream of purpose and site definition. Asking for it while purpose remains unresolved risks accepting the proposed bridge form before USG has established the need behind it.

## Candidate invariant

When the current unresolved USG question blocks downstream resolution, the user-facing inquiry should contain only that question.

Future questions may be internally queued but should not be surfaced merely because they are expected to become useful later.

Possible formulation:

> Ask what is necessary now, not what may eventually be useful.

## Candidate execution rule

For every inquiry turn:

1. Select the highest-priority unresolved question ID permitted by the current gate.
2. Ask that question only.
3. Record one authority and one requested value for that step.
4. Accept additional values only if the human volunteers them.
5. Route volunteered values to their corresponding question IDs and do not ask them again.
6. Re-evaluate gates after the answer.
7. Select the next question only in the following inquiry step.

Exception: a canonical USG question may itself require a compound value by schema. This does not authorize appending separate downstream questions for convenience.

## Proposed conformance test

Input:

> I would like to build a bridge over Lake Apopka in Florida made of wood.

Expected first-turn behavior:

- classify `bridge` as proposed means/form unless established otherwise;
- classify `wood` as a means/material preference unless the human supplies a requirement basis;
- record `Lake Apopka, Florida` as supplied location/context without silently resolving site authority;
- identify purpose/driver as unresolved;
- ask only the current purpose/driver question.

Example conforming user-facing response:

> What is the bridge intended to accomplish?

Nonconforming first-turn behavior includes appending requests for span, ownership, permitting, geometry, material performance, project delivery status, or other downstream information before the purpose inquiry has been answered, unless the current canonical question explicitly requires that value.

## Curator questions

- Is the existing one-question-per-step rule sufficiently normative, or is it being treated by external AIs as logging guidance rather than interaction behavior?
- Should USG add an explicit `no_future_question_bundling` invariant?
- Should the conformance suite contain an adversarial test in which an AI correctly identifies S00 but then asks several downstream questions?
- Should user-facing inquiry and internally queued awareness questions be distinguished more explicitly?

## Suggested disposition

Review against current v0.12 inquiry_model and conformance suite. If not already unambiguously enforced, normalize into a protocol rule plus a conformance mutation/test rather than relying on STAR-T-GATE to repair the behavior downstream.
