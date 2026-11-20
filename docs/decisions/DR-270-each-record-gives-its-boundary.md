# DR-270: Each record gives its boundary

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-27
- **Requirements:** R264
- **Threats:** T249
- **Replaces:** none
- **Closed by:** none

## Context

A record says what kind of decision it is, by its type, but not which way it faces: whether it stays inside the tool, takes something in from outside or sets what goes out to adopters. On 2026-10-27 the owner asked that every record gain a field Boundary, as inside, how the tool works and is built and checked; incoming, what it takes from outside, and how that is pinned, checked and updated; or outgoing, what adopters copy, call or configure, and on what terms; with a column for it in the index.

## Decision

Each record gives its boundary in a field right after its type, and the index gives it in a column right after the type:

- `incoming`, for a decision that chiefly governs what the tool or the project takes in from outside, and how that is pinned, checked and updated: transcripts, git's and GitHub's data, prices, dependencies, contributions, and text that could steer an agent;
- `outgoing`, for one that chiefly governs what adopters copy, call or configure, what the tool publishes to them, and on what terms: the hook, the workflow, the switch and the opt-in, the ledger, the comment, releases and the licence;
- `inside`, for one that governs how the tool works, is built and is checked, where neither applies.

A decision that faces both ways takes the one that it chiefly governs. The change that brings the field sets it on every record that the default branch holds, by these meanings, and review checks them.

## Alternatives

- Two values for a decision that faces both ways: the column would hold lists, and each record's main direction would go unsaid.
- More values, such as one for the project's own process: process records are already a type, and the owner's three values say which way a decision faces, which a type does not.
- No field, with the boundary left to each record's text: no column could show it, and no test could hold it.

## Consequences

- `tests/test_decisions.py` fails on a record that lacks the field, gives it out of its place or gives a value outside the three, and on an index whose column disagrees with a record (R264).
- Whether a record's boundary is the right one of the three rests on review, since no machine can tell which way a decision chiefly faces (T249).
- The records that the default branch holds gain the field by DR-268's exception, in a commit that changes nothing else in them. A value that turns out wrong is corrected only by closing its record (T249).

## Scope

This covers which way a record faces. How hard it is to reverse is DR-271 (Each record gives how hard it is to reverse), and what else a record gives is DR-108 (Each decision has a record of its own, in an index).

## What reversing it would change

How hard it is to reverse: reversible with work. The field would stay in every record that holds it, since only a change under DR-268's exception or a closing record can change one, and later records could leave it out once the form no longer asked for it. R264 in `project-standards` would change, with its scenarios, and so would the design's decision 13, `tests/test_decisions.py`, the index's column, T249's answer, `docs/decisions/README.md` and task 1.46. Records are not part of the public surface, so the change would not be a breaking one for adopters.
