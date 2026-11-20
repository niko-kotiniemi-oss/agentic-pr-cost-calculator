# DR-110: The cost counts CI minutes as well as model tokens

- **Type:** scope
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-17
- **Requirements:** R14, R18, R20, R21, R24, R62, R63, R64, R66, R69, R94, R97, R120, R121
- **Threats:** T18, T22, T24, T26, T51
- **Replaces:** none
- **Closed by:** none

## Context

The tokens that a pull request's agent sessions spend and the CI minutes that its pushes use are recorded in different places, and nothing adds them up per pull request. A trial on real Claude Code sessions confirmed that both can be read (see the proposal's "Why"), and GitHub's jobs API gives each CI job's start and end times with the default `GITHUB_TOKEN` and `actions: read` (see the design's context).

## Decision

A pull request's cost counts the GitHub Actions minutes that its own commits used, as well as the model tokens that its agent sessions spent. The report gives the cost of each and their total.

## Alternatives

None were recorded when this was decided.

## Consequences

- Tokens are read from transcripts on the machine that runs a session, and minutes from the jobs API by the report in GitHub Actions (see `docs/how-it-works.md`).
- The calling workflow grants `actions: read` (R24; T24).
- The comment gives the CI minutes, their cost and the minutes on runners that the price table does not list, and says that the figure counts the CI runs on the pull request's commits (R20, R63, R94). The CI cost is still reported when a ledger change is refused for its size (R66).
- The price table holds GitHub Actions rates by runner (task 3.1).
- A CI cost that the report cannot read in full, within its call budget, is marked incomplete (R64; T22, T51).

## Scope

This covers which costs a pull request's figure holds. Whom the tool is for is DR-001 (The tool is for teams that build pull requests with AI coding agents), and the cost of AI review by an app or a job in CI, which the figure leaves out, is DR-004 (The cost of AI review by an app or a job in CI is left to a later change). Which runs count is DR-019 (CI minutes come from the runs on the pull request's own commits), and how a job's minutes are found is DR-038 (CI minutes come from job times, rounded up per job).

## What reversing it would change

The `ci-minutes` spec, with R18, R62, R63, R64, R120 and R121, and its feature page would go, and R20, R21, R24, R66, R69, R94 and R97 in `report-comment` would change, with R21's clause on the runner names that the comment may show and its scenario "A runner label with markup is not shown", R69's clause on the ledger files and the runs that the report cannot tell apart, and R97's clause on job names, runner labels and other text from the jobs API. R14 in `pricing` would change in its clause on pricing each CI job. So would the `pricing` spec's purpose, the design's context on the jobs API and its decision 7, `docs/how-it-works.md`, the answers of T18, T22, T24, T26 and T51, tasks 3.1, 3.3 and 7.1, the README, the proposal, `CLAUDE.md`'s opening line and `pyproject.toml`'s description. Dropping `actions: read` from the reusable workflow's permissions, which are part of the public surface, would be a breaking change for adopters (DR-096), and DR-002, DR-019, DR-038 and DR-039 would be revisited.
