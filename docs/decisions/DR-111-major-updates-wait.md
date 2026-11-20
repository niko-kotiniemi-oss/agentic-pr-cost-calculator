# DR-111: Major updates wait for the owner's approval

- **Type:** technical
- **Boundary:** incoming
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-20
- **Requirements:** R26
- **Threats:** T64
- **Replaces:** none
- **Closed by:** none

## Context

Renovate proposes updates to what the repository pins, its development tools and the vendored Superpowers (`renovate.json`). The tool runs on Python 3.11 and every later release (DR-025), on adopters' own machines and in their own CI (see the threat model's boundary 6). Agent sessions act on GitHub as the owner's own account, so GitHub cannot tell an agent's approval from the owner's (T64).

## Decision

A major update waits on the dependency dashboard for the owner's approval, because a major version is where support for older systems is dropped. Renovate lists such an update there and opens no pull request for it until the owner approves it, and an agent never approves an item on the dashboard.

## Alternatives

None were recorded when this was decided.

## Consequences

- `renovate.json` gives major updates a rule of their own, with `dependencyDashboardApproval: true`, so minor and patch updates are proposed without approval (R26).
- A vulnerability fix is not held for approval, whatever its type, since `vulnerabilityAlerts` sets `dependencyDashboardApproval: false` (DR-028).
- `tests/test_repository.py` fails when the rule for major updates is missing or when every update would wait for approval, and a test shows that the check of the rule notices when it is missing (task 1.11).
- The approval is within agent sessions' reach, so it rests on `CLAUDE.md`'s rule that agents never approve an item on the dashboard (T64).

## Scope

This covers the approval that a major update waits for, and who may give it. The 14-day wait, and vulnerability fixes proposed at once, are DR-028 (Renovate waits 14 days, and proposes vulnerability fixes at once). When the oldest supported Python rises is DR-134 (The oldest supported Python rises only near its end of life or for a security fix), and who keeps the tags, the releases and the settings is DR-144 (Tags, releases, settings, rulesets and secrets stay with the owner).

## What reversing it would change

R26 in `releases-and-compatibility` would change in its title and in its clause on major updates, with its scenario "A major update waits for the owner", and so would the spec's purpose. The rule in `renovate.json` that names this record, its two tests in `tests/test_repository.py`, task 1.11, the line on major updates in `CLAUDE.md`'s section on compatibility and releases and the line in its section on what an agent never does here, the feature page for `releases-and-compatibility`, T64's answer and residual and the design's decision 10, which names this record, would change too. DR-028, whose vulnerability fixes skip this approval, would be revisited. Renovate's settings are not part of the public surface, so the change would not be a breaking one for adopters.
