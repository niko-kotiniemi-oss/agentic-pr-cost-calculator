# DR-003: Claude Code is the only agent `add-pr-cost-calculator` captures

- **Type:** scope
- **Boundary:** incoming
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the owner, 2026-10-27
- **Requirements:** R7, R13, R76
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

Capture depends on how one agent works. It reads the transcripts that Claude Code writes, and it runs from the hooks that Claude Code calls during a session, with the input that those hooks receive (see the design's context). The trial that confirmed the data exists was run on real Claude Code sessions (see the proposal's "Why").

## Decision

`add-pr-cost-calculator` captures the usage of Claude Code sessions only, and leaves agents other than Claude Code out of its scope. The ledger format is to be written down in `docs/ledger-format.md` by task 1.2, so that other agents can write it in a later change.

## Alternatives

None were recorded when this was decided.

## Consequences

- The usage-capture feature page lists agents other than Claude Code as not covered.
- Capture rests on Claude Code's hooks and transcripts behaving as the threat model's assumptions state, and a change to the transcript format would make its fixture tests fail (the design's risk "[Claude Code changes its transcript format]").
- Other agents, such as Gemini or Codex, come in later versions, as the owner said on 2026-10-27, each added by a record that replaces this one.
- The README lists agents other than Claude Code near its top among what this first version does not support.

## Scope

This covers which agent's sessions `add-pr-cost-calculator` captures. Commands that Claude Code sends through its PowerShell tool are DR-007 (Commands sent through the PowerShell tool are out of scope), and when and how capture reads Claude Code's transcripts is DR-009 (Capture reads the transcripts through hooks while the session runs).

## What reversing it would change

Capturing another agent would change R7, R13 and R76 in `usage-capture`, which are written for Claude Code's hook events, for the shells that it runs a hook's command in and for the project directory that it gives the hook, and it would add requirements for the other agent's records. The design's non-goals, the proposal's "What Changes" and "Impact", the README's list of what this first version does not support, the usage-capture feature page, `docs/how-it-works.md`, the threat model's assumptions about Claude Code, and tasks 1.1 and 2.1 to 2.3, which build capture on Claude Code's transcripts and hooks, would change too, and DR-009 and DR-022 would be revisited. Added behaviour alone would raise the minor number, while a change to the public surface, such as the ledger format, would be a breaking one for adopters (DR-096).
