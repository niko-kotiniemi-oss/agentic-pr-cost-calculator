# DR-141: The ruleset on `main` requires no approvals

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-18 and 2026-10-20
- **Requirements:** none
- **Threats:** T62, T64
- **Replaces:** none
- **Closed by:** none

## Context

The pull requests that agent sessions open here are opened by the owner's account, which they act as (T64), and GitHub does not let a pull request's author approve it, so a required approval could be met for them only by another account, and while there is none it would push toward a bypass for that account, as a required code-owner review would (T62, DR-075). The ruleset on `main` requires a pull request and the `ci` check (DR-072).

## Decision

The ruleset on `main` requires no approving review before a pull request merges, so it asks for no second person.

## Alternatives

None were recorded when this was decided.

## Consequences

- A pull request that passes `ci` can be merged by any session acting as the owner's account, and that merges stay with the owner rests on `CLAUDE.md` (T64's residual, DR-080).
- The setting is the owner's. No file in the repository holds it and no test reads it, so nothing in the repository can check that it is applied (T62's residual).

## Scope

This covers how many approving reviews the ruleset on `main` requires. Code-owner review is DR-075 (Code-owner review is off). The ruleset's requirement of a pull request and the `ci` check is DR-072 (The ruleset on `main` requires a pull request and the `ci` check), its lack of a bypass actor is DR-140 (The ruleset on `main` has no bypass actor), and its rule that a branch is up to date before it merges is DR-119 (Pull requests merge only when up to date with the default branch). Who decides merges is DR-080 (The owner decides every merge).

## What reversing it would change

The threat model's entry for code-owner review among the settings the owner keeps, which gives the number of approvals required, would change, with T64's statement that the ruleset asks for no second person and its residual, and T62 and T64 would be rated again (DR-094). DR-075 and DR-080 would be revisited. No requirement and no part of the public surface is involved.
