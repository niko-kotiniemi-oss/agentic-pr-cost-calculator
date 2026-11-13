# B-014: An unknown model counted as unknown

- **Status:** Open to feedback and contributions
- **Last changed:** 2026-11-13
- **Brief:** A ledger line whose model the report's price table does not list counted under `unknown`, in tokens and not in cost, instead of being refused.
- **Rests on:** DR-208, T136
- **Issue:** 24
- **Pull requests:** none

## Problem

A person's plugin can be of a later release than the report that a repository pins (DR-208). When a later release adds a model, the earlier report refuses the lines that name it, and their tokens drop out of the comment's figures (T136).

## What done looks like

A ledger line whose model name is well formed but missing from the report's price table counts under `unknown`, in tokens and not in cost, and the comment says so. The change has its own threat model first, since a hand-edited ledger file could make up a name: what makes a name well formed, and how the comment shows such calls apart from the priced ones.

## Postponed points

- From the threat review at design of pull request 22 (its threat 10): counting a line whose model the report's price table does not list, in tokens and not in cost, instead of refusing it, once a threat model says what makes a model name well formed.
