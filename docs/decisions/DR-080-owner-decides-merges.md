# DR-080: The owner decides every merge

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** none
- **Threats:** T28, T33, T35, T62, T64, T71, T72
- **Replaces:** none
- **Closed by:** none

## Context

Agent sessions use the owner's own GitHub account, and GitHub has no way to tell what an agent did from what the owner did. A merge is therefore within reach of an agent that is mistaken or steered (T64, T33). The ruleset on `main` asks for a pull request and `ci` (DR-072), but no second person (DR-141), and a merge accepts every decision record that it adds, which can afterwards be closed but never removed (T72).

## Decision

The owner decides every merge, and a report from an AI that the work succeeded is never what merges a pull request. Agent sessions never merge a pull request.

## Alternatives

None were recorded when this was decided.

## Consequences

- For merges, while the only code owner's account also opens pull requests here (DR-075), no setting names an identity that agent sessions never hold, as the tag ruleset's deploy key does for tags (DR-073), so this rule rests on `CLAUDE.md` alone (T64's residual).
- Every change reaches `main` through a pull request that the owner merges (T28), so `CLAUDE.md`, `.claude/`, the workflows and dependency updates change only with the owner's review (T33, T35).
- The answers that rest on the owner reading a pull request's diff rest on this rule too: for one that changes an accepted record together with the check that holds it (T71), and for a record's decider, which the index puts in one diff (T72).
- The comment in `.github/CODEOWNERS` states this rule but is not a control (T62).

## Scope

This covers who merges a pull request in this repository. Tags, releases, settings, rulesets and secrets are DR-144 (Tags, releases, settings, rulesets and secrets stay with the owner), and approving an item on Renovate's dependency dashboard is DR-111 (Major updates wait for the owner's approval). What a pull request needs before it can merge is DR-072 (The ruleset on `main` requires a pull request and the `ci` check), DR-119 (Pull requests merge only when up to date with the default branch) and DR-141 (The ruleset on `main` requires no approvals), the review before a merge is DR-093 (Every change is reviewed in a separate context before it merges), and sessions on dependency-update branches are DR-145 (A session starts on a dependency-update branch only after the owner reviews its diff).

## What reversing it would change

The line on merges in the section "Who owns what" of `CLAUDE.md`, and its rule against an agent merging in "What an agent never does here", would change, and so would the comment in `.github/CODEOWNERS`, the proposal's condition that the owner has reviewed and merged the change, the design's decision 13, under which the owner's merge accepts a record, the threat model's flow diagram and its paragraph on `CLAUDE.md` under the settings the owner keeps, the answers of T28, T33, T35, T62, T64 and T72, and the residuals of T64, T71 and T72. DR-075, DR-082, DR-093, DR-121, DR-122, DR-141, DR-147 and DR-156 would be revisited. No requirement and no part of the public surface is involved.
