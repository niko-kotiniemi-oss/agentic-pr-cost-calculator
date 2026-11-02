# DR-177: A removed store lets no earlier call be recorded, and leaves staged ledger files to git

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-02
- **Requirements:** R153
- **Threats:** T10, T111
- **Replaces:** none
- **Closed by:** none

## Context

A person can remove the store, as the README says how to, and so can a tool that cleans the git common directory. The store notes how far each transcript was read and which calls were taken, so a run that found no store and read every transcript from its start would record again the calls made before the removal, or made while capture was off (T111). It also notes each ledger file that a run staged, which a later run takes back if no commit took it (DR-014).

## Decision

When the store is gone, or its file does not parse, which the next run that finds both switches on takes as gone and replaces, and a run that finds a switch off removes (DR-170), the next run that finds both switches on begins a new interval, so that no call that answers a line written before that run is recorded, however far the transcripts were read before. A ledger file staged before the removal is left to git, since no note says that a run staged it.

## Alternatives

- Reading every transcript from its start when the store is gone, which records again what was recorded or taken before.
- Taking back any staged ledger file that no note names, which could remove a ledger file that the person staged themselves.

## Consequences

- Removing the store never lets a call that it kept out be recorded, but a session's calls made before the next run that finds both switches on are left out, so the count is too low.
- A ledger file staged when the store was removed stays staged, and the next commit in that worktree, on whatever branch is checked out then, takes it with its calls, which were recorded with consent, so the README says to look for one with `git status`, in every worktree that `git worktree list` names, before removing the store (T10, T111).
- A removed store also takes the note of a take-back that a later run would have put back, so the next commit deletes the file that the take-back removed (T10).
- A fresh clone holds no store, so a session resumed there records no call that answers a line written before its first run there (DR-184).

## Scope

This covers what follows when the store is removed. Take-backs are DR-014 (A ledger file that no commit took is taken back), and how long the store keeps anything is DR-175.

## What reversing it would change

R153 in `usage-capture` would change, with its scenarios, and so would the design's decision 15 and its risk on a store removed while a ledger file is staged, T10's residual, T111, the README's section on the store that task 4.4 writes, and tasks 1.1 and 2.1. The store's format would not change, so the change would not be a breaking one for adopters.
