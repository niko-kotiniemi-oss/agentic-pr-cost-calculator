## Purpose

Let a repository turn the tool on or off with one file, and let each person decide, for themselves or by the environment that they use, whether their own sessions are recorded, so that no one's usage is published without their consent and a pull request cannot turn off its own report.

Scenarios below that run the capture step follow the conventions that `usage-capture` states for its own scenarios.

## ADDED Requirements

### Requirement: Capture runs only where the tool is on and the person has opted in

The capture step SHALL record nothing unless the repository's configuration turns the tool on and the opt-in is on in the global git configuration where the session runs, which the person sets, or which the cloud environment that they use or their organization's managed settings set, and which is not part of the repository.

#### Scenario: No configuration file means no capture

- **WHEN** the capture step runs in a repository without the configuration file
- **THEN** nothing is recorded, and no ledger file is created

#### Scenario: A person who has not opted in is not recorded

- **WHEN** the repository turns the tool on, but the person running the session has not turned capture on
- **THEN** nothing is recorded, and no ledger file is created

#### Scenario: A repository's own git configuration cannot opt a person in

- **WHEN** only the repository's own git configuration turns capture on
- **THEN** nothing is recorded

#### Scenario: An environment's setup script can opt a person in

- **WHEN** the setup script of the cloud environment where a session runs has set `pr-cost.capture` to `true` in the global git configuration with `git config --global`, and the session makes calls in a repository that turns the tool on and then commits there
- **THEN** that commit adds a ledger file that holds those calls

### Requirement: Having the plugin opts no one in

The plugin SHALL record nothing for a session whose opt-in is not on, however the plugin came to that session, such as when an organization turns it on or requires it for its members.

#### Scenario: A plugin that an organization requires records nothing without the opt-in

- **WHEN** the step runs as the plugin in a session whose global git configuration does not turn capture on, as for a member who has not opted in and whose organization requires the plugin, in a repository that turns the tool on
- **THEN** nothing is recorded, no store is created and no ledger file is staged

### Requirement: One opt-in covers every agent that the tool records

Capture SHALL take the person's opt-in, `pr-cost.capture`, as the one opt-in for every agent whose calls the tool records, those that a later release adds among them, and SHALL read no opt-in of its own for any agent, so that no opt-in leaves one agent out. Tests SHALL fail otherwise.

#### Scenario: The one opt-in records each agent that the release records

- **WHEN** a repository turns the tool on, the person's opt-in is on, and a session of any agent that the surface manifest says the release records makes calls there and then commits
- **THEN** that commit adds a ledger file that holds those calls, whichever of those agents made them

#### Scenario: An opt-in key of its own for an agent changes nothing

- **WHEN** the person's global git configuration also sets a key under `pr-cost` that names an agent, such as `pr-cost.claude-code`, to `false` while the opt-in is on, or to `true` while it is off
- **THEN** capture records as it would without that key: the session's calls while the opt-in is on, and nothing while it is off

### Requirement: Capture reads the configuration file only as a regular file within its bound

The capture step SHALL read the repository's configuration file in the working tree only when it is a regular file no larger than the size bound that the configuration's format documents, and SHALL take the tool to be off otherwise, or when the file there is not valid.

#### Scenario: A configuration file that is not a regular file turns capture off

- **WHEN** the repository's configuration file in the working tree is a symbolic link, a named pipe or a folder, or is larger than its size bound
- **THEN** nothing is recorded, and the run ends without waiting on the file

### Requirement: The person's opt-in is read only from their global configuration files

The capture step SHALL read the person's opt-in (see "Capture runs only where the tool is on and the person has opted in") only from their global configuration files themselves, `~/.gitconfig` and git's configuration file in their XDG configuration folder (see "Only an absolute home folder is read" and "Only an absolute XDG folder is read"), not from files they include, ignoring any environment variable that points git at other configuration files or adds settings.

#### Scenario: The environment cannot opt a person in

- **WHEN** the session's environment points git's global configuration at a file that turns capture on, or adds the opt-in key through `GIT_CONFIG_COUNT` or `GIT_CONFIG_PARAMETERS`, and the person's own global configuration does not turn it on
- **THEN** nothing is recorded

#### Scenario: The opt-in key in an included file does not opt a person in

- **WHEN** the person's global configuration includes a file that is not one of their global configuration files, and only that included file turns capture on
- **THEN** nothing is recorded

#### Scenario: The XDG configuration file can opt a person in

- **WHEN** the repository turns the tool on and its own git configuration does not set capture, the person's `~/.gitconfig` exists and does not set capture, and git's configuration file in their XDG configuration folder turns it on
- **THEN** the session's calls are recorded

### Requirement: Only an absolute XDG folder is read

The capture step SHALL take git's configuration file in the person's XDG configuration folder to be `$XDG_CONFIG_HOME/git/config` when that variable holds an absolute path, and `~/.config/git/config` (see "Only an absolute home folder is read") otherwise.

#### Scenario: A relative XDG folder is not read

- **WHEN** `XDG_CONFIG_HOME` holds a relative path, and only a git configuration file at that path inside the repository turns capture on
- **THEN** nothing is recorded

### Requirement: Only an absolute home folder is read

The capture step SHALL take the home folder `~` to be the folder that `HOME` names when that variable holds an absolute path, and otherwise, on Windows, the one that git uses when `HOME` is not set, which is `HOMEDRIVE` and `HOMEPATH` together where they name a folder that exists and is not Windows' system folder, and `USERPROFILE` where they do not, and elsewhere none, and SHALL never read a configuration file from a relative path.

#### Scenario: The home folder is the one git reads on Windows

- **WHEN** on Windows, `HOME` holds an absolute path to a folder other than the person's profile folder, and a `.gitconfig` that turns capture on is in only one of the two folders
- **THEN** the session's calls are recorded when that file is in the folder that `HOME` names, and nothing is recorded when it is in the profile folder

#### Scenario: A relative home folder is not read

- **WHEN** `HOME` holds a relative path, and only a `.gitconfig` at that path inside the repository turns capture on
- **THEN** nothing is recorded

### Requirement: The home configuration file decides over the XDG one

Where both of the person's global configuration files (see "The person's opt-in is read only from their global configuration files") set the person's opt-in, `~/.gitconfig`, which git reads after the other, SHALL decide.

#### Scenario: The home configuration file decides when both set it

- **WHEN** git's configuration file in the person's XDG configuration folder turns capture on, and their `~/.gitconfig` turns it off
- **THEN** nothing is recorded

### Requirement: The person's opt-in is read by git's rules

The capture step SHALL read the person's opt-in (see "Capture runs only where the tool is on and the person has opted in") by git's rules for its configuration files: section and key names match in any case, a value is read without its quotes or a comment that follows it, the last value in a file decides, and a key in a subsection, such as `[pr-cost "x"]`, or in a comment is not the opt-in key.

#### Scenario: The last value in a file decides

- **WHEN** the person's `~/.gitconfig` sets `pr-cost.capture` to `false` and then, further down the same file, to `true`
- **THEN** the session's calls are recorded, and with the two values the other way round, nothing is recorded

#### Scenario: The opt-in key's names in any case, and its value in quotes, opt a person in

- **WHEN** the person's `~/.gitconfig` turns capture on only with `Capture = true` in a section written `[PR-Cost]`, or only with the value `"true"`
- **THEN** the session's calls are recorded

#### Scenario: A subsection or a comment does not opt a person in

- **WHEN** the person's `~/.gitconfig` sets capture to `true` only in a subsection, such as `[pr-cost "x"]`, or only in a comment
- **THEN** nothing is recorded

### Requirement: Only some of git's true values turn capture on

Of the values of the person's opt-in (see "The person's opt-in is read by git's rules"), only `true`, `yes`, `on` and `1`, in any case, and the key alone with no value SHALL turn capture on, and any other value SHALL leave it off, even one that git reads as true, such as `2`.

#### Scenario: Git's spellings of the setting opt a person in

- **WHEN** the person's `~/.gitconfig` turns capture on only with the value `Yes`, `on` or `1`, or only with the key alone and no value
- **THEN** the session's calls are recorded

#### Scenario: A number other than `1`, or a value that git cannot read, does not opt a person in

- **WHEN** the person's `~/.gitconfig` sets capture only to `2`, or only to a value that git cannot read as true or false, such as `maybe`
- **THEN** nothing is recorded

### Requirement: A repository's own git configuration can turn capture off

The capture step SHALL record nothing in a repository whose own git configuration turns capture off.

#### Scenario: A person can turn capture off in one repository

- **WHEN** the person has turned capture on in their global configuration, and the repository's own git configuration turns it off
- **THEN** nothing is recorded in that repository

### Requirement: Git's own reading of the opt-in can turn capture off, never on

Once a run finds both switches on, the capture step SHALL ask git, in the session's environment and again without its `GIT_` variables, for each value of the opt-in key here, and SHALL take capture to be off when either answer does not come within the run's time budget, gives no value or a refusal, ends in a value that is not true, or holds a file other than the person's two global configuration files, or the variables, whose last value is not true. What git reads SHALL never turn capture on.

#### Scenario: An opt-out in an included file turns capture off

- **WHEN** the person's `~/.gitconfig` turns capture on and includes, before or after the line that turns it on, under a condition that git finds true in this repository, a file that turns it off
- **THEN** nothing is recorded

#### Scenario: An opt-out under a condition that does not hold here leaves capture on

- **WHEN** the person's `~/.gitconfig` turns capture on and then includes, under a condition that git finds false in this repository, a file that turns it off
- **THEN** the session's calls are recorded

#### Scenario: An opt-out that git finds through the session's `PWD` turns capture off

- **WHEN** the person's `~/.gitconfig` turns capture on and includes a file that turns it off under a `gitdir:` condition that names the repository's folder through a symbolic link, the repository's `.git` is a folder, and the session's `PWD` names the repository's top level through that link
- **THEN** nothing is recorded

#### Scenario: A global configuration file that the environment names can turn capture off

- **WHEN** the person's `~/.gitconfig` turns capture on, and the session's environment points git's global configuration at another file, which does not turn it on
- **THEN** nothing is recorded

#### Scenario: A global configuration file that the environment names does not hide an opt-out

- **WHEN** the person's `~/.gitconfig` turns capture on and includes, under a condition that git finds true in this repository, a file that turns it off, and the session's environment points git's global configuration at another file, which turns capture on
- **THEN** nothing is recorded

#### Scenario: Variables that change what git reads do not hide an opt-out

- **WHEN** the person's `~/.gitconfig` turns capture on, and the system's git configuration, the repository's own, or a file that `~/.gitconfig` includes under a condition that git finds true in this repository turns it off, and the session's environment sets `GIT_CONFIG_NOSYSTEM`, or sets `GIT_DIR` to name another repository
- **THEN** nothing is recorded

#### Scenario: A reading of the opt-in that does not finish turns capture off

- **WHEN** the person's `~/.gitconfig` turns capture on, and the session's environment points git's global configuration at a named pipe that nothing writes to
- **THEN** nothing is recorded, and the run exits with success within its time budget

#### Scenario: An opt-out that the session's environment gives turns capture off

- **WHEN** the person's `~/.gitconfig` turns capture on, and the session's environment sets `GIT_CONFIG_COUNT=1`, `GIT_CONFIG_KEY_0=pr-cost.capture` and `GIT_CONFIG_VALUE_0=false`, as a cloud environment's variables can
- **THEN** nothing is recorded, and no ledger file is staged

#### Scenario: A later value that turns capture on does not undo an opt-out in an included file

- **WHEN** the person's `~/.gitconfig` turns capture on and then includes, under a condition that git finds true in this repository, a file that turns it off, and the repository's own git configuration, or a variable in the session's environment, then turns it on
- **THEN** nothing is recorded

### Requirement: Consent holds for each recorded call

Consent, the two switches that "Capture runs only where the tool is on and the person has opted in" requires, SHALL hold for each call that the capture step records, not only for the run that records it. The step SHALL record a call only when it was made inside one of its session's intervals when both were on (see "An interval when both switches were on begins and ends at a run" and "A call is inside an interval only when the line it answers and its first line are inside it").

#### Scenario: Calls made before a person opts in are not recorded

- **WHEN** the repository turns the tool on, a session makes calls while the person has not turned capture on, a run of the step then comes, and the person then turns capture on
- **THEN** none of the calls made before that run is recorded, and the calls that answer lines written after a later run that finds capture on are recorded

#### Scenario: Calls made before an opt-in are not recorded when no run came between

- **WHEN** the repository turns the tool on, a session makes calls while the person has not turned capture on, and the person turns capture on before the step's next run in that session
- **THEN** none of those calls is recorded, and the calls that answer lines written after that run are recorded

### Requirement: A call is inside an interval only when the line it answers and its first line are inside it

A call SHALL count as made inside an interval of its session when both switches were on (see "Consent holds for each recorded call") only when, by each line's own time, the line it answers, the nearest up its first line's chain of parents in its transcript that gives the person's prompt, a tool's result or a compaction's summary, was written at or after the run that began the interval and no later than the call's first line, and that first line no later than the interval's last run.

#### Scenario: A call already being made when its interval begins is not recorded

- **WHEN** a run that finds both switches on begins its session's interval while a call of that session is being made, which answers a line written before that run
- **THEN** that call is not recorded

#### Scenario: A call that answers no line of its transcript is not recorded

- **WHEN** the chain of parents that a call's first line names reaches no line of its transcript that gives a prompt or a tool result
- **THEN** that call is not recorded, whatever interval its lines fall in

#### Scenario: A call whose answered line was written after its first line is not recorded

- **WHEN** the line that a call answers gives a later time than the call's first line
- **THEN** that call is not recorded, whatever interval its lines fall in

#### Scenario: A line that Claude Code writes for itself is not the line a call answers

- **WHEN** a run that finds both switches on begins its session's interval while a call is being made, and the chain of parents from that call's first line passes, before the tool's result that the call answers, a line written after that run that Claude Code marks as its own or that gives a hook's output
- **THEN** that call is not recorded

#### Scenario: Lines are placed by their own times, not by their place in the file

- **WHEN** a transcript's lines stand in the file out of the order of their times, and their times carry an offset from UTC
- **THEN** each call is placed inside or outside an interval by the instants that its lines' times give, and not by where its lines stand in the file

### Requirement: A run that finds both switches on notes its time and a fingerprint

Each run of the capture step that finds both switches on, and no store whose version it does not know, SHALL note in its store the run's time, from the system's clock in UTC, which no environment variable sets, and a hash of a fingerprint, made of device and inode numbers, sizes and modification times and never of contents or paths, of the person's two global configuration files, each other file that git reads the opt-in key from in either of its two readings, and each link on the way to one.

#### Scenario: A fingerprint holds nothing of a configuration file's contents

- **WHEN** the person's global configuration files and the repository's own git configuration hold, beside the opt-in, distinct marker strings
- **THEN** no marker, and no hash of a marker, appears in the store

#### Scenario: The store holds no configuration file's path

- **WHEN** the person's `~/.gitconfig` includes, under a condition that git finds true in this repository, a file that turns capture on, the path to that file passes a folder whose name is a distinct marker string, and a run of the step finds both switches on
- **THEN** neither that file's path, nor the marker, nor a hash of either appears in the store

#### Scenario: The environment cannot move a run's time

- **WHEN** the session's environment sets `TZ` to a zone far from UTC, a run of the step has found both switches on, the person then turns capture off, the session makes calls, a run of the step comes, and the person then turns capture on again
- **THEN** none of the calls that the session made while capture was off is recorded

#### Scenario: A link pointed elsewhere and back changes the fingerprint

- **WHEN** the person's `~/.gitconfig` is a symbolic link, a run of the step finds both switches on, and the link is then pointed at another file and back before the step's next run
- **THEN** the next run notes another fingerprint

#### Scenario: A write to the repository's own git configuration, which does not set the opt-in key, leaves the fingerprint as it was

- **WHEN** the repository's own git configuration does not set the opt-in key, a run of the step finds both switches on, and the agent then runs `git push -u origin HEAD`, which writes that configuration
- **THEN** the next run notes the same fingerprint, and the interval goes on

### Requirement: A run that finds a switch off creates no store and notes no session

A run that finds either switch off SHALL create no store and add no note of its session to one. It SHALL remove a store that does not parse, and in one whose version it knows only end its session's interval, noting its time, and do what "An opt-out ends every session's interval and empties the store", "Ledger files are taken back and put back whatever the switches say" and, in `usage-capture`, "The store keeps nothing past its retention window" and "A store that holds nothing is removed" say.

#### Scenario: A person who has not opted in leaves no store

- **WHEN** the repository turns the tool on, no store exists, and a person who has not turned capture on runs a session there whose agent makes calls and commits
- **THEN** no run of the step creates a store, or creates or changes any file in the git common directory, and no ledger file is created

#### Scenario: A run with the repository's switch off adds nothing of its session to a store

- **WHEN** a store notes another session's interval, whose last run came within the retention window, no ledger file is due to be taken back or put back, and a run of a session that the store does not note finds the tool off in the repository, with the person's capture on
- **THEN** the run leaves the store as it was

#### Scenario: A run with a switch off still drops what the retention window ends

- **WHEN** a store notes only a session none of whose runs has come within the retention window, and a run of another session finds the tool off in the repository
- **THEN** after that run no store is left in the git common directory

#### Scenario: A run with a switch off removes a store that does not parse

- **WHEN** the store's file does not parse, as after a power loss or a sync that cut it short, and a run finds either switch off
- **THEN** after that run no store is left in the git common directory, and no ledger file is staged

### Requirement: An interval when both switches were on begins and ends at a run

A session's interval when both switches were on (see "Consent holds for each recorded call") SHALL begin only at a run that finds both on while the session has no open interval, never at the session's start, and SHALL end at its last run before one that finds either off or a fingerprint other than the last one that its store notes, which then begins the next interval if it finds both on and its clock has not moved back (see "A clock that moves back ends the session's intervals").

#### Scenario: Calls made while capture was off are not recorded when it is on again

- **WHEN** a run of the step has found both switches on, the person then turns capture off, the session makes calls, a run of the step comes, and the person then turns capture on again
- **THEN** none of the calls that the session made after the last run that found capture on, and before the next run that found it on again, is recorded

#### Scenario: Capture turned off and on again between two runs ends the interval

- **WHEN** a run of the step has found both switches on, the person then turns capture off in their `~/.gitconfig`, the session makes calls, and the person turns capture on again there before the step's next run
- **THEN** none of the calls whose first line was written after the earlier run and that answer a line written before the later run is recorded

#### Scenario: An opt-out and back in the repository's own git configuration between two runs is not seen

- **WHEN** the repository's own git configuration does not set the opt-in key, a run of the step finds both switches on, the person then turns capture off there, the session makes calls, and the person removes that setting again before the step's next run
- **THEN** the next run notes the same fingerprint, and the interval goes on

#### Scenario: Any change to the person's configuration files ends the interval

- **WHEN** a run of the step has found both switches on, the person then changes another setting in their `~/.gitconfig`, the session makes calls, and the next run finds both switches on
- **THEN** none of the calls that answer a line written before the later run reaches a ledger file staged after it, and the calls that answer lines written after the later run are recorded

### Requirement: A clock that moves back ends the session's intervals

A run that finds its clock earlier than the latest time that its session's runs noted, or that a line they read gave, SHALL end each of that session's intervals, begin none, and place no call that it or a later run reads inside any of them, so that a clock that moved back places no call that answers a line written before it inside an interval.

#### Scenario: A clock set back between two runs ends the interval

- **WHEN** a run of the step has found both switches on, the clock is then set back, the session makes calls, and the next run's clock reads earlier than the earlier run's
- **THEN** none of the calls that answer a line written before the later run is recorded, and the next ledger file staged for their worktree and branch says that calls were left out for consent

#### Scenario: A line from ahead of the clock ends the interval

- **WHEN** a run of the step reads a line whose time is later than its own clock reads once it has read that line
- **THEN** none of the calls that answer a line written before that run is recorded

#### Scenario: A clock set back past earlier lines begins no interval until it passes them

- **WHEN** a run of the step has found both switches on, the configuration file in the working tree then turns the tool off, the session makes calls, a run of the step comes, the clock is then set back to before those calls, the file turns the tool on again, and runs of the step come until the clock has passed the times of those calls' lines
- **THEN** none of those calls is recorded, and no run whose clock reads earlier than the latest of those times begins an interval

### Requirement: An opt-out ends every session's interval and empties the store

A run that finds the person's own capture off, in their global configuration, in the repository's own or as git reads it there, and a store whose version it knows, SHALL end every session's interval and remove every waiting call, flag due, note of a taken call and session's notes, but those that a take-back or a put-back still needs (see "Ledger files are taken back and put back whatever the switches say"), and the step SHALL never stage, after that run, a call made or a flag noted before it.

#### Scenario: Calls recorded before an opt-out are not staged

- **WHEN** calls were recorded and are waiting to be staged, the person then turns capture off, a run of the step comes, and the person turns capture on again before the agent's next commit
- **THEN** that commit carries none of those calls

#### Scenario: The calls of a file taken back after an opt-out are not staged again

- **WHEN** the step has staged a ledger file for a `git commit` that is then refused at a permission prompt, the person then turns capture off, and the step's next run finds that command over while no other git command holds the index
- **THEN** no later commit carries its calls

#### Scenario: An opt-out empties the store

- **WHEN** the store notes sessions, calls waiting to be staged and flags due, no ledger file is due to be taken back or put back, and a run then finds the person's capture off
- **THEN** after that run no store is left in the git common directory

#### Scenario: An opt-out keeps only what a take-back needs

- **WHEN** the step has staged a ledger file for a `git commit` that is then refused at a permission prompt, and a run of the step then finds the person's capture off before any run finds that command over
- **THEN** after that run the store holds no waiting call, no flag due, no note of a taken call and no session's notes, only the note of that file, and once a run has taken the file back, no store is left

#### Scenario: An opt-out that the session's environment gives empties the store

- **WHEN** the store notes sessions, calls waiting to be staged and flags due, no ledger file is due to be taken back or put back, and a run then comes in a session whose environment sets `GIT_CONFIG_COUNT=1`, `GIT_CONFIG_KEY_0=pr-cost.capture` and `GIT_CONFIG_VALUE_0=false`
- **THEN** after that run no store is left in the git common directory

#### Scenario: Turning capture on again after an opt-out records no earlier call

- **WHEN** a run of the step has found the person's capture off, the person then turns it on again, and a later run finds both switches on
- **THEN** none of the calls that answer a line written before that later run is recorded, though the store no longer notes how far any transcript was read

### Requirement: A run that began before an opt-out leaves nothing after it

A run of the capture step SHALL hold its lock from when it reads the store until it has written it, SHALL read both switches again under that lock before it writes a call to the store or stages a ledger file, and SHALL act only on a store whose file is still the one that its lock holds.

#### Scenario: An opt-out is not undone by a run that began before it

- **WHEN** a run of the step has found both switches on and read the store, and the person turns capture off before that run writes the store
- **THEN** that run writes no call to the store, stages no ledger file, and empties the store as a run that finds capture off does

#### Scenario: A run that waited for the lock writes nothing into a store that an opt-out removed

- **WHEN** a run of the step that found both switches on waits for the lock while a run that found capture off empties and removes the store, and capture stays off
- **THEN** no store is left once both runs are over

### Requirement: A change to the files that hold the opt-in is taken as an opt-out

A run that finds both switches on, and a fingerprint other than the last one that its store notes, whichever session's run noted it, SHALL first do what an opt-out does (see "An opt-out ends every session's interval and empties the store"), so that no call recorded before an opt-out that no run saw, or before any other change to those files, is staged.

#### Scenario: Calls recorded before an opt-out that no run saw are not staged

- **WHEN** calls were recorded and wait to be staged, the person turns capture off and on again with no run of the step in between, and a run then finds both switches on
- **THEN** the agent's next commit in the worktree and on the branch where those calls were made carries none of them, and its ledger file says that calls were left out for consent

#### Scenario: Another session's run drops calls recorded before an opt-out that no run saw

- **WHEN** a session's calls were recorded and wait to be staged, the person turns capture off and on again with no run of the step in between, and the next run, of another session in the same clone, finds both switches on
- **THEN** no commit made after that run carries any of those calls

#### Scenario: A copy of the store put back after an opt-out brings back no call

- **WHEN** a copy is made of a store that holds waiting calls, the person turns capture off, a run that finds it off empties the store, the person turns capture on again, and the copy is put back before the next run
- **THEN** none of those calls is staged

### Requirement: An opt-out leaves committed ledger files to git

An opt-out, a removal of the store, or the end of its retention window (see "The store keeps nothing past its retention window" in `usage-capture`) SHALL NOT make the capture step remove or change a ledger file that a commit holds, so that a ledger file that was pushed stays on its branch, in its history and in every clone of it.

#### Scenario: Committed ledger files stay after an opt-out

- **WHEN** a person's ledger files are committed and pushed, the person then turns capture off, and runs of the step come
- **THEN** each of those files is still on the branch, and in the index and the working tree as the commit checked out there holds it

#### Scenario: Ledger files in commits not yet pushed stay after an opt-out

- **WHEN** a person's ledger files are committed and not yet pushed, the person then turns capture off, and runs of the step come
- **THEN** each of those files is still in its commit, where the next push of its branch publishes it

### Requirement: Ledger files are taken back and put back whatever the switches say

The switches (see "Capture runs only where the tool is on and the person has opted in") SHALL keep no run of the capture step that the floors in `releases-and-compatibility` let go on from taking back and putting back ledger files, and noting as taken the calls of a file that a commit holds, as the requirements from "A ledger file that no commit takes is taken back" to "A put-back is tried once, and in no other case" in `usage-capture` say.

#### Scenario: A file staged before capture is turned off is still taken back

- **WHEN** the step has staged a ledger file for a `git commit` that is then refused at a permission prompt, the person then turns capture off, and the step's next run finds that command over while no other git command holds the index
- **THEN** that run takes the file back, from the index and the working tree

### Requirement: One file turns the tool on or off, and a pull request cannot turn off its own report

A repository SHALL turn the tool on by adding a configuration file that can be read as a valid configuration and enables the tool, and off by removing the file or disabling the tool in it. The report SHALL read the configuration from the default branch as it was before the merge and as it is after, only as a blob at each of those two commits and within the size bound that the configuration's format documents, and SHALL run when either turns the tool on.

#### Scenario: Disabled means silent

- **WHEN** a pull request merges, and the configuration disables the tool both before and after the merge
- **THEN** no comment is posted, and the job summary says that the configuration file after the merge disables the tool

#### Scenario: A pull request cannot turn off its own report

- **WHEN** a pull request that disables the tool merges
- **THEN** its report comment is posted

#### Scenario: The pull request that turns the tool on gets its report

- **WHEN** the pull request that adds a configuration file that turns the tool on merges
- **THEN** its report comment is posted

### Requirement: Capture reads the configuration in the working tree

Capture SHALL read the repository's configuration file (see "One file turns the tool on or off, and a pull request cannot turn off its own report") in the working tree.

#### Scenario: Capture follows the configuration in the working tree

- **WHEN** the configuration file in the working tree turns the tool off, and the commit checked out there holds one that turns it on
- **THEN** capture records nothing

### Requirement: A missing or unreadable configuration file neither turns the tool on nor stops the report

A configuration file that is missing at a commit, is not a regular file there, is larger than the size bound that the configuration's format documents or is not valid SHALL NOT turn the tool on at that commit, and SHALL NOT stop the report.

#### Scenario: A pull request that makes the configuration unreadable still gets its report

- **WHEN** the configuration turns the tool on before the merge, and a pull request replaces the configuration file with one that is not valid, as when its arrays nest so deep that Python's JSON reader raises an error on it, is larger than its size bound, is a symbolic link or is not a regular file
- **THEN** its report comment is posted

### Requirement: A configuration file with a key that the tool does not know, a key given twice or no `enabled` of `true` or `false` is not valid

A configuration file SHALL count as not valid (see "A missing or unreadable configuration file neither turns the tool on nor stops the report") when it is not a JSON object whose `enabled` is `true` or `false`, as `{}` is not, or, whatever the keys' values and `enabled` say, when it holds a key that the configuration's format, in the version of the tool that reads it, does not document, or gives a key more than once.

#### Scenario: A key that the tool does not know turns capture off

- **WHEN** the repository's configuration file in the working tree sets `enabled` to true and also holds a key that its format does not document, and the person running the session has turned capture on
- **THEN** nothing is recorded, and no ledger file is created

#### Scenario: A key that the tool does not know turns the report off after the pull request that adds it

- **WHEN** the configuration turns the tool on, a pull request that adds to it a key that its format does not document merges, and then another pull request, which leaves the configuration file as it is, merges
- **THEN** the first pull request's report comment is posted and says that it changed the tool's configuration, and the second pull request gets no comment, while the job summary of its merge says that the configuration file after the merge cannot be read as a valid configuration

#### Scenario: A configuration file that gives a key twice is not valid

- **WHEN** the repository's configuration file in the working tree gives `enabled` twice, first as false and then as true, which Python's JSON reader would read as true, and the person running the session has turned capture on
- **THEN** nothing is recorded, and no ledger file is created

#### Scenario: A configuration file without an `enabled` of `true` or `false` is not valid

- **WHEN** the repository's configuration file in the working tree is `{}`, or sets `enabled` to `1` or to `"true"`, and the person running the session has turned capture on
- **THEN** nothing is recorded, and no ledger file is created

### Requirement: The report says when the configuration after the merge does not turn the tool on

When the configuration before the merge turns the tool on and the configuration after it does not, the comment SHALL say, in the report's own words, that the tool is off after the merge, and whether the file there is missing, disables the tool or cannot be read as a valid configuration (see "A missing or unreadable configuration file neither turns the tool on nor stops the report"). When neither turns the tool on, the report's job summary SHALL say the same of the file after the merge.

#### Scenario: A pull request after which the tool is off is told so

- **WHEN** the configuration turns the tool on before the merge, and a pull request that adds to it a key that its format does not document merges
- **THEN** its comment says that the configuration file after the merge cannot be read as a valid configuration, so that the tool is off after it

#### Scenario: A pull request that removes the configuration file is told that it is missing

- **WHEN** the configuration turns the tool on before the merge, and a pull request that removes the configuration file merges
- **THEN** its comment says that the configuration file is missing after the merge, so that the tool is off after it

#### Scenario: A pull request that disables the tool is told so

- **WHEN** the configuration turns the tool on before the merge, and a pull request that sets `enabled` to false merges
- **THEN** its comment says that the configuration file after the merge disables the tool, so that the tool is off after it

#### Scenario: A merge with the tool off at both commits says why in its job summary

- **WHEN** the default branch has no configuration file, and a pull request merges that adds one that enables the tool and also holds a key that its format does not document
- **THEN** no comment is posted, and the job summary says that the configuration file after the merge cannot be read as a valid configuration

#### Scenario: A merge after which the tool is on says nothing of it being off

- **WHEN** the configuration turns the tool on both before and after the merge
- **THEN** the comment says nothing of the tool being off

### Requirement: A change to the configuration, the hook file, its registration or a workflow is flagged

When a pull request changes the configuration file, the hook file at the path that the README gives, `.claude/settings.json` or `.claude/settings.local.json`, the project settings files that can register it and set its environment, or any workflow file, its comment SHALL say so.

#### Scenario: A changed report is flagged

- **WHEN** a pull request changes the configuration file, the hook file, the workflow file that runs the report, or another workflow file
- **THEN** its comment says that the pull request changed the tool's configuration, its hook file or a workflow

#### Scenario: A pull request that makes the configuration unreadable is flagged

- **WHEN** the configuration turns the tool on before the merge, and a pull request replaces the configuration file with one that is not valid, is larger than its size bound, is a symbolic link or is not a regular file
- **THEN** its comment says that the pull request changed the tool's configuration

#### Scenario: A changed registration is flagged

- **WHEN** a pull request changes `.claude/settings.json`, or adds or changes `.claude/settings.local.json`
- **THEN** its comment says that the pull request changed a project settings file that can register the hook
