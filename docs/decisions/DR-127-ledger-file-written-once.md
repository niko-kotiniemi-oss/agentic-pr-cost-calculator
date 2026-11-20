# DR-127: Each commit's usage goes in a new file, written once

- **Type:** architecture
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R8, R10
- **Threats:** T4, T11, T13
- **Replaces:** none
- **Closed by:** none

## Context

Usage reaches the pull request inside the agent's own commits (DR-010), so each commit that capture stages for needs a file to carry its calls. A session and its subagents can stop at the same moment, with Claude Code running their hooks in parallel, so two runs could write one file at once, and two branches that added to one file would conflict when they merge (T13). A file's path is published with the ledger, where a branch name or a session value in it would link the record to a person or a private session (T4), and a symbolic link in a folder on that path would send the write elsewhere on the machine (T11).

## Decision

Each commit that capture stages for gets a new regular file under `.pr-cost/ledger/`, in the folder for the UTC month in which it is written, with a random name ending in `.jsonl`. Capture creates the file only where no file of that name exists, never changes it once written, and removes it whole, never edited, when no commit takes it. It writes nothing when a folder on the file's path below the repository root is a symbolic link.

## Alternatives

None were recorded when this was decided.

## Consequences

- No two runs or branches write the same file, so a merge meets no conflict in the ledger (T13).
- A file's path carries no branch name or session value (T4), and a path through a symbolic link is refused, so that the write lands nowhere else (R10, T11).
- DR-017's rule, that a pull request's usage is the ledger files its merge adds, rests on each file being written once, under a name that no other file has.

## Scope

This covers the shape of the files that carry each commit's usage. The route that they take to the pull request is DR-010 (Usage travels inside the agent's own commits), what an entry in them holds is DR-045 (Ledger entries hold counts, never content), and taking back a file that no commit took is DR-014 (A ledger file that no commit took is taken back).

## What reversing it would change

R10 in `ledger` would change, with its scenarios "A new file for every commit" and "A symbolic link in the ledger path is refused", and so would R8 in `usage-capture`, which stages a commit's calls as one new ledger file. The ledger format and the `.pr-cost/` path are part of the public surface (DR-154), so the change would be a breaking one for adopters (DR-096). The design's decisions 1 and 3, the answers of T4, T11 and T13, the ledger's row in the parts table of `docs/how-it-works.md`, the ledger's feature page, the format that task 1.2 documents and task 2.2, which writes the file, would change too, and DR-017 would be revisited.
