# DR-091: A defect found gets a test before the fix

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

The design holds that a passing test shows only that the code can pass, not that the tests would notice it breaking (DR-089), and a defect found in code whose tests pass is a case of that. New code is written test first: a failing test, seen failing for its expected reason, comes before the code that makes it pass (`CLAUDE.md`, DR-084).

## Decision

**A defect found becomes a test** that reproduces it, before the fix.

## Alternatives

None were recorded when this was decided.

## Consequences

- The fix comes only once a test fails on the defect, so the test is seen to catch it.
- Each defect found leaves behind a test that reproduces it, which then runs on every pull request with the others.
- `CLAUDE.md` holds the same rule for every change.

## Scope

This covers what follows once a defect is found. How new behaviour gets its tests is DR-084 (Acceptance tests come first) and DR-109 (Unit tests are positive and negative, at every boundary).

## What reversing it would change

No requirement would change, and no task builds it. The design's decision 8 and `CLAUDE.md`'s section on testing would change.
