# DR-173: Capture keeps operational metadata on the person's machine only where it needs it, and never publishes it

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the owner, 2026-11-02
- **Requirements:** R4, R89, R149
- **Threats:** T4, T109
- **Replaces:** none
- **Closed by:** none

## Context

To tell a call's worktree and branch, record it once, take back the ledger file of a command that was interrupted and clean up safely, the capture step needs, between runs, the worktree and branch of each call, a session's id, a transcript's path and a command's `tool_use_id` (see the design's decision 1). The design noted them in the store without saying what the store holds field by field, and T4's residual said that no scenario stated everything that the store notes.

## Decision

The owner decided on 2026-11-02 that capture keeps worktree and branch information, session ids, transcript paths and `tool_use_id` values on the person's machine only where it needs them for attribution, deduplication, recovery from an interrupted command or safe cleanup, and never publishes them: not in a ledger file, a comment, a CI artifact or a diagnostic. The store's schema, each field's purpose, its protection, its retention and cleanup, and what an opt-out does to it are specified, with as few identifiers as capture can work with, kept for as short a time as it needs them, and no transcript is copied.

## Alternatives

- Keeping these values in plain text for as long as the store lasts, as the design allowed before, which keeps more for longer than capture needs.
- Keeping none of them, which would leave capture unable to tell which worktree, branch and command a staged ledger file belongs to, and so unable to take it back.

## Consequences

- The store's fields and their purposes are the design's decision 15: its ids are hashes and its plain paths last only while a ledger file needs them (DR-174), it keeps nothing past its retention window (DR-175), it is its owner's alone (DR-176), and it keeps no transcript (DR-178).
- A ledger file holds none of these values, nor a hash of one (R4), and standard error carries nothing from the store (R89).

## Scope

This covers what operational metadata capture may keep, and where it may go. What a ledger entry holds is DR-045 (Ledger entries hold counts, never content), DR-053 (An entry records no session value) and DR-136 (Only a hash of a call's message id is kept).

## What reversing it would change

R149 in `usage-capture` and R4 in `ledger` would change, with their scenarios, and so would R89's scenario on the store, the design's decisions 1 and 15, T4's answer and residual, T109, and tasks 1.1 and 2.1. The store's format is part of the public surface, so the change would be a breaking one for adopters (DR-096).
