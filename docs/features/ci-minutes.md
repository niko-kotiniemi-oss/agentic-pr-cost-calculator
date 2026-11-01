# CI minutes

The report adds what the pull request's GitHub Actions runs cost, from the times GitHub gives for each job.

**Status:** designed, not built yet.

**Spec:** `ci-minutes`

**Requirements:** R18, R62, R120, R121, R63, R64

## Expected behaviour

- **Which runs.** Every attempt of every job of every workflow run on the pull request's own commits, created before the pull request merged. The pull request's own commits are those its head holds that the default branch did not hold before the merge.
- **Which runs are not counted.** Runs that a push to the default branch started, the merge's own runs and the report's included, and runs on commits that a force-push removed.
- **Rounding.** Each attempt's duration is rounded up to a whole minute and priced at its runner type's rate for its day.
- **Unknown runners.** A job on a runner that the price table does not list is counted in minutes and left out of the cost, and the report says how many minutes that was.
- **Incomplete.** If any run or job that counts cannot be read, has not finished, or is left unread because the report's call budget ran out or because GitHub returned only part of a listing, the CI cost is marked incomplete and is not presented as the total.

## Not covered

- A pull request based on another that was merged by squashing or rebasing counts that one's runs again unless it is rebased first.
- Included minutes and plan discounts: the figure is at GitHub's list rate.

## How it is validated

This feature is validated first by its spec's scenarios: each gets an acceptance test before its code, seen to fail for the expected reason (task 1.4). Then come the checks that DR-084 to DR-093 and DR-109 apply to all the tool's code. Beyond those, this feature has its own:

- Tests against recorded API responses for a merge commit, a squash, a rebase merge and a fast-forward, a run on the pull request's `closed` event, and a pull request with more commits than the call budget allows (task 3.3).

## See also

- `ci-minutes` in `openspec/`, and design decision 7 of `add-pr-cost-calculator`.
