# DR-075: Code-owner review is off

- **Type:** security and privacy
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** none
- **Threats:** T62
- **Replaces:** none
- **Closed by:** none

## Context

`.github/CODEOWNERS` makes the owner's account the code owner of every path, and every pull request that an agent session opens is opened by that same account (T62). A bypass for that account on the ruleset of `main` would let agent sessions skip `ci` when they merge, or push straight to `main` (T62, T64).

## Decision

Code-owner review stays off for as long as the only code owner's account also opens pull requests here, as it does for every agent session's pull request.

## Alternatives

- Requiring code-owner review, under which no pull request that the owner's account opens could be approved, so that it would push toward a bypass for that account, which agent sessions would share (T62).

## Consequences

- The comment in `.github/CODEOWNERS`, that the owner reviews every change and decides every merge, describes a rule and is not a control (T62). The owner's review rests on the owner and on `CLAUDE.md` (DR-080).
- The setting is the owner's. No file in the repository holds it and no test reads it, so nothing in the repository can check that it is applied (T62's residual).

## Scope

This covers code-owner review only while its condition holds, and decides nothing for a time when a second account owns code. The number of approvals that the ruleset on `main` requires is DR-141 (The ruleset on `main` requires no approvals), and its other terms are DR-072 (The ruleset on `main` requires a pull request and the `ci` check), DR-119 (Pull requests merge only when up to date with the default branch) and DR-140 (The ruleset on `main` has no bypass actor).

## What reversing it would change

The threat model's entry for code-owner review among the settings the owner keeps would change, with T62's answer and residual, including its statement that the code-owners file's comment is not a control. DR-080, DR-140 and DR-141 would be revisited. No requirement and no part of the public surface is involved.
