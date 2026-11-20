# DR-018: The report runs on the push that a merge makes to the default branch

- **Type:** architecture
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R68
- **Threats:** T23, T50
- **Replaces:** none
- **Closed by:** none

## Context

The report runs once a pull request has merged (DR-005), in the adopter's CI, and posts a comment on it, so it needs a token that can write to pull requests. A workflow that an outside pull request starts, and that hands a write token to that pull request's code, is the best-known way into a GitHub workflow (T23).

## Decision

The workflow from which an adopting repository calls the report (DR-132) is triggered by a `push` to the default branch, so that the report runs on the push that a merge makes there.

## Alternatives

- The `pull_request` event when a pull request closes, whose token GitHub makes read-only for pull requests from forks, so those would get no report.
- `pull_request_target`, which gives a write token in the base repository's context while the pull request is still untrusted, and which GitHub's documentation says to avoid when a workflow builds or runs the pull request's code.

## Consequences

- Because the push belongs to the base repository, a pull request from a fork gets its report too.
- The report runs only after the merge (T23).
- A push names commits, not a pull request, so the report has to tell from the push's commits which pull request it merged, and some pushes get no comment (DR-133).
- A merge that a workflow makes with `GITHUB_TOKEN` starts no workflow run, so it gets no report, and no job summary says why, as the design's risks say. The threat model holds this as T50's residual.

## Scope

This covers the event that the report is built to run on. That it runs once, at merge, is DR-005 (The report runs once, at merge), that it refuses every other event is DR-061 (The report runs only for a push to the default branch), whose code it runs is DR-062 (The report runs its own pinned code), and what its caller grants is DR-063 (The calling workflow grants only what the report needs). How adopters run the report is DR-132 (The report is a reusable workflow that adopters call), and which pushes get a comment is DR-133 (A push gets a comment only when all its commits belong to one pull request).

## What reversing it would change

R68 in `report-comment` would change, with its scenarios, among them "A fork's pull request gets its report". The design's decision 7 and its risk "[A workflow merges a pull request with `GITHUB_TOKEN`]", T23's answer, T50's entry, tasks 4.1 and 4.3, the calling workflow in the README (task 4.4) and the report's flow in `docs/how-it-works.md` would change too. Adopters would have to change their calling workflows, which is a change that existing adopters must act on (R71), although the public surface (DR-154) does not list the event, so DR-154 would be revisited too, and so would DR-019, DR-061, DR-062, DR-063 and DR-133.
