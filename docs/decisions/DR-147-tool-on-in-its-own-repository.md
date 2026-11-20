# DR-147: The tool is turned on in its own repository

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** none
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

Among the design's goals, every figure in a report can be recomputed from the ledger, the price table and the jobs API. The tests run the hook and the report end to end on fixtures and temporary repositories (DR-092), and they meet GitHub's API only through recorded responses (DR-090). The repository is public, and holds no transcripts, session identifiers or cost figures from someone's private work (DR-069).

## Decision

The tool is turned on in this repository, with the owner's own opt-in set outside it, so that the merge of `add-pr-cost-calculator` is reported by the tool itself (task 7.1). The report that this merge posts is checked against its ledger, the price table and the jobs API, and its CI minutes against the runs that GitHub lists for the pull request's own commits.

## Alternatives

None were recorded when this was decided.

## Consequences

- Task 7.1 is the last task of `tasks.md`, and its check can only follow the owner's merge, since the report runs on the push that the merge makes (DR-018).
- From then on the repository holds ledger files of its own, which `CLAUDE.md` names as the only real usage records it may hold (DR-069).
- The repository's own merges cannot check the assumption about runs that a merge starts through another event, since none of its workflows runs on one (see the threat model's assumptions).

## Scope

This covers turning the tool on in this repository and checking the report on the merge of `add-pr-cost-calculator`. The end-to-end tests on fixtures, temporary repositories and recorded responses are DR-092 (The hook and the report are tested end to end), and what the public repository may hold is DR-069 (The public repository holds no private data).

## What reversing it would change

No requirement would change. Task 7.1, the proposal's condition for success that names this merge's report and its row for `report-comment` in the section on how the outcome is validated, the section on validation of the feature page for `report-comment`, and `CLAUDE.md`'s section on privacy, which names task 7.1, would change, and so would T34's account of what could happen, which names the tool turned on here, and the threat model's assumption on runs that a merge starts through another event, which says that this repository's own merges cannot check it. DR-069, which allows the repository no real usage records but the ledger files that task 7.1 brings, would be revisited.
