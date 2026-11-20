# DR-012: A call goes only to a commit in its worktree, on its branch

- **Type:** architecture
- **Boundary:** inside
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R3, R46, R78, R81
- **Threats:** T8, T10, T19
- **Replaces:** none
- **Closed by:** none

## Context

Every worktree of a repository shares capture's one store (DR-011), sessions can run in several worktrees at once, and an agent changes branches as it works. A call recorded in one worktree or on one branch and committed in another would put its usage into the ledger of a pull request that did not spend it (T19). A plain clone, with no worktree added, still has one worktree: its checkout, which git calls the main worktree. So this record holds in a plain clone too, and there it matters only when the clone switches to another branch, or to no branch, while calls wait for a commit.

## Decision

Capture records each call with the worktree that git itself finds from the directory its transcript line names, which for a worktree inside the repository's folder, as Claude Code makes them, is that worktree and not the main checkout around it, and with the branch checked out there when the call is recorded, or the fact that none was. A ledger file holds only the calls recorded for the worktree where its commit runs and the branch checked out there, and calls recorded while no branch was checked out go only to a commit made the same way in the same worktree.

## Alternatives

- Taking a call's branch from the one that its transcript line names, which was seen reading `HEAD` while a branch was checked out (see the design's context).

## Consequences

- A call waits for a commit that capture stages for, in its own worktree and on its own branch, so some calls reach no pull request: those made after the agent's last such commit on a branch, those recorded on a branch that gets no later commit, and those recorded while no branch is checked out, unless a commit is made the same way. The design's risk "[Some calls reach no commit]" lists them, and T8's residual holds them.
- A call goes to the branch checked out when it is recorded, which can differ from the branch it was made on, in the cases that the design's risk "[A call is recorded on the branch checked out when it is recorded, which can differ from the one it was made on]" gives (T19).
- When git takes a ledger file to another branch, still staged, left in a working tree by a removal or kept in a stash, its calls go to that branch's pull request (T10, T19).

## Scope

This covers which commit a recorded call may go to. Where calls wait meanwhile is DR-011 (Recorded calls wait in the git directory), when a ledger file is staged is DR-013 (A ledger file is staged just before a commit that capture can follow), and which commits capture stages for at all is DR-034 (Capture stages only for a commit whose branch and contents it can tell).

## What reversing it would change

R46, R78 and R81 in `usage-capture` would change, with their scenarios, and so would R3's scenario "A worktree of this repository is this repository" in the same spec, and the store's format, which records each call's worktree and branch. The store's format is part of the public surface, so that change would be a breaking one for adopters (DR-096). The design's decision 1 and its risks, T8's, T10's and T19's residuals, the capture flow in `docs/how-it-works.md`, the usage-capture feature page, the README's list of the calls that reach no commit (task 4.4), and tasks 2.1 and 2.2 would change too, and DR-011 and DR-034 would be revisited.
