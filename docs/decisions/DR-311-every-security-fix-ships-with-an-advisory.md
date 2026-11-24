# DR-311: Every security fix ships as a release with a security advisory

- **Type:** process
- **Boundary:** outgoing
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-11-24
- **Requirements:** R303
- **Threats:** T318
- **Replaces:** none
- **Closed by:** none

## Context

`SECURITY.md` tells adopters that a fix of a vulnerability ships as a release with an advisory, but no requirement held it, so a fix could reach a release whose text says nothing, and an adopter would have no reason to update.

## Decision

Each fix of a vulnerability in released code ships in a release whose changelog entry, under `### Security`, names the repository security advisory that describes it by its `GHSA-` identifier, and that advisory names the affected releases and the commit that fixes it. The release workflow publishes no release whose changelog has a line under `### Security` that names no advisory (R303).

## Alternatives

- Advisories for medium or higher only: a low finding would ship with nothing that tells adopters, and `SECURITY.md` would promise less.
- No requirement: the promise would rest on memory.

## Consequences

- The owner writes and publishes each advisory; an agent never posts a finding of a vulnerability in released code.
- The check reads the changelog only, so whether the advisory exists and says what it should rests on the owner.

## Scope

This covers how a security fix is announced. How vulnerabilities are reported is `SECURITY.md`.

## What reversing it would change

How hard it is to reverse: reversible. R303 and the release workflow's check would change, and `SECURITY.md`.
