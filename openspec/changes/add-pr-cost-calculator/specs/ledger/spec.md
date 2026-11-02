## Purpose

Carry each pull request's usage in small files that hold counts and never content, are written once, travel with the agent's own commits, and stay in the repository as the pull request's record, from which the report counts each call at most once.

Scenarios below that run the capture step follow the conventions that `usage-capture` states for its own scenarios.

## ADDED Requirements

### Requirement: The ledger holds counts, never content

A ledger file SHALL contain no prompt text, response text, code, file contents, tool name, tool input or output, file path, working directory, branch name, user name, session identifier, transcript path, `tool_use_id` or time of day, nor a hash of any of them. The only text a ledger file takes from the transcript SHALL be the model's name and the values of the price attributes (see "Usage is recorded per model call" in `usage-capture`).

#### Scenario: Content in the transcript does not reach the ledger

- **WHEN** a transcript message carries text, a tool call with arguments and a session identifier
- **THEN** the entry recorded from it holds only the fields that "Usage is recorded per model call" in `usage-capture` names and its activity type (see `activity-types`)

#### Scenario: A planted string never reaches the ledger

- **WHEN** every text value in a transcript and in the hook's input, and the name of the branch checked out, is a distinct marker string, except the model names and price attribute values that the price table lists
- **THEN** no marker appears in any ledger file, whether in its contents or in its path, and neither does the SHA-256 hash of any marker but a message id

#### Scenario: The store's notes never reach the ledger

- **WHEN** the store notes, for a staged ledger file, its worktree's name and its transcript's path, and hashes of the session's id, the branch and the command's `tool_use_id`
- **THEN** none of those names, paths or hashes appears in any ledger file, whether in its contents or in its path

#### Scenario: A waiting call planted in the store carries nothing into the ledger

- **WHEN** the store holds a waiting call whose entry holds a field that capture does not write, or a value that it would not record, such as text in place of a count or a model name that the price table does not list
- **THEN** no ledger file that the step stages holds that entry, and the step drops it

### Requirement: Each ledger file states its format's version, and each version is published with a schema

Each ledger file SHALL state on its first line the version of the ledger format that it is written in, and the ledger format SHALL be published for every version that a release's capture step wrote, with a JSON Schema for each kind of its lines, so that anyone can check a ledger file without the tool. A ledger file SHALL hold nothing that the schema of its version does not allow.

#### Scenario: A ledger file names its format's version

- **WHEN** a run of the capture step writes a ledger file
- **THEN** its first line states the ledger format's version, and every line of the file validates against that version's published schema

#### Scenario: The published schema refuses what the report refuses

- **WHEN** each ledger line that a scenario of "Each ledger line is held to the ledger format" in `report-comment` refuses is checked against the published schema of its version, by a standard validator with its default options, and so is each line that the report counts as an entry
- **THEN** the schema refuses each line that the report refuses, apart from what the ledger format lists as beyond any schema, such as a field given twice, and accepts each line that the report counts

#### Scenario: A released version's schema does not change

- **WHEN** a change alters the published schema of a version of the ledger format that a release wrote
- **THEN** the checks fail, naming that version

### Requirement: Every version of the ledger format names a call by the same id

Every version of the ledger format SHALL name a call by the same id, the SHA-256 hash of its message id, so that capture stages, and the report counts, each call once, whichever versions its entries are written in.

#### Scenario: One call in two versions is counted once

- **WHEN** a pull request adds an entry, in one version of the ledger format, for a call that a ledger file of another version, which the default branch held before the merge, already holds
- **THEN** that entry is not counted

### Requirement: A model name or attribute value the price table does not list is recorded as unknown

A call's model name and each of its price attribute values (see "Usage is recorded per model call" in `usage-capture`) SHALL be recorded only when the price table that the capture step ships with lists that name or value, so that the name of a private gateway, a custom model or an alias is not published. Any other value SHALL be recorded as `unknown`.

#### Scenario: An unexpected model name is recorded as unknown

- **WHEN** a call's model name holds characters such as spaces, brackets or Markdown
- **THEN** its entry's model is `unknown`

#### Scenario: A model name the price table does not list is recorded as unknown

- **WHEN** a call's model name begins with `claude-` and is made only of lowercase letters, digits and hyphens, but the price table does not list it
- **THEN** its entry's model is `unknown`

#### Scenario: An attribute value the price table does not list is recorded as unknown

- **WHEN** a call's service tier, its speed or its inference region is a value that the price table does not list
- **THEN** that attribute is `unknown` in its entry, and the entry records each of the call's other attributes whose value the price table lists

### Requirement: A ledger file is written once

Each ledger file SHALL be a new regular file with a random name, in the ledger folder's subfolder for the UTC month in which it is written, and SHALL never be changed after it is written: a file that no commit took is removed whole, never edited. The capture step SHALL refuse to write when any folder on the ledger file's path below the repository root is a symbolic link, or when a file of that name already exists.

#### Scenario: A new file for every commit

- **WHEN** capture adds calls to a branch that already has ledger files
- **THEN** it writes a new file, and leaves every other ledger file unchanged

#### Scenario: A symbolic link in the ledger path is refused

- **WHEN** a folder on the ledger file's path below the repository root is a symbolic link
- **THEN** nothing is written through it

### Requirement: The capture step stages only the ledger file it wrote

The capture step SHALL stage only the ledger file it wrote.

#### Scenario: Other changes stay unstaged

- **WHEN** the working tree holds other changed files and untracked files
- **THEN** the ledger file is the only change the step has staged

### Requirement: A ledger file is noted before it is written

The capture step SHALL note a ledger file in its store before it writes it, so that a later run takes back a file that a run killed while writing it left behind, as the requirements from "A ledger file that no commit takes is taken back" to "A put-back is tried once, and in no other case" in `usage-capture` say for a file that no commit took.

#### Scenario: A ledger file that a killed run left is taken back

- **WHEN** a run of the step is killed while it writes a ledger file for a `git commit`, and the step's next run finds that command over while no other git command holds the index
- **THEN** that run takes the file back, from the index and the working tree, and the agent's next commit carries the calls that the file was written for

### Requirement: The ledger is the record

The pull request's ledger SHALL remain on the default branch after merge, as its record, and the report SHALL write nothing to the repository.

#### Scenario: The ledger stays after merge

- **WHEN** a pull request with a ledger merges
- **THEN** the default branch holds the ledger files that pull request added, and the report has made no commit

### Requirement: Only the ledger files that the merge adds are counted

The report SHALL count only the entries of ledger files that the merge adds: files in the ledger folder that the default branch holds after the merge and did not hold before it.

#### Scenario: A reused branch name is not double-counted

- **WHEN** a pull request's branch still holds the ledger files of an earlier pull request merged from the same branch name
- **THEN** the report counts only the ledger files this pull request adds

### Requirement: Each call is counted at most once

The report SHALL count each call at most once: an added entry for a call that a ledger file held at any commit of the default branch's first-parent history before the merge SHALL NOT be counted, added entries for one call SHALL be counted once when they are identical, and SHALL all be refused when they differ (see "Only the ledger files that the merge adds are counted").

#### Scenario: A copied entry is counted once

- **WHEN** a pull request adds an entry for a call that a ledger file on the default branch held before the merge
- **THEN** that entry is not counted

#### Scenario: One call added twice is counted once

- **WHEN** a pull request adds two identical entries for one call, in one ledger file or in two
- **THEN** that call is counted once

#### Scenario: Entries of one call that disagree are refused

- **WHEN** a pull request adds two entries for one call that differ
- **THEN** neither entry is counted, and both are counted as refused

#### Scenario: A ledger file that a revert brings back is not counted again

- **WHEN** a pull request's ledger file was counted when it merged, a later pull request reverted that merge, and a third pull request reverts that revert
- **THEN** the third pull request's report counts none of that file's entries

### Requirement: The comment says how many ledger files the pull request restores, removes or changes

An added ledger file (see "Only the ledger files that the merge adds are counted") at a path that a ledger file held at any commit of the default branch's first-parent history before the merge SHALL be counted as restored. The comment SHALL say how many ledger files it counted as restored, and how many ledger files that the default branch held before the merge the pull request removed or changed, and SHALL count none of their entries.

#### Scenario: Removed or changed ledger files are flagged

- **WHEN** a pull request removes, changes or renames a ledger file that the default branch held before the merge
- **THEN** the comment says how many such files it removed or changed, and counts none of their entries

#### Scenario: A ledger file that a revert brings back is counted as restored

- **WHEN** a pull request's ledger file was counted when it merged, a later pull request reverted that merge, and a third pull request reverts that revert
- **THEN** the third pull request's comment says that it restored one ledger file

### Requirement: The job summary says how many ledger files a push without a comment removes or changes

When a push that gets no comment, with the tool on before or after it, removes or changes ledger files that the default branch held before it, the report's job summary SHALL say how many.

#### Scenario: A removal in a push without a comment is flagged in the job summary

- **WHEN** a push to the default branch that merges no pull request, or more than one, removes or changes ledger files that the default branch held before it, with the tool on
- **THEN** no comment is posted, and the job summary says how many ledger files the push removed or changed
