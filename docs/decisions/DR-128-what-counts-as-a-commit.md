# DR-128: Only git's commit subcommand counts as a commit, and a dry run does not

- **Type:** technical
- **Boundary:** incoming
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R79, R80
- **Threats:** T8, T10
- **Replaces:** none
- **Closed by:** none

## Context

Capture stages a ledger file in the `PreToolUse` run before a Bash command that runs `git commit` (DR-013), and that run has only the command's text. That text can name a commit without running one, as `grep 'git commit' notes.txt` does, git takes options of its own before its subcommand, as in `git -c user.name=x commit -m y`, and a dry run commits nothing, though its options can be abbreviated, combined with other short options or undone by a later option (see the design's decision 1). A commit that capture missed would carry none of its calls (T8), and a command wrongly taken for one would leave a staged file that no commit takes (T10).

## Decision

Capture treats a command as running `git commit` only when one of the commands that it is made of is `git`, with or without git's own options, followed by the `commit` subcommand, and that commit is not a dry run. A commit is a dry run when any of `--dry-run`, `--short`, `--porcelain`, `--long`, `-z` and `--null`, in any spelling that git accepts, is still in effect once git has read all of its options, where the `--no-` form of any of `--short`, `--porcelain` and `--long` clears all three.

## Alternatives

None were recorded when this was decided.

## Consequences

- A commit given git's own options first, or one whose dry-run option a later option undoes, as in `git commit -z --no-null -m x`, still carries a ledger file (T8).
- A command that only names `git commit`, in quotes or as another command's argument, stages nothing, and neither does a dry run in any spelling, so no file waits in the index for a commit that never comes (T10).

## Scope

This covers which commands capture takes to run `git commit`. When the ledger file is staged for one is DR-013 (A ledger file is staged just before a commit that capture can follow), which of those commits capture stages for is DR-034 (Capture stages only for a commit whose branch and contents it can tell), and which Bash commands start the hook at all is DR-030 (The Bash hooks run only for commands that run git).

## What reversing it would change

R79 and R80 in `usage-capture` would change, with their scenarios, among them "A command that only names a commit stages nothing" and "A dry-run option that a later option undoes is still a commit". The design's decision 1, the answers of T8 and T10, the commit flow in `docs/how-it-works.md` and tasks 1.1 and 2.2 would change too, and DR-013 and DR-034 would be revisited. Which commands count as a commit is not part of the public surface (DR-154), so that change alone would not be a breaking one for adopters (DR-096).
