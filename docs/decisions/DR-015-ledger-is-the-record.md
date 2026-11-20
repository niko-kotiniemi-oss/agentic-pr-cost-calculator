# DR-015: The ledger stays in the repository as the record

- **Type:** architecture
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the owner, 2026-10-18
- **Requirements:** R22
- **Threats:** T20
- **Replaces:** none
- **Closed by:** none

## Context

The ledger files reach the pull request inside the agent's own commits (DR-010), so the merge brings them to the default branch with the rest of its changes. The question was whether a repository could also turn that record off. Using the tool means the pull request is tracked; not tracking it means not turning the tool on. Supporting both inside the tool adds complexity for no gain.

## Decision

The ledger reaches the default branch with the merge and stays there. It is the pull request's record, and the cost can be recomputed from it with the price table. No setting turns the record off, and no commit removes it at the merge.

## Alternatives

- A record file that could be turned off, with a workflow commit removing the ledger at merge, which needs write access and adds a commit to every pull request.

## Consequences

- Nothing is removed at the merge, so the report needs no write access to the repository (DR-016).
- Each branch made from the default branch carries the ledger files of every pull request merged before it, so what capture reads of its branch's ledger grows with each merge. The design's risk "[Capture and the report read the call ids of every ledger file that their branch holds, and the report those of every ledger file that the default branch's first-parent history held before the merge, which grow with every pull request, and which whoever merged them wrote, while capture's store grows with every call it records]" bounds those reads and leaves their time to what the end-to-end test measures.
- A later pull request can remove or change earlier ledger files (T20). The comment, or for a push that gets no comment the job summary, then says how many, none of their entries counts (R119, R60), and git history keeps the files as they were.

## Scope

This covers whether the ledger stays on the default branch after the merge. How it gets there is DR-010 (Usage travels inside the agent's own commits), that the report writes nothing is DR-016 (The report writes nothing to the repository), and which ledger files count is DR-017 (A pull request's usage is the ledger files its merge adds).

## What reversing it would change

R22 in `ledger` would change, with its scenario "The ledger stays after merge", and so would the spec's purpose, which calls the files the pull request's record. T20, whose premise is that the default branch keeps that record, would be revisited, with R60 and R119, which answer it. A setting that turned the record off would be something that adopters configure, which is public surface (DR-154), so it would be released as a new major version (DR-096). The design's decision 3, the ledger's feature page, `docs/how-it-works.md`, the README and the proposal, which each say that the ledger stays as the record, would change too, and DR-016 would be closed, since a commit that removed the ledger would need write access.
