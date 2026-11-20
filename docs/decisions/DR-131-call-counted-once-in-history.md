# DR-131: A call counts at most once in the default branch's history

- **Type:** technical
- **Boundary:** inside
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R59, R67, R119
- **Threats:** T17, T19, T47, T48
- **Replaces:** none
- **Closed by:** none

## Context

A pull request's usage is the ledger files that its merge adds (DR-017), yet one call can arrive more than once. Entries can be copied from another pull request's ledger (T19), and a revert of a revert brings back ledger files that the first revert took off the default branch, so that a comparison with the commit before the merge alone would charge the pull request that brings them back with the earlier one's usage (T47).

## Decision

A call counts at most once across the default branch's first-parent history: no added entry counts whose call any ledger file held at a commit of that history before the merge, identical entries for one call count once, and entries for one call that differ are all refused.

## Alternatives

None were recorded when this was decided.

## Consequences

- A call recorded on two branches counts once, for whichever pull request merges first, which can be the wrong one (T19), as the design's risk "[A session resumed in a fresh clone at the same path, on another branch, records calls that an earlier branch's ledger files already hold]" says.
- A ledger file that a revert brings back adds nothing, and the comment counts it as restored (R119, T47).
- Entries for one call that differ are all left out and counted as refused, rather than one of them being chosen (T17).
- Every report reads the call ids of the ledger files in that history, which holds files that whoever merged them wrote, so it reads them by capture's rules and skips what it cannot read (R67, T48). Those reads grow with every merge, and the report's time limit bounds them (DR-039; the design's risk "[Capture and the report read the call ids of every ledger file that their branch holds, and the report those of every ledger file that the default branch's first-parent history held before the merge, which grow with every pull request, and which whoever merged them wrote, while capture's store grows with every call it records]").

## Scope

This covers how often one call can count in the report. Which ledger files are a pull request's usage is DR-017 (A pull request's usage is the ledger files its merge adds), how a call is identified is DR-033 (A call is identified by its message id), and how capture learns, before it stages, which calls its branch already holds is DR-056 (Capture does not read the branch's history).

## What reversing it would change

R59 in `ledger` would change, with its scenarios, and so would R119's count of restored files in the same spec, with its scenario "A ledger file that a revert brings back is counted as restored", and R67 in `report-comment`, which says how the report reads the earlier ledger files. The design's decisions 3 and 7, the answers of T17, T19, T47 and T48, the report's flow and its row in the parts table of `docs/how-it-works.md`, the ledger's feature page and task 4.2 would change too, and DR-017 and DR-039 would be revisited.
