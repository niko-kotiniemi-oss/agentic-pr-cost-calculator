# DR-019: CI minutes come from the runs on the pull request's own commits

- **Type:** architecture
- **Boundary:** incoming
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R23, R62, R120
- **Threats:** T22
- **Replaces:** none
- **Closed by:** none

## Context

After a squash merge or a rebase merge, the default branch does not hold the commits that CI ran on, while the pull request's head stays readable from git (see the design's context). The merge's own push starts runs too, the report's among them, which are still going when the report runs, and GitHub's list of a pull request's commits stops at a fixed number (T22).

## Decision

The CI cost counts the workflow runs on the pull request's own commits: those that the pull request's head ref under `refs/pull/` holds and that the default branch did not hold before the merge, which the report reads from git, however many there are. Of the runs on those commits, it counts only the ones created before the pull request merged that no push to the default branch started, as each run's event and branch show.

## Alternatives

- Taking the CI commits from the push's range, which after a squash or rebase merge holds none of the commits that CI ran on.
- Taking the pull request's commits from GitHub's list of them, which stops at a fixed number (DR-017).

## Consequences

- Whatever the merge method, the same commits' runs are counted, and the runs that the merge's push starts are left out even when they run on one of those commits, as after a fast-forward, however their creation times fall (R120).
- Whether the creation-time cut also leaves out runs that the merge starts through another event, such as the pull request's `closed` event, rests on GitHub creating them at the merge time or later, which its documentation does not say; the threat model holds it as an assumption.
- Runs on commits that a force-push removed are not counted, and the comment says that its CI minutes cover the pull request's own commits only, as the design's risk "[A force-push removes commits that CI ran on]" says.
- A pull request based on one that was merged by squashing or rebasing counts that one's runs again unless it is rebased first, as the design's risk "[A pull request is based on another one that was merged by squashing or rebasing]" and the README (task 4.4) say.
- The report fetches the pull request's head ref under `refs/pull/` and the default branch's history up to the push, which a default checkout of one commit does not give it (R23).

## Scope

This covers which runs the CI cost counts. How a counted job's minutes are computed is DR-038 (CI minutes come from job times, rounded up per job), and how many calls the report may spend finding the runs is DR-039 (The report keeps to a call budget and a time limit).

## What reversing it would change

R62 and R120 in `ci-minutes` would change, with their scenarios for a squash, a rebase merge, a fast-forward and a run on the `closed` event, and so would R23 in `report-comment`, which has the report fetch the pull request's head ref. The design's decision 7 and the two risks named above, T22's answer and residual, the threat model's assumption about runs that another event starts, tasks 3.3 and 4.3, the README's notes on the two risks (task 4.4), the CI minutes feature page and `docs/how-it-works.md` would change too, and DR-038 and DR-039 would be revisited.
