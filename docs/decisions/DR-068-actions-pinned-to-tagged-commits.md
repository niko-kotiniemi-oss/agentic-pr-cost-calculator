# DR-068: Every action is pinned to a commit that its repository tagged

- **Type:** security and privacy
- **Boundary:** incoming
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R34
- **Threats:** T28, T63
- **Replaces:** none
- **Closed by:** none

## Context

The actions that the workflows use run with the workflows' tokens: those of the reusable workflow in every adopter's CI, with that repository's contents and `pull-requests: write`, and those of the release job with `contents: write` (T63). A tag can be moved (T28), and GitHub resolves a commit id in `uses:` across a repository's forks, so a commit that only a fork holds is served under the original's address (T58).

## Decision

Every action and container image that a workflow uses is pinned to a full commit or a digest, and only to one that a tag of its source names. CI fails on any other pin, such as a commit that only a fork holds.

## Alternatives

- Accepting any full commit id, which lets a pull request swap a pin for a fork's commit and keep the version comment, while the diff shows only a hash (T63).

## Consequences

- `tests/test_repository.py` holds that each `uses:` names a full commit, and task 1.15 adds the check that a tag names it, tested against a local fixture rather than the network, as the vendored copy's sync is tested.
- A container image, such as the one that a CI job runs git 2.43 in, is pinned by its digest (T28).
- Each release's bill of materials lists the reusable workflow's actions with their pinned commits (DR-097).

## Scope

This covers how this repository's workflows pin what they run. The commit that an adopter's workflow pins the tool to, from which the report runs its own code, is DR-062 (The report runs its own pinned code), and when Renovate proposes a new pin is DR-028 (Renovate waits 14 days, and proposes vulnerability fixes at once) and DR-111 (Major updates wait for the owner's approval).

## What reversing it would change

R34 in `project-standards` would change, with its scenario "An action pinned to an untagged commit fails CI", and so would the spec's purpose, the feature page's line on pinned actions, the answers of T28 and T63, task 1.15 and the pin test in `tests/test_repository.py`. The pins are not part of the public surface, so the change would not be a breaking one for adopters.
