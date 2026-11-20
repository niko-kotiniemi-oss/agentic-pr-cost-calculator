# DR-037: Adopters keep git's sparse index off

- **Type:** technical
- **Boundary:** outgoing
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-10-20
- **Requirements:** none
- **Threats:** T8, T10
- **Replaces:** none
- **Closed by:** none

## Context

Git's sparse index is off unless someone turns it on. With it on, git 2.43, the oldest git that CI tests, can write a damaged index in a cone-mode `git sparse-checkout` command, or one given `--sparse-index`, run while a file has an intent-to-add entry, and in some squashes made with `git reset -N`, after which the next commit can delete ledger files from the branch (see the design's risk "[A person removes a ledger file from their branch, or a commit that holds one is undone]"). The owner chose on 2026-10-20 to keep the sparse index off, over asking adopters to remember to turn it off before each squash made with `git reset -N`, and over squashing with `git reset --soft` instead, which keeps the ledger files but leaves the sparse index on, with the damage that a `git sparse-checkout` command can then do.

## Decision

While the tool is on, adopters keep git's sparse index off and give no command `--sparse-index`.

## Alternatives

- Asking adopters to turn the sparse index off before each squash made with `git reset -N`, which would rest on their remembering to.
- Squashing with `git reset --soft`, which keeps the ledger files, while a sparse index left on would still let `git sparse-checkout` damage the index.

## Consequences

- The change `add-pr-cost-calculator` carries the choice out in every worktree: the README's section on adopting the tool says to keep the sparse index off in each, with a way to turn it off that reaches every worktree, one added later included.
- Where the sparse checkout holds `.pr-cost/` and the sparse index is off, a squash made with `git reset -N` loses no ledger file to a damaged index, which task 4.4 tests.
- The safeguard is advice, so where an adopter leaves the sparse index on, the damage stays in the residuals of T8 and T10.

## Scope

This covers git's sparse index only. The README's other advice on sparse checkouts, such as running `git sparse-checkout` only while no file has an intent-to-add entry, which git 2.43 needs even with the sparse index off, belongs to the same risk and to task 4.4.

## What reversing it would change

No requirement would change, since no spec mentions the sparse index. The design's risk "[A person removes a ledger file from their branch, or a commit that holds one is undone]" would change where it gives this advice, and so would the residuals of T8 and T10, the README's section on adopting the tool, and task 4.4, which writes and tests it.
