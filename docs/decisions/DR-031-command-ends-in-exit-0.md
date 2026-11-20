# DR-031: The registered command ends in `; exit 0`

- **Type:** technical
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R13
- **Threats:** T14
- **Replaces:** none
- **Closed by:** none

## Context

Claude Code runs a hook's command in `sh`, in Git Bash on Windows, and in PowerShell on Windows without Git Bash, and a `PreToolUse` or `Stop` hook that exits with code 2 blocks the agent's command or sends the agent back to work (see the design's context). A capture hook that did either by accident would steer the agent (T14).

`exit 0` matters because Python exits 2 when it cannot start as asked, as when it does not know an option, which a `PreToolUse` hook turns into a blocked commit and a `Stop` hook into "keep working", and the command has to exit with success whatever Python exits with, or when there is no `python3` to start. It ends the command, rather than `|| true`, because Claude Code runs the command in PowerShell on Windows without Git Bash, where Windows PowerShell 5.1 does not read `||` and there is no `true` command, while `sh`, Git Bash and PowerShell all read `;` and `exit 0`.

## Decision

The command that an adopter registers for the hook is a shell command that ends in `; exit 0`, so that it exits with success in `sh`, Git Bash and PowerShell, whatever Python exits with.

## Alternatives

- Registering the command in exec form, which Claude Code's documentation prefers for a command that names a path placeholder, but which has no shell to turn Python's exit code 2 into success.
- Ending the command in `|| true`, which Windows PowerShell 5.1 cannot run, for the reasons that the context gives.

## Consequences

- A hook file that cannot be read or started, or a machine without `python3`, never blocks a commit or keeps the agent working, in any of the three shells (R13).
- Task 2.3 runs the command in each of those shells.
- A run that fails shows nothing, since Claude never sees the standard error of a hook that exits 0, so the calls that the script refuses are counted in the ledger instead (the design's risk "[Capture fails without anyone seeing it, since a hook that succeeds shows nothing]").

## Scope

This covers how the registered command ends. When the command runs the hook file at all is DR-058 (The hook file runs only when its checksum matches), and which Bash commands it runs around is DR-030 (The Bash hooks run only for commands that run git).

## What reversing it would change

R13 in `usage-capture` would change, with its scenarios "Capture never asks the agent to continue" and "The registered command succeeds in PowerShell", and so would the command in the design's decision 1 and in the README, where task 2.3 documents it, the capture flow in `docs/how-it-works.md`, T14's answer and task 2.3. Since the command's form is part of the public surface, the change would be released as a new major version (DR-096), and DR-058, whose check the command carries, would be revisited.
