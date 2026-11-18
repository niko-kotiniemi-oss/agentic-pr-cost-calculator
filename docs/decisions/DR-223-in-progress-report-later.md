# DR-223: A report that shows a pull request as still in progress is left to a change after the first build

- **Type:** scope
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-09
- **Requirements:** R206, R207
- **Threats:** T161
- **Replaces:** none
- **Closed by:** none

## Context

The report runs once, on the push that a merge makes to the default branch, and no cost is reported while a pull request is open (DR-005, DR-018). On 2026-11-09 the owner asked that the tool say whether a pull request was merged and, when it is run before the pull request is finished, show it as still in progress. A report that runs before a merge meets events that the report refuses today, such as `pull_request`, whose code a pull request can change (T23, T29).

## Decision

A report run before a pull request merges, which shows it as still in progress, is left to a change of its own after the first build, with its own spec and threat review, which may join the change that brings the command of DR-222. The roadmap lists it under Next as planned. The first version reports only at merge, as DR-005 says.

## Alternatives

- Building it in the first version, which would widen the events that the report accepts before its threat review.
- Leaving it off the roadmap, which would drop the owner's ask.

## Consequences

- DR-005 and DR-018 hold for the first version.
- The later change decides how a report before merge runs without running code that the pull request changes, and is reviewed against T23 and T29.

## Scope

This covers when a report before merge comes. When the report runs is DR-005 (The report runs once, at merge) and DR-018 (The report runs on the push that a merge makes to the default branch).

## What reversing it would change

The roadmap's Next and design decision 12 would change, and building it would close DR-005 with a record that restates what still holds.
