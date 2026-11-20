# DR-120: Threat IDs are retired, never renumbered

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R130, R132
- **Threats:** T75
- **Replaces:** none
- **Closed by:** none

## Context

Records cite threats by ID, and a record that the default branch holds is never edited, only closed (DR-121). If the threats had to be numbered without a gap, removing one would renumber every later threat, and a record would then cite other threats while every citation still resolved (T75).

## Decision

A threat keeps its ID while it exists, and a removed threat's ID is retired: the threat model lists it with the change that removed it, and it is never used again or given to another threat.

## Alternatives

None were recorded when this was decided.

## Consequences

- The threat model's section "Retired IDs" lists each retired ID with the change that removed it. `tests/test_threat_model.py` accepts only the gaps that this list explains, and fails on a retired ID still in use or one that names no change (R132).
- A threat ID that the default branch's threat model holds or retires stays held or retired, and `tests/test_decisions.py` fails on one that vanishes, so no record comes to cite another threat (R130).
- A new threat takes the next free number, so threats found later follow under continued headings for their boundaries (see the threat model's introduction).
- An ID that keeps its number but changes its meaning is not caught (T75).

## Scope

This covers threat IDs. Requirement IDs follow the same rule, which is DR-106 (Requirement IDs are stable and never reused), and the rule that a held record is only ever closed, which makes stable IDs necessary, is DR-121 (A record is never edited once accepted, only closed by a record that replaces it).

## What reversing it would change

R130 and R132 in `project-standards` would change, with their scenarios "An ID that vanishes fails CI" and "A gap or a reused ID in the threats fails CI", and so would the threat model's introduction and its section "Retired IDs", the numbering check in `tests/test_threat_model.py`, the check of IDs in `tests/test_decisions.py`, the design's decision 13, T75's answer, task 1.18 and the feature page for `project-standards`. DR-121 would be revisited. The threat model is not part of the public surface, so the change would not be a breaking one for adopters.
