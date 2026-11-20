# DR-042: OpenSpec is pinned and its skills are regenerated in CI

- **Type:** technical
- **Boundary:** incoming
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** none
- **Threats:** T35, T66
- **Replaces:** none
- **Closed by:** none

## Context

OpenSpec holds what the tool must do (DR-079). It is a Node program, used here only in development (DR-024), and it writes the `openspec-*` skills under `.claude/skills/`, which agents working here load. A changed skill changes what those agents do (T35), and a development dependency that is not locked resolves to its newest release at every session start (T66).

## Decision

OpenSpec is pinned to an exact version in `package.json` and installed from `package-lock.json`. CI regenerates the `openspec-*` skills with the pinned CLI and fails when they differ from the ones committed.

## Alternatives

None were recorded when this was decided.

## Consequences

- `scripts/verify-openspec.sh`, which CI's `openspec` job and a person at a terminal both run, stops when the installed CLI is not the version that `package-lock.json` pins. It then empties each generated skill, has the CLI write it again and fails on any difference.
- A hand edit to a generated skill fails the check, which is why `CLAUDE.md` says that they are never edited.
- A new version of OpenSpec reaches the repository only as a pull request that the owner reviews (T35), and one that writes its skills differently fails the check until that pull request also carries what it writes.
- The check keeps OpenSpec's configuration in a scratch folder, so a person's own OpenSpec settings cannot change what it writes.
- A test holds that `package.json` names an exact version.

## Scope

This covers which OpenSpec runs here and how its generated skills are kept. The same script also validates every spec and change strictly, which is outside this record. That Node serves development only is DR-024 (The tool, its release and its documentation are Python and Markdown), OpenSpec's telemetry is DR-071 (Development tools report nothing about how they are used), and the vendored Superpowers is DR-041 (Superpowers is vendored and compared with upstream in CI).

## What reversing it would change

No requirement states this. `package.json`, `package-lock.json`, the pin's test in `tests/test_repository.py`, `scripts/verify-openspec.sh`, CI's `openspec` job, the `npm ci` step of `.claude/hooks/session-start.sh` and the setup steps in the README and `CONTRIBUTING.md` would change, and so would the answers of T35 and T66, the npm registry's row in `docs/how-it-works.md` and `CLAUDE.md`'s line on the generated skills. DR-043, whose `ci` job needs the `openspec` job, and DR-071 would be revisited. OpenSpec is used only in development and is outside the public surface, so the change would not be a breaking one for adopters.
