# DR-309: The tool reads no secret and keeps no transcript text

- **Type:** security and privacy
- **Boundary:** incoming
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the owner, 2026-10-27
- **Requirements:** R301
- **Threats:** T312
- **Replaces:** none
- **Closed by:** none

## Context

A transcript holds what a session said and saw, which can include passwords, tokens and keys, and the capture step runs where the person's environment and git configuration may hold more. The ledger holds counts only (R4), but nothing said what the step may read on the way.

## Decision

The capture step reads from a transcript only the fields that it records or needs to tell a call, and keeps, prints, logs and sends none of its other text. Neither the capture step nor the report reads a password, a token or a key, but the report's own token, from the environment, a file or git's configuration. A test plants a secret in a transcript, in the environment and in git's configuration, and fails when anything that the tool writes holds it (R301).

## Alternatives

- Filtering secrets out of what the tool keeps: a filter misses what it does not know, while reading nothing needs no filter.

## Consequences

- A field that a later change wants from a transcript is added by name, in a change of its own.

## Scope

This covers what the tool reads and keeps. What the ledger holds is the ledger's own records.

## What reversing it would change

How hard it is to reverse: reversible with work. R301 and its test would change, and the README's account of what the tool reads.
