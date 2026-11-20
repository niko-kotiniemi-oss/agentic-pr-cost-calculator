# DR-126: Development dependencies are locked with hashes

- **Type:** security and privacy
- **Boundary:** incoming
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** none
- **Threats:** T28, T66
- **Replaces:** none
- **Closed by:** none

## Context

The development tools run in CI and in cloud sessions, whose start-up hook installs them from the session's branch with the owner's account, so a compromised one would run with the owner's credentials (T66). Adopters never run them (DR-025). A tool pinned to an exact version still leaves its own dependencies free, and a dependency that is not locked resolves to its newest release at every session start, outside Renovate's wait (T66).

## Decision

Every development dependency, each tool's own dependencies included, is locked to an exact version and a hash, and CI and sessions install only what the lock holds: the Python tools with pip's `--require-hashes` (task 1.8), and the Node packages that OpenSpec needs with `npm ci` from `package-lock.json`.

## Alternatives

None were recorded when this was decided.

## Consequences

- The Node half is in place: `package-lock.json` gives OpenSpec and every package it needs a SHA-512 integrity value, and CI's `openspec` job and the session hook install them with `npm ci`.
- The Python half is task 1.8, still open. `requirements-dev.txt` pins the tools themselves to exact versions without hashes, and CI's `python` job and the session hook install it with a plain `pip install -r`, so until the task is done the tools' own dependencies are not locked (T66's residual).
- Once locked, a dependency changes only when its lock does, so a new release reaches CI and sessions only from a branch that changes the lock. A session started on a dependency-update branch would still install what that branch locks, which `CLAUDE.md`'s rule on such branches answers (T66, DR-145).

## Scope

This covers CI and the cloud sessions that `.claude/hooks/session-start.sh` sets up; a local clone follows the README's setup, run by hand. Which OpenSpec version is pinned is DR-042 (OpenSpec is pinned and its skills are regenerated in CI), Superpowers, vendored by commit, is DR-041 (Superpowers is vendored and compared with upstream in CI), and when Renovate proposes updates is DR-028 (Renovate waits 14 days, and proposes vulnerability fixes at once) and DR-111 (Major updates wait for the owner's approval).

## What reversing it would change

No requirement states this. T66's answer and residual and T28's answer would change, and so would task 1.8, `requirements-dev.txt` and its comment, the install steps in CI and in `.claude/hooks/session-start.sh`, and the design's decision 2, which names task 1.8's locking. DR-042, whose OpenSpec is installed from a hashed lock, would be revisited. The development tools are not part of the public surface, so the change would not be a breaking one for adopters.
