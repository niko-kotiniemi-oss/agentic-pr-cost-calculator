# DR-017: A pull request's usage is the ledger files its merge adds

- **Type:** architecture
- **Boundary:** inside
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R58, R119
- **Threats:** T19, T20, T22
- **Replaces:** none
- **Closed by:** none

## Context

The default branch keeps every merged pull request's ledger files (DR-015), and each ledger file is written once, under a random name (R10, DR-127). A branch name used again still carries the ledger files of the pull request merged from it before (T19).

## Decision

A pull request's usage is the entries of the ledger files that its merge adds: files in the ledger folder that the default branch holds after the merge and did not hold before it, which the report finds in git by comparing the commit before the push with the one after it.

## Alternatives

- GitHub's lists of a pull request's files and commits, which return at most 3000 files and 250 commits. Built on them, the report would miss the rest of a larger pull request (T22).

## Consequences

- Earlier ledger files that the pull request removes or changes are not its usage: none of their entries counts, and the comment says how many there were (R119, T20).

## Scope

This covers which ledger entries are a pull request's usage. How often one call can count is DR-131 (A call counts at most once in the default branch's history), which CI runs count is DR-019 (CI minutes come from the runs on the pull request's own commits), and a ledger edited by hand is DR-066 (A ledger edited by hand is an accepted risk).

## What reversing it would change

R58 in `ledger` would change, with its scenario "A reused branch name is not double-counted", and so would R119 in `ledger`, on the earlier ledger files that a pull request removes or changes. The design's decisions 3 and 7, the answers of T19, T20 and T22, task 4.2, the ledger's feature page and the report's flow in `docs/how-it-works.md` would change too, and DR-131 would be revisited.
