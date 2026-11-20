# DR-007: Commands sent through the PowerShell tool are out of scope

- **Type:** scope
- **Boundary:** incoming
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the owner, 2026-10-27
- **Requirements:** R7
- **Threats:** T8, T19
- **Replaces:** none
- **Closed by:** none

## Context

Claude Code can send shell commands through a PowerShell tool instead of Bash. For claude.ai and Console accounts on Windows, that tool is on by default; on Windows without Git Bash it is always on, and it can be enabled on other systems too (see the design's non-goals). Capture tells whether a Bash command commits by reading it as the shell splits it, and its hooks around commands are registered for Bash, so they never run for commands sent through the PowerShell tool (see the design's decision 1). Supporting them would take a second parser, for PowerShell's syntax.

## Decision

Shell commands that Claude Code sends through its PowerShell tool, commits and changes of branch among them, are outside the scope of the change `add-pr-cost-calculator`.

## Alternatives

- Capturing commands sent through the PowerShell tool too, which would take hooks registered for that tool and a second parser, for PowerShell's syntax.

## Consequences

- A commit made through that tool gets no ledger file, so the calls waiting for a commit may reach none (the design's risk "[Some calls reach no commit]", T8).
- Capture misses a change of branch made through that tool, so calls not yet recorded go to the branch checked out next (the design's risk "[A call is recorded on the branch checked out when it is recorded, which can differ from the one it was made on]", T19).
- The hooks for the end of a turn, a subagent or a session are not tied to a tool, and on Windows without Git Bash they run in PowerShell, where the registered command still exits with success (DR-031).
- The README's section on adopting the tool, which task 4.4 writes, says that commits and changes of branch made through that tool are not seen.
- The README also lists these commands near its top among what this first version does not support, and a later version may support them, as the owner said on 2026-10-27.

## Scope

This covers shell commands sent through Claude Code's PowerShell tool. How the registered command succeeds in PowerShell is DR-031 (The registered command ends in `; exit 0`), and which Bash commands the hooks run around is DR-030 (The Bash hooks run only for commands that run git).

## What reversing it would change

Supporting that tool's commands would change R7 in `usage-capture`, which names the Bash commands that capture runs around, and would add requirements for PowerShell's syntax. The design's non-goals and decision 1, the two risks above, the residuals of T8 and T19, the proposal's "Impact", the usage-capture feature page, the README's list of what this first version does not support and its section on adopting the tool would change too, with tasks 2.2, 2.3 and 4.4, and DR-030 and DR-034 would be revisited. Added behaviour alone would raise the minor number, while a change to the public surface, such as the hook file's registered command, would be a breaking one for adopters (DR-096).
