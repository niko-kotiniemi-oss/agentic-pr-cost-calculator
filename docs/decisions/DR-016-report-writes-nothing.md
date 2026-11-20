# DR-016: The report writes nothing to the repository

- **Type:** architecture
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the owner, 2026-10-18
- **Requirements:** R22, R24
- **Threats:** T24
- **Replaces:** none
- **Closed by:** none

## Context

Whether the report should write to the repository came up with the record: a commit that removed the ledger at the merge would have needed write access (DR-015). The report runs in the adopter's CI with the workflow's own token, and a token with wider permissions than the report needs turns any bug into a bigger one (T24).

## Decision

The report only posts its comment, so it needs no `contents: write` and no exception in a ruleset that protects the default branch. It makes no commit and pushes nothing, and apart from its job summary and its log, its one comment is all that it writes.

## Alternatives

- A commit that a workflow makes at the merge to take the ledger out of the repository, which would need write access and would add one more commit for every pull request; DR-015 (The ledger stays in the repository as the record) records it as not chosen.

## Consequences

- A bug in the report has no permission with which to change the adopter's code or history (T24).
- Whatever would need the report to write to the repository stays out while this holds, the workflow commit that DR-015 turned down among them.
- `docs/how-it-works.md` says that the report needs no `contents: write`, and so no ruleset exception, and task 4.3 has the repository's workflow tests allow the report's workflow exactly its three permissions, of which `pull-requests: write` is the only write.

## Scope

This covers whether the report writes to the repository. That the ledger stays as the record is DR-015 (The ledger stays in the repository as the record), and the permissions that the calling workflow grants are DR-063 (The calling workflow grants only what the report needs).

## What reversing it would change

R22 in `ledger` would change, with its scenario "The ledger stays after merge", which checks that the report has made no commit, and so would R24 in `report-comment`, which allows the report no permission beyond reading the repository and its Actions data and writing pull request comments, and T24's answer. The reusable workflow's permissions are part of the public surface, so a report that needed `contents: write` would be released as a new major version (DR-096). The design's decision 3, the section on credentials and permissions in `docs/how-it-works.md`, the calling workflow in the README (task 4.4), task 4.3 and the allowance it adds to `tests/test_repository.py` would change too, and DR-063 would be revisited.
