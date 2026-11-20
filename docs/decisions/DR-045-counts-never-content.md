# DR-045: Ledger entries hold counts, never content

- **Type:** security and privacy
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R4
- **Threats:** T1, T4, T31
- **Replaces:** none
- **Closed by:** none

## Context

The ledger is committed with the pull request and stays in the repository as the record (DR-015), so in a public repository anyone can read it. It is built from transcripts, which hold prompts, code, tool output, web pages and possibly secrets (see the threat model's first trust boundary). Pricing a call needs only its counts, model, price attributes and UTC day, and splitting the cost needs its activity type (see `docs/how-it-works.md`).

## Decision

A ledger entry holds counts, never content. The only text that it takes from a transcript is the model's name and the values of the price attributes.

## Alternatives

None were recorded when this was decided.

## Consequences

- No prompt, response, code, file contents, tool name, path, branch name, user name, session identifier or time of day reaches an entry, and a ledger file's name is random, so neither an entry nor a file's path ties the ledger to a person or a session (R4, T1, T4). A property test with planted markers holds this (task 2.1).
- Model names and attribute values are still text, so the hook records them only when its price table lists them, and anything else as `unknown` (DR-054).
- What the ledger does hold is public in a public repository: which models were used, how many tokens, and on which days (T31).

## Scope

This covers what a ledger entry may hold. Which names it records is DR-054 (Names the price table does not list are recorded as `unknown`), that it records the day and not the time is DR-052 (An entry records the UTC day of a call, not its time), that it records no session value is DR-053 (An entry records no session value), and how tool names are used without being recorded is DR-029 (Activity types come from tool names, which are never recorded).

## What reversing it would change

R4 in `ledger` would change, with its scenarios "Content in the transcript does not reach the ledger" and "A planted string never reaches the ledger", and so would the design's goals, the answers of T1 and T4, T31's account of what is published, the ledger format that task 1.2 documents, the property tests of task 2.1, the ledger feature page, the list of what the tool never does in `docs/how-it-works.md`, and `SECURITY.md`, which counts a change that breaks this as a security issue. DR-029, DR-052, DR-053 and DR-054 would be revisited. The ledger format is part of the public surface, so the change would be a breaking one for adopters (DR-096).
