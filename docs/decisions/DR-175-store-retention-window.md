# DR-175: The store keeps nothing past a retention window of 30 days, and removes itself when empty

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the owner, 2026-11-02 and 2026-11-03
- **Requirements:** R150, R151
- **Threats:** T110, T114
- **Replaces:** none
- **Closed by:** none

## Context

Before this change, the store kept a call's note for as long as the store lasted, and the store was never removed. The owner asked on 2026-11-02 for short retention and specified cleanup, and picked the window from 7, 14 and 30 days: 14 that day, and 30 on 2026-11-03. A call waits in the store until a commit in its worktree, on its branch, takes it (DR-012), which can take days on a branch that waits, and a note of a taken call keeps it from being staged again (DR-055).

## Decision

The store's retention window is 30 days. A run records no call whose day is more than 30 days before the run's day, drops each waiting call, each flag due, by the day a run last raised it, and each note of a taken call once that is so of its day, flagging a dropped waiting call for its age in the next ledger file staged for its worktree and branch (DR-180), drops a session's notes once none of its runs has come within the window, takes back a ledger file whose note is older than the window, as for a command that is over, and drops a take-back's note that old. A run that leaves the store holding nothing, no flag among it, removes its file and its folder, and every run that finds a store of a version that it knows does all this, whatever the switches say (DR-170), while one that finds a version that it does not know leaves the store as it was (DR-187).

## Alternatives

- A window of 7 days, which keeps less for less long, but drops the calls of a branch whose next commit waits more than a week.
- A window of 14 days, which the owner picked first, and which keeps a shorter record of when the person worked, but drops the calls of a branch whose next commit waits more than two weeks.
- No window, which keeps what capture no longer needs for as long as the repository is used.

## Consequences

- No call older than the window can be recorded, so dropping a taken call's note at the end of the window cannot let its calls be staged again, and DR-055 still holds.
- A branch that waits longer than the window for its next commit loses its waiting calls, so the count is too low, and its next ledger file says that calls were left out for their age.
- Retention runs only when a run comes, so a repository where no session runs again keeps its store until the person removes it, which the README says how to do (T114).

## Scope

This covers how long the store keeps anything. What it keeps is DR-173, and what an opt-out removes at once is DR-171.

## What reversing it would change

R150 and R151 in `usage-capture` would change, with their scenarios, and so would the design's decision 15 and its risk on a repository where no session runs again, T110, T114, the README's section on the store that task 4.4 writes, the pages that give the window's length, which are the usage-capture feature page, the how-it-works page, `SECURITY.md`, the changelog and the glossary, and tasks 1.1 and 2.1. The window is part of the store's format, which is part of the public surface, so the change would be a breaking one for adopters (DR-096).
