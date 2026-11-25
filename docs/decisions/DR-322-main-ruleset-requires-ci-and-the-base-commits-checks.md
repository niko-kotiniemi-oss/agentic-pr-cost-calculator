# DR-322: The ruleset on `main` requires a pull request, the `ci` check and the base commit's checks

- **Type:** security and privacy
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-18, 2026-10-20 and 2026-11-24
- **Requirements:** R299
- **Threats:** T28, T33, T35
- **Replaces:** DR-072
- **Closed by:** none

## Context

Adopters pin only commits that releases name, and a release can name only a commit on the first-parent history of the default branch (T58), so what reaches `main` is what can reach adopters. CI ends in one aggregate `ci` job, which passes only when every other job of its workflow has passed (DR-320). DR-072 had the ruleset require `ci` alone. The owner chose on 2026-11-24 that the base commit's checks run from the base branch's own workflow (DR-312), whose check `ci` cannot gather.

## Decision

The ruleset on `main` requires a pull request, the `ci` check and the check of the job that runs the base commit's checks, so that nothing reaches the default branch without all three.

## Alternatives

- The ruleset requiring `ci` alone: a pull request whose base commit's checks fail would still merge.

## Consequences

- Since the ruleset has no bypass actor either (DR-140), no change reaches `main` except through a pull request that passed CI and the base commit's checks (T28), so `CLAUDE.md`, `.claude/`, the workflows and the vendored and generated skills change there only through a merge (T33, T35).
- Both checks have to report on every pull request, so neither workflow has `paths:` filters: a required check that does not run never reports, and its pull request would wait for good.
- The ruleset is the owner's setting on GitHub: no file in the repository holds it and no test reads it, so nothing in the repository can check that it is applied (see the threat model's settings the owner keeps). The owner adds the second check once the build has added its job, and a pull request that fails it is seen held back.
- DR-072 is closed, and this record holds what it decided. T28, T33 and T35, which rested on it, rest on this record, and the threat model, the assumptions and the feature page of `project-standards` cite it in DR-072's place; records that name DR-072 keep their text.

## Scope

This covers what the ruleset on `main` requires before a change reaches the default branch. That it has no bypass actor is DR-140 (The ruleset on `main` has no bypass actor), that it requires no approvals is DR-141 (The ruleset on `main` requires no approvals), and that a pull request's branch is up to date before it merges is DR-119 (Pull requests merge only when up to date with the default branch). Code-owner review is DR-075 (Code-owner review is off), the tag ruleset is DR-073 (Only a deploy key may bypass the tag ruleset) and DR-161 (The tag ruleset covers every tag), the aggregate job is DR-320 (CI ends in one aggregate `ci` job, beside the base commit's checks), and who decides merges is DR-080 (The owner decides every merge).

## What reversing it would change

How hard it is to reverse: reversible. The threat model's entry for this ruleset among the settings the owner keeps would change, with the answers of T28, T33 and T35, and so would the comments in `.github/workflows/ci.yml` on the aggregate job and on `paths:` filters, and R299's job would no longer hold back a merge. DR-075, DR-080, DR-119, DR-140, DR-141 and DR-320 would be revisited. No part of the public surface is involved.
