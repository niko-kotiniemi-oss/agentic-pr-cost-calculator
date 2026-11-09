# DR-059: The hook starts only git, by absolute path, from a safe folder

- **Type:** security and privacy
- **Status:** closed
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R54, R118
- **Threats:** T46
- **Replaces:** none
- **Closed by:** DR-188

## Context

Hooks run in Claude's current directory, which is usually in the repository, and on Windows a program started by a name alone is looked for in the current directory before the system's folders and those that `PATH` names (see the design's context). So a `git.exe` in a folder that Claude has moved into, such as an extracted archive or a third-party clone, would run at the next git command or turn end, even for people who never opted in (T46). Python's isolated mode covers only what Python imports (T15).

## Decision

The hook starts no program other than git. It looks for git only in the folders that the absolute entries of `PATH` name, and starts it by that absolute path from a current directory that only the system's administrator can write, such as `/` or Windows' system folder, naming the folder that each git command works in with `-C`.

## Alternatives

None were recorded when this was decided.

## Consequences

- A program named `git` that is planted in Claude's current directory, in the repository's folder or in a folder named by a relative entry of `PATH` is never the one started (R54), and task 2.3 plants one in each on a Windows runner.
- A run that finds capture off still starts git, by the same absolute path, to note that in its store and to take back and put back ledger files, which T46's residual accepts (R118).

## Scope

This covers which programs the hook starts, and from where. A Python module planted beside the hook is kept out by DR-125 (The hook runs in Python's isolated mode), and what the git commands that the hook starts may reach over the network is DR-060 (The hook opens no network connection).

## What reversing it would change

R54 in `usage-capture` would change, with its scenario "A program planted in the current directory is not run", and so would R118, whose scenario "A run that finds a switch off starts git only for its store" holds that every program such a run starts is git, the design's decision 1, T46's answer and residual, and tasks 2.1 and 2.3, which build and test the lookup.
