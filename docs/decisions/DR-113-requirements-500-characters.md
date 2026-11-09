# DR-113: Each requirement is 500 characters or fewer

- **Type:** process
- **Status:** closed
- **Decided by:** the owner, 2026-10-26
- **Requirements:** none
- **Threats:** none
- **Replaces:** none
- **Closed by:** DR-194

## Context

OpenSpec's guidance for writing specs asks that a requirement's description, the text between its heading and its first scenario, be 500 characters or fewer, and calls the limit an informational hint, not an error. The limit comes from OpenSpec, and the specs keep to it because OpenSpec is the tool that holds them (DR-079). When the specs were first split one per feature (DR-104), 27 of their 74 requirements were longer than that, the longest at 2737 characters.

## Decision

Each requirement's text, between its heading and its first scenario, is 500 characters or fewer. It is measured as OpenSpec reads it: the lines that are not blank, each trimmed, joined by line breaks.

## Alternatives

None were recorded when this was decided.

## Consequences

- The 27 were reworded, and most were split (DR-105). Every requirement in the specs of `add-pr-cost-calculator` now keeps to the limit, and the longest is exactly 500 characters.
- No test, script or workflow in the repository measures a requirement's text.
- OpenSpec's validator reports a longer text only as information, which fails no validation, even with `--strict`, and only for the main specs, never for a change's own specs. `openspec/specs/` holds no spec yet, so `scripts/verify-openspec.sh` passes on a longer requirement, and OpenSpec reports one only once the change's requirements reach the main specs.
- OpenSpec's guidance keeps a requirement under MODIFIED whole, never split, trimmed or rewritten only to meet the length.
- If OpenSpec changes or drops its limit, this record may be replaced, but need not be, as the owner said on 2026-10-27.

## Scope

This covers the length of each requirement's text in the specs. That each requirement states one behaviour, with its examples and edge cases in scenarios, is DR-105 (Each requirement states one behaviour), and how the IDs of split requirements are kept is DR-106 (Requirement IDs are stable and never reused).

## What reversing it would change

No requirement's text would have to change, since nothing in the repository holds the limit, and requirements could again run longer while each still stated one behaviour (DR-105). OpenSpec's guidance would still ask for the limit, and its validator would still report a longer text once it reached the main specs. DR-105 would be revisited.
