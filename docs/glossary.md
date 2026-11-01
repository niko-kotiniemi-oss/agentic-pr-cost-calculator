# Glossary

The words that the specs and the other pages use, each with its meaning and the words to avoid for it (R137, R138). Each meaning is one sentence, taken from the spec or the page that defines the word. Where a meaning differs from a requirement, a scenario or `CLAUDE.md`, those hold, and this page is corrected (DR-166). A word with several right senses is given with the sense that each document gives it, and the reviews check its uses.

A word to avoid is one that is wrong wherever a page uses it in prose. `tests/test_glossary.py` fails on each use of one, in any case and in its plural, outside inline code and fenced code blocks, and names the file, the line and the term to use. The decision records, the archived changes, the changelog's released entries, the vendored files, the generated skills and each title that an accepted record quotes keep the words they were written with, so the words to avoid also say what an older text means. In this page, every column but the words to avoid is read. `scripts/rewording.py` lists each line that a pull request changed by more than a word to avoid replaced with its term.

Each concept that a rule tells apart from another has a term of its own, so that listing one as a word to avoid for the other fails the test. The tool's name, Agentic PR cost calculator, is a name and keeps its words.

## The tool and its parts

| Term | Meaning | Words to avoid |
|---|---|---|
| the tool | What the tool's repository builds and releases to estimate what a pull request cost in model tokens and CI minutes: the capture step, the report, and the files that adopters copy or call to use them. | the calculator, the product |
| capture step | The tool's part that records each model call of a Claude Code session and stages it in a ledger file, a single Python file that the session's hooks run. | capture hook |
| hook | Claude Code's way of running a command at set points of a session, giving it the transcript's path and Claude's current directory; "the hook" also names the capture step that the tool's hooks run. | |
| hook file | The capture step's single file, which an adopter copies from the commit that their workflow pins and which the registered command runs only when it matches the checksum that the command carries. | |
| registered command | The command registered for the capture step's hooks, which carries the SHA-256 of the hook file that the adopter copied, reads the hook file in the working tree once, and runs what it read only when it matches. | |
| git hook | A program that git runs at a point of its own work, such as a repository's `pre-commit` or `commit-msg` hook, which can refuse a commit. | |
| report | The tool's part that runs after a merge, a reusable workflow and its Python code, which turns a pull request's ledger files and CI runs into a cost and posts the report comment; "a report" also names what it posts. | cost step |
| report comment | The one comment that the report posts on a pull request that merges with the tool on, giving its cost and the counts of what it did not count. | |
| configuration file | `.pr-cost.json` at a repository's root, which turns the tool on there while it enables the tool; a person's or a repository's git configuration is another thing. | |
| price table | The tool's dated prices, `prices/models.json` and `prices/github-actions.json`, each price with its effective date and the page it came from, which the capture step ships a copy of. | |
| store | Where the capture step keeps its notes between runs: inside the git common directory, outside the working tree, shared by every worktree, and never committed. | |
| notes | What the capture step keeps in its store, such as the calls it has recorded, the ledger files it has staged and the runs that found the switches on or off. | |

## Repositories, directories and branches

| Term | Meaning | Words to avoid |
|---|---|---|
| this repository | Either the repository that holds the project directory that Claude Code gives the hook, where capture runs, as `usage-capture` uses it, or the tool's own repository, as `CLAUDE.md` uses it, each line using one of the two. | |
| adopting repository | A repository that adopts the tool, gaining its configuration file, the ledger files that each pull request's commits add, and a workflow of its own that calls the report. | |
| git common directory | The directory that a repository's worktrees share, which `git rev-parse --git-common-dir` names, and which a repository nested inside its folder does not share. | git directory, common git directory |
| main worktree | The worktree that a repository's clone checked out, which every clone has, as git calls it. | main folder, main checkout |
| linked worktree | A worktree that a repository gains beside its main worktree, inside the repository's own folder, as Claude Code's worktrees are, or outside it. | |
| project directory | The directory where the session started, which Claude Code gives each hook as `${CLAUDE_PROJECT_DIR}`, and which stays put when Claude changes directory or enters a worktree. | |
| Claude's current directory | The directory that Claude is in, which a hook's input gives as `cwd` and each transcript line names for its call. | |
| a line's working directory | The directory that a transcript line gives for its call, which is Claude's current directory at that time and not always where the call worked. | |
| the directory that the hook runs in | The working directory of a hook's command, which is Claude's current directory except in a worktree session started from the desktop app and when that directory no longer exists. | |
| no branch checked out | The state of a worktree whose HEAD names a commit and not a branch, as during a rebase that stops at a conflict. | detached HEAD |
| a change of branch | The branch that a worktree has checked out becoming another, whichever command does it. | switching branches, switch branches |

## Sessions and calls

| Term | Meaning | Words to avoid |
|---|---|---|
| session | One Claude Code conversation from its start to its end, which has a transcript of its own and can work in several repositories. | |
| transcript | The file of JSON lines, one object per line, in which Claude Code writes what a session saw, its model calls among it, on the machine that runs the session. | |
| model call | One request to a model and its response, identified by its message id, which a transcript can write over several lines and more than one transcript can hold, and which is not a tool call. | |
| subagent | An agent that the session's main agent starts, whose calls Claude Code writes to a transcript of its own, in a `subagents/` folder under the session's. | |
| a run of the capture step | One time that the capture step runs, at one of the events that `usage-capture` lists, such as when Claude finishes responding or before and after the agent's git commands. | |
| workflow run | One run of a GitHub Actions workflow, whose jobs can each be attempted more than once. | |
| job attempt | One attempt of a job of a workflow run, whose minutes are its duration rounded up to a whole minute, priced at its runner type's rate on its UTC day. | |

## The ledger

| Term | Meaning | Words to avoid |
|---|---|---|
| ledger | The ledger files under `.pr-cost/ledger/`, which the agent's commits add, which carry each pull request's counts to it, and which stay on the default branch after the merge as its record. | usage ledger |
| ledger file | A new regular file with a random name, in the ledger folder for the UTC month it is written in, that a run of the capture step writes and stages and that nothing changes after. | |
| entry | A line of a ledger file that gives one model call's usage as `usage-capture` records it, with its activity type, and nothing that `ledger` bars from it, such as prompt text, a file path or a session identifier. | |
| a pull request's ledger files | The ledger files that the merge adds: those in the ledger folder that the default branch holds after the merge and did not hold before it, the only ones whose entries the report counts. | ledger change |
| recorded | Kept by the capture step for a model call, inside the git common directory and out of the working tree and the index, until a run stages it. | |
| staged | Written by a run of the capture step, just before the agent commits, into one new ledger file that the run adds to git's index, so that the agent's commit carries it. | |
| usage record | A record of model usage in any form, real or synthetic, such as a transcript's usage lines, a ledger file or a test's fixture. | |

## Switches and consent

| Term | Meaning | Words to avoid |
|---|---|---|
| the person's opt-in | The person's own switch for capture, `pr-cost.capture` in their global git configuration, which is part of no repository; it turns capture on when it holds one of the values that `switch-and-opt-in` accepts. | opt-in setting, the person's setting |
| consent | The agreement of the person whose session capture records, which they give by turning their opt-in on (DR-046); the requirement "Consent holds for each recorded call" uses it for both switches together. | |
| the repository's switch | The tool on or off in a repository: on while its configuration file enables the tool, and off when the file is removed or disables it. | |

## What the comment counts

| Term | Meaning | Words to avoid |
|---|---|---|
| API-equivalent estimate | The comment's figure: what the usage that the pull request's commits carry, and the CI runs on those commits, would cost at list prices, which is not a bill. | |
| refused call | A model call that capture records no entry for and counts in the ledger as refused, once and with nothing else about it, for a reason that `usage-capture` gives. | |
| refused line | A line of a pull request's ledger files that the report counts as refused instead of as an entry, such as one that does not match the ledger format. | |
| refused file | A path among a pull request's ledger files that the report counts as refused instead of reading it, such as one that is not a regular file. | |
| refused entry | An entry that the report counts as refused instead of counting it, such as one of two entries for one call that disagree, or one dated after the day the report runs. | |
| too large to read | What the comment says when a pull request's ledger files are larger in total than the size bound that the ledger format documents, counting none of their entries and still giving the CI cost. | |
| copied entry | An added entry for a call that a ledger file held at a commit of the default branch's first-parent history before the merge, which the report does not count again. | |
| a call added twice | A call that a pull request's ledger files give in identical entries, which the report counts once. | |
| restored | Said of a ledger file that the merge adds at a path that a ledger file held earlier in the default branch's first-parent history, whose entries the report does not count again. | |
| removed or changed ledger file | A ledger file that the default branch held before the merge and that the pull request removes or changes, which the comment counts and none of whose entries it counts. | |
| skipped | Passed over without being read, and counted only where its requirement says so, as a line that capture could not finish is counted as one refused call. | |
| left out of the cost | Counted in tokens or minutes but not in the cost, because the price table gives no price for its day, model, attribute or runner, and shown as such in the comment. | |
| lower bound | What the comment says the token cost is when capture read calls without a stop reason, whose lines give less usage than the calls made. | |
| may be low | What the comment says the token cost is when a call's usage held a field that capture does not know. | |
| incomplete | What the CI cost is marked when a run or job that it counts cannot be read, has not finished or is left unread, so that the comment does not present it as the total. | |

## Releases

| Term | Meaning | Words to avoid |
|---|---|---|
| bill of materials | The CycloneDX JSON software bill of materials that each release carries, written from the tagged tree by a standard-library Python script in the tool's repository. | SBOM |
| public surface | What existing adopters configure or depend on, as `releases-and-compatibility` lists it, so that any change to it raises the major version. | |

## Process

| Term | Meaning | Words to avoid |
|---|---|---|
| decision record | A file in `docs/decisions/`, named for its number, that holds one decision about what the tool is, how it works or how it is built: what was decided, why, what else was considered, what follows, what it covers and what reversing it would change. | |
| accepted record | A decision record that the default branch holds, the owner's merge of the pull request that adds it being its acceptance, until a later record closes it. | |
| design decision | A numbered section of a change's `design.md`, which says how the change meets its specs and names the decision records that hold its choices. | |
| proposal | A change's `proposal.md`, which says why the change is made, lists the capabilities that its specs hold and says how each is validated; the README's status calls the tool a proposal while no code of it exists, and `CLAUDE.md` calls a record that the default branch does not hold one. | |
| residual | What can still happen with a threat's answer in place, as the threat model gives it under the threat, so that the threat's likelihood rates the risk that remains (DR-112). | |
| trust boundary | A place where data crosses from one party's control into another's, as the threat model marks each. | |
