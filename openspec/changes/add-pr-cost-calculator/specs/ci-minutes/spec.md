## Purpose

Add the cost of the GitHub Actions minutes that a pull request's own commits used, counted for every job attempt and rounded up per attempt.

## ADDED Requirements

### Requirement: Each job attempt's minutes are rounded up to a whole minute

Each attempt's minutes (see "Every job attempt of the pull request's own runs is counted") SHALL be its duration rounded up to a whole minute, priced at the rate for its runner type on its UTC day (see "Prices are dated" in `pricing`).

#### Scenario: A job's minutes are rounded up

- **WHEN** a job ran for 61 seconds on a standard Linux runner
- **THEN** it counts as two minutes at that runner's rate

#### Scenario: Each attempt of a re-run job is rounded up on its own

- **WHEN** a job ran twice, each attempt for 61 seconds on a standard Linux runner
- **THEN** it counts as four minutes, two for each attempt, not as three for the two attempts added together

#### Scenario: A job's minutes are priced at its day's rate

- **WHEN** a runner type's rate changes on a date, and a pull request has jobs on that runner type the day before and the day after
- **THEN** the earlier jobs' minutes are priced at the old rate and the later ones' at the new rate

### Requirement: Every job attempt of the pull request's own runs is counted

The CI cost SHALL count every attempt of every job of every workflow run on the pull request's own commits that no push to the default branch started and that was created before the pull request merged. The pull request's own commits are those that its head holds and that the default branch did not hold before the merge, read from git, however many there are.

#### Scenario: A re-run job counts every attempt

- **WHEN** a job ran twice, because its workflow run was re-run
- **THEN** the minutes of both attempts are counted

#### Scenario: Every commit is counted, beyond what the API lists

- **WHEN** a pull request has more commits than GitHub's pull request commit listing returns
- **THEN** the runs of all of its commits are counted

#### Scenario: A squash merge counts the runs on the pull request's commits

- **WHEN** a pull request whose commits ran CI is merged by squashing them into one new commit
- **THEN** the CI cost counts the runs on the pull request's own commits

#### Scenario: A rebase merge counts the runs on the pull request's commits

- **WHEN** a pull request whose commits ran CI is merged by rebasing them onto the default branch as new commits
- **THEN** the CI cost counts the runs on the pull request's own commits

#### Scenario: A run that the pull request's closing starts is not counted

- **WHEN** a workflow on the pull request's `closed` event runs on its head commit, with a creation time at or after the pull request's merge time
- **THEN** none of its jobs are counted

### Requirement: Runs that the merge's push starts, and runs on other commits, are not counted

The CI cost SHALL NOT count the runs that the merge's push starts, even when they run on one of the pull request's own commits (see "Every job attempt of the pull request's own runs is counted"), as after a fast-forward, and whatever their creation times, and SHALL NOT count runs on any other commit, such as the new commits that a squash or rebase merge makes.

#### Scenario: Runs on other commits are not counted

- **WHEN** a workflow run's commit is not one of the pull request's commits
- **THEN** none of its jobs are counted

#### Scenario: Runs that the merge starts are not counted

- **WHEN** the merge's push to the default branch starts workflow runs
- **THEN** none of their jobs are counted

#### Scenario: A fast-forward merge counts the pull request's runs, not the push's

- **WHEN** the default branch is moved forward to the pull request's head commit as it is, and that push starts workflow runs on the same commit, one of them with a creation time before the pull request's merge time
- **THEN** the runs created before the merge that the push did not start are counted, and none of the runs that the push started is

### Requirement: The report finds the pull request's runs with the fewest calls it can

The report SHALL find the runs that the CI cost counts (see "Every job attempt of the pull request's own runs is counted") with the fewest calls to GitHub's API that it can: a listing for each commit, or, where that takes fewer calls and GitHub returns the whole of it, the repository's runs listed page by page, filtered by their event and by when they were created.

#### Scenario: A runs listing that GitHub cuts short is not taken as whole

- **WHEN** the repository's runs, filtered by their event and by when they were created, are more than GitHub returns for a filtered listing
- **THEN** the report reads the runs of the pull request's commits commit by commit instead, and counts every run on those commits that it would count otherwise

### Requirement: Minutes on a runner the price table does not list are counted, not priced

A job on a runner that the price table does not list SHALL be counted in minutes and left out of the cost, and the report SHALL say how many minutes ran on runners it could not price.

#### Scenario: A job on a runner the price table does not list is not priced

- **WHEN** a job ran on a runner that the price table does not list
- **THEN** its minutes are counted and left out of the CI cost, and the report says how many minutes ran on runners it could not price

### Requirement: A CI cost missing any run or job is marked incomplete

If any run or job counted (see "Every job attempt of the pull request's own runs is counted") cannot be read, has not finished, or is left unread because the report's call budget ran out or because GitHub returned only part of a listing, the CI cost SHALL be marked incomplete, and SHALL NOT be presented as the total.

#### Scenario: An incomplete jobs listing is reported as incomplete

- **WHEN** the jobs of one of the pull request's runs cannot be read
- **THEN** the report marks the CI cost as incomplete

#### Scenario: A run that has not finished makes the cost incomplete

- **WHEN** a run on one of the pull request's commits has not finished when the report runs
- **THEN** none of its jobs are counted, and the report marks the CI cost as incomplete

#### Scenario: A pull request with more commits than the call budget allows is marked incomplete

- **WHEN** reading the runs and jobs of a pull request's own commits would take more calls to GitHub's API than the report's call budget leaves
- **THEN** the report reads no more than the budget allows, marks the CI cost as incomplete, and posts its comment
