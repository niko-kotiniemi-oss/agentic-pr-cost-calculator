# DR-043: CI ends in one aggregate `ci` job

- **Type:** technical
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** closed
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R25
- **Threats:** none
- **Replaces:** none
- **Closed by:** DR-320

## Context

CI runs several jobs for every pull request: the Python checks on each version in its matrix, the OpenSpec check and the check of the vendored copy (`.github/workflows/ci.yml`). The ruleset on `main` lets a pull request merge only once the checks it requires have passed (DR-072).

## Decision

CI's last job, `ci`, needs every other job and passes only when each of them succeeded. It is the one check that the ruleset requires.

## Alternatives

None were recorded when this was decided.

## Consequences

- `ci` runs even when a job it needs has failed, and fails unless every result is a success, so a job that failed, was cancelled or was skipped fails it too.
- A job counts toward the merge only once `ci` lists it among the jobs it needs, and task 1.7 adds a check that every CI job is gated by `ci`.
- The workflow has no `paths:` filters, since a required check that never runs never reports and the pull request would then wait for good.
- `ci` holds the same read-only token as the other jobs (`docs/how-it-works.md`).

## Scope

This covers how CI's jobs reach the ruleset as one check. What the ruleset on `main` requires is DR-072 (The ruleset on `main` requires a pull request and the `ci` check), that it has no bypass actor is DR-140 (The ruleset on `main` has no bypass actor), and the jobs' tokens are DR-067 (Workflow tokens are read-only, except for releases and the report's comment).

## What reversing it would change

R25 in `releases-and-compatibility` would change in its scenario "The tests run on the oldest supported Python", which names the `ci` check, and so would the `ci` job in `.github/workflows/ci.yml`, its row in the table of permissions in `docs/how-it-works.md`, task 1.7, the checks that the ruleset on `main` requires, and the threat model's list of the owner's settings and the descriptions of T62 and T64, which name `ci`. DR-072 would be revisited. CI is not part of the public surface, so the change would not be a breaking one for adopters.
