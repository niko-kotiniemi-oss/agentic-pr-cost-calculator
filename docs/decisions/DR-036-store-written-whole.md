# DR-036: The store is replaced whole, under a lock

- **Type:** technical
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R11
- **Threats:** T13, T42
- **Replaces:** none
- **Closed by:** none

## Context

Claude Code runs all matching hooks in parallel, so a session's run and its subagents' runs can meet, and a run can be killed at its timeout while it writes (see the design's context; T13, T42).

## Decision

Capture changes its store only by writing a new one in place of the old, under a lock that the operating system releases when the process holding it ends.

## Alternatives

None were recorded when this was decided.

## Consequences

- A run killed in the middle of a write leaves either the old store or the new one, and no lock that would stop later runs (R11, T42).
- Runs at the same moment take turns at the store, so they neither split each other's records nor both record one call (R11, T13).

## Scope

This covers how the store is written. Where the store lives is DR-011 (Recorded calls wait in the git directory), and the version of its format, with what a run does with a version it does not know, is DR-137 (The store states its format's version). Noting a ledger file in the store before writing it belongs to DR-014 (A ledger file that no commit took is taken back).

## What reversing it would change

R11 in `usage-capture` would change, with its scenarios. The design's decision 1, the answers of T13 and T42, the usage-capture feature page and task 2.1, which builds the store, would change too, and DR-011 would be revisited.
