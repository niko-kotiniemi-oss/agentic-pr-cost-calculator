# DR-145: A session starts on a dependency-update branch only after the owner reviews its diff

- **Type:** security and privacy
- **Boundary:** incoming
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** none
- **Threats:** T35, T66
- **Replaces:** none
- **Closed by:** none

## Context

An update to a development tool or to the vendored Superpowers arrives as a pull request on a branch of its own, which Renovate opens (`renovate.json`). A session takes the hooks, skills and settings that it loads from the branch it starts on, and `.claude/settings.json` runs vendored hook scripts at session start with the session's credentials (T35). In a cloud session, the start-up hook also takes the development tools from the session's own branch and installs them with the owner's account, so a session on an update branch installs the new version before the owner has read it (T66).

## Decision

A session starts on a dependency-update branch only once the owner has reviewed the update's diff.

## Alternatives

None were recorded when this was decided.

## Consequences

- A dependency update is read by the owner before any session here runs it, on top of the pins, hashes and CI checks that answer T35 and T66.
- The rule is part of the answers of T35 and T66, and only `CLAUDE.md` holds it.

## Scope

This covers when a session may start on a branch that updates a dependency. Branches that outside contributors wrote are DR-081 (Outside pull requests are reviewed from `main`), when Renovate proposes an update is DR-028 (Renovate waits 14 days, and proposes vulnerability fixes at once) and DR-111 (Major updates wait for the owner's approval), and how the development dependencies are locked is DR-126 (Development dependencies are locked with hashes).

## What reversing it would change

The line on dependency-update branches in `CLAUDE.md`'s section "What an agent never does here" would change, with the answers of T35 and T66. DR-126, whose consequences rely on this rule for a session started on such a branch, would be revisited. No requirement and no part of the public surface is involved.
