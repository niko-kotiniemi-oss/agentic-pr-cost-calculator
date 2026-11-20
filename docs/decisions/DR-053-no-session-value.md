# DR-053: An entry records no session value

- **Type:** security and privacy
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R2, R4
- **Threats:** T4
- **Replaces:** none
- **Closed by:** none

## Context

A transcript carries session ids and request ids, as well as the working directory, user names inside paths and the branch, and any of them in a public ledger would link it to a person or to a private session (T4). A call is told apart from every other by a SHA-256 hash of its message id (DR-033, DR-136), which keeps it from being recorded twice without any session value.

## Decision

An entry holds no session value, such as the session's identifier.

## Alternatives

None were recorded when this was decided.

## Consequences

- Whoever holds the original message ids, such as the session's owner, can still match them to entries through the hash that DR-136 keeps, which T4's residual accepts, since that is the person the data came from.
- The comment can give the cost by model, by token type and by activity type (R20), but nothing in the ledger lets it split the cost by session.

## Scope

This covers whether an entry keeps a session value. The store keeps each staged file's session id and transcript path, but it stays in the git directory and is never committed (DR-011). Whether the main agent or a subagent made an entry's call is DR-138 (An entry records whether the main agent or a subagent made its call), the rest of an entry's contents is DR-045 (Ledger entries hold counts, never content), its time is DR-052 (An entry records the UTC day of a call, not its time), and how calls are told apart, by a hash of their message ids, is DR-033 (A call is identified by its message id) and DR-136 (Only a hash of a call's message id is kept).

## What reversing it would change

R2 in `usage-capture`, whose list of what an entry holds has no session value, and R4 in `ledger`, which names the session identifier among what an entry never holds, would change, and so would the ledger format that task 1.2 documents, T4's answer, the design's decision 1, `docs/how-it-works.md`, the `ledger` and `usage-capture` feature pages, and `SECURITY.md`, which says that the tool never records any session identifier. The ledger format is part of the public surface, so the change would be a breaking one for adopters (DR-096).
