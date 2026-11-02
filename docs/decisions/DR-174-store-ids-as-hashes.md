# DR-174: The store keeps ids as hashes, and plain paths only while a ledger file needs them

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-02
- **Requirements:** R149
- **Threats:** T4, T10, T109
- **Replaces:** none
- **Closed by:** none

## Context

Capture keeps operational metadata only where it needs it (DR-173). For most of what the store notes, a run needs only to tell whether two values are equal: whether a call belongs to a session, a transcript, a worktree or a branch, and whether a command is the one that a ledger file was staged for. A take-back, though, has to run git in the worktree of the file that it takes back, and read that session's transcript to tell that its command is over (DR-014).

## Decision

The store keeps a session's id, a transcript's path, a worktree, a branch and a `tool_use_id` as the SHA-256 hash of the value alone, never the value. It knows a worktree by the worktree's folder in the git common directory, which `git worktree move` keeps, and the main worktree, which has no such folder and which `git worktree move` does not move, as the main one. The only plain values that it keeps are, in the note of a staged or taken-back ledger file, the file's path in its worktree, the worktree's name, which is the name of that folder and leads git to the worktree, and, for a staged file, its transcript's path, and they go when the note does.

## Alternatives

- Keeping every value in plain text, which keeps more than a run needs.
- A keyed hash, with its key kept beside the store, which would hide nothing from whoever can read the store, since the key would be readable there too.
- Knowing a worktree by its path, which a move of the worktree leaves naming nothing, so that its waiting calls would never match and a staged file's note would leave the file stranded.

## Consequences

- A hash is not anonymity: whoever holds a value can compute its hash and find it in the store, so none of these values, plain or hashed, reaches a ledger file (R4).
- The transcript's path in a staged file's note carries the session's id and the person's home folder, so while a ledger file is staged the store holds the session's id in plain there (T109).
- A store that someone else reads while no ledger file is staged shows no session's id, path, worktree or branch in plain text, though it shows how many sessions and calls it notes, and when its runs came (T109).
- The calls and notes of a worktree that is moved still find it, and a worktree's name, which git takes from the name of the worktree's folder, can say what the worktree is for.

## Scope

This covers the form in which the store keeps identifiers. What it keeps is DR-173 and the design's decision 15, and the hash of a call's message id that an entry holds is DR-136 (Only a hash of a call's message id is kept).

## What reversing it would change

R149 in `usage-capture` would change, with its scenarios, and so would the design's decision 15, T4's residual, T109 and task 2.1. The store's format is part of the public surface, so the change would be a breaking one for adopters (DR-096).
