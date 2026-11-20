# DR-271: Each record gives how hard it is to reverse

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-27 and 2026-11-13
- **Requirements:** R264
- **Threats:** T249
- **Replaces:** none
- **Closed by:** none

## Context

DR-230 has each record say how hard it is to reverse, as reversible, reversible with work, or a one-way door, with the reason, in the first sentence of its section on what reversing it would change, until records gain a field for it, which the backlog item B-004 (Two new fields on every record) brings. The owner asked for the field on 2026-10-27 and for the statement on 2026-11-13. The records from DR-225 to DR-267 give the statement in varied words, such as easy, or reversible, with work.

## Decision

Each record gives its reversibility in a field right after its boundary, as `reversible`, `reversible with work` or `one-way door`, and the index gives it in a column right after the boundary's. The reason stays where DR-230 puts it, in the first sentence of the section on what reversing it would change, and from this record on that sentence opens with "How hard it is to reverse: " and the field's value. A record whose own text gives two values, as for versions already released and later ones, or a value that holds only until some point, takes the harder. The change that brings the field sets it on every record that the default branch holds, from what each record's last section says, and the owner confirms each that it marks as a one-way door before the change is accepted, as DR-230 asks of a one-way door.

## Alternatives

- The field alone, with no sentence: the reason would have no fixed place, and DR-230 asks for one.
- The sentence alone, as before: no column could show it, and no test could hold it.
- The words of the records from DR-225 on, such as easy: those records use several words for one value, and the field takes the three that DR-230 gives.

## Consequences

- `tests/test_decisions.py` fails on a record that lacks the field, gives it out of its place or gives a value outside the three, on an index whose column disagrees with a record, and on a record from DR-268 on whose sentence does not open with its value (R264).
- For the records before DR-268, whether the field fits what the record says rests on review, and the change compares each statement from DR-225 to DR-267 with its field by a script, as evidence in its pull request (T249).
- The records that the default branch holds gain the field by DR-268's exception, in a commit that changes nothing else in them. A value that turns out wrong is corrected only by closing its record (T249).

## Scope

This covers how a record gives how hard it is to reverse. That each record says it, with its reason, and what replacing a record starts are DR-230 (Each record says how hard it is to reverse, and replacing one starts an assessment of what rests on it), and which way a record faces is DR-270 (Each record gives its boundary).

## What reversing it would change

How hard it is to reverse: reversible with work. The field would stay in every record that holds it, as for DR-270, and later records could leave it out. R264 in `project-standards` would change, with its scenarios, and so would the design's decision 13, `tests/test_decisions.py`, the index's column, T249's answer, `docs/decisions/README.md`, `docs/CLAUDE.md`'s rule on records and task 1.46. DR-230 would be revisited. Records are not part of the public surface, so the change would not be a breaking one for adopters.
