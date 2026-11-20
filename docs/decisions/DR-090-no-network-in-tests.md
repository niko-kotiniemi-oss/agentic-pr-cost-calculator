# DR-090: No test uses the network

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

The report's CI figures come from GitHub's API, and what it finds there depends on how the pull request merged (see the design's decision 7). The hook opens no network connection at all, and the report connects only to GitHub: to the host that `GITHUB_API_URL` names and, by git, to the tool's own repository and the repository it reports on (R30).

## Decision

**No test uses the network.** A test that opens a connection fails, and recorded responses stand in for GitHub's API.

## Alternatives

None were recorded when this was decided.

## Consequences

- Task 1.6 adds the network guard, verified by a test that opens a connection, and task 1.13 gives it two rules from R30: the hook connects nowhere, and the report only to that host, over HTTPS.
- The report's tests run against recorded responses for each way a pull request can merge (task 3.3), as the vendoring script's tests run against a local upstream (`tests/test_vendor_sync.py`).
- The guard watches the Python process, so it does not see a connection that a git subprocess makes (T45). Capture keeps its git commands offline through their environment instead (R111), and task 1.13 checks that the report's git commands, other than the checkout of its own code, reach no remote but that of the repository it reports on.
- The report meets GitHub's real API only outside the tests, as on the merge of `add-pr-cost-calculator` (DR-147).

## Scope

This covers the tests. CI itself connects to install the development tools and to compare the vendored copy of Superpowers with upstream, as `docs/how-it-works.md` lists, and none of those connections is made by a test (DR-041).

## What reversing it would change

No requirement would change. The design's decision 8, tasks 1.6, 1.13 and 3.3, `CLAUDE.md`'s section on testing, the proposal's section on how the outcome is validated, with its row for `ci-minutes`, and the section on validation of the feature page for `ci-minutes` would change. DR-092, whose end-to-end run of the report uses recorded responses, would be revisited.
