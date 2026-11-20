# DR-034: Capture stages only for a commit whose branch and contents it can tell

- **Type:** technical
- **Boundary:** inside
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R8, R48, R49, R82, R83, R86, R112
- **Threats:** T8, T10, T19
- **Replaces:** none
- **Closed by:** none

## Context

The run that stages the ledger file has only the text of the whole command, before any of it runs (DR-013). From that text it cannot know what files an earlier part of the command will stage, where a commit after an arbitrary command will land, or when a commit sent to the background will run, and substitutions and here-documents whose delimiter is not quoted run commands of their own before the commit (T10). A file staged for the wrong branch takes its calls into the wrong pull request (T19), and a commit that leaves the file out, or that git writes as something other than its entries, loses them (T8).

## Decision

Capture stages a ledger file only for a commit whose branch and contents it can tell from the command's text, and for any other command stages nothing and lets the calls wait for a later commit. It can tell them for a top-level `git commit` in the foreground, not in a pipeline, joined to the others by a double ampersand, a semicolon or line breaks, after nothing but `cd` to a path written in the command and git's `add`, `rm`, `mv`, `status`, `diff`, `log` and `show`, in a worktree that it finds from the hook's input and the command's text, when the commit names no paths and no attribute gives the ledger path a filter or a working-tree encoding. A command or process substitution counts as a command before the commit unless all it runs is `cat` reading a here-document whose delimiter is quoted, and a here-document whose delimiter is not quoted, in or before the commit, means nothing is staged.

## Alternatives

None were recorded when this was decided.

## Consequences

- The calls wait when the agent commits in the background, in a pipeline, a subshell or a group, joined to another command by `||`, behind a wrapper such as `timeout`, after a command other than those listed, or with a message that another command writes, so they may reach no commit (the design's risk "[Some calls reach no commit]"; T8).
- A command that capture stages for can still run a program that git's own options or environment variables name, as a commit run with git's option `-c core.hooksPath` naming another hooks folder can, and a change of branch that such a program makes takes the staged file to the other branch (the design's risk "[A call is recorded on the branch checked out when it is recorded, which can differ from the one it was made on]"; T19).
- Where the ledger path has a filter or a working-tree encoding, no call reaches a commit, and the comment says that no agent usage was recorded (the design's risk "[A repository's settings act on the ledger path]").

## Scope

This covers which commits capture can follow. When it stages is DR-013 (A ledger file is staged just before a commit that capture can follow), what it leaves alone in a commit, and that it stages nothing after a `git rm` or `git mv` that may reach the ledger folder, is DR-035 (Capture never changes what the agent's commit would do), and commands sent through the PowerShell tool are DR-007 (Commands sent through the PowerShell tool are out of scope).

## What reversing it would change

R8, R48, R49, R82, R83, R86 and R112 in `usage-capture` would change, with their scenarios. The design's decision 1 and its risks, the answers and residuals of T8, T10 and T19, the commit flow in `docs/how-it-works.md`, the usage-capture feature page, the README's list of the calls that reach no commit (task 4.4) and task 2.2 would change too. Nothing on the design's public surface would change. DR-013 and DR-035 would be revisited.
