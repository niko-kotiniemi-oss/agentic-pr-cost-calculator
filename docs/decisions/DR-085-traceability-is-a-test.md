# DR-085: Traceability is a test

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

Each scenario in the specs is what an acceptance test checks (DR-084). The threat model cites, for each threat, what holds its answer: a scenario by its spec and its name, a task or a decision of a change, or a file (see its method). A citation that names nothing looks like a control while it holds none (see `tests/test_threat_model.py`).

## Decision

**Traceability is a test.** Every scenario has a test that names it, every test that names a scenario names one that exists, and every threat in `docs/threat-model.md` cites a scenario, task, decision or file that exists.

## Alternatives

None were recorded when this was decided.

## Consequences

- `tests/test_threat_model.py` already checks every threat's citations. Task 1.3 adds the test that traces scenarios, which fails at first, naming every scenario that has no test, until task 1.4's acceptance tests make it pass.
- A check already in place names in its own test the scenarios it holds (task 1.4), so it is traced like an acceptance test.
- A scenario that is renamed or removed fails the test wherever a test or a threat still names it.
- The test shows that a citation resolves, not that it still says what holds the answer, which is left to review (DR-095), as `CLAUDE.md` and the feature page for `project-standards` say.

## Scope

This covers the links between scenarios, tests and the threat model's citations. Whether the register, the feature pages and the specs agree is DR-100 (A register lists every requirement with its kind) and DR-101 (Each feature has a page).

## What reversing it would change

No requirement would change. The design's decision 8, task 1.3, the citation checks in `tests/test_threat_model.py`, the threat model's introduction, which says what that test checks, the proposal's section on how the outcome is validated, `CLAUDE.md`'s sections on the threat model and on testing, and the part of the feature page for `project-standards` that says what is not covered would change. DR-084, whose task 1.4 makes the traceability test pass, and DR-095, whose review checks what a citation says, would be revisited.
