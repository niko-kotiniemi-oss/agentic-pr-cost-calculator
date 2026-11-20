# DR-039: The report keeps to a call budget and a time limit

- **Type:** technical
- **Boundary:** incoming
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R64, R70
- **Threats:** T51
- **Replaces:** none
- **Closed by:** none

## Context

How many calls the report makes to GitHub's API depends on what the pull request's author controls: it looks up the pull request of each commit that the push adds, and lists the runs and every job attempt on each of the pull request's own commits. The requests that `GITHUB_TOKEN` can make in an hour are capped for the repository as a whole, a limit that every workflow there draws on, and GitHub cuts a filtered runs listing short (see the design's context). A pull request with enough commits could use up the shared limit, so that other workflows' calls fail, and a job without a time limit could run on (T51).

## Decision

The report spends no more calls on GitHub's API than the call budget that the README states, and `timeout-minutes` sets a time limit on its job. A push that the report cannot match to its pull request within the budget gets no comment, only a job summary that gives the reason (R70), and a pull request whose runs and jobs the budget cannot cover gets its comment with the CI cost marked incomplete (R64).

## Alternatives

None were recorded when this was decided.

## Consequences

- One report cannot use up the requests that the repository's other workflows need, as the design's risk "[A pull request's commits and runs use up the report's call budget, or the requests per hour that `GITHUB_TOKEN` can make in the repository]" says.
- Within the budget, the report finds the runs with the fewest calls it can, and does not take a runs listing that GitHub cuts short as whole (R121).
- The time limit also bounds how long the report reads the ledger files of the default branch's history, which grows with every pull request (DR-131).

## Scope

This covers how many calls the report may make and how long its job may run. How it finds the merged pull request is DR-133 (A push gets a comment only when all its commits belong to one pull request), and which runs and jobs it counts are DR-019 (CI minutes come from the runs on the pull request's own commits) and DR-038 (CI minutes come from job times, rounded up per job).

## What reversing it would change

R70 in `report-comment` would change, with its scenario "A push with more commits than the call budget allows gets no comment", and so would R64 in `ci-minutes`, with its scenario "A pull request with more commits than the call budget allows is marked incomplete". The design's decision 7 and the risk named above, T51's answer, the call budget in the README (task 4.4), tasks 3.3, 4.1 and 4.3, the report comment and CI minutes feature pages, and the report's flow in `docs/how-it-works.md` would change too.
