# DR-130: A taken-back ledger file is put back once, when its commit holds it

- **Type:** technical
- **Boundary:** inside
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R110, R115, R116, R117
- **Threats:** T2, T8, T10, T38
- **Replaces:** none
- **Closed by:** none

## Context

A run takes back a ledger file that the commit checked out in its worktree does not hold (DR-014). A take-back can race a commit that holds no index lock while its `prepare-commit-msg` and `commit-msg` hooks run, or follow a reset in the commit's own command that a later reset undoes (see the design's decision 1). Either way, a commit holds the file while the index and the working tree lack it, so that the next commit would delete it, with its calls (T10).

## Decision

Every take-back notes, for its file, the commit it found checked out, which does not hold the file, and whether it removed the file from the index, the working tree or both. The first later run in that worktree that finds another commit checked out and the index free puts the file back where the take-back removed it, as that commit holds it, if that commit holds it, and then forgets the note, whether it put the file back or not. No file is put back in any other case.

## Alternatives

None were recorded when this was decided.

## Consequences

- A put-back can undo, once, a removal that the person made before it, while a `git stash` made before the put-back, or a mixed `git reset` back to the commit that took the file once a run has found another commit checked out, can still leave the file deleted, so that a later `git commit -a` removes it with its calls (the design's risk "[A git command starts while a run stages or takes back a ledger file]"; T2, T8).
- A put-back puts the file only where the take-back removed it, and into the working tree only while the index holds it, so a removal from the index that another command makes while the commit runs stands, and the next commit deletes the file, as it would without capture (R116, R117).
- Like a take-back, a put-back goes ahead whatever the switches say (R110, T38), and waits for a later run while another git command holds the index lock.

## Scope

This covers putting back a ledger file that a take-back removed although a commit holds it. Taking back a file that no commit took is DR-014 (A ledger file that no commit took is taken back), and leaving to git a file that a run has found in a commit, whose calls are never staged again, is DR-055 (Calls of a ledger file found in a commit are never staged again).

## What reversing it would change

R115, R116 and R117 in `usage-capture` would change, with their scenarios, and so would R110 in `switch-and-opt-in`, under which files are put back whatever the switches say. The notes that the store keeps for take-backs are part of the store's format, which is on the public surface (DR-154), so the change would be a breaking one for adopters (DR-096). The design's decision 1 and its risks, the answers and residuals of T2, T8, T10 and T38, the capture flow in `docs/how-it-works.md`, the README's account of what a put-back can undo (task 4.4) and task 2.2 would change too, and DR-014 and DR-055 would be revisited.
