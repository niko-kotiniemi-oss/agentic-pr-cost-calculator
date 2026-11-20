# DR-005: The report runs once, at merge

- **Type:** scope
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-17
- **Requirements:** R20, R68
- **Threats:** T23, T29
- **Replaces:** none
- **Closed by:** none

## Context

The proposal describes a tool that collects a pull request's usage while the work happens and reports it when the pull request merges (see the proposal's "Why"). A pull request's usage arrives with the agent's commits, one ledger file per commit (DR-010, DR-127), and the report counts the CI runs created on the pull request's own commits before it merged (DR-019).

## Decision

The report runs when a pull request merges, and that is when the pull request gets its one comment. No cost is reported while a pull request is open.

## Alternatives

None were recorded when this was decided.

## Consequences

- When the report runs again for the same merge, it updates its comment and posts no second one (R96).
- The report refuses every event but the push that a merge makes to the default branch (R68). So it runs only after a pull request has been merged, whatever started the workflow that calls it, and a calling workflow that runs it for a pull request's own events, such as `pull_request_target`, gets no comment and a failed job (T23, T29).

## Scope

This covers when a pull request's cost is reported. Which event the report runs on, and why, is DR-018 (The report runs on the push that a merge makes to the default branch), and how the report checks that event itself is DR-061 (The report runs only for a push to the default branch).

## What reversing it would change

R20 and R68 in `report-comment` would change, R68 with its scenario "Another event is refused", and so would the design's non-goals and decision 7, the proposal's "What Changes" and "Impact", the answers of T23 and T29, the README's list of what the tool will do, the report comment's feature page and the flow "A merge and its report" in `docs/how-it-works.md`. Tasks 4.3 and 4.4 would change too: the reusable workflow, which refuses every other event, and the calling workflow that the README's section on adopting the tool gives. DR-018 and DR-061 would be revisited. Added behaviour alone would raise the minor number, while a change to the public surface, such as the reusable workflow's inputs or permissions, would be a breaking one for adopters (DR-096).
