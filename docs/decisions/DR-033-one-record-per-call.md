# DR-033: A call is identified by its message id

- **Type:** technical
- **Boundary:** incoming
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R2, R41
- **Threats:** T7
- **Replaces:** none
- **Closed by:** none

## Context

One call can be written over several transcript lines and can appear in more than one transcript, and capture runs again and again over the same transcript (see the design's context; T7).

## Decision

Capture identifies each call by its message id, so that a call written over several lines, read by two runs or found in two transcripts is recorded once.

## Alternatives

None were recorded when this was decided.

## Consequences

- Each ledger entry carries its call's id, as a hash (DR-136), so that capture, in a fresh clone too, and the report can tell which calls the ledger files already hold (R2; DR-056, DR-131).

## Scope

This covers how capture tells calls apart. Which calls count as already recorded, from the store and the ledger files that the branch holds, is DR-056 (Capture does not read the branch's history), and what capture keeps of the id is DR-136 (Only a hash of a call's message id is kept). Counting each call at most once in the report is DR-131 (A call counts at most once in the default branch's history), and never staging again the calls of a file found in a commit is DR-055 (Calls of a ledger file found in a commit are never staged again).

## What reversing it would change

R41 in `usage-capture` would change, with its scenarios, and so would R2 there, whose record holds a hash of the message id, and the ledger format, whose entries carry that hash. The ledger format is part of the public surface, so the change would be a breaking one for adopters (DR-096). The design's decision 1, T7's answer, the outputs and the capture flow in `docs/how-it-works.md`, the usage-capture feature page, and tasks 1.2 and 2.1 would change too, and DR-055, DR-056, DR-131 and DR-136, which rely on the id, would be revisited.
