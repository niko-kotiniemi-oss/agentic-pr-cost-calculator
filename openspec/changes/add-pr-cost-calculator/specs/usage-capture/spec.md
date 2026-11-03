## Purpose

Record what an agent session spends on model calls in this repository, as it works, and carry it to the pull request with the agent's own commits, in a form the pull request's CI can read at merge without any external service.

In the scenarios below, a commit that is expected to carry a ledger file is made where git's attributes give the ledger path no filter and no working-tree encoding, git does not refuse to add the file, and no git hook of the repository refuses it, and a commit that a scenario does not spell out, such as the agent's next commit, is one that the step stages for, unless the scenario says otherwise. In them, each run of the step reads the transcripts to their end within its time budget, and no other session commits in the repository, unless the scenario says otherwise. In them, too, every run of the step finds the tool on in the repository and the person opted in, a run of the step that found both on came before every line that a scenario's calls answer, as a start run does, and the hook file in the working tree is the one whose checksum the registered command carries, unless the scenario says otherwise.

## ADDED Requirements

### Requirement: Usage is recorded per model call

The capture step SHALL record each model call once. It SHALL record the call's UTC day, its model, a SHA-256 hash of its message id, whether the main agent or a subagent made it, its input tokens, output tokens, cache-write tokens split by cache lifetime where the source gives it, and cache-read tokens, and, where the source gives them, the attributes that change its price: service tier, speed, inference region and server-side tool requests.

#### Scenario: A turn's calls are recorded once

- **WHEN** the session's transcript holds three model calls of one turn, not yet recorded, which the agent made in one worktree, and the agent then commits in that worktree, with no change of branch there in between and no other call waiting to be staged there
- **THEN** the commit's new ledger file holds exactly three entries, one per call, with each call's model and token counts

#### Scenario: Running again records nothing twice

- **WHEN** the capture step runs a second time over the same transcript with no new calls
- **THEN** nothing new is recorded

#### Scenario: A change of branch records nothing twice

- **WHEN** the agent switches to another branch, and the capture step runs again over the same transcript
- **THEN** no call already recorded is recorded again

#### Scenario: A resumed session records nothing its branch already holds

- **WHEN** a session is resumed in a fresh clone of its branch, and the ledger files on that branch already hold some of its calls
- **THEN** none of those calls is recorded again

#### Scenario: Price attributes are recorded

- **WHEN** a call's usage gives its service tier, its speed, its inference region and a number of web searches, each a value the price table lists
- **THEN** its entry records each of them

#### Scenario: An entry records the UTC day, not the time

- **WHEN** a call's transcript time is `2026-03-02T01:30:00+02:00`
- **THEN** its entry's day is `2026-03-01`, and the entry holds no time of day

#### Scenario: An entry records that the main agent made its call

- **WHEN** the main agent makes a model call, and the capture step records it
- **THEN** its entry records that the main agent made it, not a subagent

### Requirement: A subagent's calls are read from its own transcript

The capture step SHALL read a subagent's calls from the subagent's own transcript.

#### Scenario: Subagent calls are included

- **WHEN** a session started a subagent whose calls are in its own transcript
- **THEN** the subagent's calls are recorded, marked as a subagent's

### Requirement: A call is identified by its message id and read from its lines that give a stop reason

A call SHALL be identified by its message id, so that a call the transcript writes over several lines, or that appears in more than one transcript, is recorded once. A call's usage SHALL be read from its lines that give a stop reason, because its earlier lines can give partial usage. When two of a call's lines that give a stop reason give different usage, the step SHALL record no entry for the call and SHALL count it as refused.

#### Scenario: A call written over several lines is recorded once

- **WHEN** one model call's message appears on three transcript lines, each giving its stop reason and the same usage
- **THEN** one entry is recorded for that call

#### Scenario: A call's partial lines are not used

- **WHEN** a call's first lines give partial usage and no stop reason, and its last line gives its stop reason and its final usage
- **THEN** its entry records the final usage

#### Scenario: A call whose lines disagree is refused

- **WHEN** two transcript lines of one model call both give a stop reason, and give different usage
- **THEN** no entry is recorded for that call, and the ledger counts one refused call

### Requirement: A call with no stop reason is read from its last line once it is over

A call none of whose lines gives a stop reason SHALL be read from its last line once the call is over: when a later call follows it in the same transcript, or when the agent that made it has stopped. The ledger SHALL count the calls read that way, because such lines give the usage of the call's start, with fewer output tokens and server-side tool requests than the call made. A call that is not over yet SHALL be left for a later run.

#### Scenario: A call followed by a later one is read without its stop reason

- **WHEN** none of a call's lines gives a stop reason, and a later call follows it in the same transcript
- **THEN** the call is recorded from its last line, and the ledger counts it as read without a stop reason

#### Scenario: A stopped agent's last call is read without its stop reason

- **WHEN** a subagent finishes, and none of the lines of its last call gives a stop reason
- **THEN** that call is recorded from its last line, and the ledger counts it as read without a stop reason

#### Scenario: A call still being written is recorded later

- **WHEN** none of a call's lines gives a stop reason, no later call follows it, and the agent that made it has not stopped
- **THEN** nothing is recorded for that call yet, and a later run records it

### Requirement: A call with an unknown usage field is recorded and counted

A call whose usage, or a block nested in it, holds a field that the step does not know SHALL be recorded from the fields it knows, and the ledger SHALL count such calls, without naming the field, because a new field can carry a charge that the entry then leaves out.

#### Scenario: A usage field the step does not know is counted

- **WHEN** a call's usage holds, besides the fields that the step reads, a field that it does not know, at its top level or in a block nested in it
- **THEN** the call's entry is recorded from the fields that the step knows, the ledger counts one call whose usage held a field that the step does not know, and neither that field's name nor its value is in the ledger

### Requirement: Capture reads only lines that end in a line break, and no one line holds it back

The step SHALL read only the transcript lines that end in a line break, leaving a line that is still being written for a later run, and a line that a run began as the first line it read, or as the first that no earlier run read whole, and could not finish reading within its time budget, SHALL be skipped by the next run and counted in the ledger as one refused call, so that no one line can hold capture back for good.

#### Scenario: A half-written last line waits for a later run

- **WHEN** a transcript's last line does not yet end in a line break, as when Claude Code is still writing it
- **THEN** the run reads nothing from that line and counts nothing for it, and a later run reads it once its line break is written

#### Scenario: A line too long for a run's budget is skipped and counted

- **WHEN** a run of the step begins with a transcript line, and cannot finish reading it within its time budget
- **THEN** the next run skips that line, the ledger counts it as one refused call, and the lines after it are read

#### Scenario: A line too long for what a run has left after reading lines again is skipped

- **WHEN** a run of the step reads again lines that an earlier run read, then begins the first line that no earlier run read whole, and cannot finish reading it within its time budget
- **THEN** the next run skips that line, the ledger counts it as one refused call, and the lines after it are read

### Requirement: A call is placed by the line it answers, whichever run read that line

A run SHALL read again, from the earliest line that a call not yet recorded may answer, the lines that earlier runs read, so that a call is placed by the line it answers even when an earlier run read that line. A call whose answered line comes before that point, or was skipped as too long, SHALL NOT be recorded, and the next ledger file staged for its worktree and branch SHALL say that calls were left out for consent.

#### Scenario: A call is placed when an earlier run read the line it answers

- **WHEN** a run of the step reads a tool's result and stops before the call that answers it is written, and a later run reads that call
- **THEN** that call is recorded

#### Scenario: A call whose answered line comes before where runs read again is not recorded

- **WHEN** the chain of parents from a call's first line leads to the line that it answers only before the earliest line that runs read again in its transcript
- **THEN** that call is not recorded, and the next ledger file staged for its worktree and branch says that calls were left out for consent

#### Scenario: A call whose answered line was skipped is not recorded

- **WHEN** the line that a call answers was skipped as too long for a run's time budget
- **THEN** that call is not recorded, and the next ledger file staged for its worktree and branch says that calls were left out for consent

### Requirement: Capture reads the branch's ledger files only from git

To learn which calls the branch's ledger files already hold, the step SHALL read those files only as blobs from git, never through the working tree, skipping any path in the ledger folder that is not a regular file, and SHALL learn each file's size before reading it, skipping any file larger than the size bound that the ledger format documents, and any file whose blob the clone does not hold, as a partial clone may not.

#### Scenario: Capture reads no ledger file through a link

- **WHEN** the branch holds a symbolic link in the ledger folder
- **THEN** capture reads nothing through it, and still records the session's calls

#### Scenario: Capture does not read an oversized ledger file

- **WHEN** the branch holds a ledger file larger than the size bound
- **THEN** capture does not read that file, and still records the session's calls

#### Scenario: Capture skips a ledger file whose blob its clone lacks

- **WHEN** the branch holds a ledger file whose blob the clone does not hold
- **THEN** capture reads nothing of that file, and still records the session's calls

### Requirement: Capture reads each ledger file by the version that it states

The capture step SHALL read each of the branch's ledger files by the version that its first line states, and SHALL skip one whose first line states no version or a version that it does not read.

#### Scenario: Capture skips a ledger file of a version it does not read

- **WHEN** the branch holds a ledger file whose first line states a version that the step does not read
- **THEN** capture reads nothing of that file, and still records the session's calls

### Requirement: The capture step's git commands stay offline

Every git command that the step runs SHALL run with `GIT_NO_LAZY_FETCH=1` and `GIT_TERMINAL_PROMPT=0`, so that none of them fetches what the clone lacks, asks for credentials or opens a network connection.

#### Scenario: Capture fetches no ledger file that its clone lacks

- **WHEN** the branch holds a ledger file whose blob a partial clone has not fetched
- **THEN** capture reads nothing of that file, no git command that it runs fetches anything or opens a network connection, and it still records the session's calls

### Requirement: Only calls made from this repository are recorded

The capture step SHALL record only the calls whose transcript line gives a working directory in this repository (see "Capture works on the repository that holds the project directory"): a directory whose git common directory is this repository's, which includes this repository's worktrees and excludes another repository nested inside its folder.

#### Scenario: Calls made from outside this repository are not recorded

- **WHEN** a session made calls while Claude's current directory was in another repository, or in a folder that contains this one
- **THEN** none of those calls is recorded in this one

#### Scenario: A repository nested inside this one is not this one

- **WHEN** a session made calls while Claude's current directory was in a separate git repository inside this repository's folder
- **THEN** none of those calls is recorded in this one

#### Scenario: A worktree of this repository is this repository

- **WHEN** a session made calls while Claude's current directory was in a worktree of this repository, whether inside the repository's own folder, as Claude Code's worktrees are, or outside it, and no ledger file that the step wrote was in a stash
- **THEN** those calls are recorded, and only a commit made in that worktree carries them

#### Scenario: A call whose line gives no working directory is not recorded

- **WHEN** a session in this repository has a call whose lines give no working directory
- **THEN** the call is not recorded, whatever directory the hook's input or the project directory names, and the next ledger file that holds a call of its session says that calls whose repository could not be told were left out

### Requirement: A call's repository is told by its working directory alone

The capture step SHALL tell a call's repository and worktree by its line's working directory alone, as git finds them from that directory when a run reads the call (see "Git runs without the session's git variables"), never by what the call reads or writes, nor by the branch, and SHALL leave out a call whose line gives no working directory, or whose directory no longer exists or names no repository that git can tell.

#### Scenario: A call whose working directory is gone is not recorded

- **WHEN** a call's line gives a working directory in a worktree of this repository, inside the repository's folder as Claude Code keeps its worktrees, that is removed before a run reads the call
- **THEN** the call is not recorded, and the session's next ledger file here says that calls whose repository could not be told were left out

#### Scenario: A call made here that works on another repository is recorded here

- **WHEN** a call's line gives a working directory in this repository, and the call's tool reads or writes another repository through an absolute path or `git -C`
- **THEN** the call is recorded in this repository, and in no other

#### Scenario: A call made in another repository that works on this one is not recorded here

- **WHEN** a call's line gives a working directory in another repository, and the call's tool reads or writes this repository through an absolute path or `git -C`
- **THEN** the call is not recorded in this repository

#### Scenario: The environment cannot move a call into this repository

- **WHEN** the session's environment sets `GIT_DIR`, `GIT_COMMON_DIR` or `GIT_WORK_TREE` to name this repository, and a call's line gives a working directory in another repository
- **THEN** that call is not recorded in this repository

#### Scenario: A clone whose ownership git does not trust records nothing

- **WHEN** the repository's folder is owned by another user than the one that a run runs as, and no `safe.directory` setting that git reads without the session's `GIT_` variables names it
- **THEN** no call is recorded, no store is created, no ledger file is staged, and the run exits with success

#### Scenario: A `safe.directory` setting that only the session's environment gives does not make the clone trusted

- **WHEN** the repository's folder is owned by another user than the one that a run runs as, and only the session's `GIT_` variables give a `safe.directory` setting that names it, through `GIT_CONFIG_COUNT` or in a file that `GIT_CONFIG_GLOBAL` names
- **THEN** no call is recorded, no store is created, no ledger file is staged, and the run exits with success

### Requirement: Capture works on the repository that holds the project directory

This repository SHALL be the one that holds the project directory that Claude Code gives the hook, whatever directory the hook runs in, and the registered command SHALL name the capture step's file through that project directory.

#### Scenario: A run from another directory works on this repository

- **WHEN** the capture step runs while Claude's current directory is in another repository
- **THEN** it records and stages only in this repository, and only the calls made from this repository

### Requirement: Counts are whole numbers

Every token count and request count SHALL be a whole number from zero up to a ceiling that the ledger format documents. A value that is text, a fraction, negative, not a number, infinite, `true` or `false`, or above the ceiling SHALL be refused: no entry is recorded for the call, and the ledger counts it as refused, once, with nothing else about it.

#### Scenario: A count that is not a whole number is refused

- **WHEN** a call's output tokens are given as text, as a fraction, or as `true`
- **THEN** no entry is recorded for that call, and the ledger counts one refused call

#### Scenario: A negative count is refused

- **WHEN** a call's input tokens are negative
- **THEN** no entry is recorded for that call, and the ledger counts one refused call

#### Scenario: A count at the ceiling is recorded

- **WHEN** a call's input tokens equal the ceiling that the ledger format documents
- **THEN** its entry records that count

#### Scenario: A count above the ceiling is refused

- **WHEN** a call's input tokens are one more than the ceiling
- **THEN** no entry is recorded for that call, and the ledger counts one refused call

#### Scenario: A count that is not a number or is `false` is refused

- **WHEN** a call's output tokens are given as `false`, or as `NaN`, `Infinity` or `1e999`, which Python's JSON reader reads as not-a-number or as infinity
- **THEN** no entry is recorded for that call, and the ledger counts one refused call

### Requirement: Usage reaches the pull request with the agent's commits

Capture SHALL run when a session starts, when Claude finishes responding, when a subagent finishes, when a turn ends in an API error, when the session ends, and before and after each of the agent's Bash commands that the hook's condition `Bash(git *)` matches. Every run but a start run (see "A start run reads no transcript") SHALL record the calls that the transcript holds as over, up to its time budget, and the run before such a command SHALL do so before that command can change the branch.

#### Scenario: A one-turn session's commit carries its calls

- **WHEN** in a session's first turn, after a start run that found both switches on, the agent makes model calls in one worktree and then makes its first commit there, by running `git commit -m x` alone with changes staged, with no change of branch there in between, and the transcript holds at least one of those calls as over when that commit's run reads it
- **THEN** that commit adds a ledger file holding each of those calls that the transcript held as over by then

#### Scenario: A turn that ends in an API error is still recorded

- **WHEN** a turn in which the agent makes model calls in one worktree and does not commit ends in an API error, and the agent's next commit is made in that worktree, with no change of branch there from the start of that turn until that commit
- **THEN** once the run of the step when that turn ends is over, each of those calls that the transcript held as over when that run read it is recorded, and that commit carries them

#### Scenario: The run before a git command records the calls before the command can change the branch

- **WHEN** the agent runs `git checkout other`, and the run of the step before that command reads a call that the transcript holds as over, within that run's time budget
- **THEN** that run records the call before the checkout can change the branch

### Requirement: A start run reads no transcript

The run when a session starts, is resumed or forked, or is cleared or compacted SHALL read no transcript and SHALL begin its session's interval when it finds both switches on and no store whose version it does not know, while it takes back and puts back as any run does (see "Ledger files are taken back and put back whatever the switches say" in `switch-and-opt-in`). Nothing SHALL depend on a start run coming: where none comes, the session's interval begins at its first run that finds both on.

#### Scenario: A session started opted in records its first turn

- **WHEN** the person turned capture on before a session started, its start run noted its time before the session's first prompt was written, and in its first turn the agent makes calls in one worktree and commits there, with no change of branch in between
- **THEN** that commit carries each of those calls that the transcript held as over when that commit's run read it

#### Scenario: A session with no start run records from its first run

- **WHEN** the person turned capture on before a session started, no start run comes, as where Claude Code does not run that event, and the agent makes calls before the step's first run in that session
- **THEN** none of the calls that answer a line written before that run is recorded, and the next ledger file staged for the worktree and branch of those calls says that calls were left out for consent

#### Scenario: A start run records nothing from a resumed transcript

- **WHEN** a session is resumed, and its transcript holds calls that no run has read
- **THEN** its start run records nothing, and a later run reads those calls

#### Scenario: A start run prints nothing

- **WHEN** a start run finds both switches on, a ledger file due to be taken back and a store that an earlier release wrote
- **THEN** it writes nothing to standard output, which Claude Code would give Claude as context

### Requirement: A call goes only to a commit in its worktree, on the branch it was recorded on

A call SHALL go only into a ledger file staged in the worktree that git itself finds from its line's working directory, which for a directory in a worktree inside the repository's folder is that worktree and not the main worktree around it, for a commit on the branch that was checked out there when the call was recorded, which is not the branch it was made on when a run reads the call only after a change of branch.

#### Scenario: Calls go to the worktree and branch they were recorded on

- **WHEN** calls were recorded in a worktree while one branch was checked out there, and the agent then commits in another worktree, or in that worktree on another branch, and until that commit no stash held any of those calls, and no file held any of them in the index or the working tree of the worktree where the agent commits but the ledger files of the commit checked out there
- **THEN** that commit carries none of those calls

#### Scenario: A call made before a checkout stays with its branch

- **WHEN** the agent makes calls with one branch checked out, then, with no change of branch in between, runs `git checkout` to another branch and commits on that branch, in the same turn, and until that commit no stash holds any of those calls, and no file holds any of them in the index or the working tree but the ledger files of the commit checked out there
- **THEN** the commit on the other branch carries none of those calls that the transcript held as over when the last run of the step before the checkout read it

#### Scenario: A call read only after a change of branch goes to the branch checked out then

- **WHEN** the agent makes a call with one branch checked out and then runs `git checkout` to another branch, and the run before that command cannot yet read the call as over, as when the transcript lags
- **THEN** a later run records the call with the branch checked out when that run reads it, and a commit on the first branch carries none of it

#### Scenario: Calls and notes follow a moved worktree

- **WHEN** calls were recorded in a linked worktree of this repository, a ledger file was staged there for a commit that did not happen, and the worktree is then moved with `git worktree move` before any run takes the file back
- **THEN** a later run takes the file back in the worktree at its new path, and the agent's next commit there, on the same branch, carries those calls

### Requirement: Calls recorded with no branch checked out go only to a commit made the same way

Calls recorded while no branch was checked out SHALL go only to a commit made while no branch is checked out, in the same worktree.

#### Scenario: Calls made with no branch checked out wait for a commit made the same way

- **WHEN** calls were recorded while no branch was checked out, and the agent then checks out a branch and commits
- **THEN** that commit carries none of those calls

### Requirement: Capture keeps what it records inside the git common directory

Apart from staging a ledger file, taking it back and putting it back, as the requirements from "A ledger file is staged only for a commit whose branch and contents the step can tell" to "A put-back is tried once, and in no other case" say, the step SHALL keep what it records inside the repository's git common directory, and SHALL NOT change the working tree or the index.

#### Scenario: A turn's end leaves the working tree alone

- **WHEN** capture runs at the end of a turn in which the agent did not commit, and no ledger file is due to be taken back or put back
- **THEN** the working tree and the index are unchanged, so a change of branch or a rebase is not blocked

### Requirement: A ledger file is staged only for a commit whose branch and contents the step can tell

Before a command that runs `git commit` (see "Only git's commit subcommand counts as a commit") in this repository, the capture step SHALL stage, as one new ledger file, the calls that "A ledger file holds the new calls of its commit's worktree and branch" names, when the commit stands as "Only a top-level commit in the foreground, after nothing but listed commands, takes a ledger file" requires, unless another requirement says that it stages nothing for that commit.

#### Scenario: A commit that stages its own files carries a ledger file

- **WHEN** the agent runs `git add f && git commit -m x`, with nothing staged before, and calls are waiting to be staged
- **THEN** that commit holds `f` and a ledger file

### Requirement: Only git's commit subcommand counts as a commit

The capture step SHALL treat a command as running `git commit` when one of the commands it is made of is `git`, with or without git's own options, followed by the `commit` subcommand, and is not a dry run (see "A commit is a dry run when a dry-run option is left in effect"), and SHALL NOT treat a command that only names it, such as in single quotes or as an argument of another command, as running it.

#### Scenario: A command that only names a commit stages nothing

- **WHEN** the agent runs a command that only names `git commit` in its text, such as `grep 'git commit' notes.txt`
- **THEN** no ledger file is staged

#### Scenario: A commit with git's own options is still a commit

- **WHEN** the agent runs `git -c user.name=x commit -m y` in this repository
- **THEN** that commit carries a ledger file

### Requirement: A commit is a dry run when a dry-run option is left in effect

The capture step SHALL treat a `git commit` as a dry run when any of `--dry-run`, `--short`, `--porcelain`, `--long`, `-z` and `--null`, in any spelling that git accepts, abbreviated or combined with other short options, is in effect once git has read all of the commit's options, where `--short`, `--porcelain` and `--long` are one setting, which the `--no-` form of any of them clears.

#### Scenario: A dry run of a commit stages nothing

- **WHEN** the agent runs `git commit --dry-run`, `git commit --dry`, `git commit --porcelain` or `git commit -z`
- **THEN** no ledger file is staged

#### Scenario: A dry-run option that a later option undoes is still a commit

- **WHEN** the agent runs `git commit --dry-run --no-dry-run -m x`, `git commit -z --no-null -m x` or `git commit --porcelain --no-short -m x` alone, with changes staged and calls waiting to be staged
- **THEN** that commit carries a ledger file

### Requirement: A ledger file holds the new calls of its commit's worktree and branch

The calls that the capture step stages for a commit SHALL be those recorded in the worktree where the commit runs, while the branch now checked out there was checked out, that no ledger file on that branch holds and that the step has not noted as taken (see "A ledger file that a commit takes stays taken"), and the step SHALL stage nothing when there is no such call to stage.

#### Scenario: A commit with nothing new to record takes no ledger file

- **WHEN** the agent commits, and a ledger file already holds every call recorded in that worktree on that branch
- **THEN** no ledger file is staged

#### Scenario: A commit carries the calls that another session recorded on its branch

- **WHEN** a run of the step for one session has recorded calls in a worktree while a branch was checked out there, no commit has taken them, and another session then commits there, with no change of branch there in between
- **THEN** that commit carries those calls

### Requirement: Only a top-level commit in the foreground, after nothing but listed commands, takes a ledger file

The capture step SHALL stage a ledger file only for a commit that is one of its command's top-level commands, not part of a pipeline, joined to the others by `&&`, `;` or line breaks, that runs in the foreground, and that comes after nothing but `cd` to a path that the command writes out and the git commands `add`, `rm`, `mv`, `status`, `diff`, `log` and `show`, with or without git's own options, and so none for a commit in a subshell or a group, or behind a wrapper such as `timeout`.

#### Scenario: A commit after another command takes no ledger file

- **WHEN** the agent runs `npm test && git commit -am x`, or `git checkout other && git commit -m x`
- **THEN** no ledger file is staged, and the calls wait for a later commit

#### Scenario: A commit in the background takes no ledger file

- **WHEN** the agent runs `git commit` in the background, or as `git commit -m x &`
- **THEN** no ledger file is staged, and the calls wait for a later commit

#### Scenario: A commit in a pipeline, a subshell, a group, joined by `||` or behind a wrapper takes no ledger file

- **WHEN** the agent runs `git commit -m x | cat`, `(git commit -m x)`, `{ git commit -m x; }`, `git commit -m x || echo failed`, `git status || git commit -m x` or `timeout 60 git commit -m x`, with changes staged and calls waiting to be staged
- **THEN** no ledger file is staged, and the calls wait for a later commit

### Requirement: No ledger file is staged for a commit that names its paths

The capture step SHALL stage nothing for a commit that names the paths to commit.

#### Scenario: A commit of named paths takes no ledger file

- **WHEN** the agent runs `git commit` naming the paths to commit
- **THEN** no ledger file is staged, and the calls wait for a later commit

### Requirement: A commit with nothing to commit and no git add, rm or mv before it takes no ledger file

The capture step SHALL stage nothing for a commit that would otherwise commit nothing, counting the changes to tracked files that `-a` adds, when no `git add`, `git rm` or `git mv` comes before it, so that it fails, or makes the empty commit asked for, as it would without the tool.

#### Scenario: A `git add` that stages nothing leaves the ledger file alone in the commit

- **WHEN** the agent runs `git add f && git commit -m x`, where `f` has no changes, with nothing staged before, and calls are waiting to be staged
- **THEN** the commit is made, and holds a ledger file and nothing else

#### Scenario: A commit with nothing to commit stays empty

- **WHEN** the agent runs `git commit -m x` alone, with nothing staged
- **THEN** no ledger file is staged, and the command fails as it would have without the tool

#### Scenario: An empty commit asked for stays empty

- **WHEN** the agent runs `git commit --allow-empty -m x` alone, with nothing staged
- **THEN** no ledger file is staged, and the commit it makes is empty

#### Scenario: A commit of all changes with nothing staged carries a ledger file

- **WHEN** the agent runs `git commit -am x` alone, with nothing staged, a tracked file changed and calls waiting to be staged
- **THEN** that commit holds the changed file and a ledger file

### Requirement: No ledger file is staged after a removal or move that may reach the ledger folder

The capture step SHALL stage nothing for a commit when a `git rm` or `git mv` before the commit is given a `-C` option that names a path that the command does not write out, or names a path with a wildcard or other pathspec magic, a path that the command does not write out, or the folder that the ledger file is written in or a folder above it, with its paths read from the directory where it runs, after the `cd`s before it and its own `-C` options.

#### Scenario: Removing the ledger folder before a commit takes no ledger file

- **WHEN** the agent runs `git rm -r .pr-cost && git commit -m x`, `git -C .pr-cost rm -r ledger && git commit -m x`, or `git -C "$P" rm -r ledger && git commit -m x`, where that variable holds `.pr-cost`, on a branch that holds ledger files, with calls waiting to be staged
- **THEN** no ledger file is staged, and the command removes the folder and commits, as it would without the tool

#### Scenario: Moving the ledger folder before a commit takes no ledger file

- **WHEN** the agent runs `git mv .pr-cost old && git commit -m x`, `git -C .pr-cost mv ledger ../old && git commit -m x`, or `git -C "$P" mv ledger ../old && git commit -m x`, where that variable holds `.pr-cost`, on a branch that holds ledger files, with calls waiting to be staged
- **THEN** no ledger file is staged, and the command moves the folder and commits, as it would without the tool

#### Scenario: Removing ledger files by a pattern before a commit takes no ledger file

- **WHEN** the agent runs `git rm '*.jsonl' && git commit -m x` or `git rm -r ':(icase).PR-COST' && git commit -m x` on a branch that holds ledger files, with calls waiting to be staged
- **THEN** no ledger file is staged, and the command removes those files and commits, as it would without the tool

### Requirement: No ledger file is staged where the ledger path has a filter or a working-tree encoding

The capture step SHALL stage nothing for a commit when git's attributes for the ledger path, from whichever file git reads them, include a filter or a working-tree encoding, because the commit could then hold something other than the entries as they were written.

#### Scenario: A ledger path with a filter takes no ledger file

- **WHEN** git's attributes for the ledger path give it a filter, such as Git LFS, or a working-tree encoding, whether the repository's `.gitattributes`, its `.git/info/attributes` or the person's own attributes file sets it
- **THEN** no ledger file is staged, and none is written in the working tree

### Requirement: A substitution counts as a command before the commit

Each command substitution and process substitution in the commit or in a command before it, whether in an argument, a leading assignment or a redirection, SHALL count as a command that comes before the commit (see "Only a top-level commit in the foreground, after nothing but listed commands, takes a ledger file"), unless all it runs is `cat` reading a here-document whose delimiter is quoted, in whole or in part, so that the shell expands nothing in its body.

#### Scenario: A commit message from a here-document still carries a ledger file

- **WHEN** the agent runs `git commit -m "$(cat <<'EOF'`, then the lines of the message, then `EOF` and `)"`, whose here-document's delimiter is quoted, with changes staged and calls waiting to be staged
- **THEN** that commit carries a ledger file

#### Scenario: A commit whose message another command writes takes no ledger file

- **WHEN** the agent runs `git commit -m "$(./message.sh)"` or `git commit -F <(./message.sh)`
- **THEN** no ledger file is staged, and the calls wait for a later commit

#### Scenario: A substitution before the commit takes no ledger file

- **WHEN** the agent runs `git add "$(./pick.sh)" && git commit -m x`, or `X="$(./prepare.sh)" git commit -m x`
- **THEN** no ledger file is staged, and the calls wait for a later commit

### Requirement: An unquoted here-document in or before the commit stages nothing

The capture step SHALL stage nothing for a commit when the commit or a command before it reads a here-document whose delimiter is not quoted, because the shell then runs any command substitution in its body.

#### Scenario: A here-document whose delimiter is not quoted takes no ledger file

- **WHEN** the agent passes a commit message in a here-document whose delimiter is not quoted, as in `git commit -F - <<EOF` or `git commit -m "$(cat <<EOF`, followed by the lines of the message and `EOF`
- **THEN** no ledger file is staged, and the calls wait for a later commit

### Requirement: A ledger file is staged in the worktree where its commit runs

The step SHALL find the worktree where the commit runs from the current directory that the hook's input gives, followed through each top-level `cd` before the commit and through the `-C` options that the commit's own git command is given before `commit`, and never from the directory that the hook runs in, and SHALL stage nothing when such a `-C` option names a path that the command does not write out (see "A ledger file is staged only for a commit whose branch and contents the step can tell").

#### Scenario: A `-C` after `commit` is not a path

- **WHEN** the agent runs `git commit -C HEAD` alone, on a branch that has a commit, with changes staged and calls waiting to be staged
- **THEN** that commit carries a ledger file

#### Scenario: A commit in another repository stages nothing here

- **WHEN** the agent runs `git -C <another repository> commit`
- **THEN** no ledger file is staged in this repository

#### Scenario: A commit whose `-C` path is not written out takes no ledger file

- **WHEN** the agent runs `git -C "$WT" commit -m x`, where that variable holds the path of one of the repository's worktrees, with calls waiting to be staged there
- **THEN** no ledger file is staged, and the calls wait for a later commit

#### Scenario: A commit stages in the worktree where it runs

- **WHEN** calls were recorded in one of the repository's worktrees, with the branch now checked out there, and the agent commits there, while the hook runs in the repository's main worktree, or after a `cd` to that worktree's path, or with a `-C` before `commit` that names it, written out in the same command
- **THEN** the ledger file is staged in that worktree, holding those calls, and the main worktree's index is unchanged

### Requirement: A ledger file is added despite ignore rules and sparse checkouts, unless git refuses it

The step SHALL add the file even when the repository's ignore rules match it, or a sparse checkout leaves its folder out, and when git refuses to add it, the step SHALL remove the file it wrote and stage nothing (see "A ledger file is staged only for a commit whose branch and contents the step can tell").

#### Scenario: An ignored ledger path is still committed

- **WHEN** the repository's ignore rules match the ledger files
- **THEN** the agent's commit still carries its ledger file

#### Scenario: A sparse checkout still commits the ledger file

- **WHEN** the agent commits in a sparse checkout that leaves out the ledger folder
- **THEN** that commit still carries its ledger file

#### Scenario: A ledger file that git refuses to add is not left behind

- **WHEN** git refuses to add the ledger file, as it does where `core.safecrlf` is on and line endings are converted
- **THEN** no ledger file is staged, none is left in the working tree, and the calls wait for a later commit

### Requirement: A run that comes again before the same command stages nothing twice

A run that comes again before the same command, as when a call that another hook deferred is resumed, SHALL stage nothing new while the file it staged for that command is still staged and the branch that it was staged for is still checked out there, and when that branch is no longer checked out there, SHALL first take that file back, as the requirements from "A ledger file that no commit takes is taken back" to "A put-back is tried once, and in no other case" say.

#### Scenario: A run that comes again before a command stages that command's calls once

- **WHEN** the run before a `git commit` fires a second time for the same call, as when a call that another hook deferred is resumed, with the same branch checked out, and no commit has taken the file staged the first time
- **THEN** that commit carries one ledger file of those calls: the one staged the first time if it is still staged, or else a new one

#### Scenario: A run that comes again before a command after a change of branch takes that command's file back

- **WHEN** the run before a `git commit` fires a second time for the same call, as when a call that another hook deferred is resumed, after the person checked out another branch while the file staged the first time was still staged, no commit has taken that file since, and no other git command holds the index
- **THEN** that run takes the file back before the commit runs, and the commit carries none of the calls recorded on the first branch

### Requirement: A ledger file that no commit takes is taken back

A commit holds a ledger file in a worktree when the commit checked out there holds it. When the result of the command that the file was staged for returns, whether the command succeeded or failed, the run after that command SHALL take the file back, from the index and the working tree of the worktree where it was staged, unless a commit holds it there, and its calls SHALL wait for a later commit.

#### Scenario: A commit that does not happen leaves nothing staged

- **WHEN** the step has staged a ledger file for a `git commit` that then fails, no commit has taken the file, and no other git command holds the index when the run after that command runs
- **THEN** after that run, the ledger file is neither staged nor in the working tree, and the agent's next commit on that branch in the worktree where the file was staged carries its calls

### Requirement: A ledger file whose command is refused at a permission prompt or by a permission rule, blocked, cancelled or interrupted is taken back by a later run

A command that gets no run after it (see "A ledger file that no commit takes is taken back"), because it was refused at a permission prompt or by a permission rule, blocked by another hook, cancelled or interrupted, SHALL have its file taken back the same way by any later run of the step in the repository, in that session or another, that finds the command over: by its result in a transcript, by a later call of the agent that ran it, by that agent having stopped, or by its session having ended.

#### Scenario: A commit refused at a permission prompt or by a permission rule leaves nothing staged

- **WHEN** the step has staged a ledger file for a `git commit` that is then refused at a permission prompt or by a permission rule, blocked by another hook, or cancelled, the transcript then holds that command's result, no commit has taken the file, and no other git command holds the index at the step's next run
- **THEN** after that run, the ledger file is neither staged nor in the working tree, and a later commit on that branch in the worktree where the file was staged carries its calls

#### Scenario: A session's end takes back what its commands left staged

- **WHEN** a session ends while the step has a ledger file staged for one of its commands that no commit took, such as a `git commit` that was interrupted, no other git command holds the index of its worktree, and the session's transcript holds more than that run can read within its time budget
- **THEN** the run when the session ends takes the file back, from the index and the working tree

#### Scenario: A later session takes back what an earlier one left staged

- **WHEN** a session was interrupted while the step had a ledger file staged for its `git commit`, no commit took the file, no later run of that session took it back, as when its process was then killed, and another session's run in the repository finds that command's result in the earlier session's transcript while no other git command holds the index
- **THEN** that run takes the file back, from the index and the working tree

### Requirement: A ledger file that a commit takes stays taken

Once a run finds a commit holding a ledger file that the step staged, the step SHALL note the file's calls as taken in that run's clone, and SHALL never stage them again there, whatever later removes the file from the branch, the index or the working tree. A fresh clone at the same path holds no note, and a session resumed there stages none of the calls that answer a line written before its first run there that finds both switches on (see "A removed store lets no earlier call be recorded").

#### Scenario: A ledger file that a person removes stays removed

- **WHEN** a run of the step has found the commit checked out in a worktree holding a ledger file that the step staged, while no other git command held that worktree's index, and the person then removes that file there with `git rm`, with or without `--cached`, or with `git reset`, mixed or `--hard`, to a commit before the one that holds it, and the session goes on in that run's clone
- **THEN** no run of the step puts the file back there, and no ledger file that the step stages there later holds its calls

#### Scenario: A ledger file that a person removes stays removed for another session

- **WHEN** a run of the step has found the commit checked out in a worktree holding a ledger file that the step staged, while no other git command held that worktree's index, the person then removes that file there with `git rm` and commits, and another session then commits there, in that run's clone, with no change of branch there in between
- **THEN** no ledger file that the step stages for that session's commit holds any of the calls that the removed file held

#### Scenario: A fresh clone does not stage a removed ledger file's calls again

- **WHEN** a run of the step has found a commit holding a ledger file that the step staged, whose calls' lines give the repository root as their working directory, the person then removes that file with `git rm`, commits and pushes, and the session is then resumed in a fresh clone of that branch, at the same path, with no change of branch there before the agent's next commit
- **THEN** the agent's next commit there carries none of the calls that the removed file held

### Requirement: Only a ledger file that no run has found in a commit is taken back

A take-back SHALL NOT remove a file from a worktree where a commit holds it (see "A ledger file that no commit takes is taken back"). The step SHALL take back only a file that it staged and that no run has found a commit holding, and SHALL leave any other ledger file to git, wherever git leaves it.

#### Scenario: A take-back leaves a committed file in place

- **WHEN** a commit takes the ledger file after its command's result has returned and before a take-back of that file runs, as a commit that Claude Code moved to the background at its timeout can, and before the step next runs there with that commit checked out and the index free, nothing but a take-back removes the file from the index or the working tree, and no other commit is made in that worktree
- **THEN** the file stays in that commit, and after that run the index and the working tree hold it as that commit does

#### Scenario: A ledger file that a removal leaves is left to git

- **WHEN** the agent's commit took a ledger file that the step staged, that commit has a parent, a run of the step has found that commit checked out, and then, with that commit still checked out and that file in the working tree, the agent runs `git reset HEAD~1` or `git reset -N HEAD~1` alone, or the person removes that file from the index with `git rm --cached` and commits, and the step's next run comes before any other git command
- **THEN** after that run, the working tree still holds that file, the index still has no entry for it, or only the intent-to-add index entry that `git reset -N` leaves, and no ledger file that the step stages later in that clone holds its calls

#### Scenario: A squash with a plain reset keeps its ledger files

- **WHEN** two of the agent's commits in a row took ledger files that the step staged, the first of them has a parent, a run of the step has found each of them checked out, no ignore rule matches the ledger path and no sparse checkout leaves it out, and then, with the second of them checked out, the agent runs `git reset HEAD~2` alone, and then `git add -A && git commit`, while no other git command holds the index
- **THEN** that commit holds both ledger files

### Requirement: A take-back leaves the file for a later run while the index is in use

A take-back SHALL leave a ledger file for a later run while another git command holds the index of the worktree that it would remove the file from.

#### Scenario: A take-back waits while the index is in use

- **WHEN** a ledger file is due to be taken back, and another git command that does not commit the file holds the index lock of its worktree
- **THEN** the run leaves the file and the lock as they are, and a later run takes the file back

### Requirement: Each take-back is noted

For each ledger file that it takes back from a worktree, the step SHALL note the commit that it found checked out there, not holding the file, and whether it removed the file from the index, the working tree or both.

#### Scenario: A take-back notes the commit it found and what it removed

- **WHEN** a run of the step takes a ledger file back from both the index and the working tree of a worktree
- **THEN** the step has noted, for that file, the commit that the run found checked out there, and that the run removed the file from both

### Requirement: A ledger file that a take-back removed is put back for a commit that holds it

After a take-back of a ledger file from a worktree (see "Each take-back is noted"), the first later run there that finds another commit checked out and the index free SHALL put the file back where the take-back removed it, as that commit holds it, when that commit holds it: into the index, when the take-back removed it from there and the index lacks it, and then into the working tree, when the take-back removed it from there, the index holds it as that commit does and the working tree lacks it.

#### Scenario: A ledger file that a commit takes while a take-back runs is put back

- **WHEN** a commit takes the ledger file after its command's result has returned and while a take-back of that file runs, as a commit that Claude Code moved to the background at its timeout can, and before the step next runs there with that commit checked out and the index free, nothing but a take-back removes the file from the index or the working tree, and no other commit is made in that worktree
- **THEN** the file stays in that commit, and after that run the index and the working tree hold it as that commit does

#### Scenario: A ledger file comes back with a commit that its own command reset away

- **WHEN** the agent runs `git commit && git reset HEAD~1` alone, for a commit that has a parent and for which the step staged a ledger file, and then, with that commit's parent still checked out, runs a mixed `git reset` alone, back to that commit, while no other git command holds the index
- **THEN** after the run that follows that reset, the index and the working tree hold the file as that commit does, and the agent's next commit carries none of its calls

### Requirement: A put-back is tried once, and in no other case

After a take-back of a ledger file from a worktree (see "Each take-back is noted"), the first later run there that finds another commit checked out and the index free SHALL, once it has done what "A ledger file that a take-back removed is put back for a commit that holds it" says, forget the take-back's note, whether it put the file back or not. The step SHALL put back no file in any other case.

#### Scenario: A file that a later commit deleted is not put back

- **WHEN** a take-back removes a ledger file while a commit that takes it is still running, the person then makes another commit on that branch in that worktree that does not hold the file, before any run of the step finds the first commit checked out there, and that other commit stays checked out there until the agent's next commit on that branch in that worktree
- **THEN** no run of the step puts the file back, and the agent's next commit on that branch in that worktree carries its calls

#### Scenario: A file removed from the index while its commit runs stays removed

- **WHEN** a commit that takes the ledger file is still running after its command's result has returned, another command removes the file from the index with `git rm --cached`, a take-back of the file then finds it only in the working tree, and the step next runs there with that commit checked out and the index free
- **THEN** after that run, neither the index nor the working tree holds the file, and the next commit there does not hold it

#### Scenario: A soft reset back to a commit that its own command reset away leaves its ledger file out

- **WHEN** the agent runs `git commit && git reset HEAD~1` alone, for a commit that has a parent and for which the step staged a ledger file, a run of the step then takes that file back from the working tree alone, and next, with that commit's parent still checked out and nothing having put the file in the index or the working tree since, the agent runs `git reset --soft` alone, back to that commit, while no other git command holds the index
- **THEN** after the run that follows that reset, neither the index nor the working tree holds the file, and no ledger file that the step stages there later holds its calls

#### Scenario: A put-back does not undo a staged removal

- **WHEN** a run of the step has found a commit holding a ledger file that the step staged, the person then removes that file from the index with `git rm --cached` and commits, the step's next run comes, and then `git reset --soft HEAD~1` runs alone, while no other git command holds the index
- **THEN** after the step's next run, the index still has no entry for that file, and the next commit there does not hold it unless a command adds the file again

#### Scenario: A put-back note is forgotten after its run

- **WHEN** the step has taken a ledger file back and noted the commit it found checked out, and the first later run there finds another commit checked out, the index free, and that commit not holding the file
- **THEN** that run puts nothing back, and after it the store holds no note for that file

### Requirement: Runs at the same time keep every note whole

Two runs of the capture step at the same time, such as the main agent's and a subagent's, or those of two worktrees of one repository, SHALL NOT split or interleave each other's notes, and SHALL NOT both record the same call. The step SHALL write its store only by replacing it whole, under a lock that the operating system releases when the process that holds it ends, so that a run killed while it writes leaves the store whole and leaves no lock behind.

#### Scenario: Two runs at once

- **WHEN** two runs of the capture step go over the same transcripts at the same moment
- **THEN** every note that either keeps is whole, and no call is recorded twice

#### Scenario: Two worktrees share one note of a call

- **WHEN** the main agent in this repository's main worktree and a subagent in one of its worktrees both read the subagent's transcript
- **THEN** each of its calls is recorded once

#### Scenario: A run killed while it writes leaves its store whole

- **WHEN** a run of the step is killed while it writes its store
- **THEN** the store is whole, as it was before that write or as that write left it, and the next run takes the lock and goes on

### Requirement: The capture step is one self-contained file

The capture step SHALL be one Python file that imports nothing but Python's standard library, so that it runs in Python's isolated mode, which imports nothing from the file's own folder, and an adopter can copy it into their repository whole.

#### Scenario: The capture step runs alone in isolated mode

- **WHEN** the capture step's file is copied into a folder that holds nothing else but a planted `json.py`, and run with `python3 -I`
- **THEN** it runs, and the planted module is not imported

### Requirement: The capture step's first line names its release

The capture step's first line SHALL name the release that it comes from.

#### Scenario: The hook file names its release

- **WHEN** the capture step's file at the commit of a release is read
- **THEN** its first line names that release

### Requirement: The capture step starts only git, from an absolute path

The step SHALL start no program but git, which it SHALL find at an absolute path, looking only in the folders that the absolute entries of `PATH` name, and in none of them that lies inside this repository's working trees or its git common directory. Before it starts git, it SHALL change its own current directory to a folder that only the system's administrator can write, such as Windows' system folder, and it SHALL name the folder that each git command works in.

#### Scenario: A program planted in the current directory is not run

- **WHEN** the step runs on Windows, with a program named `git` planted in Claude's current directory, in the repository's folder and in a folder that a relative entry of `PATH` names
- **THEN** the step starts none of them, and records and stages with the git that an absolute entry of `PATH` names

#### Scenario: A git in a folder of the repository is not run

- **WHEN** an absolute entry of `PATH`, such as one that a tool which sets up a folder's environment adds, names a folder inside the repository's working tree that holds a program named `git`
- **THEN** the step does not start it, and records and stages with the git that another absolute entry of `PATH` names

#### Scenario: A git in a worktree outside the repository's folder is not run

- **WHEN** an absolute entry of `PATH` names a folder inside a linked worktree of this repository that lies outside the repository's folder, and that folder holds a program named `git`
- **THEN** the step does not start it, and records and stages with the git that another absolute entry of `PATH` names

#### Scenario: A checkout whose git folder holds no `commondir` file is recorded

- **WHEN** the project directory is a submodule's checkout, or a working tree whose git folder was moved out of it, so that its `.git` file names a folder that holds no `commondir` file, and a session there makes calls and commits
- **THEN** the step takes that folder as the git common directory, keeps its store there, and records the session's calls and stages a ledger file for the commit

#### Scenario: A run that cannot read the files that name the worktrees starts no program

- **WHEN** the project directory's `.git` file, the `commondir` file in the folder that it names, or the `gitdir` file of a folder in the git common directory's `worktrees/` cannot be read or is not a regular file, as a named pipe is not, or a folder in `worktrees/` holds no `gitdir` file
- **THEN** the run starts no program, records, stages, takes back and puts back nothing, says so on standard error in its own words, and exits with success

#### Scenario: A run in a linked worktree whose main worktree it cannot tell starts no program

- **WHEN** the project directory is a linked worktree whose git common directory is not named `.git`, such as a linked worktree of a submodule, a worktree of a bare repository in a folder named `repo.git`, or a linked worktree of a repository whose git folder was moved out of its working tree to a folder named `gd`
- **THEN** the run starts no program, records, stages, takes back and puts back nothing, says so on standard error in its own words, and exits with success

### Requirement: Git runs without the session's git variables

The capture step SHALL start every git command without the session's environment variables whose names begin with `GIT_`, setting only its own, so that the session's environment chooses neither the repository, its index, its objects nor the files that git reads its settings from, save for the one reading of the opt-in in the session's environment that "Git's own reading of the opt-in can turn capture off, never on" in `switch-and-opt-in` asks for, and SHALL start every other one without `PWD`.

#### Scenario: The environment cannot move the store or a staged ledger file into another repository

- **WHEN** the session's environment sets `GIT_DIR`, `GIT_WORK_TREE` or `GIT_INDEX_FILE` to name another repository or its index, and runs of the step record calls made here and stage a ledger file for a `git commit` here
- **THEN** the store is in this repository's git common directory, the ledger file is staged in this repository's index alone, and the other repository is left as it was

#### Scenario: A variable that stops git's search does not stop capture

- **WHEN** the session's environment sets `GIT_CEILING_DIRECTORIES` to this repository's folder, and a session makes calls from a folder inside it
- **THEN** those calls are recorded in this repository

#### Scenario: Only git's reading of the opt-in in the session's environment keeps its `PWD`

- **WHEN** the session's `PWD` names the repository's top level through a symbolic link, and a run that finds both switches on stages a ledger file
- **THEN** git's reading of the opt-in in the session's environment runs with that `PWD`, and every other git command that the run starts runs without `PWD`

### Requirement: Capture reads both switches before it starts any program

The capture step SHALL read both switches (see "Capture runs only where the tool is on and the person has opted in" in `switch-and-opt-in`) before it starts any program. A run whose own reading finds either off SHALL start git only to find its store and, where one exists, to do there what `switch-and-opt-in` says, and one whose reading finds both on but git's reading of the opt-in finds capture off SHALL start git only for that reading and then as such a run.

#### Scenario: A run that finds a switch off starts git only for its store

- **WHEN** a run's own reading finds the tool or the person's capture off, and no store exists, or its store notes no file to take back or put back
- **THEN** the run reads both switches before it starts any program, and every program that it starts is git, run only to find the store and to do in it what `switch-and-opt-in` says

#### Scenario: A run that learns from git that capture is off starts git only for that and its store

- **WHEN** a run's own reading finds both switches on, git's reading of the opt-in then finds capture off in a file that the person's `~/.gitconfig` includes, and no store exists
- **THEN** every program that the run starts is git, run only to read the opt-in and to find the store, and no store is created

### Requirement: Capture never breaks or steers the session

A failure inside the capture step SHALL NOT stop or fail the agent's session, and on failure the step SHALL leave the ledger and its store as they were. The registered command SHALL exit with success even when its script cannot be read or started, in each shell that Claude Code runs a hook's command in: `sh`, Git Bash on Windows, and PowerShell on Windows without Git Bash. The step SHALL print nothing on standard output and SHALL let no git command that it runs print there.

#### Scenario: An unreadable transcript is skipped

- **WHEN** the transcript path the hook receives does not exist
- **THEN** the step exits with success and records nothing

#### Scenario: Capture never asks the agent to continue

- **WHEN** the step fails for any reason, including when its script cannot be read or started
- **THEN** the registered command exits with success and has printed nothing on standard output

#### Scenario: The registered command succeeds in PowerShell

- **WHEN** the registered command runs in Windows PowerShell or in PowerShell 7, as Claude Code runs a hook's command on Windows without Git Bash, and its script cannot be found or Python cannot be started
- **THEN** the command exits with success and prints nothing on standard output

#### Scenario: Nothing that git prints reaches standard output

- **WHEN** a run of the step stages a ledger file, a later run takes a ledger file back, and both read ledger files whose names and contents hold hostile text, on a branch that holds them
- **THEN** neither run prints anything on standard output, not even what the git commands it runs print, such as the `rm '<path>'` line of `git rm --cached`

#### Scenario: A transcript that is not a regular file is not opened

- **WHEN** the transcript path that the hook receives, or that a note of the store names, is a named pipe or a folder
- **THEN** the run opens nothing there, and exits with success

### Requirement: The registered command runs the hook file only when its checksum matches

The registered command SHALL carry the SHA-256 of the hook file that the adopter copied, SHALL read the hook file in the working tree once, and SHALL run what it read only when that matches the checksum, so that a hook file that a checked-out branch changes runs none of its code, and the command then exits with success too.

#### Scenario: A changed hook file is not run

- **WHEN** the hook file in the working tree differs from the one whose checksum the registered command carries, as after a checkout of a branch that changes it
- **THEN** the registered command runs none of that file's code, prints nothing on standard output and exits with success, in each shell that Claude Code runs a hook's command in

### Requirement: The capture step writes only its own words and numbers to standard error

The capture step SHALL write to standard error only its own words and numbers, never text taken from the transcript, the hook's input or the store, from a ledger file or its name, or from what a git command printed, nor a hash of any of them.

#### Scenario: A failure message quotes nothing from the transcript

- **WHEN** a transcript line that cannot be read contains text
- **THEN** the message on standard error contains none of that text

#### Scenario: Standard error carries no ledger or transcript text

- **WHEN** a run of the step reads transcript lines and ledger files whose contents or names hold hostile text, some of which it cannot read, and the git commands it runs print messages about them
- **THEN** nothing that the run writes on standard error contains any of that text, or anything that a git command printed

#### Scenario: Standard error carries nothing from the store

- **WHEN** a run of the step fails while the store notes a staged ledger file whose worktree's and transcript's paths, session id and `tool_use_id` are distinct marker strings
- **THEN** nothing that the run writes on standard error contains any of those markers, or a hash of one

### Requirement: The capture step finishes within a time budget

The capture step SHALL finish within a time budget, leaving what it has not read for a later run.

#### Scenario: A long transcript does not hold up the session

- **WHEN** reading the transcript would take longer than the time budget
- **THEN** the step stops at the budget and exits with success, and a later run records the rest

### Requirement: The store is versioned: an earlier version is upgraded, an unknown one left alone

The store SHALL carry the version of its format from the first release on, in a field that every release reads in the same way. A run that finds a store of an earlier version SHALL rewrite it in its own, keeping its waiting calls and its notes of taken calls and of staged and taken-back ledger files, and beginning every session's interval anew, and one that finds a version that it does not know SHALL record, stage, take back and put back nothing, leave the store as it was, and exit with success.

#### Scenario: A store of a format the step does not know is left alone

- **WHEN** a run of the step finds its store at a format version that it does not know, as one that a later release of the step wrote
- **THEN** it records, stages, takes back and puts back nothing, leaves the store as it was, and exits with success

#### Scenario: A store that an earlier release wrote is upgraded

- **WHEN** a run of the step finds a store that an earlier release wrote, which notes a staged ledger file and an open interval
- **THEN** it rewrites the store in its own version, keeps the staged file's note, and records no call that answers a line written before that run

#### Scenario: A store that a later release wrote is left alone by a run with a switch off

- **WHEN** a run that finds either switch off finds a store whose version is one that a later release gives, and whose other fields are of a form that the run's own version does not have
- **THEN** it leaves the store as it was, and exits with success

### Requirement: The store keeps only what attribution, deduplication and take-backs need

The store SHALL hold only its format's version; for each session, hashes of its id and its transcripts' paths, where runs read each transcript, its intervals, its flag for calls whose repository could not be told, and its last run's time; each waiting call's entry and each flag due with its day, with hashes of its session, worktree and branch; each taken call's hash and day; and the notes of ledger files (see "A ledger file's note keeps only what a take-back needs").

#### Scenario: The store holds ids and paths only as hashes while no file is staged

- **WHEN** a session's runs have recorded calls that wait to be staged, no ledger file is staged or due to be put back, and the session's id, its transcript's path, Claude's current directory, the branch's name and every `tool_use_id` are distinct marker strings
- **THEN** none of those markers appears in the store

#### Scenario: The store holds only the fields that its format documents

- **WHEN** runs of the step record calls, flag calls left out, stage a ledger file, take it back and stage it again
- **THEN** after each run every field of the store is one that the store's format documents

### Requirement: A ledger file's note keeps only what a take-back needs

The store's note of a ledger file that a run staged SHALL hold only the file's path, its worktree's name, hashes of its branch, its session and its command's `tool_use_id`, its transcript's path, its flags and its calls, until a run finds a commit holding the file or takes it back, and the note of a take-back only the file's path, its worktree's name, the commit found and what it removed, until a run puts the file back or forgets it.

#### Scenario: A staged file's note keeps its paths only until it is resolved

- **WHEN** the step has staged a ledger file whose worktree's name and path and transcript's path are distinct marker strings, and a later run finds a commit holding the file, or takes it back and has nothing to put back
- **THEN** the worktree's path never appears in the store, and after that run neither of the others does

### Requirement: The store keeps nothing past its retention window

The step SHALL record no call whose day is more than the store's retention window, which its format documents, before the run's day. Each run that finds a store of a version that it knows, whatever the switches say, SHALL drop each waiting call, flag due and note of a taken call once its day is that old, and a session's notes once none of its runs came within the window; SHALL take back, as for a command that is over, a ledger file whose note is that old; and drop a take-back's note that old.

#### Scenario: A call older than the retention window is not recorded

- **WHEN** a run reads a call made inside an interval when both switches were on, whose day is more than the retention window before the run's day
- **THEN** the call is not recorded

#### Scenario: A waiting call is dropped at the end of the retention window

- **WHEN** a recorded call has waited to be staged until its day is more than the retention window before a run's day
- **THEN** after that run the store no longer holds it, and no ledger file that the step stages later holds it

#### Scenario: A session's notes are dropped when it has not run within the retention window

- **WHEN** no run of a session has come within the retention window, and a run of another session comes
- **THEN** after that run the store holds no note of the first session

#### Scenario: A flag is dropped at the end of the retention window

- **WHEN** a flag for calls left out has been due, with no ledger file staged for its worktree and branch, until its day is more than the retention window before a run's day
- **THEN** after that run the store no longer holds that flag

#### Scenario: A staged ledger file older than the retention window is taken back

- **WHEN** a ledger file was staged for a command that no run has found over, its note is older than the retention window, no commit holds the file, and no other git command holds the index
- **THEN** the next run takes the file back, from the index and the working tree

#### Scenario: Calls dropped for their age are flagged

- **WHEN** a recorded call has waited to be staged until its day is more than the retention window before a run's day, and the agent then commits in that call's worktree and on its branch
- **THEN** that commit carries no entry for that call, and its ledger file says that calls were left out for their age, with no count

### Requirement: A store that holds nothing is removed

A run that leaves the store holding no session's notes, no call, no flag and no note of a ledger file SHALL remove the store's file and its folder, so that the git common directory keeps nothing of the tool's once nothing waits.

#### Scenario: An empty store is removed

- **WHEN** a run leaves the store holding no session's notes, no call, no flag and no note of a ledger file
- **THEN** after that run the git common directory holds no file or folder of the store

#### Scenario: A store that holds only a flag is kept

- **WHEN** a run leaves the store holding only a flag due, whose day is within the retention window
- **THEN** the store is still there after that run, and holds that flag

### Requirement: The store is readable and writable by its owner alone

On each write, the capture step SHALL leave the store's folder and file readable and writable by their owner alone, except on Windows, never through a link; SHALL keep each user's store in its own folder of the git common directory where the system numbers users; SHALL leave alone a store whose file or folder is a link or a reparse point, is not a regular file or folder, or is not its user's; and SHALL act on a note only for a ledger file of its own form, in a worktree of this repository.

#### Scenario: The store is created for its owner alone

- **WHEN** a run creates the store on Linux or macOS, under a umask that lets every user read new files
- **THEN** only the store's owner can read, write or enter its folder, and read or write its file

#### Scenario: A store reached through a link is left alone

- **WHEN** the store's folder or file is a symbolic link
- **THEN** the run writes nothing through it, records, stages, takes back and puts back nothing, and exits with success

#### Scenario: A store that another user owns is left alone

- **WHEN** the store's file is owned by another user than the one the run runs as
- **THEN** the run records, stages, takes back and puts back nothing, leaves the store as it was, and exits with success

#### Scenario: A note that names a file outside a ledger folder is not acted on

- **WHEN** the store's note of a staged or taken-back ledger file names a path outside the ledger folder, or one of another form than the step writes, or a worktree whose git common directory is not this repository's
- **THEN** the run removes, stages and puts back no file for that note, drops the note, and exits with success

#### Scenario: Each write keeps the store its owner's alone

- **WHEN** on Linux or macOS the store's folder has mode 0755 and its file mode 0644, the umask lets every user read new files, and a symbolic link stands at the name that a run writes its new store under
- **THEN** after the run's write the folder has mode 0700 and the file 0600, nothing was written through the link, and the folder holds no other file that a run wrote

#### Scenario: Each user has a store of their own

- **WHEN** two users of a system that numbers users, such as root in a container and the person on the host, run sessions in one clone that git trusts for both, whichever of them runs first
- **THEN** each run reads and writes only the store of the user it runs as, which only that user can enter, and records, stages and takes back for that user's sessions as if the other's store did not exist

#### Scenario: A run that cannot make its store's folder records nothing

- **WHEN** no store of the user that a run runs as exists, and the git common directory does not let that user create a folder
- **THEN** the run records, stages, takes back and puts back nothing, says so on standard error in its own words, and exits with success

#### Scenario: On Windows, a store reached through a junction is left alone

- **WHEN** on Windows the store's folder is a junction or another reparse point
- **THEN** the run writes nothing through it, records, stages, takes back and puts back nothing, and exits with success

#### Scenario: A folder replaced by a link during a run is not written through

- **WHEN** on Linux or macOS, after a run has checked its store's folder and before it writes the store, the folder is moved away and a symbolic link to another folder is put in its place
- **THEN** the run creates, renames and removes no file in the folder that the link names

### Requirement: A removed store lets no earlier call be recorded

When the store is removed, by the person or otherwise, or does not parse, which it does only when a run cannot read a version from it, or reads one that it knows from a store that is not of that version's form, the capture step SHALL record no call that answers a line written before the next run that finds both switches on, which SHALL begin a new interval, and SHALL leave to git any ledger file that a run staged before the removal.

#### Scenario: Calls made before the store was removed are not recorded

- **WHEN** a session's runs have recorded calls, the store is then removed, and a later run finds both switches on
- **THEN** none of the calls that answer a line written before that later run is recorded, and the calls that answer lines written after it are recorded

#### Scenario: A ledger file staged before the store was removed is left to git

- **WHEN** the step has staged a ledger file, the store is then removed, and a later run comes
- **THEN** that run does not take the file back, and the file stays as git holds it

#### Scenario: A store that does not parse is treated as removed

- **WHEN** the store's file does not parse, as after a power loss or a sync that cut it short, or as when it gives a version that the run knows and a field of another form than that version's, and a run finds both switches on
- **THEN** the run records no call that answers a line written before it, leaves to git any ledger file staged before, and writes a new store in its place

### Requirement: Capture keeps no copy of a transcript

The capture step SHALL write no line of a transcript, and no value from one beyond the fields that an entry or the store's notes name, to any file, the store, a ledger file and a temporary file included, or to standard error, so that no transcript is kept for reprocessing.

#### Scenario: A planted string reaches no file but the store's note of a staged file

- **WHEN** every text value in a transcript and in the hook's input is a distinct marker string, except the model names and price attribute values that the price table lists, and runs of the step record calls, stage a ledger file, take it back and stage it again
- **THEN** no marker appears in any file that a run writes or in its standard error, but the worktree's name and the transcript's path in the store's note of a staged ledger file, and none appears there once no such note is left

### Requirement: A ledger file says when calls of its sessions were left out

When a run leaves out a call made here because it was not made inside an interval when both switches were on, or drops a waiting call at the retention window, the next ledger file staged for that call's worktree and branch SHALL say so; when it leaves out a call whose line gives no working directory, or a directory inside this repository's folder that names no repository that git can tell, the session's next ledger file here SHALL say so; each with no count, time or other fact about those calls.

#### Scenario: A ledger file says that calls were left out for consent

- **WHEN** a run leaves out calls of a session made in this repository before the person opted in, and the agent then commits calls of that session in the worktree and on the branch where those calls were made
- **THEN** the commit's ledger file says that calls were left out for consent, and holds no count, time or other fact about them

#### Scenario: A session whose calls were all inside an interval raises no flag

- **WHEN** every call of a session made in this repository was made inside one of its intervals when both switches were on, and each gives a working directory whose repository git can tell
- **THEN** no ledger file says that calls of that session were left out

#### Scenario: Calls left out in another repository raise no flag here

- **WHEN** a session makes calls in another repository before the person opts in, and then calls here inside an interval when both switches were on
- **THEN** no ledger file here says that calls were left out for consent

#### Scenario: A flag for calls left out goes only to their own branch

- **WHEN** a run leaves out for consent calls of a session made in one worktree on one branch, and the session's next commit here is made on another branch
- **THEN** that commit's ledger file says nothing of calls left out, and the next ledger file staged for the first branch in that worktree says that calls were left out for consent

#### Scenario: A flag goes back with the calls of a file taken back

- **WHEN** a ledger file that says calls were left out for consent is staged for a `git commit` that is then refused at a permission prompt, and a later run takes it back
- **THEN** the next ledger file staged for that worktree and branch says that calls were left out for consent

#### Scenario: A call made outside this repository's folder in a directory that is gone raises no flag

- **WHEN** a session's call gives a working directory outside this repository's folder that no longer exists, or that holds no repository, and the session then commits here
- **THEN** no ledger file here says that calls were left out
