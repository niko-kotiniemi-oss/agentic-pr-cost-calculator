# DR-269: A record number held twice is mended by renumbering the later record

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-11-20
- **Requirements:** R266
- **Threats:** T76, T248, T250
- **Replaces:** none
- **Closed by:** none

## Context

Records run from DR-001 without a gap or a repeat (R124), and DR-119 has `main`'s ruleset require a pull request to be up to date before it merges, so that two pull requests cannot both take the next number. A repeat can still reach the default branch, as when the setting is off for a time, and then every later pull request fails CI, while renumbering either record is a change that the rule on accepted records forbids (T76). The threat model left how to recover to the owner, and on 2026-11-20 the owner chose to renumber the later record.

## Decision

When the default branch holds two records with one number, a pull request that does only this moves the record that the default branch's first-parent history added later to the number after the highest that the default branch holds. The moved record's text stays as it was, but for the number in its heading. In the other records that the same merge added, the old number becomes the new one where it names the moved record, and so does the Closed by of each record that the moved one replaces, and nothing else changes. The index and every other page that names the moved record follow it. Any other removal or renaming of a record that the default branch holds still fails. A number held more than twice, two numbers held twice, and two records with one number that one merge added fit no such rule, and are left to the owner.

## Alternatives

- Reverting the later merge whole and bringing it back under a new number: the check would have to allow removing records as the exact undoing of a merge, and every other change of that merge would go and come back with them.
- Deciding case by case, with no rule or check: CI would stay red on the default branch until the owner decided, and the recovery would rest on whoever was there to do it.

## Consequences

- `tests/test_decisions.py` accepts the move only when each base that it compares with holds the number twice, only for the record that the base's first-parent history added later, by the order of that history, only to the number after the base's highest, and only with the text unchanged but for that number, in it, in the records added with it and in the Closed by of the records that it replaces (R266; T248, T250).
- A repeat that the rule cannot mend fails with a message that names the records and says that the owner decides how to mend them (T250).
- The record that merged first keeps its number, so what cited it before the repeat still names it. What cited the later record by that number is ambiguous until the move, and the pull request that moves it names it by its new number everywhere but in records the default branch holds from other merges, which keep their text (DR-268).
- DR-119 still keeps a repeat from forming; this record only mends one that forms anyway (T76).

## Scope

This covers how a repeated record number is mended once the default branch holds it. How a record that the default branch holds otherwise changes is DR-268 (A record is closed, never edited, but one change may add a field to every record), and the setting that keeps a repeat from forming is DR-119 (Pull requests merge only when up to date with the default branch).

## What reversing it would change

How hard it is to reverse: reversible. The rule is an exception in one check, which one pull request can remove, leaving a repeat with no fix but the owner's decision. R266 in `project-standards` would change, with its scenarios, and so would the answers of T76, T248 and T250, `tests/test_decisions.py`, the design's decision 13 and task 1.45. Records are not part of the public surface, so the change would not be a breaking one for adopters.
