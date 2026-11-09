# DR-179: A call whose repository cannot be told is left out

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the owner, 2026-11-02
- **Requirements:** R3, R147
- **Threats:** T2, T108, T122
- **Replaces:** none
- **Closed by:** none

## Context

Capture keeps a call for this repository when the working directory that its transcript line names is in this repository (DR-057), and records it with the worktree and branch that git finds there (DR-012). That directory is Claude's current directory when the call was made, not what the call read or wrote, so absolute paths, `git -C` and nested repositories can make a call work on another repository than the one its directory is in (T2). A run reads a call some time after it was made, and by then the directory may be gone, as when a worktree is removed, or may hold another repository (T108).

## Decision

The owner decided on 2026-11-02 that, where a call's repository is ambiguous, capture leaves the call out, and the ledger says that calls were left out, rather than risk publishing another repository's usage. So a call's repository and worktree are told by its line's working directory alone, as git finds them from that directory when the run reads the call, without the session's `GIT_` variables (DR-188), never by what the call reads or writes. A call whose line gives no working directory, or whose directory no longer exists or names no repository that git can tell, is left out. When the line gives no directory, or that directory is inside this repository's folder, where Claude Code keeps its worktrees, the session's next ledger file here says that calls whose repository could not be told were left out (DR-180); when it is outside, nothing here says so, so that no ledger file tells of work in another folder.

## Alternatives

- Recording a call whose directory is gone for the repository that holds the project directory, which would publish here the work of a removed worktree of another repository.
- Telling a call's repository by what it read or wrote, which would mean reading commands, which can do anything (DR-057).
- Flagging every call whose repository could not be told, wherever its directory was, which would tell, in this repository's ledger, of work in another folder.

## Consequences

- A call made here that works on another repository through absolute paths or `git -C` is still recorded here, as DR-057 accepts, and a call made in another repository that works on this one is not (T2).
- A call made in a worktree that is removed before a run reads it is left out, so the count is too low, and when that worktree was inside this repository's folder the comment says that calls were left out (R157). A worktree of this repository kept in another folder raises no flag.
- A directory that holds another repository by the time a run reads the call sends the call to that repository, a gap that runs before and after every git command keep short (T108).
- A clone that git does not trust, as one that another user owns and that no `safe.directory` setting names in the person's global configuration or the system's, the only files that git takes it from without the session's `GIT_` variables, holds no repository that git can tell, so nothing is recorded there and no ledger file says so, as the README's section that task 4.4 writes says (T122).

## Scope

This covers what capture does when a call's repository cannot be told. Which calls count as this repository's is DR-057 (Calls are kept by the session's working directory), and which worktree and branch a call goes to is DR-012 (A call goes only to a commit in its worktree, on its branch).

## What reversing it would change

R3 and R147 in `usage-capture` would change, with their scenarios, and so would the design's decision 1 and its risk on a removed worktree, T2's answer, T108, the README's warning about other repositories that task 4.4 writes, and tasks 1.1 and 2.1. The flag is part of the ledger format, which is part of the public surface, so the change would be a breaking one for adopters (DR-096).
