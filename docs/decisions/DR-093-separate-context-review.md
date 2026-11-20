# DR-093: Every change is reviewed in a separate context before it merges

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

The owner decides every merge, and nothing merges because an AI reported success (DR-080). Superpowers' skills drive how a change is built, review among them (DR-142).

## Decision

**The change `add-pr-cost-calculator` is reviewed in a context separate from the one that built it,** by `/simplify`, `/security-review`, `/code-review` and `/verify`, and every finding is fixed or answered before the owner merges. The same holds for every later change, as `CLAUDE.md` says, and a finding that is not fixed is answered with the reason.

## Alternatives

None were recorded when this was decided.

## Consequences

- Task 5.1 runs the four reviews on `add-pr-cost-calculator`, and the proposal counts every finding fixed or answered among the conditions for the change to succeed.
- The review informs the owner's decision and does not make it: a review that reports success merges nothing (DR-080).
- Each change takes four reviews before the owner merges it.

## Scope

This covers the review of what a change builds. The threat model's own review against the code is DR-095 (Threats are modelled twice in every change), and how an outside pull request is reviewed is DR-081 (Outside pull requests are reviewed from `main`).

## What reversing it would change

No requirement would change. The design's decision 8, task 5.1, `CLAUDE.md`'s section on review, and the proposal's list of what changes and its conditions for success would change, and so would `CLAUDE.md`'s section on testing and the feature pages' sections on validation, which name this record as the end of the range of testing records.
