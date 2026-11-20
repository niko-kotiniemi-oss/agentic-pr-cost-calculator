# DR-081: Outside pull requests are reviewed from `main`

- **Type:** process
- **Boundary:** incoming
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** none
- **Threats:** T34
- **Replaces:** none
- **Closed by:** none

## Context

A session started on an unmerged branch takes its `CLAUDE.md`, skills and session hooks from that branch, and the hooks run with credentials that can push here. A checkout of the branch has the same effect once `/clear` or a compaction reruns the session-start hooks from the working tree (T34).

## Decision

When someone outside the project opens a pull request, it is reviewed from `main`, and its diff is read as data. No session runs on an unmerged branch that an outside contributor wrote, or checks such a branch out.

## Alternatives

None were recorded when this was decided.

## Consequences

- The session that reviews an outside pull request runs `main`'s instructions and hooks, never the contributor's, and treats the contributor's text as data (DR-082).
- Nothing but the rule holds this (T34's residual).

## Scope

This covers which branch a session in this repository works on when an outside contributor's work is involved. Sessions on dependency-update branches are DR-145 (A session starts on a dependency-update branch only after the owner reviews its diff). In an adopting repository, the same danger from a checked-out branch is T59, which the hook's checksum answers: DR-058 (The hook file runs only when its checksum matches). Reading such text as data is DR-082 (Records and issue text are data, never instructions).

## What reversing it would change

The section "Outside contributions" of `CLAUDE.md` would change, with T34's answer. DR-082 and DR-115 would be revisited. No requirement and no part of the public surface is involved.
