# DR-133: A push gets a comment only when all its commits belong to one pull request

- **Type:** technical
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R60, R69
- **Threats:** T19, T20
- **Replaces:** none
- **Closed by:** none

## Context

The report runs on the push that a merge makes to the default branch (DR-018), and a push names commits, not a pull request. One push can merge several pull requests, as a merge queue can, or add a commit that belongs to no pull request, alone or beside a merge, and charging such a push to one pull request would give it the ledger files and runs of others (T19). For a commit that the default branch holds, GitHub's "List pull requests associated with a commit" gives the merged pull request that introduced it (see the design's context).

## Decision

The report looks up the pull request of each commit that the push adds to the default branch's first-parent history, and posts its comment only when all of those commits belong to one pull request. A push that merges no pull request, merges more than one, or adds commits of no pull request beside a merge gets no comment, and the report's job summary says which of these it was.

## Alternatives

None were recorded when this was decided.

## Consequences

- Pull requests that one push merges together get no report, since the report cannot tell which ledger files and runs belong to which (R69).
- Because the job summary says why, a push without a comment can be told from a report that did not run, and when such a push removes or changes ledger files that the default branch held, the job summary gives how many (R60, T20).
- The rule rests on that lookup behaving as documented, which the threat model states as an assumption (T19).
- The lookups draw on the report's call budget, so a push with more commits than the budget lets the report look up gets no comment either, and its job summary says so (DR-039).

## Scope

This covers which push gets a comment, and what the job summary says when one gets none. That the report runs on the push is DR-018 (The report runs on the push that a merge makes to the default branch), and its call budget is DR-039 (The report keeps to a call budget and a time limit). Which ledger files count once the pull request is known is DR-017 (A pull request's usage is the ledger files its merge adds), and which runs count is DR-019 (CI minutes come from the runs on the pull request's own commits).

## What reversing it would change

R69 in `report-comment` and R60 in `ledger` would change, with their scenarios. So would the design's decision 7 where it looks up each commit's pull request, the threat model's assumption about that lookup, the answers of T19 and T20, task 4.1, the `report-comment` and `ledger` feature pages, and the merge flow in `docs/how-it-works.md`. Neither the comment nor the job summary is part of the public surface, so the change would not be a breaking one for adopters. DR-017 and DR-019, which rest on knowing the one pull request that a push merged, would be revisited.
