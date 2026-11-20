# DR-092: The hook and the report are tested end to end

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-18
- **Requirements:** none
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

The hook and the report meet only through git: the hook's ledger files travel in the agent's commits, and the report reads them on the push that a merge makes to the default branch (DR-010, DR-018).

## Decision

**End to end:** the hook runs against fixture transcripts in a temporary git repository, and the report runs against a temporary repository and recorded API responses (task 4.5).

## Alternatives

None were recorded when this was decided.

## Consequences

- The end-to-end test measures how long capture and the report take to read the ledger files, the store and the history, as the design's risk "[Capture and the report read the call ids of every ledger file that their branch holds, and the report those of every ledger file that the default branch's first-parent history held before the merge, which grow with every pull request, and which whoever merged them wrote, while capture's store grows with every call it records]" says.

## Scope

This covers the tests of the whole flow. The tests of each scenario are DR-084 (Acceptance tests come first), and the recorded responses that stand in for GitHub's API are DR-090 (No test uses the network). Turning the tool on in this repository, so that the merge of `add-pr-cost-calculator` is reported, is DR-147 (The tool is turned on in its own repository).

## What reversing it would change

No requirement would change. The design's decision 8, which names this record, and its risk on how long the reads take, which has the reads measured in the end-to-end test, would change, and so would T42's residual, which rests on that measurement, task 4.5, which writes the end-to-end tests, `CLAUDE.md`'s section on testing and the feature pages' sections on validation, which cite this record among the testing records.
