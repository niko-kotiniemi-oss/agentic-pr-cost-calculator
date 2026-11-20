# DR-153: A closed record's lines may be replaced by `[removed]`

- **Type:** security and privacy
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R129
- **Threats:** T77
- **Replaces:** none
- **Closed by:** none

## Context

A record that the default branch holds changes only by being closed by a record that replaces it (DR-121). Most of a record is new prose about reasons that often come from conversations the repository does not keep, and its consequences could carry a cost figure from someone's own work, so private text can reach a record that the rule then forbids correcting (T77).

## Decision

Once a record is closed, any line of text under its sections may be replaced by `[removed]`, and nothing else in it changes.

## Alternatives

None were recorded when this was decided.

## Consequences

- The comparison with the default branch accepts a closed record whose lines of text under its sections carry that word in place of what they said, and refuses a cleared heading, a cleared field, a cleared blank line and any change to the number of lines (R129; task 1.18).
- The record that closes it restates whatever still holds, so clearing lines leaves no decision unexplained (DR-121).
- Git history keeps the cleared text, and only the owner can rewrite history (T77).
- A closed record's heading, its file name, its row in the index and the titled mentions of it in records that stay accepted cannot be cleared this way, so a title or a file name that should not have been written stays in the default branch's tree, and only the review of the diff before the merge keeps one out (T77).
- The private-reference check reads tracked path names as well as what the files hold, so a pattern that it knows in a record's file name fails CI before the merge (T32).

## Scope

This covers what may change in a record once it is closed. That a record changes only by being closed, and what closing it means, is DR-121 (A record is never edited once accepted, only closed by a record that replaces it).

## What reversing it would change

R129's clause on the lines of a closed record would change, with the clearing half of its scenario "A record closed, or cleared once closed, passes", and so would the comparison in `tests/test_decisions.py`, task 1.18, the design's decision 13, T77's answer and residual, and the line of `CLAUDE.md`'s section on decision records that allows the clearing. DR-121 would be revisited. Records are not part of the public surface, so the change would not be a breaking one for adopters.
