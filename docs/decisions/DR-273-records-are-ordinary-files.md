# DR-273: Every file in the records' folder is an ordinary file, not an executable one

- **Type:** process
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R133
- **Threats:** T79
- **Replaces:** none
- **Closed by:** none

## Context

The records' folder holds only the records and their index, each a file and not a link (R133), and the comparison with the default branch counts a held record whose mode changes as changed. A new record's mode was not checked otherwise, which a review of PR 1 left open: a record could reach the default branch as an executable file, which no record needs to be.

## Decision

Every file in `docs/decisions/` has git's mode 100644, an ordinary file that is not executable, in HEAD's tree and in the index.

## Alternatives

- Leaving a new record's mode unchecked, as before: an executable record would pass, and once held, keep its mode, since a held record's mode cannot change.

## Consequences

- `tests/test_decisions.py` fails on a file in the folder whose mode is other than 100644, and names the file and its mode (R133; T79).
- Every file in the folder had that mode when the check was added, so no record changes.

## Scope

This covers the mode of the files in the records' folder. What else the folder may hold is DR-108 (Each decision has a record of its own, in an index).

## What reversing it would change

How hard it is to reverse: reversible. The check is a few lines of one test. R133 in `project-standards` would change, with its scenario "A record committed as executable fails CI", and so would T79's answer, `tests/test_decisions.py` and task 1.47. Records are not part of the public surface, so the change would not be a breaking one for adopters.
