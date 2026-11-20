# DR-272: A record's decider gives no date before the owner's first brief

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-11-20
- **Requirements:** R267
- **Threats:** T72
- **Replaces:** none
- **Closed by:** none

## Context

A record's decider may give the dates of the owner's decision or request (DR-151), and a date later than the day the tests run already fails. A review of PR 1 proposed that a date earlier than the repository's first commit fail as well, which was left open. The repository's first commit is dated 2026-10-18, but the owner's first brief for the tool came on 2026-10-17, before the repository was created again under a new name, and records name the owner's requests of that day.

## Decision

A date that a record's decider gives is no earlier than 2026-10-17, the day of the owner's first brief for the tool, and no later than the day the tests run. The earliest date is fixed in the test, rather than read from the history, so that the check does not depend on where a clone's history starts.

## Alternatives

- The repository's first commit: it would fail the records that name the owner's requests of 2026-10-17, which are correct.
- No earliest date, as before: a typed year or month could put a decision before the project began, and nothing would fail.

## Consequences

- `tests/test_decisions.py` fails on a decider's date before 2026-10-17 and passes one on that day (R267).
- A date between the first brief and the test's day that is still wrong, such as a day swapped for another, rests on review, as T72 has it.

## Scope

This covers the range of a decider's dates. The forms that a decider takes are DR-151 (A record's decider takes one of three forms).

## What reversing it would change

How hard it is to reverse: reversible. The earliest date is one constant in a test. R267 in `project-standards` would change, with its scenarios, and so would T72's answer, `tests/test_decisions.py` and task 1.47. Records are not part of the public surface, so the change would not be a breaking one for adopters.
