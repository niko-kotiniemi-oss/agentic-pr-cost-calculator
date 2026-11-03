# DR-167: A release needs every acceptance test to pass

- **Type:** process
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-28
- **Requirements:** R139
- **Threats:** T99
- **Replaces:** none
- **Closed by:** none

## Context

Acceptance tests are kept as expected failures that may not pass early, with the error that each expects, so that CI stays green while their code is built (DR-084). The owner asked on 2026-10-28 for a golden set of figures that every version reproduces. The threat review at design found that a golden test whose code gives a wrong figure can keep failing with the error that its marker names, which counts as an expected failure, so that the release's tests pass on a version that does not reproduce the set.

## Decision

The release's test job runs every expected failure as an ordinary test, so that a version is released only when every acceptance test passes, the golden set's among them.

## Alternatives

- Running only the golden set's expected failures as ordinary tests at a release, which would release a version whose code leaves other scenarios unbuilt.
- Running the golden set in the release job itself, which would install the test tools beside the release's write token (T68).

## Consequences

- Releases wait until the code reaches every scenario and reproduces the golden set.
- The tests that parse the release workflow check that its test job runs expected failures as ordinary tests (task 6.3).
- Each golden test names as its expected error one that only a missing capture step or report raises, so that a wrong figure fails CI on the pull request, before any tag (task 1.21).

## Scope

This covers what the release's tests must pass. How releases are made is DR-148 (Each release is made from a tag), and the acceptance tests themselves are DR-084 (Acceptance tests come first).

## What reversing it would change

Task 6.3's test job and the tests that parse it would change, and so would the design's decision 14 and its risk on releases, and the scenario in `project-standards` that refuses a release which does not reproduce the golden set. A release could then pass on a version whose code leaves a scenario unbuilt. The release workflow's tests are not part of the public surface, so the change would not be a breaking one for adopters.
