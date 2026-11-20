# DR-021: One file, `.pr-cost.json`, turns the tool on or off

- **Type:** architecture
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-17
- **Requirements:** R1, R19, R36, R91
- **Threats:** T49
- **Replaces:** none
- **Closed by:** none

## Context

Whether the tool is used in a repository is the repository's choice, beside each person's own opt-in (DR-046). Capture, where a session runs, and the report, after a merge, both read that choice, and the report counts the pull request being reported among its untrusted inputs (see the design's goals). A file is visible in review and versioned with the code.

## Decision

A repository turns the tool on by adding `.pr-cost.json` at its root with `enabled` set to true, and off by removing the file or setting `enabled` to false. Capture reads the copy in the working tree where the session works.

## Alternatives

None were recorded when this was decided.

## Consequences

- Turning the tool on or off is a pull request like any other, so the change is in its diff, and its comment flags it (DR-064).
- Capture follows the working tree: where the file there turns the tool off, capture records nothing, even when the commit checked out holds one that turns it on (R91).
- Capture reads the file only as a regular file within its documented size bound, and takes any other, or one that is not valid, as leaving the tool off, so a named pipe in the working tree cannot hold a run up (R36, T49).

## Scope

This covers what turns the tool on or off, and where capture reads it. Each person's consent is DR-046 (Each person turns on capture of their own sessions), how the report reads the file, at the commits before and after the merge, and when it then runs is DR-051 (A pull request cannot turn off its own report), and the hook's path, which the file does not hold, is DR-065 (The hook's path is fixed, not a setting).

## What reversing it would change

R19, R36 and R91 in `switch-and-opt-in` would change, with their scenarios, and so would R1's scenario "No configuration file means no capture". So would the design's decision 6 where it describes the file, T49's answer, the proposal, the README, the `switch-and-opt-in` feature page, `docs/how-it-works.md`, and tasks 1.2, which documents the file in `docs/ledger-format.md`, and 2.4. The configuration file is part of the public surface, so the change would be a breaking one for adopters (DR-096). DR-051, which reads the file at the two commits, DR-064 and DR-065 would be revisited.
