# DR-046: Each person turns on capture of their own sessions

- **Type:** security and privacy
- **Status:** closed
- **Decided by:** the owner, 2026-10-18
- **Requirements:** R1
- **Threats:** T3
- **Replaces:** none
- **Closed by:** DR-202

## Context

When a repository's owner turns the tool on, the usage of everyone who works there, outside contributors who never agreed among them, could be committed and published with their pull requests (T3), and the ledger and the comment are as public as the repository (T31). In a public repository, publishing someone's usage needs their own consent.

## Decision

Capture records a session's calls only when the repository has turned the tool on and the person running the session has also turned capture on for themselves. The repository decides whether the tool is used there. Only the person decides whether their session's usage is published, so an outside contributor's usage is not committed merely because the repository's owner turned the tool on.

## Alternatives

- The repository's setting alone, which would publish the usage of everyone who works in the repository, including people who never agreed to it.

## Consequences

- Nothing is recorded unless both switches are on, so a pull request made without anyone's opt-in has no ledger, and its comment gives the CI cost and says that no agent usage was recorded (R20).
- A person's opt-in applies in every repository that has the tool on, until they turn it off in one (T3's residual, DR-050).
- The README's section on adopting the tool, which task 4.4 writes, says how each person opts in, before they start a session, and what a public repository publishes when the tool is on (T31).

## Scope

This covers whose consent capture needs. The repository's switch is DR-021 (One file, `.pr-cost.json`, turns the tool on or off). Where the person's opt-in is kept, `pr-cost.capture` in their global git configuration, is DR-048 (The opt-in is read only from the person's global git configuration), and how it is read and applied is DR-047 (Consent holds for each recorded call), DR-049 (The opt-in is read strictly) and DR-050 (A repository's git configuration can turn capture off, never on).

## What reversing it would change

R1 in `switch-and-opt-in` would change, with its scenarios, and so would the design's decision 6, T3's answer, T31's answer where it names how each person opts in, the proposal, the README, `SECURITY.md`, the `switch-and-opt-in` feature page, `docs/how-it-works.md`, and tasks 1.2, which documents the opt-in setting in `docs/ledger-format.md`, 2.4, 4.4 and 7.1. DR-047 to DR-050, with the requirements they shape, would be closed or revisited. The opt-in key is part of the public surface, so removing it would be a breaking change for adopters (DR-096).
