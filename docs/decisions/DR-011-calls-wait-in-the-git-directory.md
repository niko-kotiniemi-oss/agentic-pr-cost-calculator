# DR-011: Recorded calls wait in the git directory

- **Type:** architecture
- **Boundary:** inside
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R11, R47
- **Threats:** T10, T13, T38, T42, T44
- **Replaces:** none
- **Closed by:** none

## Context

A run records a call once it finds the call over, but the call reaches the pull request only with a later commit (DR-010), so recorded calls wait somewhere in between. Whatever capture leaves in the working tree or the index between commits gets in the way: staged changes make `git rebase` refuse, and a new file left staged follows `git checkout` to the next branch (T10). Several worktrees of one repository can be in use at once, and a store kept per worktree would record again a call that another worktree's store holds, so that it could reach two branches (T13).

## Decision

Capture keeps the calls it records in a store inside the repository's common git directory, which `git rev-parse --git-common-dir` names, outside the working tree and shared by every worktree. Recording changes nothing in the working tree or the index, which only staging, taking back and putting back a ledger file touch (DR-013, DR-014, DR-130).

## Alternatives

- Staging entries at the end of every turn, the first version of the design, which left the index changed between commits, so that in a test repository `git checkout` and `git rebase` refused to run.

## Consequences

- Recording never stands in the way of a checkout or a rebase, in whichever worktree the session runs (R47).
- Every worktree shares one record of each call, so no worktree records a call again (R11, T13).
- Sessions in two worktrees that hold different releases of the hook can meet one store, which is why the store carries its format's version (DR-137; the design's risk "[Two releases of the hook meet one store, as when sessions start in two worktrees that hold different releases]"; T44).
- The store is never committed, so nothing in it leaves the machine, not even the note that a run found capture off for someone who has not opted in (T38). In a fresh clone, which starts without one, capture knows what is already recorded only from the ledger files its branch holds (DR-056).
- The store grows with every call it records, and how large it grows is measured, not bounded (T42).

## Scope

This covers where recorded calls wait and what recording leaves alone. Which commit a waiting call goes to is DR-012 (A call goes only to a commit in its worktree, on its branch), how the store is written is DR-036 (The store is replaced whole, under a lock), and how it states its format's version is DR-137 (The store states its format's version).

## What reversing it would change

R11 and R47 in `usage-capture` would change, with their scenarios. The store's format is part of the public surface, so the change would be a breaking one for adopters (DR-096). The design's decision 1, the answers and residuals of T10, T13, T38, T42 and T44, the parts table, the capture flow and the hook's credentials in `docs/how-it-works.md`, the usage-capture feature page and task 2.1, which builds the store, would change too. DR-012, DR-014, DR-047, DR-055, DR-130 and DR-137, which keep their notes in the store, and DR-036, which writes it, would be revisited.
