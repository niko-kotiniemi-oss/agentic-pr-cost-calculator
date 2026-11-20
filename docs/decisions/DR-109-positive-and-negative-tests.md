# DR-109: Unit tests are positive and negative, at every boundary

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-18
- **Requirements:** none
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

Everything that crosses into the tool is untrusted (DR-044). A transcript or a ledger line can give a count as text, a fraction, a negative number, not-a-number or `true`, and Python takes some of these where it expects a number (T6, T17). Every count has a ceiling that the ledger format documents (R5).

## Decision

**Unit tests are positive and negative,** at every boundary: zero, one, the ceiling and one above it, and the values that Python accepts where it should not, such as `true` read as a number and not-a-number read from JSON.

## Alternatives

None were recorded when this was decided.

## Consequences

- Tasks 2.1 and 4.2 test every boundary of the counts and of the ledger format, and task 2.1 names `false`, `NaN`, `Infinity` and `1e999` among them.
- Each behaviour is tested for what it must refuse as well as for what it must do, so code that accepts a value it should refuse fails a test.
- `CLAUDE.md`, the step on tests in `CONTRIBUTING.md` and the pull request template hold every change to positive and negative tests.

## Scope

This covers the unit tests. The example that each scenario gives is tested first by DR-084 (Acceptance tests come first), and what holds for every input by DR-088 (Invariants get property-based tests).

## What reversing it would change

No requirement would change. The design's decision 8, tasks 2.1 and 4.2, the proposal's row for `ledger` in its section on how the outcome is validated, the sections on validation of the feature pages for `usage-capture`, `ledger` and `report-comment`, `CLAUDE.md`'s section on testing, the step on tests in `CONTRIBUTING.md` and the pull request template's checklist would.
