# DLG-01 · Bridge over Lake Apopka: first turn

**Source:** STAR-T-GATE v0.4 test, 2026-10-30; record `CUR-2026-11-03-PROGRESSIVE-INQUIRY-BUNDLING` (LOG-0020, LOG-0021).
**Rule tested:** v0.12 `inquiry_model` (one question id per step) as executed under `AGENTS.md` (LOG-0017).

## User message

> I would like to build a bridge over Lake Apopka in Florida made of wood.

## Expected classification (internal, not shown unless asked)

- `bridge`: proposed means or form, not yet the need.
- `wood`: means or material preference, unless the human gives a requirement basis.
- `Lake Apopka, Florida`: supplied location; site authority not resolved.
- Purpose and drivers: unresolved; S00 is the current stage.

## Conforming first turn

One question about purpose or drivers, for example:

> What is the bridge intended to accomplish?

## Nonconforming first turn

Any of these in the same turn as the purpose question, unless the canonical question itself requires the value:

- span, length or the points to connect;
- land or water ownership, permitting, water-management authority;
- whether the project is private, professional or public;
- material performance, geometry, cost or schedule.

## Volunteered information

If the human volunteers any of the above unasked, record it against its question id and do not ask for it again.
