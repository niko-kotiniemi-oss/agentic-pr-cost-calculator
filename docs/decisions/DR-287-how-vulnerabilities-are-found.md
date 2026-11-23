# DR-287: Vulnerabilities are found through Renovate's two feeds, private reporting, the threat model and a security review of each pull request

- **Type:** security and privacy
- **Boundary:** incoming
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-27
- **Requirements:** none
- **Threats:** T28
- **Replaces:** none
- **Closed by:** none

## Context

The owner asked on 2026-10-27 for a record of how vulnerabilities are found. The tool itself uses Python's standard library alone (DR-023), so what it depends on from outside is the repository's development tools, OpenSpec, the vendored Superpowers and the GitHub actions that its workflows run. `renovate.json` sets `osvVulnerabilityAlerts`, with which Renovate reads OSV's database, and `vulnerabilityAlerts`, with which it acts on the alerts that GitHub gives the repository once Dependabot alerts are on, a setting that the owner keeps and confirmed on 2026-11-23 as on.

## Decision

Vulnerabilities in what the repository depends on are found by Renovate, from OSV's database and from GitHub's Dependabot alerts, and Renovate proposes their fixes at once, without the wait that other updates take (DR-028). Vulnerabilities in the repository's own code are found by private vulnerability reporting (DR-077), by the threat model at design and at implementation (DR-095), and by the security review that each pull request gets before the owner merges it. GitHub's code scanning is decided with the change that corrects the tool's requirements before the build.

## Alternatives

None were recorded when this was decided.

## Consequences

- A vulnerability that neither feed lists for a pinned version is not proposed as a fix: the vendored Superpowers is pinned by a git tag through a custom manager in `renovate.json`, and its updates reach the owner's review of their diff (DR-145).
- The owner keeps Dependabot alerts turned on; without them Renovate reads OSV's database alone.

## Scope

This covers how vulnerabilities are found. When Renovate proposes an update is DR-028 (Renovate waits 14 days, and proposes vulnerability fixes at once), and how a vulnerability is reported is DR-077 (Private vulnerability reporting is on).

## What reversing it would change

How hard it is to reverse: reversible. `renovate.json`'s two settings would change, and so would the way that a vulnerability in a dependency reaches the owner. Nothing that adopters configure or depend on changes, so the change would not be a breaking one for adopters.
