# Turning it on, and personal opt-in

Two switches decide whether anything is recorded. The repository decides whether the tool is used there, and each person decides whether their own sessions' usage is published.

**Status:** designed, not built yet.

**Spec:** `switch-and-opt-in`

**Requirements:** R1, R36, R37, R103, R104, R105, R38, R106, R39, R40, R107, R108, R109, R110, R19, R91, R92, R93

## Expected behaviour

- A repository turns the tool on by adding `.pr-cost.json` at its root with `enabled` set to true, and off by removing the file or setting `enabled` to false.
- A person turns capture on for themselves by setting `pr-cost.capture` to `true` in their global git configuration: `~/.gitconfig`, or git's file in their XDG configuration folder. Nothing in a repository can turn it on for them, so an outside contributor's usage is never committed because a repository's owner turned the tool on.
- Setting `pr-cost.capture` to `false` in one repository's own git configuration turns capture off there. Setting it to `true` there opts no one in.
- Capture records nothing unless both switches are on. Each run notes in the store, inside the git common directory, whether it found both on, at a time read from the system's clock in UTC, which no setting of the session's environment can move, and only calls made while both were on are recorded: calls made before a person opts in, or while capture was off, are never recorded later, and calls recorded before an opt-out are not staged after it. A ledger file staged before capture was turned off is still taken back.
- `pr-cost.capture` opts a person in only as `true`, `yes`, `on`, `1` or the bare key. Any other value, including ones that git itself reads as true, such as `2`, does not.
- The report reads `.pr-cost.json` from the default branch as it was before the merge and as it is after, and runs when either turns the tool on. So a pull request cannot turn off its own report, and the pull request that turns the tool on gets one.
- A pull request that changes `.pr-cost.json`, any workflow file or the hook file has that change flagged in its comment.

## How it is validated

This feature is validated first by its spec's scenarios: each gets an acceptance test before its code, seen to fail for the expected reason (task 1.4). Then come the checks that DR-084 to DR-093 and DR-109 apply to all the tool's code. Beyond those, this feature has its own:

- Tests that try each way that a repository or its environment could opt a person in, and check that capture stays off: the repository's own git configuration, git's environment variables, an included file, and a relative configuration folder (task 2.4).
- Tests that the report reads `.pr-cost.json` from before and after the merge, including a file that a pull request makes unreadable (task 4.1).

## See also

- `switch-and-opt-in` in `openspec/` for the full requirements and their scenarios.
- Design decision 6 of `add-pr-cost-calculator`.
