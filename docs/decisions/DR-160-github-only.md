# DR-160: GitHub is the only repository and CI service `add-pr-cost-calculator` supports

- **Type:** scope
- **Boundary:** incoming
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the owner, 2026-10-27
- **Requirements:** R30
- **Threats:** T24
- **Replaces:** none
- **Closed by:** none

## Context

Through GitHub's REST API the report finds the merged pull request, lists its runs and jobs and posts its comment, and by git it fetches its own code and the repository it reports on, as `docs/how-it-works.md` lists. It runs as a reusable GitHub Actions workflow, and the CI minutes that it prices are GitHub Actions minutes. Other services that hold repositories and run CI, such as GitLab or Gitea, have APIs, CI and prices of their own. On 2026-10-27 the owner agreed that the report should connect to GitHub by both its REST API and git (R30), and kept every other repository and CI service out of this first version.

## Decision

`add-pr-cost-calculator` supports GitHub alone as the service that holds the repository and runs its CI, and leaves GitLab, Gitea and every other repository or CI service out of its scope.

## Alternatives

- Supporting other repository and CI services as well, each of which would need the report to read its own API, CI and prices, and to post its comment there.

## Consequences

- The report connects only to GitHub, by its REST API and by git (R30; T24).
- The design's non-goals and the proposal's "Impact" leave other services out, and the README lists them near its top among what this first version does not support.
- Which GitHub is supported is narrower still: GitHub.com, not GitHub Enterprise Server (DR-006).
- A later version may add another service, by a record that replaces this one.

## Scope

This covers which repository and CI services the tool works with. Which GitHub it supports is DR-006 (GitHub.com only, not GitHub Enterprise Server), and which agent's sessions it captures is DR-003 (Claude Code is the only agent `add-pr-cost-calculator` captures).

## What reversing it would change

Supporting another service would change R30 in `project-standards`, with its scenario "The report connects only to GitHub", and would add requirements for that service's API, CI and prices. The `ci-minutes` and `report-comment` specs, the design's goals and non-goals, the proposal's "Impact", `docs/how-it-works.md`, T24's answer and the README's list of what this first version does not support would change too, and DR-006, DR-020 and DR-062 would be revisited. Added behaviour alone would raise the minor number, while a change to the public surface, such as the reusable workflow's inputs, would be a breaking one for adopters (DR-096).
