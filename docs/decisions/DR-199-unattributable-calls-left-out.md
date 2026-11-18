# DR-199: A call whose repository cannot be told is left out

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the owner, 2026-11-02 and 2026-11-09
- **Requirements:** R3, R147, R155
- **Threats:** T2, T108, T122, T128
- **Replaces:** DR-179
- **Closed by:** none

## Context

Capture keeps a call for a repository when the working directory that its transcript line names is in that repository (DR-057), and records it with the worktree and branch that git finds there (DR-012). That directory is Claude's current directory when the call was made, not what the call read or wrote, so absolute paths, `git -C` and nested repositories can make a call work on another repository than the one its directory is in (T2). A run reads a call some time after it was made, and by then the directory may be gone, as when a worktree is removed, or may hold another repository (T108). The owner decided on 2026-11-02 that a call whose repository is ambiguous is left out, which DR-179 records.

A project's cloud thread starts in a folder that holds each of its clones and is in no repository, and many of its calls name that folder until Claude moves into a clone, as its subagents' calls do (A70). Such a call can work on any of the clones, through their paths, so its repository cannot be told. DR-179 left such calls out with no flag, since their directory is outside every repository's folder. The owner chose on 2026-11-09 that the calls made from a folder that holds the repository are left out, and that the ledger says so. This record restates DR-179 with that flag added.

## Decision

The owner decided on 2026-11-02 that, where a call's repository is ambiguous, capture leaves the call out, and the ledger says that calls were left out, rather than risk publishing another repository's usage, and on 2026-11-09 that this holds for the calls made from a folder that holds the repository. So a call's repository and worktree are told by its line's working directory alone, as git finds them from that directory when the run reads the call, without the session's `GIT_` variables (DR-188), never by what the call reads or writes. A call whose line gives no working directory, or whose directory no longer exists or names no repository that git can tell, is left out. When the line gives no directory, or that directory is inside this repository's folder, where Claude Code keeps its worktrees, or holds this repository's folder, as a project's cloud thread's folder holds its clones, the session's next ledger file here says that calls whose repository could not be told were left out (DR-200). When it is anywhere else, nothing here says so, so that no ledger file tells of work in another folder.

## Alternatives

- Recording a call whose directory is gone for the repository that holds the project directory, which would publish here the work of a removed worktree of another repository.
- Telling a call's repository by what it read or wrote, which would mean reading commands, which can do anything (DR-057).
- Recording a call made from a folder that holds this repository for this repository when the folder holds no other, which would publish here the work that such a call did elsewhere through absolute paths, and which the owner turned down on 2026-11-09.
- Leaving out with no flag the calls made from a folder that holds this repository, as DR-179 did, which would present as whole a project thread's figure from which most of its calls can be missing.
- Flagging every call whose repository could not be told, wherever its directory was, which would tell, in this repository's ledger, of work in another folder.

## Consequences

- A call made here that works on another repository through absolute paths or `git -C` is still recorded here, as DR-057 accepts, and a call made in another repository that works on this one is not (T2).
- A call made in a worktree that is removed before a run reads it is left out, so the count is too low, and when that worktree was inside this repository's folder the comment says that calls were left out (R157). A worktree of this repository kept in another folder raises no flag.
- In a project's cloud thread, the calls made from the folder that holds its clones are left out, and the session's next ledger file in each clone that turns the tool on says so, so the comment says that the token cost is a lower bound, by an amount that it cannot give (T128). The README advises asking Claude, as in the project's instructions, to work inside the repository.
- A flag in one clone can stand for calls that worked on another clone of the same folder, since nothing tells them apart, and it says only that calls were left out (DR-200).
- A directory that holds another repository by the time a run reads the call sends the call to that repository, a gap that runs before and after every git command keep short (T108).
- A clone that git does not trust, as one that another user owns and that no `safe.directory` setting names in the person's global configuration or the system's, the only files that git takes it from without the session's `GIT_` variables, holds no repository that git can tell, so nothing is recorded there and no ledger file says so, as the README's section that task 4.4 writes says (T122).

## Scope

This covers what capture does when a call's repository cannot be told. Which calls count as a repository's is DR-057 (Calls are kept by the session's working directory), which worktree and branch a call goes to is DR-012 (A call goes only to a commit in its worktree, on its branch), and which repositories a run of the plugin works on is DR-198 (A plugin run works on each repository that it meets).

## What reversing it would change

R3 and R147 in `usage-capture` would change, with their scenarios, and so would R155, the design's decision 1 and its risks on a removed worktree and on a session that works from a folder that holds the repository, T2's answer, T108, T128, the README's warning about other repositories and its section on cloud threads, which task 4.4 writes, and tasks 1.1 and 2.1. The flag is part of the ledger format, which is part of the public surface, so the change would be a breaking one for adopters (DR-096).
