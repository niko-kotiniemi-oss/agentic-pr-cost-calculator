# DR-089: Every check is shown to fail

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

A test that passes once shows that the code can pass. It does not show that the tests would notice the code breaking. The same is true of a check in CI, and nothing reaches `main` without the `ci` check, which passes only when every job before it passed (DR-043, DR-072).

## Decision

**Every check is shown to fail.** Each CI gate has a test that plants the defect it exists for, and asserts that the gate fails for that reason. Each check also reports what it examined, and fails when that is nothing.

## Alternatives

None were recorded when this was decided.

## Consequences

- Each task that adds a check verifies it against a planted defect, from the coverage and mutation gates (task 1.5) to the check of pins (task 1.15) and the check of what the tool's code reads (task 5.3).
- `tests/test_documentation.py` already works this way: it fails when it finds no requirement in the specs, no workflow or no proposal to examine, and its own tests plant the defects that it reports, such as a missing permission, action or diagram.

## Scope

This covers the checks that gate CI. Whether the tests of the tool's own code would notice a fault in it is DR-087 (Mutation testing runs on the tool's code).

## What reversing it would change

No requirement would change. The design's decision 8 would, and so would each task that verifies a check against a planted defect, such as tasks 1.5, 1.15 and 5.3, the tests that plant those defects, `CLAUDE.md`'s section on testing and the proposal's list of what changes.
