# DR-310: Capture's git commands refuse every transport, and the git floor stays at 2.43

- **Type:** technical
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-11-24
- **Requirements:** R111
- **Threats:** T45
- **Replaces:** none
- **Closed by:** none

## Context

The capture step must fetch nothing that a partial clone lacks. `GIT_NO_LAZY_FETCH` stops it from git 2.43.4, 2.44.1 and 2.45.0 on, but a plain git 2.43.0 to 2.43.3 or 2.44.0, which the floor of 2.43 admits, ignores it (T45). Raising the floor would refuse Ubuntu 24.04's git 2.43.0, which carries the fix as a backport.

## Decision

Every git command that the capture step runs also runs with `-c protocol.allow=never`, and with `-c protocol.<name>.allow=never` for `file`, `git`, `ssh`, `http`, `https` and `ext` and for each protocol that a `protocol.<name>.allow` key of git's configuration names, since such a key, set to `always` in the repository's or the person's configuration, overrides `protocol.allow` on the command line; so git refuses each transport that it knows by those names, and the git floor stays at 2.43 (R111). On git 2.43.0, a partial clone's missing blob stayed missing and git exited with an error, as the evidence of 2026-11-24 records.

## Alternatives

- Raising the git floor to 2.43.4: it would refuse Ubuntu 24.04's git, which is safe.
- A check of git's build: `git --version` prints the same version for builds that differ (T86).

## Consequences

- A git command that would need a missing object fails, and the step skips that file, as it skips one whose blob the clone lacks (R45).
- A transport that git knows by a name that neither the list nor the configuration gives is not refused by name; `GIT_ALLOW_PROTOCOL`, which would also widen what git allows, is one of the session's `GIT_` variables, which the step does not pass to git.

## Scope

This covers how capture's git commands stay offline. The floors themselves are R32's.

## What reversing it would change

How hard it is to reverse: reversible. R111 and its scenarios would change, and T45's answer would rest on the floor again.
