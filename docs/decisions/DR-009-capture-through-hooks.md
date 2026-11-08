# DR-009: Capture reads the transcripts through hooks while the session runs

- **Type:** architecture
- **Status:** closed
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-17
- **Requirements:** R7, R13, R44, R90
- **Threats:** T8, T14, T40, T42
- **Replaces:** none
- **Closed by:** DR-172

## Context

Claude Code writes each session's transcript, with every call's model and usage, as JSON lines on the session's machine, and it runs hooks at set points of the session, each given the transcript's path (see the design's context). A cloud session's machine is thrown away when the session ends, taking the transcript with it, and reading transcripts afterwards proved slow for a long pull request (see the design's context; T8).

## Decision

Capture is one script that Claude Code runs as a hook while the session runs, registered for `Stop`, `SubagentStop`, `StopFailure` and `SessionEnd`, and for `PreToolUse`, `PostToolUse` and `PostToolUseFailure` on Bash commands. Each run reads the session's transcript, and its subagents' transcripts, on from where the previous run stopped.

## Alternatives

- Reading transcripts after the session through an API, which is slow and depends on access a CI job does not have.

## Consequences

- The hook runs inside the person's session, where a run that failed or took long could block a commit, send the agent back to work or hold the session up (R13, T14). The registered command always exits with success (DR-031), and each run stops at a time budget and leaves the rest for a later run (R90).
- Claude Code writes the transcript asynchronously, so a run reads only the lines that end in a line break (R44, T42). The call that runs the agent's last commit on a branch may not yet read as over when that commit's run reads the transcript, and it then reaches no pull request (the design's risk "[Some calls reach no commit]"; T8).
- Capture sees only what the transcripts hold, so model calls that Claude Code makes for its own tools without recording them there are left out, and the comment, and the README's section on adopting the tool that task 4.4 writes, say so rather than estimating them (the design's risk "[Claude Code makes model calls for its own tools, such as WebFetch, that the session's transcript does not record]"; T40).
- Capture rests on Claude Code's hooks and transcripts behaving as documented and as observed, which the threat model lists among its assumptions. Task 1.1's fixtures carry every shape seen, so that a change of format fails a test (the design's risk "[Claude Code changes its transcript format]").

## Scope

This covers where and when capture reads usage. Which Bash commands start it is DR-030 (The Bash hooks run only for commands that run git), how its command ends is DR-031 (The registered command ends in `; exit 0`), how usage reaches the pull request is DR-010 (Usage travels inside the agent's own commits), and delivering the script as a copied file is DR-022 (Adopters copy the hook file from a pinned commit).

## What reversing it would change

R7, R13, R44 and R90 in `usage-capture` would change, with their scenarios, and so would the hook registration that tasks 2.3 and 4.4 document in the README. The registered command is part of the public surface, so the change would be a breaking one for adopters (DR-096). The design's decision 1 and its context, the answers of T8, T14, T40 and T42, the parts table and the capture flow in `docs/how-it-works.md`, the usage-capture feature page and tasks 2.1 and 2.3 would change too, and DR-010, DR-013, DR-014, DR-030, DR-031, DR-128 and DR-130 would be revisited.
