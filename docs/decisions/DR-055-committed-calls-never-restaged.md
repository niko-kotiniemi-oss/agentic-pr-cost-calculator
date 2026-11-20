# DR-055: Calls of a ledger file found in a commit are never staged again

- **Type:** security and privacy
- **Boundary:** inside
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the owner, 2026-10-19
- **Requirements:** R52, R81, R110, R113, R117
- **Threats:** T2, T8, T10
- **Replaces:** none
- **Closed by:** none

## Context

Capture stages for a commit the calls that no ledger file on its branch holds (R81). By that rule alone, when a committed ledger file leaves the branch, removed by someone, as by a person who finds another repository's work in it (T2), or with its commit undone, the next commit would carry its calls again. Whether capture would stage them again was a choice that had to be made.

The owner decided this on 2026-10-19, because publishing usage that someone removed is the worse mistake for a public tool, and a count that is too low is the smaller harm, knowing that a session resumed in a fresh clone at the same path, which has no store, can record those calls again, as the design's risks say.

## Decision

The first run of capture that finds a ledger file it staged in a commit has the store note the file's calls as taken. From then on capture never stages them again in that clone, however the file later leaves the branch, the index or the working tree.

## Alternatives

- Bringing back, in the agent's next commit, the calls of a ledger file that someone removes once a run has found it in a commit, which the owner turned down because it undoes a removal made for privacy, or only those of work that is kept, which could not tell that work from a removal by the file alone, since in a sparse checkout that leaves out `.pr-cost/` a reset that keeps a commit's changes can leave its ledger file as a removal does, nor by the commands that removed the file, which the step reads in its transcript for the agent and git records in its reflog for a reset, since the same mixed `git reset` that takes the file out of a commit for someone who means to remove it also keeps a commit's changes to squash them with others.

## Consequences

- In that clone, a commit that is reverted, reset away in any mode but `--soft`, or split in an interactive rebase leaves its calls out of later ledger files, even when its changes are committed again, so the count is too low (T8).
- Only the file itself brings them back. Capture leaves it to git (R113), so a squash made with a mixed `git reset` and `git add -A` keeps it, except in the cases that the design's risk "[A person removes a ledger file from their branch, or a commit that holds one is undone]" lists.

## Scope

This covers the calls of a ledger file that a run has found in a commit. A file that no commit took is taken back, its calls waiting for a later commit, which is DR-014 (A ledger file that no commit took is taken back), and what a fresh clone knows of earlier removals is DR-056 (Capture does not read the branch's history).

## What reversing it would change

R52 in `usage-capture` would change, with its scenarios, and so would R81's exception for calls noted as taken, R110 in `switch-and-opt-in`, the scenarios of R113 and R117 that end with no later ledger file holding the calls, the design's decision 1 and its risks, T2's and T8's residuals, T10's answer, the README's section on adopting the tool (task 4.4), the `usage-capture` feature page and task 2.2. The notes are in the store, whose format is part of the public surface, so the change would be a breaking one for adopters (DR-096), and DR-056 would be revisited.
