# DR-028: Renovate waits 14 days, and proposes vulnerability fixes at once

- **Type:** technical
- **Boundary:** incoming
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-17 and 2026-10-20
- **Requirements:** R26
- **Threats:** T28
- **Replaces:** none
- **Closed by:** none

## Context

The repository pins its development tools to exact versions, and the vendored Superpowers to a commit and its tag, and Renovate proposes their updates (`requirements-dev.txt`, `renovate.json`). A malicious release of something the repository depends on could reach adopters by way of the tool (T28).

## Decision

Renovate's wait is 14 days from a release, for every update that it can date, major updates included. Renovate proposes minor and patch updates after the wait, as R26 says, and vulnerability fixes at once, so that security keeps up.

## Alternatives

None were recorded when this was decided.

## Consequences

- A vulnerability fix skips both the wait and the approval that a major update otherwise waits for (DR-111), whatever its type, so a major update that fixes one is proposed at once (R26).
- The wait covers digest updates too, while pinning a version already in use is not delayed, since it is no upgrade (`renovate.json`).
- An update that Renovate cannot date is proposed without the wait, since `renovate.json` sets `minimumReleaseAgeBehaviour` to `timestamp-optional`.
- The testing tools that the design's decision 8 adds come in at versions already past the wait.
- `tests/test_repository.py` holds the wait and the exception for vulnerability fixes.

## Scope

This covers when Renovate proposes updates to what the repository pins. When the oldest supported Python rises is DR-134 (The oldest supported Python rises only near its end of life or for a security fix), the approval that a major update waits for is DR-111 (Major updates wait for the owner's approval), and keeping sessions off an update branch until the owner has reviewed it is DR-145 (A session starts on a dependency-update branch only after the owner reviews its diff).

## What reversing it would change

R26 in `releases-and-compatibility` would change in its sentence on dependency updates, with its scenarios "A minor or patch update is proposed" and "A vulnerability fix is not held back", and so would `renovate.json`, its tests in `tests/test_repository.py`, the design's decisions 8 and 10 and T28's answer. The line on dependency updates in `CLAUDE.md` and the feature page would change too, and DR-111 would be revisited. Renovate's policy is not part of the public surface, so the change would not be a breaking one for adopters.
