# DR-072: The ruleset on `main` requires a pull request and the `ci` check

- **Type:** security and privacy
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** closed
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-18 and 2026-10-20
- **Requirements:** none
- **Threats:** T28, T33, T35
- **Replaces:** none
- **Closed by:** DR-322

## Context

Adopters pin only commits that releases name, and a release can name only a commit on the first-parent history of the default branch (T58), so what reaches `main` is what can reach adopters. CI ends in one aggregate `ci` job, which passes only when every other job has passed, so that a ruleset has one check to require (DR-043).

## Decision

The ruleset on `main` requires a pull request and the `ci` check, so that nothing reaches the default branch without both.

## Alternatives

None were recorded when this was decided.

## Consequences

- Since the ruleset has no bypass actor either (DR-140), no change reaches `main` except through a pull request that passed CI (T28), so `CLAUDE.md`, `.claude/`, the workflows and the vendored and generated skills change there only through a merge (T33, T35).
- `ci` has to report on every pull request, so the CI workflow has no `paths:` filters: a required check that does not run never reports, and its pull request would wait for good.
- The ruleset is the owner's setting on GitHub: no file in the repository holds it and no test reads it, so nothing in the repository can check that it is applied (see the threat model's settings the owner keeps).

## Scope

This covers what the ruleset on `main` requires before a change reaches the default branch. That it has no bypass actor is DR-140 (The ruleset on `main` has no bypass actor), that it requires no approvals is DR-141 (The ruleset on `main` requires no approvals), and that a pull request's branch is up to date before it merges is DR-119 (Pull requests merge only when up to date with the default branch). Code-owner review is DR-075 (Code-owner review is off), the tag ruleset is DR-073 (Only a deploy key may bypass the tag ruleset) and DR-161 (The tag ruleset covers every tag), the aggregate job is DR-043 (CI ends in one aggregate `ci` job), and who decides merges is DR-080 (The owner decides every merge).

## What reversing it would change

The threat model's entry for this ruleset among the settings the owner keeps would change, with the answers of T28, T33 and T35, and so would the comments in `.github/workflows/ci.yml` on the aggregate job and on `paths:` filters. DR-043, DR-075, DR-080, DR-119, DR-140 and DR-141 would be revisited. No requirement and no part of the public surface is involved.
