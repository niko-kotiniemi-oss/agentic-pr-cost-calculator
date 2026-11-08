# DR-184: Capture does not read the branch's history

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the owner, 2026-10-19
- **Requirements:** R2, R45, R52, R81, R153
- **Threats:** T2, T19
- **Replaces:** DR-056
- **Closed by:** none

## Context

Capture keeps the calls it has recorded, and the notes that keep a removed ledger file's calls out (DR-055), in its store, inside one clone's git common directory (DR-011), so a fresh clone, such as one where a session is resumed, has none of them (T19). A file that a later commit removes stays in git history, though, where a fresh clone could still find it (T2). The owner decided on 2026-10-19 that capture does not read the branch's history, which DR-056 records.

DR-056 said that a session resumed in a fresh clone at the same path could stage again the calls of a ledger file that its branch no longer holds. That no longer follows: an interval when both switches were on now begins only at a run (DR-168), and a run that finds no store records no call that answers a line written before it (DR-177), so a fresh clone, which holds no store, records none of those calls. This record restates the owner's decision with that consequence corrected.

## Decision

Capture learns which calls are already recorded only from its store and from the ledger files that the branch holds, and it does not read the branch's history.

## Alternatives

- Treating as recorded the calls of every ledger file in the branch's history, which the owner turned down on 2026-10-19, and which would work in a fresh clone that holds that history too, but would keep a removed file's calls out only when a later commit removed the file, whose content that history then still holds, and not when a rewrite of that history removed it, and would have the step read the history of `.pr-cost/` before it stages.

## Consequences

- A session resumed in a fresh clone does not record again a call that its branch's ledger files already hold, since capture reads the hashes in those files, as git blobs within the size bound (R2, R45, T19).
- A session resumed in a fresh clone at the same path records none of the calls that answer a line written before its first run there that finds both switches on, those of a ledger file that its branch no longer holds among them, so a removal made for privacy is not undone there (R52, R153, T2). The session's other calls from before that run, which no commit took, are left out with them, and the next ledger file staged for their worktree and branch says that calls were left out for consent (DR-180).
- A file that a later commit removes stays in git history, so such a removal hides nothing that was pushed (DR-182).
- DR-055 was decided knowing of the gap that DR-056 described, as its Context says, and holds without it.

## Scope

This covers what capture reads to tell which calls are already recorded. How it identifies a call is DR-033 (A call is identified by its message id) and DR-136 (Only a hash of a call's message id is kept). Keeping out the calls of a file that a run found in a commit, within one clone, is DR-055 (Calls of a ledger file found in a commit are never staged again), and what a run that finds no store records is DR-177 (A removed store lets no earlier call be recorded, and leaves staged ledger files to git). The report reads the call ids of the default branch's first-parent history so that a call is counted once across pull requests, which is DR-131 (A call counts at most once in the default branch's history).

## What reversing it would change

R52 in `usage-capture` would change, with its scenario "A fresh clone does not stage a removed ledger file's calls again", and so would R2's scenario "A resumed session records nothing its branch already holds", R81, which names the calls that capture stages, R45, which says how capture reads ledger files from git, the design's decisions 1 and 15 and its risks "[A person removes a ledger file from their branch, or a commit that holds one is undone]" and "[A session is resumed in a fresh clone at the same path]", T2's residual, T19's answer, the README's section on adopting the tool (task 4.4) and tasks 2.1 and 2.2. DR-055 would be revisited.
