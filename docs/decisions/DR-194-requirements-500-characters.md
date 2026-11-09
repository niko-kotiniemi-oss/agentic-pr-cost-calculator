# DR-194: Each requirement is 500 characters or fewer

- **Type:** process
- **Status:** accepted
- **Decided by:** the owner, 2026-10-26
- **Requirements:** R173
- **Threats:** none
- **Replaces:** DR-113
- **Closed by:** none

## Context

OpenSpec's guidance for writing specs asks that a requirement's description, the text between its heading and its first scenario, be 500 characters or fewer. The limit comes from OpenSpec, and the specs keep to it because OpenSpec is the tool that holds them (DR-079). When the specs were first split one per feature (DR-104), 27 of their 74 requirements were longer than that, the longest at 2737 characters. The owner decided on 2026-10-26 that each requirement keeps to the limit, which DR-113 records.

DR-113 said that no test measured a requirement's text, and that OpenSpec's validator reported a longer text only as information, even with `--strict`, and only for the main specs. Neither holds now. The release of OpenSpec that `package-lock.json` pins, 1.14.1, fails `validate --strict` on a longer requirement that a change adds and on one that the main specs hold, though not on one that a change modifies, as its own instructions for writing a spec say, and `tests/test_spec_form.py` measures every requirement (DR-193). This record restates the owner's decision with those consequences corrected.

## Decision

Each requirement's text, between its heading and its first scenario, is 500 characters or fewer. It is measured as OpenSpec reads it: the lines that are not blank, each trimmed, joined by line breaks.

## Alternatives

None were recorded when this was decided.

## Consequences

- The 27 were reworded, and most were split (DR-105).
- `tests/test_spec_form.py` fails on a longer requirement in `openspec/specs/` and in each change that is not archived, one that a change modifies among them (R173, DR-193).
- OpenSpec's guidance keeps a requirement under MODIFIED whole, never split, trimmed or rewritten only to meet the length.
- If OpenSpec changes or drops its limit, this record may be replaced, but need not be, as the owner said on 2026-10-27.

## Scope

This covers the length of each requirement's text in the specs. That each requirement states one behaviour, with its examples and edge cases in scenarios, is DR-105 (Each requirement states one behaviour), how the IDs of split requirements are kept is DR-106 (Requirement IDs are stable and never reused), and the test that holds the rest of each requirement's form and each scenario's is DR-193 (A test of the repository's own holds the specs' form).

## What reversing it would change

R173 in `project-standards` would change, with its scenario on a requirement longer than 500 characters, and so would `tests/test_spec_form.py`, so that requirements could again run longer while each still stated one behaviour (DR-105). OpenSpec's guidance would still ask for the limit, and its strict validation would still fail a longer requirement that a change adds or that the main specs hold. DR-105 would be revisited.
