# DR-087: Mutation testing runs on the tool's code

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

The tests run every branch of the tool's code (DR-086), and the design holds that a passing test shows only that the code can pass, not that the tests would notice it breaking (DR-089).

## Decision

**Mutation testing** (mutmut) changes the tool's code one small fault at a time and expects a test to fail each time. A surviving mutant fails CI, unless it is marked as making no difference, with the reason.

## Alternatives

- Line coverage alone, which counts the lines that ran, not the faults the tests would catch.

## Consequences

- A test that runs code without checking its result lets that code's mutants survive, so the gate fails until a test checks the result, or until each surviving mutant that makes no difference is marked so, with the reason.
- How long it takes in CI is not known yet. The design's risk "[Mutation testing takes time in CI]" has that measured once the gate is added, and settles what to do about it then.
- mutmut joins the development tools with the first code, pinned like the others (see the design's decisions 2 and 8), and task 1.5 makes it a CI gate, shown failing on a planted surviving mutant (DR-089).

## Scope

This covers the tool's code. How much of it the tests run is DR-086 (The tool's code keeps 100% branch coverage), and whether the checks that gate CI fail on their own defects is DR-089 (Every check is shown to fail).

## What reversing it would change

No requirement would change. The design's decision 8 and its risk on mutation testing's time, task 1.5, which adds the gate, `CLAUDE.md`'s section on testing, and the proposal's lists of what changes and of the development tools it adds, with its section on how the outcome is validated, would change. DR-086, which task 1.5 adds as a gate beside it, would be revisited.
