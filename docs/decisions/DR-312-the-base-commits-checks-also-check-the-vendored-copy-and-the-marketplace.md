# DR-312: A pull request that changes the vendored copy or the marketplace is also checked by its base commit's scripts

- **Type:** security and privacy
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-12 and 2026-11-24
- **Requirements:** R299, R317, R321
- **Threats:** T132, T137, T320, T327
- **Replaces:** none
- **Closed by:** none

## Context

A pull request that changes the vendor check or a marketplace check together with what it checks passes its own CI, so only the owner's review stops it (T132, T137). The owner chose on 2026-11-12 that the vendor check runs the base commit's script, as the marketplace check already takes its build script from a trusted commit, and on 2026-11-24 that the job runs from the base branch's own workflow, so that a pull request that also changes the workflow cannot drop or weaken it.

## Decision

CI runs, on every pull request, from the base branch's own workflow on `pull_request_target`, a job that, where the pull request changes `vendor/` or the marketplace's root file or plugin folder, runs the base commit's own vendor check and marketplace checks over the merge commit that GitHub tests, holding no secret and only `contents: read`, and fails when either check fails or it cannot read that commit, and that otherwise passes, saying in its log what it compared (R299). The job runs only programs from the base commit's checkout or the runner, its shell included, never with the pull request's tree as its working directory or on a search path; reads that tree from git's objects alone, with no checkout, attributes or submodule, failing on a link or a gitlink under a checked path; restores and saves no cache; and fails where the pull request's lock names another repository or other vendored paths than the base's, ignoring `SYNC_REMOTE_BASE` (R317). No other workflow triggers on `pull_request_target`, none on `workflow_run`, and the job's workflow checks out only the base's commit and gives the pull request's number and commits to a command only through `env:` (R321).

## Alternatives

- `pull_request`, which runs the pull request's own copy of the workflow: a pull request that also changes the workflow would drop or weaken the job, leaving only the owner's review.
- `pull_request_target` with its default permissions: it is the event through which a pull request's code most often reaches a write token, so the job grants only `contents: read`, reads no secret, checks out no ref of the pull request and runs none of its code.

## Consequences

- A pull request that changes a check, or the job's workflow, reaches the default branch only through the owner's review, and checks only the pull requests after it.
- The job's check is outside the aggregate `ci` job, which cannot need a job of another workflow, so the ruleset on `main` requires it beside `ci`: a setting that the owner makes, and DR-320, DR-321 and DR-322, which replace the records that made `ci` the one required check and let no workflow trigger on `pull_request_target`.
- A pull request from a fork runs the job without the approval that DR-078 asks for its own workflows, since the job runs the base's code alone.
- The job reads the pull request's tree through git, which the design threat-models (T320).
- The base's sync script finds its tree from its own location, so the build gives it a way to read another tree; the marketplace half holds only once task 6.9 builds the marketplace's checks.

## Scope

This covers which commit's checks hold the vendored copy and the marketplace. The checks themselves are R184, R190 and the vendored copy's own requirement.

## What reversing it would change

How hard it is to reverse: reversible. R299, R321 and the job that runs it would change, the ruleset on `main` would require `ci` alone again, and the answers of T132 and T137 would rest on the owner's review alone.
