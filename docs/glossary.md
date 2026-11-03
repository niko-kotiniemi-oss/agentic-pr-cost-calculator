# Glossary

The words that the specs and the other pages use, each with its meaning and the words to avoid for it (R137, R138). Each meaning is one sentence, taken from the spec or the page that defines the word. Where a meaning differs from a requirement, a scenario or `CLAUDE.md`, those hold, and this page is corrected (DR-166). A word with several right senses is given with the sense that each document gives it, and the reviews check its uses.

A word to avoid is one that is wrong wherever a page uses it in prose. `tests/test_glossary.py` fails on each use of one, in any case and in its plural, outside inline code and fenced code blocks, and names the file, the line and the term to use, and it fails on a page that it cannot read whole. Where a page means another tool's own thing by a word to avoid, as git means a state by `detached HEAD`, it gives the word in code, and where a word to avoid would be right in another sense, as `the product` of two numbers is, the page words it otherwise. The decision records, the archived changes, the changelog's released entries, the vendored files, the generated skills and each title that an accepted record quotes keep the words they were written with, so the words to avoid also say what an older text means. In this page, every column but the words to avoid is read. `scripts/rewording.py` lists each line that a pull request changed by more than a word to avoid replaced with its term and, apart from those, each line that replaces a word that the glossary at the pull request's base did not give for its term.

Each concept that a rule tells apart from another has a term of its own, so that listing one as a word to avoid for the other fails the test. The tool's name, Agentic PR cost calculator, is a name and keeps its words.

## The tool and its parts

| Term | Meaning | Words to avoid |
|---|---|---|
| the tool | What the tool's repository builds and releases to estimate what a pull request cost in model tokens and CI minutes: the capture step, the report, and the files that adopters copy or call to use them. | the calculator, the product |
| capture step | The tool's part that records each model call of a Claude Code session whose transcript line gives a working directory in the repository that holds the session's project directory, made inside one of its session's intervals, and stages it in a ledger file: a single Python file that the session's hooks run. | capture hook |
| hook | Claude Code's way of running what a session's settings register, such as a command, at set points of a session, giving it the transcript's path and Claude's current directory; "the hook" also names the capture step that the tool's hooks run, or that step and its registered command together, and "a hook", "an older hook" or "the copied hook" names the capture step at one release or in one repository's copy. | |
| hook file | The capture step's single file, which an adopter copies from the commit that their workflow pins and which the registered command runs only when it matches the checksum that the command carries. | |
| registered command | The command registered for the capture step's hooks, which carries the SHA-256 of the hook file that the adopter copied, reads the hook file once, from the working tree at the project directory, and runs what it read only when it matches. | |
| git hook | A program that git runs at a point of its own work, such as a repository's `pre-commit` or `commit-msg` hook, which can refuse a commit, so that the commit runs and fails and a run of the capture step follows it, while a command refused at a permission prompt or by a permission rule never runs and no run follows it. | |
| report | The tool's part that runs on the push that a merge makes to the default branch, a reusable workflow and its Python code, which turns a pull request's ledger files and CI runs into a cost and posts the report comment; "a report" also names one run of it, what that run posts, or one version of it, such as the report of one release, as in "an older report", and "a changed report" is a pull request's change to the configuration file, the hook file or a workflow, which the comment flags, as it flags a change to `.claude/settings.json` or `.claude/settings.local.json`, which can register the hook. | cost step |
| report comment | The one comment that the report posts on a merged pull request when the tool is on before its merge or after it, giving its cost, how many entries it counted, how many entries and files it did not count for each reason, how many calls may leave the token cost low, and for which reasons its ledger files say that calls were left out. | |
| configuration file | `.pr-cost.json` at a repository's root, which turns the tool on there while it enables the tool and only while it is a valid regular file within its size bound, and which "cannot be read as a valid configuration" when it is not a regular file, is over its size bound or is not valid under its format; a person's or a repository's git configuration is another thing. | |
| price table | The tool's dated prices, `prices/models.json` and `prices/github-actions.json`, each price with its effective date and the page it came from, which the capture step ships a copy of. | |
| store | Where the capture step keeps its notes between runs: one file for each user in the git common directory, outside the working tree, shared by every worktree, never committed and removed once it holds nothing, whose layout and protection the usage-capture feature page gives. | |
| notes | What the capture step keeps in its store for no longer than the retention window, only what it needs to tell a call's worktree and branch, to record each call once and to take back a ledger file, as the usage-capture feature page lists it. | |
| retention window | The 30 days for which the store keeps what capture needs, and within which a call's day must fall for a run to record it, as the usage-capture feature page sets out. | |

## Repositories, directories and branches

| Term | Meaning | Words to avoid |
|---|---|---|
| this repository | Either the repository that holds the project directory that Claude Code gives the hook, which capture works on whatever directory the hook runs in, as `usage-capture` uses it, or the tool's own repository, as `CLAUDE.md` uses it, each line using one of the two, and a row of the requirements register taking its spec's sense. | |
| adopting repository | A repository that adopts the tool, gaining its configuration file, the ledger files that each pull request's commits add, and a workflow of its own that calls the report. | |
| git common directory | The directory that a repository's worktrees share, which `git rev-parse --git-common-dir` names, and which a repository nested inside its folder does not share. | git directory, common git directory |
| main worktree | The worktree that a repository's clone checked out, which every clone but a bare one has, as git calls it. | main folder, main checkout |
| linked worktree | A worktree that a repository gains beside its main worktree, inside the repository's own folder, as Claude Code's worktrees are, or outside it. | |
| project directory | The project root that Claude Code gives each hook as `${CLAUDE_PROJECT_DIR}`, which stays put when Claude changes directory or enters a worktree. | |
| Claude's current directory | The directory that Claude is in, which a hook's input gives as `cwd` and each transcript line names for its call. | |
| a line's working directory | The directory that a transcript line gives for its call, which is Claude's current directory at that time and not always where the call worked. | |
| the directory that the hook runs in | The working directory of a hook's command, which is Claude's current directory except in a worktree session started from the desktop app and when that directory no longer exists. | |
| no branch checked out | The state of a worktree whose HEAD names a commit and not a branch, as during a rebase that stops at a conflict. | detached HEAD |
| a change of branch | The branch that a worktree has checked out becoming another, whichever command does it. | switching branches, switch branches |

## Sessions and calls

| Term | Meaning | Words to avoid |
|---|---|---|
| session | One Claude Code conversation from its start to its end, and the same one when it is resumed, which has a transcript of its own and can work in several repositories; the rules that keep session links and identifiers out of the repository mean a session of any Claude product, and a golden session is another thing. | |
| transcript | The file of JSON lines, one object per line, in which Claude Code writes what a session saw, its model calls among it, on the machine that runs the session; a rule that keeps transcripts out of the repository, a pull request or an issue means any part or copy of one, and a synthetic transcript is one that a test makes up. | |
| golden session | One case of the golden set that `project-standards` holds (R139): a synthetic session with its transcripts, or none where it tests the report alone, the pull request it is reported for, a price table of its own, each call with its entry or the scenario that leaves it out, and the figures worked out by hand; the passages about the golden set call it a session. | |
| model call | One request to a model and its response, identified by its message id, which a transcript can write over several lines and more than one transcript can hold, and which is not a tool call. | |
| subagent | An agent that the session's main agent starts, or that Claude Code runs for its own features, whose calls Claude Code writes to a transcript of its own, which `SubagentStop` names; for an agent that the main agent starts, that transcript is in a `subagents/` folder under the session's. | |
| a run of the capture step | One time that the capture step runs, at one of the events that `usage-capture` lists, such as when a session starts, when Claude finishes responding or before and after each of the agent's Bash commands that the hook's condition `Bash(git *)` matches, which the capture specs also call a run, and other pages a capture run or the hook's run. | |
| start run | The run of the capture step when a session starts, is resumed or forked, or is cleared or compacted, which reads no transcript, takes back and puts back what is due, as any run does, and begins its session's interval when it finds both switches on and no store whose version it does not know, so that the interval can begin before the session's first call. | |
| the line that a call answers | The nearest line up the chain of parents that a call's first line names, in the same transcript, that gives the person's prompt, a tool's result or a compaction's summary, passing over Claude Code's own bookkeeping lines, a hook's output and system lines, whose own time, with that of the call's first line, places the call inside or outside an interval. | |
| workflow run | One run of a GitHub Actions workflow, whose jobs can each be attempted more than once, which `ci-minutes` and `report-comment` also call a run, and other pages a CI run. | |
| job attempt | One attempt of a job of a workflow run, whose minutes are its duration rounded up to a whole minute, priced at its runner type's rate on its UTC day. | |
| the pull request's own runs | The workflow runs on a pull request's own commits, those that its head holds and the default branch did not hold before the merge, that no push to the default branch started and that were created before it merged, the only runs whose job attempts the CI cost counts (R62). | |

## The ledger

| Term | Meaning | Words to avoid |
|---|---|---|
| ledger | The ledger files under `.pr-cost/ledger/`, which the agent's commits add, though any commit can add one, which carry each pull request's counts to it, and which stay on the default branch after the merge as its record. | usage ledger |
| ledger file | Whatever is at a path under `.pr-cost/ledger/`, whoever wrote it and whatever it holds; one that a run of the capture step writes is a new regular file with a random name, in the ledger folder's subfolder for the UTC month it is written in, whose first line states the version of the ledger format that it is written in, which the run stages and the tool never changes after. | |
| entry | A line of a ledger file that gives one model call's usage as `usage-capture` records it, with its activity type, and nothing that `ledger` bars from it, such as prompt text, a file path or a session identifier; git's index and tree entries and a changelog's entries are other things. | |
| a pull request's ledger files | The ledger files that the merge adds: those in the ledger folder that the default branch holds after the merge and did not hold before it, the only ones whose entries the report counts. | ledger change |
| recorded | Kept by the capture step for a model call, with the worktree and branch that the call goes to, inside the git common directory and out of the working tree and the index until a run stages it, and from then on as the call's entry; a recorded response is a test's stored reply from an API. | |
| staged | Written by a run of the capture step, just before the agent commits, into one new ledger file that the run adds to git's index, so that the agent's commit carries it, which the specs also say of that ledger file and, in git's sense, of any change added to the index. | |
| hashed id | An id that the tool keeps only as its SHA-256 hash, as an entry keeps its call's message id and the store a session's id, which does not hide whose record it is, since whoever holds the value can compute its hash and the commit that adds a ledger file names its author. | anonymous |
| usage record | A record of model usage in any form, real or synthetic, such as a transcript's usage lines, a ledger file or a test's fixture. | |

## Switches and consent

| Term | Meaning | Words to avoid |
|---|---|---|
| the person's opt-in | The person's own switch for capture, `pr-cost.capture` in their global git configuration, which is part of no repository; it turns capture on in every repository that turns the tool on when it holds one of the values that `switch-and-opt-in` accepts, git's own reading of it, a repository's own git configuration and an included file among them, can turn it off but not on, and "an opt-in" or "an opt-out" is the person turning it on or off. | opt-in setting, the person's setting |
| consent | The agreement of the person whose session capture records, which they give by turning their opt-in on (DR-046); the requirement "Consent holds for each recorded call" and T38 use it for both switches together. | |
| interval | A span of a session when both switches were on, which begins only at a run of the capture step that finds both on while the session has no open interval, never at the session's start, and ends at its last run before one that finds either switch off or another fingerprint, or once a run finds the clock moved back, so that a call is recorded only when the line it answers was written at or after the run that began one and the call began no later than its last run. | |
| fingerprint | What a run that finds both switches on notes of the files that can turn the person's capture on or off, kept only as a hash and made of nothing from their contents or paths, so that a change to any of them between two runs ends the interval and is taken as an opt-out; which files it covers, and which of their attributes, the switch and opt-in feature page gives. | |
| the repository's switch | The tool on or off in a repository: on while its configuration file can be read as a valid configuration and enables the tool, and off when the file is removed, disables it or cannot be read as a valid configuration; the report runs for a merge that finds it on before the merge or after it. | |

## What the comment counts

| Term | Meaning | Words to avoid |
|---|---|---|
| API-equivalent estimate | The comment's figure: what the usage that the pull request's commits carry, and the CI runs on those commits, would cost at list prices, which is not a bill. | |
| refused call | A model call that capture records no entry for and counts in the ledger as refused, once and with nothing else about it, for a reason that `usage-capture` gives, such as a value of it that is refused or final lines of it that disagree; a line that a run could not finish reading counts as one refused call too. | |
| refused line | A line of a pull request's ledger files that the report counts as refused instead of as an entry, such as one that does not match the ledger format, a value that is refused making its whole line refused. | |
| refused file | A path that the merge adds in the ledger folder that the report counts as refused, using none of its entries, counts or flags, such as one that is not a regular file, or a ledger file whose first line states no version of the ledger format, or one that the report does not read, or that breaks its version's rules. | |
| refused entry | An entry that the report counts as refused instead of counting it, such as one of two entries for one call that disagree, or one dated after the day the report runs. | |
| too large to read | What the comment says when a pull request's ledger files are larger in total than the size bound that the ledger format documents, counting none of their entries and still giving the CI cost, which `report-comment` calls refusing them. | |
| copied entry | An added entry for a call that a ledger file held at a commit of the default branch's first-parent history before the merge, which the report does not count again. | |
| a call added twice | A call that a pull request's ledger files give in identical entries, which the report counts once. | |
| restored | Said of a ledger file that the merge adds at a path that a ledger file held earlier in the default branch's first-parent history, whose entries the report does not count again. | |
| removed or changed ledger file | A ledger file that the default branch held before the merge and that the pull request removes or changes, which the comment counts and none of whose entries it counts. | |
| skipped | Passed over, unread or once read and found not to match the ledger format, and counted only where its requirement says so, as a line that capture could not finish is counted as one refused call. | |
| a call left out | A model call that capture leaves out of every ledger file because it cannot show that the call was made inside an interval, because the call waited to be staged past the retention window, or because its repository could not be told, which a ledger file then flags for that reason, with no count, as `usage-capture` says, and which, unlike what is left out of the cost, no figure counts. | |
| left out of the cost | Counted in tokens or minutes but not in the cost, because the price table gives no price for its day, its model, an attribute's value or a combination of its attributes, or its runner, and shown as such in the comment; a model or attribute value that the table does not list, other than `unknown`, makes its line refused instead. | |
| lower bound | What the comment says the token cost is when capture read calls without a stop reason, whose lines give less usage than the calls made, and what it says of the token cost, each of its parts and the total when the pull request's ledger files flag calls left out. | |
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
