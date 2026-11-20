# DR-159: A record and the threats it lists name each other

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R131
- **Threats:** T78, T80
- **Replaces:** none
- **Closed by:** none

## Context

A record lists the threats whose answer it holds (DR-108), and each threat in the threat model names what holds its answer in its own line for that (step 5 of the method in `docs/threat-model.md`). A threat that names a record the base commit does not hold was already to be listed in that record, so that whoever wrote the record agreed it holds the answer (T78). A record can be closed, and then it holds nothing (DR-121), while the threat that rested on it keeps its answer (T80).

## Decision

A record and the threats it lists name each other: every threat that an accepted record lists names that record among what holds its answer, and a threat that names a record which the base commit does not hold is listed among that record's threats.

## Alternatives

- Failing a pull request that closes a record unless each threat that the record lists changes in that same pull request, which would answer the case from the threat model's side rather than by the two names agreeing.

## Consequences

- A change that closes a record then meets every threat that rests on it, because the threat model names the closed record, and no tracked file but the records, their index, the changelog and an archived change may name one, so CI fails until each threat is revisited (R127; T80).
- `tests/test_decisions.py` reads each threat's line of what holds its answer and each record's threats, and fails naming the record and the threat when an accepted record lists a threat that does not name it, and when a threat names a record that the base commit does not hold and that record does not list the threat (R131; task 1.18).
- A record's threats are written with the record, so whoever wrote it agreed that it holds each threat's answer; whether it really does is left to the review against the code (T78).

## Scope

This covers the two names agreeing. What a record's fields hold, its threats among them, is DR-108 (Each decision has a record of its own, in an index), and that a held record changes only by being closed is DR-121 (A record is never edited once accepted, only closed by a record that replaces it).

## What reversing it would change

R131 in `project-standards` would change, with its scenario "A new record that leaves out a threat citing it fails CI", and so would the check in `tests/test_decisions.py`, task 1.18, the design's decision 13, the lines of the threat model that name the records holding each answer, and the answers of T78 and T80. DR-108 would be revisited. The records and the threat model are not part of the public surface, so the change would not be a breaking one for adopters.
