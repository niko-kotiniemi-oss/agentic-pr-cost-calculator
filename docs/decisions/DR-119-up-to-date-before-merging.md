# DR-119: Pull requests merge only when up to date with the default branch

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** none
- **Threats:** T76
- **Replaces:** none
- **Closed by:** none

## Context

A new record takes the next number, and the records run from DR-001 without a gap or a repeat (R124). GitHub runs a pull request's CI again when the pull request is pushed to, not when its base moves, so two pull requests that each add the next number can both pass and both merge (T76). Once the default branch holds both, renumbering either is a change that the rule on accepted records forbids (DR-121).

## Decision

`main`'s ruleset requires a pull request's branch to be up to date with the default branch before it merges, so that the pull request's CI has run on what the default branch holds.

## Alternatives

None were recorded when this was decided.

## Consequences

- A pull request that falls behind the default branch is brought up to date, and its CI runs again, before it can merge. When two take the same number, the second one's CI then fails while its record can still be renumbered (T76).
- The decision rests on the owner's setting, which no file holds and no test reads, and the threat model lists it among the settings the owner keeps.
- A repeat that reaches the default branch anyway is named by the check and reported by CI's run on the push, and how to recover from it is the owner's decision.

## Scope

This covers when a pull request may merge relative to the default branch. That the ruleset requires a pull request and the `ci` check is DR-072 (The ruleset on `main` requires a pull request and the `ci` check), and who keeps the settings is DR-144 (Tags, releases, settings, rulesets and secrets stay with the owner).

## What reversing it would change

The setting would leave the threat model's list of settings the owner keeps, T76's answer and residual would change, and so would the design's decision 13, which names this record. DR-108, whose numbering the setting protects, and DR-121, whose rule leaves a repeated number with no fix, would be revisited, and so would DR-072, DR-075, DR-080, DR-140, DR-141 and DR-144, which name this rule among the ruleset's terms or the settings the owner keeps. No requirement's text would have to change, since R124 asks for numbers without a repeat whatever the setting. The setting is not part of the public surface, so the change would not be a breaking one for adopters.
