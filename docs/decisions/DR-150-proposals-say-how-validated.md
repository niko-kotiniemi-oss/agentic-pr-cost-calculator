# DR-150: Each proposal says how its capabilities are validated

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-25
- **Requirements:** R74
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

A change's specs hold what the tool must do, one spec per feature (DR-104), and a proposal lists the capabilities that its specs hold. Each feature's page says how that feature is validated (DR-101), so a change's own account of how its outcome is validated was the one part that nothing held to its specs.

## Decision

Each change's proposal lists the capabilities that its specs hold and says how each of them is validated, in a row of its own in the proposal's section on how the outcome is validated.

## Alternatives

None were recorded when this was decided.

## Consequences

- `tests/test_documentation.py` reads every proposal under `openspec/changes`, archived changes included, and fails naming the capability when a proposal leaves out one that its change's specs hold, lists one that they do not hold, or gives one no row, or an empty row, in that section (R74).
- The proposal of `add-pr-cost-calculator` has such a row for each of its capabilities, beside its statement that every capability is validated first by its own scenarios.
- Task 1.17 listed each capability in the proposal with how it is validated.
- What a row says is not read by any test, so whether the validation it names fits the capability is left to review.

## Scope

This covers what a proposal says about validating the capabilities of its change. That each feature is one spec is DR-104 (Each feature is one spec), and what a feature's page holds, including its own account of how the feature is validated, is DR-101 (Each feature has a page).

## What reversing it would change

R74 in `project-standards` would change, with its scenarios "A proposal out of step with its specs fails CI" and "A capability without its validation fails CI". So would the proposal's section on how the outcome is validated, the proposal's checks in `tests/test_documentation.py`, task 1.17 and the item on validation written down on the feature page for `project-standards`. DR-104 would be revisited. A proposal is not part of the public surface, so the change would not be a breaking one for adopters.
