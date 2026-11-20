# DR-121: A record is never edited once accepted, only closed by a record that replaces it

- **Type:** process
- **Status:** closed
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-26
- **Requirements:** R126, R127, R129, R130
- **Threats:** T70, T71, T74, T75, T76, T77, T80
- **Replaces:** none
- **Closed by:** DR-268

## Context

Each decision was to be reversible or replaceable on its own (see the proposal's "What Changes"). The owner's merge of the pull request that adds a record accepts it, and agents and readers then build on what it says (T73).

## Decision

Once the default branch holds a record, it changes only by being closed, as a whole, by a new record that replaces it and restates whatever still holds. Its status then becomes closed and it names its closer, which names it among those it replaces.

## Alternatives

None were recorded when this was decided.

## Consequences

- `tests/test_decisions.py` compares git trees with no rename detection, so a record removed, renamed, moved or changed other than by closing fails, and a mistaken merge's records are undone by records that close them (R129; T70, T75).
- CI, which clones the whole history and names the base in `BASE_COMMIT`, is the gate, since a local run compares with the remote-tracking branch as last fetched (T70).
- The check and the workflow that runs it can still change together in one pull request, which rests on the owner's review of the diff (T71).
- A held record is never renumbered, so DR-119 keeps two pull requests from taking one number (T76), and the IDs that records cite stay held or retired (R130; T75).
- A closed record keeps its text, so only the records, their index, the changelog and archived changes may name one (R127; T74, T80).
- Private text that reached a record cannot be edited out of it while it holds, so the text can be cleared only once the record is closed (T77; DR-153).

## Scope

This covers how a record that the default branch holds may change. What a record holds is DR-108 (Each decision has a record of its own, in an index), and what may change in a record once it is closed is DR-153 (A closed record's lines may be replaced by `[removed]`).

## What reversing it would change

R126, R127, R129 and R130 in `project-standards` would change, with their scenarios, and so would the design's decision 13, `tests/test_decisions.py`, CI's whole-history clone and its `BASE_COMMIT`, tasks 1.18 and 6.3, the answers of T70, T71, T74 to T77 and T80, the proposal's "What Changes", the opening of `docs/decisions/README.md`, `CLAUDE.md`'s section on decision records, `CONTRIBUTING.md`, the feature page for `project-standards` and `docs/how-it-works.md`. DR-108, DR-119, DR-120 and DR-153 would be revisited. Records are not part of the public surface, so the change would not be a breaking one for adopters.
