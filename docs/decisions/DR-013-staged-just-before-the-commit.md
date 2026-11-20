# DR-013: A ledger file is staged just before a commit that capture can follow

- **Type:** architecture
- **Boundary:** inside
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R8, R49, R51
- **Threats:** T8, T10
- **Replaces:** none
- **Closed by:** none

## Context

A ledger file reaches the pull request only if the agent's commit holds it (DR-010), while a file left staged between commits gets in the way of git work, as staging at every turn's end did in an earlier version (DR-011; T10). A `PreToolUse` run sees a Bash command's text and `tool_use_id` before the command runs and before any permission prompt, and it can run twice for one command, as for a deferred call that is resumed (see the design's context).

## Decision

Capture stages the ledger file in the `PreToolUse` run before a Bash command that runs `git commit` in this repository (DR-128), after that run has read the transcripts, when the commit is one it can follow (DR-034). The command runs as Claude wrote it, and capture installs no git hook.

## Alternatives

- Staging the file inside the command, by having the `PreToolUse` run rewrite it through `updatedInput`, so that a command that never runs stages nothing, which changes the command that the person and their permission rules then approve.
- A `pre-commit` git hook, which would sit beside the repository's own git hooks and run for every commit, not just the agent's.

## Consequences

- The file is staged before the command is approved or runs, so a refused, blocked, cancelled or interrupted commit leaves it staged until a later run takes it back (DR-014; the design's risk "[A commit is refused, blocked, cancelled or interrupted after its ledger file was staged]"; T10).
- A git command that starts while the file is being staged fails at the index lock (the design's risk "[A git command starts while a run stages or takes back a ledger file]").
- The run knows only the command's text, so the worktree comes from the current directory in the hook's input, followed through the command, never from where the hook runs (R49).
- A run that comes again for the same command stages nothing new while its file is still staged and its branch checked out (R51).
- A commit made by `git merge`, `git cherry-pick` or `git rebase --continue`, by a script or through an API gets no ledger file, and its calls wait (the design's risk "[Some calls reach no commit]"; T8).

## Scope

This covers when the ledger file is staged. What counts as a command that runs `git commit` is DR-128 (Only git's commit subcommand counts as a commit, and a dry run does not), adding the file despite ignore rules and sparse checkouts is DR-129 (A ledger file is added despite ignore rules and sparse checkouts), which commits it is staged for is DR-034 (Capture stages only for a commit whose branch and contents it can tell), what the commit otherwise does is DR-035 (Capture never changes what the agent's commit would do), and taking back a file that no commit took is DR-014 (A ledger file that no commit took is taken back).

## What reversing it would change

R8, R49 and R51 in `usage-capture` would change, with their scenarios. The design's decision 1 and its risks, the answers of T8 and T10, the commit flow in `docs/how-it-works.md`, the usage-capture feature page, and tasks 2.2 and 2.3, which build the staging and its registration, would change too. A git hook in its place would be something that existing adopters had to install, so that change would be a breaking one (DR-096). DR-014, DR-034, DR-035, DR-128 and DR-130 would be revisited.
