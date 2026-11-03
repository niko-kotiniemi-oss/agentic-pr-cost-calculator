# Usage capture

While a Claude Code session works in the repository, a hook records what each model call spent, and the agent's own commits carry those records to the pull request. Nothing is sent anywhere: the records stay on the machine until a commit takes them.

**Status:** designed, not built yet.

**Spec:** `usage-capture`

**Requirements:** R2, R75, R41, R42, R43, R44, R45, R111, R3, R76, R5, R7, R78, R46, R47, R8, R79, R80, R81, R82, R83, R84, R85, R86, R48, R112, R49, R50, R51, R9, R87, R52, R113, R114, R115, R116, R117, R11, R12, R53, R54, R118, R13, R88, R89, R90, R55

## Expected behaviour

- **What is recorded.** For each model call, once: its UTC day, its model, a hash of its message id, whether the main agent or a subagent made it, and its input, output, cache-write and cache-read tokens. Where the transcript gives them, it also records the attributes that change the price: service tier, speed, inference region and server-side tool requests.
- **Where from.** Only calls made while Claude's working directory is in this repository or one of its worktrees. Calls made from anywhere else, including another repository that the same session works in, are not recorded here, and neither is a call whose transcript lines give no working directory.
- **When.** The hook runs when Claude finishes responding, when a subagent finishes, when a turn ends in an API error, when the session ends, and before and after each Bash command that runs git.
- **How it reaches the pull request.** Just before the agent's `git commit`, the hook writes the waiting calls into one new ledger file and stages it, so that the commit takes it. It does this only for a commit whose branch and contents it can tell from the command. Otherwise the calls wait for a later commit.
- **When no commit takes the file.** If the commit fails, is refused, is cancelled or never runs, the hook takes the file back, and its calls wait for a later commit.
- **Removed calls stay removed.** Once a run has found a commit holding a ledger file, the hook never stages that file's calls again in that clone, so a ledger file removed after that takes its calls with it.
- **Counts are checked.** A count that is not a whole number within the documented ceiling is refused, and the ledger says how many calls were refused.
- **Two runs at once.** Runs at the same time, such as a session's and a subagent's, never split each other's records or record one call twice.
- **It never gets in the way.** A failure in the hook never stops the session. The hook prints nothing that Claude reads, writes no transcript text anywhere, and stops at a time budget, leaving the rest for its next run.

## Not covered

- Commits the hook cannot follow: `git merge`, `git cherry-pick`, `git rebase --continue`, a script, an API, a commit in the background, in a pipeline, a subshell or a group, joined by `||` or behind a wrapper, and commits made through Claude Code's PowerShell tool. Their calls wait, and may reach no pull request. The design's risks list every such case.
- Agents other than Claude Code.

## How it is validated

This feature is validated first by its spec's scenarios: each gets an acceptance test before its code, seen to fail for the expected reason (task 1.4). Then come the checks that DR-084 to DR-093 and DR-109 apply to all the tool's code. Beyond those, this feature has its own:

- Synthetic transcripts and hook inputs in each shape that Claude Code writes, with the lines for refused, blocked, cancelled and interrupted commands checked against what Claude Code writes for them (task 1.1).
- Unit tests at every boundary of the counts, and property tests that no planted string reaches the ledger and that a second run changes nothing (task 2.1).
- Tests against real git of the commits that the hook follows and of those it does not, refused, cancelled and interrupted ones included (task 2.2).
- What the README's section on adopting the tool says about how git treats a ledger file, tested with the CI runner's git and, in a CI job of its own, with git 2.43 (task 4.4).
- The hook run from another directory and in each shell that its registered command meets, Windows PowerShell included (task 2.3).

## See also

- `usage-capture` in `openspec/` for the full requirements and their scenarios.
- Design decision 1 of `add-pr-cost-calculator`, and its risks.
