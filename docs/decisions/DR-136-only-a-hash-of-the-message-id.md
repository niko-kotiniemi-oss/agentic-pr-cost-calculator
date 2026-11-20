# DR-136: Only a hash of a call's message id is kept

- **Type:** security and privacy
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R2, R4
- **Threats:** T4, T43
- **Replaces:** none
- **Closed by:** none

## Context

Calls are told apart by their message ids, and capture and the report learn which calls the ledger files already hold from what each entry carries of its call's id (DR-033). The ledger is public, and a raw identifier from the transcript would link a public entry to a session or a person (T4).

## Decision

Capture keeps only the SHA-256 hash of a call's message id, never the id itself: the hash is what it records with the call, and what the call's ledger entry carries.

## Alternatives

None were recorded when this was decided.

## Consequences

- Whoever holds the original message ids, as the session's owner does, can still match entries to calls (T4).
- A hash can look like a secret to a scanner in the repository's own git hooks, so its field's name ends in `_id`, which detect-secrets' default filters read as an identifier, and task 1.2 checks a ledger file against that scanner. Scanners with other rules may still flag the file (the design's risk "[A repository's own git hooks see the staged ledger file]"; T43).

## Scope

This covers what capture keeps of a call's message id. That calls are told apart by that id is DR-033 (A call is identified by its message id), and what else an entry may hold is DR-045 (Ledger entries hold counts, never content) and DR-053 (An entry records no session value).

## What reversing it would change

R2 in `usage-capture`, whose record holds the hash, and R4 in `ledger`, which lets an entry take no text from a transcript but the model's name and the price attributes' values, would change, with R4's scenario "A planted string never reaches the ledger", and so would the ledger format, whose entries carry the hash. The ledger format is part of the public surface, so the change would be a breaking one for adopters (DR-096). The design's decision 1 and the risk named above, the answers of T4 and T43, the outputs and the capture flow in `docs/how-it-works.md`, the usage-capture and ledger feature pages, `SECURITY.md`, which lists a hash of the call's message id among what the tool records, and tasks 1.2 and 2.1 would change too, and DR-045 and DR-053 would be revisited.
