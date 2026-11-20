# DR-084: Acceptance tests come first

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-18
- **Requirements:** none
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

The specs say what the tool must do, as requirements with scenarios, and code follows an approved change (DR-079). The design of `add-pr-cost-calculator` comes before any of its code, which starts once the change is approved (README). A pull request reaches `main` only with the `ci` check (DR-072).

## Decision

**Acceptance tests come first,** at least one per scenario, each seen failing for its expected reason before its code exists. They are kept as expected failures that may not pass early (`pytest.mark.xfail` with `strict=True` and the expected error), so CI stays green and meaningful while the code is built.

## Alternatives

- One failing example per task, then green, which shows the code can pass and little more.

## Consequences

- Each task's acceptance tests are written in the first group of `tasks.md`, before any code (task 1.4).
- Under `CLAUDE.md`, an acceptance test is never weakened or rewritten to make an implementation pass. When one is wrong, the spec or the test is corrected first, with the reason.
- The threat model makes each answer a scenario wherever it can be one, so that an acceptance test holds it (see the threat model's introduction).

## Scope

This covers the scenarios whose code is still to be written. A scenario that a check already in place holds is named in that check's own test instead (task 1.4). That every scenario is named by a test is DR-085 (Traceability is a test), and tests at each boundary are DR-109 (Unit tests are positive and negative, at every boundary).

## What reversing it would change

No requirement would change. The design's decision 8 and tasks 1.3 and 1.4 would, and so would the opening of `tasks.md`, the proposal's list of what changes and its section on how the outcome is validated, the section on validation of every feature page, `CLAUDE.md`'s section on testing, the step on tests in `CONTRIBUTING.md`, the pull request template's checklist and the README's section on working on this repository. The threat model's introduction, which has an acceptance test hold each answer that is a scenario, would change too, and DR-085 would be revisited.
