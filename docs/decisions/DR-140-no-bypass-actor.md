# DR-140: The ruleset on `main` has no bypass actor

- **Type:** security and privacy
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-18 and 2026-10-20
- **Requirements:** none
- **Threats:** T28, T33, T35, T62, T64
- **Replaces:** none
- **Closed by:** none

## Context

The ruleset on `main` requires a pull request and the `ci` check, so that nothing reaches the default branch without both (DR-072). Agent sessions act on GitHub as the owner's own account, so whatever the ruleset lets that account do, an agent can do too (T64). One account opens every pull request here, so a rule that its pull requests cannot meet, such as a required code-owner review, would push toward a bypass for that account (T62).

## Decision

The ruleset on `main` has no bypass actor, so that no account, the owner's included, may skip its terms.

## Alternatives

- A bypass actor that the owner's account holds, which would let agent sessions, acting as that account, merge without `ci` or push straight to `main` (T62, T64).

## Consequences

- The terms of DR-072 bind every account, so no change reaches `main`, from the owner's account or from an agent session, except through a pull request that passed CI (T28, T33, T35).
- The owner's own changes take the same path, through a pull request that passes `ci`.
- The setting is the owner's. No file in the repository holds it and no test reads it, so nothing in the repository can check that it is applied (T62's residual).

## Scope

This covers who may bypass the ruleset on `main`, and DR-072 (The ruleset on `main` requires a pull request and the `ci` check) covers what the ruleset requires. Its approvals are DR-141 (The ruleset on `main` requires no approvals), and its rule that a branch is up to date before it merges is DR-119 (Pull requests merge only when up to date with the default branch). The tag ruleset's one bypass is DR-073 (Only a deploy key may bypass the tag ruleset), and which tags it covers is DR-161 (The tag ruleset covers every tag).

## What reversing it would change

The threat model's entry for the ruleset on `main` among the settings the owner keeps would change, and so would the answers of T28, T33, T35, T62 and T64. DR-072 and DR-075 would be revisited. No requirement and no part of the public surface is involved.
