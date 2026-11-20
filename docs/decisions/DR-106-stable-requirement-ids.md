# DR-106: Requirement IDs are stable and never reused

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R126, R130
- **Threats:** T57, T75
- **Replaces:** none
- **Closed by:** none

## Context

The register gives every requirement an ID (DR-100), and other documents cite requirements by it, as each feature page does in its list of requirements. Later changes add requirements and remove them.

## Decision

The register keeps a requirement's ID for as long as the requirement exists. A requirement that a later change removes leaves the register, and its ID is listed under the register's retired IDs, with the change that removed it, and never used again.

## Alternatives

None were recorded when this was decided.

## Consequences

- A new requirement takes the next free number, so the register's rows follow the order in which requirements were added, not the order of the specs (`docs/requirements.md`).
- Since a retired ID is never used again, an ID that a feature page cites never comes to mean another requirement. T57's answer includes that a removed requirement's ID is retired.
- `tests/test_documentation.py` fails when the register's and the retired IDs do not run from R1 without a gap, when the register's IDs are out of order, and when an ID is both registered and retired.

## Scope

This covers the IDs of requirements. What the register holds is DR-100 (A register lists every requirement with its kind).

## What reversing it would change

R130's clause on requirement IDs would change, with its scenario "An ID that vanishes fails CI", and so would R126's clauses on a retired requirement that a record names and on an accepted record that rests only on retired requirements. The design's decision 12, the sentence in its decision 13 that threat IDs, like requirement IDs, are retired rather than reused, the same sentence on the feature page for `project-standards`, the paragraph on IDs and the list of retired IDs in `docs/requirements.md`, the register's checks in `tests/test_documentation.py` and the answers of T57 and T75 would change, and so would every document that cites a requirement by its ID once an ID moved or came back. DR-100 and DR-120 (Threat IDs are retired, never renumbered) would be revisited.
