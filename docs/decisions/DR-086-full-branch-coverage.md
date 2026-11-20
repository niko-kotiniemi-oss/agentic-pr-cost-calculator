# DR-086: The tool's code keeps 100% branch coverage

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

The design sets out to test everything that can be tested, and holds that a passing test shows only that the code can pass, not that the tests would notice it breaking (DR-089). No code of the tool exists yet (README).

## Decision

**Branch coverage is 100%** of the tool's code (coverage.py). Any exclusion carries its reason.

## Alternatives

None were recorded when this was decided.

## Consequences

- Every path of the tool's code that refuses an input or handles a failure needs a test that takes it, as the paths of ordinary use do.
- coverage.py joins the development tools with the first code, pinned like the others (see the design's decisions 2 and 8).
- Task 1.5 makes coverage a CI gate and shows it failing on a planted uncovered branch (DR-089). `CLAUDE.md` counts the gate among the checks to run once it exists.

## Scope

This covers how much of the tool's code the tests must run. Whether they would notice a fault in what they run is DR-087 (Mutation testing runs on the tool's code).

## What reversing it would change

No requirement would change. The design's decision 8 and task 1.5, which adds the gate, would change, and so would `CLAUDE.md`'s section on testing, the proposal's lists of what changes and of the development tools it adds, and its section on how the outcome is validated. DR-087, which task 1.5 adds as a gate beside it, would be revisited.
