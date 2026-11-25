# DR-320: CI ends in one aggregate `ci` job, beside the base commit's checks

- **Type:** technical
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-24
- **Requirements:** R25, R299
- **Threats:** none
- **Replaces:** DR-043
- **Closed by:** none

## Context

CI runs several jobs for every pull request: the Python checks on each version in its matrix, the OpenSpec check and the check of the vendored copy (`.github/workflows/ci.yml`). The ruleset on `main` lets a pull request merge only once the checks it requires have passed (DR-322). DR-043 made `ci` the one check that the ruleset requires. The owner chose on 2026-11-24 that the base commit's checks run from the base branch's own workflow (DR-312), and a job cannot need a job of another workflow, so `ci` cannot gather that one.

## Decision

CI's last job, `ci`, needs every other job of `.github/workflows/ci.yml` and passes only when each of them succeeded. It is one of the two checks that the ruleset requires; the other is the job of the base commit's checks, which runs from its own workflow on every pull request (R299).

## Alternatives

- `ci` waiting for the other workflow's run through the API: it would need a permission to read runs, and a wait that can time out.
- The base commit's checks inside `ci.yml`: a pull request could change or drop them with the workflow, which DR-312 answers.

## Consequences

- `ci` runs even when a job it needs has failed, and fails unless every result is a success, so a job that failed, was cancelled or was skipped fails it too.
- A job of `ci.yml` counts toward the merge only once `ci` lists it among the jobs it needs, and task 1.7 adds a check that every CI job is gated by `ci`.
- Neither workflow has `paths:` filters, since a required check that never runs never reports and the pull request would then wait for good.
- `ci` and the job of the base commit's checks hold read-only tokens (`docs/how-it-works.md`).
- DR-043 is closed, and this record holds what it decided. R25, which rested on it, rests on this record, and the assumptions, the feature page of `project-standards` and the design cite it in DR-043's place; records that name DR-043 keep their text.

## Scope

This covers how CI's jobs reach the ruleset. What the ruleset on `main` requires is DR-322 (The ruleset on `main` requires a pull request, the `ci` check and the base commit's checks), that it has no bypass actor is DR-140 (The ruleset on `main` has no bypass actor), and the jobs' tokens are DR-321 (Workflow tokens are read-only, except for releases and the report's comment, and only the base commit's checks run on `pull_request_target`).

## What reversing it would change

How hard it is to reverse: reversible. R25 in `releases-and-compatibility` would change in its scenario "The tests run on the oldest supported Python", which names the `ci` check, and R299 in its scenarios that name the job's check; so would the `ci` job in `.github/workflows/ci.yml`, the workflow of the base commit's checks, its row in the table of permissions in `docs/how-it-works.md`, task 1.7, the checks that the ruleset on `main` requires, and the threat model's list of the owner's settings and the descriptions of T62 and T64, which name `ci`. DR-322 would be revisited. CI is not part of the public surface, so the change would not be a breaking one for adopters.
