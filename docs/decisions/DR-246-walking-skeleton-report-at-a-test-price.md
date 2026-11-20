# DR-246: The walking skeleton's report prices at a fixed test price and posts to the job summary and one comment

- **Type:** architecture
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-11-14
- **Requirements:** R237, R241
- **Threats:** T187, T191
- **Replaces:** none
- **Closed by:** none

## Context

The second choice of the plan that the owner approved on 2026-11-14 was how far the skeleton's report goes. The report that the design specifies prices each day's tokens from a dated price table, counts CI minutes from the jobs API and keeps one comment up to date (`report-comment`, `pricing`, `ci-minutes`). The skeleton exists to meet the assumptions about Claude Code's transcripts and hooks, and the path to the report's figure needs only a price.

## Decision

The skeleton's report compares the push's `before` and `after` commits and, only when GitHub's API gives exactly one merged pull request for the push, reads the ledger files that the push added, counts each call's key once, sums the tokens of each model, multiplies them by a fixed test price that `skeleton/` holds and names as a test price, and writes the figure, saying that it is at a test price and not a real cost, to the job summary and as one comment on the pull request; otherwise it posts no comment and says why in the job summary (R241). It counts no CI minutes and reads no real price. Its workflow, `skeleton/workflow.yml`, runs only on a push to `main`, asks only to read contents and to write pull requests, uses no action but `actions/checkout`, pinned to a full commit and keeping no credentials, fetches only the push's two commits, reads no secret, puts no expression inside a command and sets a time limit (R237).

## Alternatives

- Real prices from the dated price table: the price table does not exist yet, and a real price adds nothing to what the run is for.
- The figure in the job summary only: it would leave untested the step that posts to the pull request, which the build needs.

## Consequences

- The comment shows a figure that is not a real cost, and says so (R241).
- The workflow and the report run as the scratch repository's `main` holds them, so the run checks that the skeleton's files there are those of the commit that it names (T192).
- CI minutes, real prices and the comment's full form stay with tasks 3.1 to 4.4 of the build.

## Scope

This covers what the skeleton's report computes and where it posts. What the tool's report does is the `report-comment` spec.

## What reversing it would change

How hard it is to reverse: reversible. The test price and the workflow are files under `skeleton/`, which one pull request can change. R237 and R241 in `project-standards` would change, with their scenarios, and so would design decision 18, task 1.33 and the answers of T187 and T191.
