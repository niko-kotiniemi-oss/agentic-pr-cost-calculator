# DR-311: Every security fix ships as a release with a security advisory

- **Type:** process
- **Boundary:** outgoing
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-11-24
- **Requirements:** R303, R318
- **Threats:** T318, T328
- **Replaces:** none
- **Closed by:** none

## Context

`SECURITY.md` tells adopters that a fix of a vulnerability ships as a release with an advisory, but no requirement held it, so a fix could reach a release whose text says nothing, and an adopter would have no reason to update.

## Decision

Each fix of a vulnerability in released code reaches the default branch without a public pull request, through the temporary private fork of its repository security advisory, with an entry under `### Security` that the owner writes, and ships in a release, after which the owner publishes the advisory, which names the affected releases and the commit that fixes it (R303). Each entry gives the advisory's identifier in full, in text that the release page shows, linked to this repository's advisory page, and the release workflow, and CI on each pull request that changes the changelog's `## [Unreleased]` section, fail and name an entry that does not (R318).

## Alternatives

- Advisories for medium or higher only: a low finding would ship with nothing that tells adopters, and `SECURITY.md` would promise less.
- No requirement: the promise would rest on memory.

## Consequences

- The owner writes and publishes each advisory; an agent never posts a finding of a vulnerability in released code.
- The check reads the changelog only, so whether the advisory exists and says what it should rests on the owner, and a fix filed under another section, or under none, is not caught.
- How the path through the temporary private fork meets the ruleset's required `ci` check is checked by the owner at the first security fix.

## Scope

This covers how a security fix is announced. How vulnerabilities are reported is `SECURITY.md`.

## What reversing it would change

How hard it is to reverse: reversible. R303 and the release workflow's check would change, and `SECURITY.md`.
