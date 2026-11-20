# DR-088: Invariants get property-based tests

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-18
- **Requirements:** none
- **Threats:** T4, T52
- **Replaces:** none
- **Closed by:** none

## Context

Everything that crosses into the tool is untrusted (DR-044), and some of what the tool must keep has to hold for every input, such as that a ledger entry holds counts and no content from the transcript (R4) and that the comment, the job summary and the log hold only what the report computed (R21).

## Decision

**Property-based tests** (Hypothesis) hold the invariants: no planted string reaches the ledger, a ledger file's name, the hook's output, the comment, the report's job summary or its log, a second capture changes nothing, the cost adds up across any split of the ledger, and no cost is negative. CI runs them derandomised, so a run can be repeated exactly.

## Alternatives

None were recorded when this was decided.

## Consequences

- Two threats rest on these tests: the property test over planted strings is part of T52's answer, and holds T4's, that no identifier reaches a ledger entry or a ledger file's path.
- Tasks 2.1, 3.2 and 4.1 write them, and task 1.6 adds the derandomised profile for CI.
- Hypothesis joins the development tools with the first code, pinned like the others (see the design's decisions 2 and 8).

## Scope

This covers the invariants. The example that each scenario gives is tested by DR-084 (Acceptance tests come first), and the boundaries of each value by DR-109 (Unit tests are positive and negative, at every boundary).

## What reversing it would change

No requirement would change. The design's decision 8 and tasks 1.6, 2.1, 3.2 and 4.1 would, and so would T52's answer and what holds T4, the proposal's lists of what changes and of the development tools it adds, its section on how the outcome is validated, the sections on validation of the feature pages for `usage-capture`, `ledger`, `pricing` and `report-comment`, and `CLAUDE.md`'s section on testing.
