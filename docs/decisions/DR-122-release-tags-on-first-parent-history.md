# DR-122: A release tag names a commit in the default branch's first-parent history

- **Type:** security and privacy
- **Boundary:** outgoing
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R27
- **Threats:** T28, T58, T67
- **Replaces:** none
- **Closed by:** none

## Context

Adopters pin the commit that a release names, so each release tells them which commit to trust (see the design's decision 11). Pushing a tag starts the release workflow, and GitHub runs that workflow as it stands at the tagged commit (T67). A commit from inside a merged pull request can be held by the default branch, though the branch never had its state (T67), and GitHub serves a commit that only a fork holds under this repository's address (T58).

## Decision

A release is made only from a tag that names a commit in the default branch's first-parent history, so a commit from the middle of a merged pull request, a state the default branch never had, is refused.

## Alternatives

None were recorded when this was decided.

## Consequences

- A commit that only a fork holds is outside that history too, so no release names one, and an adopter who pins only what a release names never pins one (T58).
- What a release names has reached the default branch, where changes arrive only through pull requests that pass CI and that the owner merges (T28).
- The check runs in the release workflow as the tagged commit holds it, so a tag on a commit outside the default branch runs that commit's own copy of the check. It catches a mistaken tag, not a hostile one. The control over releases is who may create a tag or a release (DR-073, DR-074, DR-161), and T67's residual leaves that to settings that no test reads.

## Scope

This covers which commit a release tag may name. That each release is made from a tag that carries its version number is DR-148 (Each release is made from a tag), how that number is chosen is DR-096 (Versions are semantic), who may create, move or delete a tag is DR-073 (Only a deploy key may bypass the tag ruleset), and that a published release cannot change is DR-074 (Releases are immutable).

## What reversing it would change

R27 in `releases-and-compatibility` would change in its clause on the first-parent history, with its scenario "A tag on a commit outside the default branch's first-parent history is refused", and so would the answers of T28, T58 and T67, task 6.1, the release flow in `docs/how-it-works.md`, the feature page's account of releases, and the design's decision 11, which names this record. DR-073, whose context sets out what this check cannot do, would be revisited. The release check is not part of the public surface, so the change would not be a breaking one for adopters.
