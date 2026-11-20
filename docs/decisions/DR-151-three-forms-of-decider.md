# DR-151: A record's decider takes one of three forms

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R124, R126
- **Threats:** T72
- **Replaces:** none
- **Closed by:** none

## Context

A record's fields say who decided it (DR-108). An agent, or an outside contributor, could write that the owner made a choice the owner never made, and one merge accepts every record in a pull request, with its attributions, whether or not each was read (T72).

## Decision

A record's decider takes one of three forms: the owner, with the dates of the decision; the change that made it; or that change, with the dates on which the owner asked for what it then decided. `CLAUDE.md` says which of the three fits: the owner is named only for a choice that the owner stated or picked, and where the owner asked for an outcome and the change chose how to meet it, the decider is the change, as the owner asked, with the dates.

## Alternatives

None were recorded when this was decided.

## Consequences

- `tests/test_decisions.py` fails on a decider outside the three forms, on a date in the field that is not a date, and on a change that this repository does not hold (R124, R126; task 1.18).
- The field holds no link, no quotation and no identifier, so a record cannot point at a conversation for its attribution.
- The index gives every record's decider in a column of its own, so one diff carries every attribution for the owner to read before merging. No machine can tell whether the owner made a decision, so an attribution rests on that reading, and `CLAUDE.md` says that the owner's present word decides, not a record's attribution (T72).

## Scope

This covers the forms that a record's decider takes and which of them fits. What else a record's fields give, and the index that repeats them, are DR-108 (Each decision has a record of its own, in an index).

## What reversing it would change

R124's list of what a record gives would change, with its scenario "A record out of form fails CI", and so would R126's clauses on the dates and the change that a record names. The decider's check in `tests/test_decisions.py`, the index's column of deciders, task 1.18, the design's decision 13, T72's answer and the lines of `CLAUDE.md` on who is named as a record's decider would change too, and DR-108 would be revisited. Records are not part of the public surface, so the change would not be a breaking one for adopters.
