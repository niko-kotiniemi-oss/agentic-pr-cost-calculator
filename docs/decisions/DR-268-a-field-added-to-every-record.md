# DR-268: A record is closed, never edited, but one change may add a field to every record

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-27 and 2026-11-13
- **Requirements:** R126, R127, R129, R130, R265
- **Threats:** T70, T71, T74, T75, T76, T77, T80, T247
- **Replaces:** DR-121
- **Closed by:** none

## Context

DR-121 has a record that the default branch holds change only by being closed, as a whole, by a record that replaces it. On 2026-10-27 the owner asked that every record gain the fields Boundary and Reversibility, and approved a plan that adds them in a change that first replaces DR-121 with a narrow rule that lets one change add a field to every record and change nothing else. On 2026-11-13 the owner asked that each record say how hard it is to reverse, and DR-230 left the field to the backlog item B-004 (Two new fields on every record), which plans that rule. Under DR-121 alone, a field on every record would close all of them and add as many records again.

## Decision

Once the default branch holds a record, it changes only by being closed, as a whole, by a new record that replaces it and restates whatever still holds. Its status then becomes closed and it names its closer, which names it among those it replaces. One exception holds: the change that brings a field to every record adds its line, in its place, to every record that the default branch holds, closed ones included, and changes nothing else in any of them. That extends the form of every record and edits no decision: a decision still changes only by being superseded by a record that replaces it, which may close it. The requirement that allows it names each such field, Boundary and Reversibility so far, so that a later field comes only with a change to that requirement, which the owner reads. DR-269 (A record number held twice is mended by renumbering the later record) gives the only other exception.

## Alternatives

- Fields in the index only: the index would hold what no record holds, and a record read alone would not say what its row says.
- Closing every record with a record that restates it with the fields: every record would be added again under a new number, and every mention of the old numbers would have to move to the new ones.
- No new field on records that the default branch holds, only on later ones: the index's columns would be empty for every record before the change, and the records most built on would say least.

## Consequences

- `tests/test_decisions.py` compares git trees with no rename detection, so a record removed, renamed, moved or changed other than by closing fails, and a mistaken merge's records are undone by records that close them (R129; T70, T75). A commit that adds the lines of Boundary and Reversibility, in their places, to every record that the base holds, and changes nothing else in them but what closing a record allows, passes, and one that adds another field, adds them to some records and not to others, or changes any other line fails (R265; T247).
- CI, which clones the whole history and names the base in `BASE_COMMIT`, is the gate, since a local run compares with the remote-tracking branch as last fetched (T70).
- The check and the workflow that runs it can still change together in one pull request, which rests on the owner's review of the diff (T71).
- A held record is otherwise never renumbered, so DR-119 keeps two pull requests from taking one number, and DR-269 mends a repeat that reaches the default branch anyway (T76). The IDs that records cite stay held or retired (R130; T75).
- A closed record keeps its text, so only the records, their index, the changelog and archived changes may name one (R127; T74, T80).
- Private text that reached a record cannot be edited out of it while it holds, so the text can be cleared only once the record is closed (T77; DR-153).
- Of what rests on DR-121, as DR-230 asks: DR-108, DR-119, DR-120, DR-153 and DR-230 still hold, since each rests on records being closed rather than edited, which this record restates, and DR-119's recovery is now DR-269. R126, R127, R129 and R130 still hold, with R129 pointing at the two exceptions. T70, T71, T74, T75, T76, T77 and T80 name this record in place of DR-121 and keep their answers.

## Scope

This covers how a record that the default branch holds may change. What a record holds is DR-108 (Each decision has a record of its own, in an index), which fields it gives beyond those is DR-270 (Each record gives its boundary) and DR-271 (Each record gives how hard it is to reverse), what may change in a record once it is closed is DR-153 (A closed record's lines may be replaced by `[removed]`), and how a repeated number is mended is DR-269.

## What reversing it would change

How hard it is to reverse: reversible with work. Dropping the exception would leave the fields that it let in place, so a later field would again need every record closed. R126, R127, R129, R130 and R265 in `project-standards` would change, with their scenarios, and so would the design's decision 13, `tests/test_decisions.py`, CI's whole-history clone and its `BASE_COMMIT`, tasks 1.18, 1.44 and 6.3, the answers of T70, T71, T74 to T77, T80 and T247, the opening of `docs/decisions/README.md`, `docs/CLAUDE.md`'s section on decision records, the feature page for `project-standards` and `docs/how-it-works.md`. DR-108, DR-119, DR-120, DR-153, DR-269, DR-270 and DR-271 would be revisited. Records are not part of the public surface, so the change would not be a breaking one for adopters.
