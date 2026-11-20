# DR-052: An entry records the UTC day of a call, not its time

- **Type:** security and privacy
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R2, R4
- **Threats:** T5
- **Replaces:** none
- **Closed by:** none

## Context

A cost uses the latest price whose effective date is on or before the UTC day of the usage (R14, DR-020), so pricing needs nothing finer than the day. The ledger is published in a repository that anyone can read, and a time on every model call would show, call by call, when a contributor's agent was at work (T5).

## Decision

Each ledger entry gives the UTC date of its call and no time of day.

## Alternatives

None were recorded when this was decided.

## Consequences

- The ledger adds nothing finer than the day to what commit times in git already show of when someone worked, which T5's residual accepts.
- The day is taken in UTC, so it can differ from the local date of the call, as R2's scenario "An entry records the UTC day, not the time" shows.

## Scope

This covers what an entry says about when its call was made. The capture step still reads each call's transcript time on the machine, to tell whether the call fell inside an interval when both switches were on (DR-047), and writes it into no entry. Which other values an entry holds is DR-045 (Ledger entries hold counts, never content), DR-053 (An entry records no session value) and DR-138 (An entry records whether the main agent or a subagent made its call).

## What reversing it would change

R2 in `usage-capture`, with its scenario "An entry records the UTC day, not the time", and R4 in `ledger` would change, and so would the ledger format that task 1.2 documents, T5's answer, the proposal's "What Changes", which lists the UTC day among what capture records, the design's decision 1, `docs/how-it-works.md`, the `ledger` and `usage-capture` feature pages, `SECURITY.md`, which lists the UTC day among what the tool records, and task 2.1. The ledger format is part of the public surface, so the change would be a breaking one for adopters (DR-096), and a newer report would go on reading the earlier format (DR-040).
