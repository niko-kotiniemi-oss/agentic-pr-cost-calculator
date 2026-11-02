# DR-176: The store is its owner's alone, and capture leaves alone a store that it cannot trust

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-02
- **Requirements:** R152
- **Threats:** T109, T112
- **Replaces:** none
- **Closed by:** none

## Context

The store lies in the repository's git common directory, which other users of a shared machine, a backup or a sync service can read, and anything that can write the store can change what a run records, stages or removes (T109, T112). The owner asked on 2026-11-02 that the store's protection on the file system be specified.

## Decision

The capture step creates the store's folder with mode 0700 and its file with mode 0600, whatever the umask, never through a symbolic link. It leaves alone a store whose file or folder is a symbolic link, is not a regular file or a folder, or is not owned by the user that the run runs as, and records, stages, takes back and puts back nothing then. It acts on a note only for a file in the ledger folder of a worktree whose git common directory is this repository's. On Windows, where Python's standard library cannot set an access list, the store has the access of the git common directory around it.

## Alternatives

- Leaving the store to the umask, which on many systems lets every user read it.
- Encrypting the store, which would need a key kept on the same machine, readable by the same user.

## Consequences

- On Linux and macOS, only the person and an administrator can read the store.
- A store that someone else planted or redirected is not followed, and a note that someone rewrote can remove, stage or put back only a ledger file in a worktree of this repository (T112).
- A hook that a repository's own settings register can already run any command as the person, so these protections do not stop such a hook from changing the store, as T112's residual says.

## Scope

This covers who can read and change the store, and which files a note can make a run act on. What the store keeps is DR-173.

## What reversing it would change

R152 in `usage-capture` would change, with its scenarios, and so would the design's decision 15, T109, T112, the README's section on the store that task 4.4 writes, and task 2.1. A store's modes are not part of its format, so the change would not be a breaking one for adopters.
