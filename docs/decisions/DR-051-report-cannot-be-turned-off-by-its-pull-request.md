# DR-051: A pull request cannot turn off its own report

- **Type:** security and privacy
- **Boundary:** incoming
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R19, R92
- **Threats:** T21, T49
- **Replaces:** none
- **Closed by:** none

## Context

A pull request can change the configuration file, and its merge is then reported by what it changed, so it could turn the tool off to go unreported (T21). The design's goals count the pull request being reported among the untrusted inputs. A report that stopped on a configuration file made unreadable would post nothing, not even the notice that the pull request changed its report (T49).

## Decision

The report reads `.pr-cost.json` at the default branch's commit before the merge and at the commit after it, and runs when either turns the tool on. At either commit, a file that is not there, or cannot be read as a valid configuration within its size bound, counts as leaving the tool off, and does not stop the report.

## Alternatives

- Reading the configuration after the merge only, which would let a pull request turn off its own report.

## Consequences

- The pull request that turns the tool off gets its report, as do the one that turns it on and one that makes the file unreadable when the file before the merge turned the tool on, while a merge with the tool off on both sides gets none (R19, R92).
- A pull request can still change the calling workflow itself. It can remove it, so that its own merge goes unreported, or pin a different version of the tool. Either is in its diff for review, and a pull request that changes the workflow and still gets a report has that change flagged. This is T21's residual.

## Scope

This covers where the report reads the configuration, at the default branch's commits before and after the merge, and when it runs, given what it finds there. The file itself is DR-021 (One file, `.pr-cost.json`, turns the tool on or off), the flags on a changed configuration or workflow are DR-064 (The report flags changes to the switch, the hook and the workflows), and the push that the report runs for is DR-018 (The report runs on the push that a merge makes to the default branch).

## What reversing it would change

R19 and R92 in `switch-and-opt-in` would change, with their scenarios. So would the design's decisions 6 and 7 where the report reads the file at both commits, the answers of T21 and T49, the proposal, the `switch-and-opt-in` feature page, the merge flow in `docs/how-it-works.md`, and task 4.1. DR-064 would be revisited, since a pull request that makes the file unreadable gets its flag only in a report that this record keeps running.
