## Purpose

Let a repository turn the tool on or off with one file, and let each person decide for themselves whether their own sessions are recorded, so that no one's usage is published without their consent and a pull request cannot turn off its own report.

Scenarios below that run the capture step follow the conventions that `usage-capture` states for its own scenarios.

## ADDED Requirements

### Requirement: Capture runs only where the tool is on and the person has opted in

The capture step SHALL record nothing unless the repository's configuration turns the tool on and the person running the session has turned capture on for themselves, in their global git configuration, which is not part of the repository.

#### Scenario: No configuration file means no capture

- **WHEN** the capture step runs in a repository without the configuration file
- **THEN** nothing is recorded, and no ledger file is created

#### Scenario: A person who has not opted in is not recorded

- **WHEN** the repository turns the tool on, but the person running the session has not turned capture on
- **THEN** nothing is recorded, and no ledger file is created

#### Scenario: A repository's own git configuration cannot opt a person in

- **WHEN** only the repository's own git configuration turns capture on
- **THEN** nothing is recorded

### Requirement: Capture reads the configuration file only as a regular file within its bound

The capture step SHALL read the repository's configuration file in the working tree only when it is a regular file no larger than the size bound that the configuration's format documents, and SHALL otherwise take the tool to be off.

#### Scenario: A configuration file that is not a regular file turns capture off

- **WHEN** the repository's configuration file in the working tree is a symbolic link, a named pipe or a folder, or is larger than its size bound
- **THEN** nothing is recorded, and the run ends without waiting on the file

### Requirement: The person's setting is read only from their global configuration files

The capture step SHALL read the person's setting (see "Capture runs only where the tool is on and the person has opted in") only from their global configuration files themselves, `~/.gitconfig` and git's configuration file in their XDG configuration folder (see "Only an absolute home folder is read" and "Only an absolute XDG folder is read"), not from files they include, ignoring any environment variable that points git at other configuration files or adds settings.

#### Scenario: The environment cannot opt a person in

- **WHEN** the session's environment points git's global configuration at a file that turns capture on, or adds that setting through `GIT_CONFIG_COUNT` or `GIT_CONFIG_PARAMETERS`, and the person's own global configuration does not turn it on
- **THEN** nothing is recorded

#### Scenario: A setting in an included file does not opt a person in

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

Where both of the person's global configuration files (see "The person's setting is read only from their global configuration files") set the person's setting, `~/.gitconfig`, which git reads after the other, SHALL decide.

#### Scenario: The home configuration file decides when both set it

- **WHEN** git's configuration file in the person's XDG configuration folder turns capture on, and their `~/.gitconfig` turns it off
- **THEN** nothing is recorded

### Requirement: The setting is read by git's rules

The capture step SHALL read the person's setting (see "Capture runs only where the tool is on and the person has opted in") by git's rules for its configuration files: section and key names match in any case, a value is read without its quotes or a comment that follows it, the last value in a file decides, and a key in a subsection, such as `[pr-cost "x"]`, or in a comment is not the setting.

#### Scenario: The last value in a file decides

- **WHEN** the person's `~/.gitconfig` sets `pr-cost.capture` to `false` and then, further down the same file, to `true`
- **THEN** the session's calls are recorded, and with the two values the other way round, nothing is recorded

#### Scenario: The setting's names in any case, and its value in quotes, opt a person in

- **WHEN** the person's `~/.gitconfig` turns capture on only with `Capture = true` in a section written `[PR-Cost]`, or only with the value `"true"`
- **THEN** the session's calls are recorded

#### Scenario: A subsection or a comment does not opt a person in

- **WHEN** the person's `~/.gitconfig` sets capture to `true` only in a subsection, such as `[pr-cost "x"]`, or only in a comment
- **THEN** nothing is recorded

### Requirement: Only some of git's true values turn capture on

Of the values of the person's setting (see "The setting is read by git's rules"), only `true`, `yes`, `on` and `1`, in any case, and the key alone with no value SHALL turn capture on, and any other value SHALL leave it off, even one that git reads as true, such as `2`.

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

### Requirement: Consent holds for each recorded call

Consent, the two switches that "Capture runs only where the tool is on and the person has opted in" requires, SHALL hold for each call that the capture step records, not only for the run that records it. The step SHALL record a session's calls only when they were made inside one of that session's intervals when both were on (see "An interval when both switches were on begins at the session's start or at a run, and ends at a run").

#### Scenario: Calls made before a person opts in are not recorded

- **WHEN** the repository turns the tool on, a session makes calls while the person has not turned capture on, a run of the step then comes, and the person then turns capture on
- **THEN** none of the calls made before that run is recorded, and the calls that the session makes after a later run finds capture on are recorded

### Requirement: Each run notes in the store whether it found both switches on

The capture step SHALL note in its store, for each session, when a run finds both switches on and when a run finds either off (see "Capture runs only where the tool is on and the person has opted in"), creating the store where there is none. It SHALL read each run's time from the system's clock in UTC, which no environment variable sets.

#### Scenario: A run that finds a switch off creates the store to note it

- **WHEN** a run of the step finds that the person has not turned capture on, and no store exists yet
- **THEN** the run creates the store, and notes in it, for the run's session, when the run found a switch off

#### Scenario: The environment cannot move a run's time

- **WHEN** the session's environment sets `TZ` to a zone far from UTC, a run of the step has found both switches on, the person then turns capture off, the session makes calls, a run of the step comes, and the person then turns capture on again
- **THEN** none of the calls that the session made while capture was off is recorded

### Requirement: An interval when both switches were on begins at the session's start or at a run, and ends at a run

A session's interval when both switches were on (see "Consent holds for each recorded call") SHALL begin at the session's start when the session's first run finds both on, and otherwise at a run that finds both on after one that found either off, and SHALL end at the last run that finds both on before the next run that finds either off.

#### Scenario: Calls made while capture was off are not recorded when it is on again

- **WHEN** a run of the step has found both switches on, the person then turns capture off, the session makes calls, a run of the step comes, and the person then turns capture on again
- **THEN** none of the calls that the session made after the last run that found capture on, and before the next run that found it on again, is recorded

### Requirement: An opt-out ends every session's interval and withholds earlier calls

A run of the capture step that finds the person's own capture off, in their global configuration or in the repository's own, SHALL end, for every session that the store notes, the interval when both switches were on (see "An interval when both switches were on begins at the session's start or at a run, and ends at a run"), and the step SHALL never stage, after that run, a call made before it.

#### Scenario: Calls recorded before an opt-out are not staged

- **WHEN** calls were recorded and are waiting to be staged, the person then turns capture off, a run of the step comes, and the person turns capture on again before the agent's next commit
- **THEN** that commit carries none of those calls

#### Scenario: The calls of a file taken back after an opt-out are not staged again

- **WHEN** the step has staged a ledger file for a `git commit` that is then refused at a permission prompt, the person then turns capture off, and the step's next run finds that command over while no other git command holds the index
- **THEN** no later commit carries its calls

### Requirement: Ledger files are taken back and put back whatever the switches say

Whatever the switches (see "Capture runs only where the tool is on and the person has opted in") say, every run of the capture step that the floors in `releases-and-compatibility` let go on SHALL take back and put back ledger files, and note as taken the calls of a file that a commit holds, as the requirements from "A ledger file that no commit takes is taken back" to "A put-back is tried once, and in no other case" in `usage-capture` say.

#### Scenario: A file staged before capture is turned off is still taken back

- **WHEN** the step has staged a ledger file for a `git commit` that is then refused at a permission prompt, the person then turns capture off, and the step's next run finds that command over while no other git command holds the index
- **THEN** that run takes the file back, from the index and the working tree

### Requirement: One file turns the tool on or off, and a pull request cannot turn off its own report

A repository SHALL turn the calculator on by adding its configuration file with the tool enabled, and off by removing the file or disabling the tool in it. The report SHALL read the configuration from the default branch as it was before the merge and as it is after, only as a blob at each of those two commits and within the size bound that the configuration's format documents, and SHALL run when either turns the tool on.

#### Scenario: Disabled means silent

- **WHEN** a pull request merges, and the configuration disables the tool both before and after the merge
- **THEN** no comment is posted

#### Scenario: A pull request cannot turn off its own report

- **WHEN** a pull request that disables the tool merges
- **THEN** its report comment is posted

#### Scenario: The pull request that turns the tool on gets its report

- **WHEN** the pull request that adds the configuration file, with the tool enabled, merges
- **THEN** its report comment is posted

### Requirement: Capture reads the configuration in the working tree

Capture SHALL read the repository's configuration file (see "One file turns the tool on or off, and a pull request cannot turn off its own report") in the working tree.

#### Scenario: Capture follows the configuration in the working tree

- **WHEN** the configuration file in the working tree turns the tool off, and the commit checked out there holds one that turns it on
- **THEN** capture records nothing

### Requirement: A missing or unreadable configuration file neither turns the tool on nor stops the report

A configuration file that is missing at a commit, is not a regular file there, is larger than the size bound that the configuration's format documents or is not valid SHALL NOT turn the tool on at that commit, and SHALL NOT stop the report.

#### Scenario: A pull request that makes the configuration unreadable still gets its report

- **WHEN** the configuration turns the tool on before the merge, and a pull request replaces the configuration file with one that is not valid, is larger than its size bound, is a symbolic link or is not a regular file
- **THEN** its report comment is posted

### Requirement: A change to the configuration, the hook or a workflow is flagged

When a pull request changes the configuration file, the hook file at the path that the README gives, or any workflow file, its comment SHALL say so.

#### Scenario: A changed report is flagged

- **WHEN** a pull request changes the configuration file, the hook file, the workflow file that runs the report, or another workflow file
- **THEN** its comment says that the pull request changed the tool's configuration, its hook or a workflow

#### Scenario: A pull request that makes the configuration unreadable is flagged

- **WHEN** the configuration turns the tool on before the merge, and a pull request replaces the configuration file with one that is not valid, is larger than its size bound, is a symbolic link or is not a regular file
- **THEN** its comment says that the pull request changed the tool's configuration
