# DR-176: The store is its owner's alone, and capture leaves alone a store that it cannot trust

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-02
- **Requirements:** R152
- **Threats:** T109, T112
- **Replaces:** none
- **Closed by:** none

## Context

The store lies in the repository's git common directory, which other users of a shared machine, a backup or a sync service can read, and anything that can write the store can change what a run records, stages or removes (T109, T112). Two users can work in one repository's folder, as when a container runs a session as an administrator over a folder that the person also uses, and a folder or a file can arrive with looser modes than it was written with, from a sync or an archive. The owner asked on 2026-11-02 that the store's protection on the file system be specified.

## Decision

The store is one file for each user, in a folder of that user's own directly in the git common directory: `pr-cost-<uid>/store.json` where the system numbers users, as POSIX systems do, and `pr-cost/store.json` where it does not, so that no folder of the tool's is shared between users. Each write leaves the store's folder with mode 0700 and its file with mode 0600, whatever the umask or the modes it found: a run writes the new store to a new file that it creates itself, never through a link, syncs it to disk and renames it over the old one, and removes a new file that a killed run left. A run leaves alone a store whose file or folder is a link or, on Windows, another reparse point, is not a regular file or a folder, or, where the system numbers users, is not owned by the user that the run runs as, and records, stages, takes back and puts back nothing then, as does a run that cannot create or enter its own folder, which says so on standard error. It opens a transcript only when it is a regular file, acts on a note only for a file of the form that it writes, in the ledger folder of a worktree whose git common directory is this repository's, and checks each waiting call's entry again when it stages it, by the rules that it records by. On Windows, where a file's mode sets only its read-only flag, the step checks neither the store's access list nor its owner, so the store can have the access of the git common directory around it.

## Alternatives

- One shared `pr-cost/` folder with a folder for each user inside it, which would need a mode that lets every user in and a check of its own against a link in its place, or else one user's folder would lock the others out.
- Leaving the store to the umask, which on many systems lets every user read it.
- Encrypting the store, which would need a key kept on the same machine, readable by the same user.
- One store for every user of the repository's folder, which the check of its owner would leave unusable to all of them but the one who created it.
- Setting the modes only when the store is created, which would leave a store that arrived looser readable by others.
- Setting an access list and checking the owner on Windows through Windows' own security functions, which Python's `ctypes` can call, and which this change leaves out.

## Consequences

- On Linux and macOS, only the person and an administrator can read the store after any run has written it, whatever modes it arrived with, and each user's runs keep notes of their own.
- On Windows, a store that another user planted is not told apart by its owner (T112).
- A store that someone else planted or redirected is not followed, a note that someone rewrote can remove, stage or put back only a ledger file in a worktree of this repository (T112), and a waiting call that someone wrote into the store carries no text into a ledger file.
- A hook that a repository's own settings register can already run any command as the person, so these protections do not stop such a hook from changing the store, as T112's residual says.

## Scope

This covers who can read and change the store, and which files a note can make a run act on. What the store keeps is DR-173.

## What reversing it would change

R152 in `usage-capture` would change, with its scenarios, and so would the design's decision 15, T109, T112, the README's section on the store that task 4.4 writes, and task 2.1. A store's modes are not part of its format, so the change would not be a breaking one for adopters.
