# DR-014: A ledger file that no commit took is taken back

- **Type:** architecture
- **Boundary:** inside
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R9, R51, R57, R87, R110, R113, R114
- **Threats:** T8, T10, T19, T38, T42
- **Replaces:** none
- **Closed by:** none

## Context

Capture stages a ledger file before its command runs (DR-013), and the command may fail, or never run: it can be refused, blocked by another hook, cancelled or interrupted, and then gets no `PostToolUse` or `PostToolUseFailure` run, while an interrupt runs no `Stop` either (see the design's context). A file left staged gets in the way of git work and can carry its calls to another branch (T10, T19).

## Decision

The run after the command takes the file back, from the index and the working tree, when the commit checked out in that worktree does not hold it, and for a command that gets no such run, any later run in the repository, from that session or another, does so once it finds the command over.

## Alternatives

- Taking a ledger file that no commit took back at the next turn's end, the second version of the design, which left it staged until then, where in a test repository it made `git rebase` refuse and followed `git checkout` to another branch, and where a run holding the index lock makes a commit fail.
- Taking a file back at `UserPromptSubmit`, whose standard output Claude Code adds to Claude's context, and which runs only once the next prompt is sent.
- Taking it back at `PermissionDenied`, which runs only in auto mode, where the denied command's result already lets the next run take the file back.

## Consequences

- Until a run finds the command over, the file stays staged, and meanwhile `git rebase` refuses to run, `git checkout` carries the file to another branch and `git stash` takes it, while a session killed during its commit leaves it staged until the person removes it or the session is resumed (the design's risk "[A commit is refused, blocked, cancelled or interrupted after its ledger file was staged]"; T10, T19).
- A take-back never removes a file that the checked-out commit holds, and leaves the file for a later run while another git command holds the index (R113, R114). It goes ahead whatever the switches say (R110, T38), and it also reaches a file that a killed run left, since a file is noted in the store before it is written (R57, T42).
- How soon the file of a refused, blocked or cancelled command is taken back rests on Claude Code writing that command's result into the transcript, an assumption of the threat model that task 1.1 checks. Without it, the file waits for a later call of its agent, its agent's stop or its session's end.

## Scope

This covers ledger files that no commit took. Putting back a file that a take-back removed although a commit holds it is DR-130 (A taken-back ledger file is put back once, when its commit holds it). A file that a run has found in a commit is left to git, and its calls are never staged again, which is DR-055 (Calls of a ledger file found in a commit are never staged again).

## What reversing it would change

R9, R51, R87, R113 and R114 in `usage-capture`, R57 in `ledger` and R110 in `switch-and-opt-in` would change, with their scenarios. The notes that the store keeps for staged files are part of the store's format, which is on the public surface, so the change would be a breaking one for adopters (DR-096). The design's decision 1 and its risks, the answers and residuals of T8, T10, T19, T38 and T42, the flows of a commit and of a commit that never ran in `docs/how-it-works.md`, the usage-capture feature page and task 2.2 would change too, and DR-013, DR-055 and DR-130 would be revisited.
