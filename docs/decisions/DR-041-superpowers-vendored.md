# DR-041: Superpowers is vendored and compared with upstream in CI

- **Type:** technical
- **Boundary:** incoming
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** none
- **Threats:** T35
- **Replaces:** none
- **Closed by:** none

## Context

Superpowers' skills guide how the tool is built (DR-142). Agents working here load them, and `.claude/settings.json` runs its hook scripts at session start with the session's credentials, so a changed file changes what agents do or runs code (T35). A fetch by commit id takes any commit that upstream serves, those of its open pull requests included, so a pinned commit could hold code that no release contains (T35).

## Decision

Superpowers is copied into `vendor/superpowers/` from the upstream repository and commit that `UPSTREAM.lock` names, and only when that commit is the one that the lock's release tag names. CI re-creates the copy from that commit and fails on any difference.

## Alternatives

- Having `.claude/settings.json` enable the plugin from an external source, turned down because such a plugin does not install itself in a fresh session (`vendor/superpowers/UPSTREAM.lock`).

## Consequences

- A hand edit to a vendored file fails CI's `vendor` job, which runs `scripts/sync-superpowers.sh --check` to rebuild the copy in a temporary folder and compare the two. Only `UPSTREAM.lock` is written here, and the comparison leaves it out by name.
- Only part of upstream is copied: the plugin's manifest, the skills, two hook scripts and the licence, a list that a test holds equal in the script and in the lock.
- A new version arrives as a pull request that the owner reviews, in which Renovate moves the lock's commit and tag together, and which needs the sync script run on its branch (T35, `renovate.json`).
- The check reads the tag from upstream on every run, so a tag that upstream moves or removes fails it.
- Each release's bill of materials lists Superpowers as a development-only component, with its source and licence (DR-097).

## Scope

This covers how Superpowers' files come into the repository and stay equal to upstream's. What Superpowers is for is DR-142 (Superpowers owns how the tool is built), and OpenSpec's generated skills are DR-042 (OpenSpec is pinned and its skills are regenerated in CI). Superpowers' telemetry, which `.claude/settings.json` turns off, is DR-071 (Development tools report nothing about how they are used).

## What reversing it would change

No requirement states this. The vendored tree, `scripts/sync-superpowers.sh` and its tests, CI's `vendor` job, Renovate's custom manager, and the plugin's entries in `.claude/settings.json`, `.claude-plugin/marketplace.json` and `.claude/hooks/session-start.sh` would change, and so would T35's answer, the `vendor` job's row in the table of permissions and the connection for the check in `docs/how-it-works.md`, the design's decision 11, whose bill of materials names Superpowers as a development-only component, the README's paragraph on the pinned tools and `CLAUDE.md`'s section on who owns what. DR-043, whose `ci` job needs the `vendor` job, and DR-142 would be revisited. Superpowers is a development-only part, outside the public surface, so the change would not be a breaking one for adopters.
