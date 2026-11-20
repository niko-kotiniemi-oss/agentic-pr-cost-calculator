# DR-156: Adopters pin the commit that a release names

- **Type:** security and privacy
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** none
- **Threats:** T28, T58, T64
- **Replaces:** none
- **Closed by:** none

## Context

An adopter's calling workflow names the commit of the tool whose code the report runs (DR-062), and the hook file is copied from that same commit (DR-022). A release's own text names its tag and its commit in the release workflow's fixed words (R27, DR-148), while a tag can be moved (T28). GitHub resolves a commit id in `uses:` across the repository's fork network and serves a fork's commits under this repository's address (T58).

## Decision

Adopters still pin a full commit, as the design's decision 7 says; the release names it, so the release is how they find the commit to pin, and the README's section on adopting the tool, which task 4.4 writes, tells them to pin only a commit that a release of this repository names, which a commit that only a fork holds is not.

## Alternatives

None were recorded when this was decided.

## Consequences

- A release names only a commit in the default branch's first-parent history (DR-122), where changes arrive through pull requests that pass CI and that the owner merges (T28).
- An agent's merge reaches no adopter until the owner publishes a release that names its commit (T64).
- The README's section on adopting the tool, which task 4.4 writes, has adopters check a candidate commit in a clone of this repository with `git merge-base --is-ancestor`, which fails for a commit that only a fork holds (T58).
- The pin sits in the adopter's own workflow, so no check in this repository holds them to it, and the checksum that the README at the pinned commit gives shows only that their copy of the hook is whole, not that the commit is honest (T28's residual).

## Scope

This covers which commit adopters pin. How the hook file reaches them from that commit is DR-022 (Adopters copy the hook file from a pinned commit), whose code the report runs is DR-062 (The report runs its own pinned code), which commit a release may name is DR-122 (A release tag names a commit in the default branch's first-parent history), and who may create a tag or a release is DR-073 (Only a deploy key may bypass the tag ruleset).

## What reversing it would change

No requirement states which commit adopters pin. The README's section on adopting the tool, which task 4.4 writes, and its section on compatibility and releases would change, and so would the design's decisions 1, 7 and 11, the answers of T28, T58 and T64, T28's residual, the account of releases on the feature page for `releases-and-compatibility`, and the price-update flow in `docs/how-it-works.md`, where the next release names the commit that adopters then take. DR-022, DR-062, DR-073, DR-122 and DR-161, whose reasons rest on adopters pinning what a release names, would be revisited. The reusable workflow's path and the hook file's path are part of the public surface, but how an adopter chooses a commit is not, so the change would not be a breaking one for adopters.
