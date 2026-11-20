# DR-030: The Bash hooks run only for commands that run git

- **Type:** technical
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R7
- **Threats:** T8, T19
- **Replaces:** none
- **Closed by:** none

## Context

The runs around Bash commands stage a ledger file before a commit, take it back after (DR-013, DR-014), and record the calls that are over before a command can change the branch (DR-012). Claude Code lets a hook on a tool event carry an `if` condition, written in permission-rule syntax, which it checks against each command that a Bash input is made of, matching git only as Claude wrote it, and it runs the hook anyway when it cannot tell what an input runs (see the design's context).

## Decision

The `PreToolUse`, `PostToolUse` and `PostToolUseFailure` hooks are registered for Bash with the condition `Bash(git *)`, so that around Bash commands the script starts only for one that runs git as Claude wrote it, or one whose commands Claude Code cannot tell. The `Stop`, `SubagentStop`, `StopFailure` and `SessionEnd` hooks carry no condition, since a hook with one never runs on those events.

## Alternatives

- Registering the Bash hooks with no condition, which would also run around git written in forms that the condition does not match and around scripts that change the branch, but would start the script before and after every Bash command the agent runs.

## Consequences

- Git run by its path, through `sh -c`, `env` or an environment runner, or through a shell alias or function does not match, so a commit made that way gets no ledger file and its calls wait (the design's risk "[Some calls reach no commit]"; T8).
- A change of branch that no matching command makes, as by a script or the person, sends the calls recorded before it to the branch checked out next (the design's risk "[A call is recorded on the branch checked out when it is recorded, which can differ from the one it was made on]"; T19).
- A Bash command that runs no git starts no run.

## Scope

This covers which Bash commands start the script. Which of them capture stages for is DR-034 (Capture stages only for a commit whose branch and contents it can tell), and commands sent through Claude Code's PowerShell tool, which no Bash hook sees, are DR-007 (Commands sent through the PowerShell tool are out of scope).

## What reversing it would change

R7 in `usage-capture` would change, with its scenarios, and so would the registration that tasks 2.3 and 4.4 document in the README. Existing adopters would have to change their registration, and a change that they have to act on is a breaking one (DR-096). The design's decision 1 and its risks, the answers and residuals of T8 and T19, the commit flow in `docs/how-it-works.md`, the usage-capture feature page and task 2.3, whose test holds the condition, would change too, and DR-009 and DR-034 would be revisited.
