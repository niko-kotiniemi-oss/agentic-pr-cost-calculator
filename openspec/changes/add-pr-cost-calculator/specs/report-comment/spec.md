## Purpose

Give each merged pull request one short, readable comment saying what it cost, computed by trusted code that reads the pull request's files only as data.

## ADDED Requirements

### Requirement: A merged pull request gets one report comment

When a pull request merges with the tool on before its merge or after it, the report SHALL post one comment giving the total cost; the cost by model, by token type and by activity type; the CI minutes and their cost, and how many of those minutes ran on runners that the price table does not list; and the number of ledger entries it counted, and the number of entries and files it did not count, for each reason that this capability and `ledger` give.

#### Scenario: The comment states the totals

- **WHEN** a pull request with ledger files and CI runs merges
- **THEN** one comment is posted with the token cost, the CI cost and their total

#### Scenario: A pull request without ledger files says so

- **WHEN** a pull request that adds no ledger file merges
- **THEN** the comment gives the CI cost and says that no agent usage was recorded

### Requirement: The comment says what its figure is and where it comes from

The report's comment (see "A merged pull request gets one report comment") SHALL give the price table's date and the tool's version, and SHALL state that the figure is an API-equivalent estimate, not a bill, that it counts the usage that the pull request's commits carry and the CI runs on those commits, and that it does not count the model calls that Claude Code makes for its own tools without writing them to the session's transcript.

#### Scenario: The comment says what the figure is

- **WHEN** the report posts its comment
- **THEN** the comment says that the figure is an API-equivalent estimate and not a bill, that it counts the usage the pull request's commits carry and the CI runs on those commits, and that it does not count the model calls that Claude Code makes for its own tools without writing them to the transcript, and names the price table's date and the tool's version

### Requirement: The comment counts refused calls and calls that may leave the token cost low

The report's comment (see "A merged pull request gets one report comment") SHALL give the number of calls that capture refused; the number of calls that capture read without a stop reason, and, when there are any, that the token cost is a lower bound; and the number of calls whose usage held a field that capture does not know, and, when there are any, that the token cost may be low.

#### Scenario: Calls that capture refused are counted in the comment

- **WHEN** the ledger files that a pull request adds count calls that capture refused
- **THEN** the comment gives their number

#### Scenario: Calls read without a stop reason are counted in the comment

- **WHEN** the ledger files that a pull request adds count calls that capture read without a stop reason
- **THEN** the comment gives their number, and says that the token cost is a lower bound

#### Scenario: Calls with a usage field that capture does not know are counted in the comment

- **WHEN** the ledger files that a pull request adds count calls whose usage held a field that capture does not know
- **THEN** the comment gives their number, and says that the token cost may be low

#### Scenario: A restored or copied ledger file adds no counts or flags

- **WHEN** a pull request adds a ledger file that is counted as restored, or one that holds at least one entry, each of which the default branch already held before the merge
- **THEN** the comment counts none of that file's counts and none of its flags

#### Scenario: A mark on an entry that is not counted is not counted

- **WHEN** a pull request adds an entry, marked as read without a stop reason, for a call that the default branch already held before the merge
- **THEN** the comment's count of calls read without a stop reason leaves that entry out

### Requirement: The comment says when the ledger files flag calls left out

When a pull request's ledger files say that calls were left out, for consent, for their age or because their repository could not be told (see "A ledger file says when calls of its sessions were left out" in `usage-capture`), the report's comment SHALL say, for each reason, that its ledger files say so, with no count, and that the token cost, each of its parts and the total are then lower bounds.

#### Scenario: Calls left out for consent are flagged in the comment

- **WHEN** a ledger file that a pull request adds says that calls were left out for consent
- **THEN** the comment says that the pull request's ledger files say that capture could not show that some calls were made while it was on, says nothing of capture being off, gives no count of them, and says that the token cost, its parts and the total are lower bounds

#### Scenario: Calls whose repository could not be told are flagged in the comment

- **WHEN** a ledger file that a pull request adds says that calls whose repository could not be told were left out
- **THEN** the comment says that the pull request's ledger files say so, gives no count of them, and says that the token cost, its parts and the total are lower bounds

#### Scenario: Calls left out for their age are flagged in the comment

- **WHEN** a ledger file that a pull request adds says that calls were left out for their age
- **THEN** the comment says that the pull request's ledger files say that some calls waited too long for a commit to be recorded, gives no count of them, and says that the token cost, its parts and the total are lower bounds

#### Scenario: A comment with no flag still says what it does not count

- **WHEN** no ledger file that a pull request adds says that calls were left out
- **THEN** the comment still says that calls that no ledger file holds are neither counted nor flagged

### Requirement: A report run again updates only its own comment

When the report runs again, it SHALL update its earlier comment (see "A merged pull request gets one report comment"), and SHALL update only a comment that its own identity wrote.

#### Scenario: Running the report twice posts one comment

- **WHEN** the report runs again for a pull request that already has its comment
- **THEN** the existing comment is updated and no second one is posted

#### Scenario: A planted marker does not redirect the update

- **WHEN** a comment written by someone else carries the report's marker
- **THEN** that comment is left unchanged, and the report posts or updates its own

### Requirement: A hook file that does not come from the report's commit is named, not quoted

When the hook file at the path that the README gives is missing from the merged commit, or differs from the hook file at the tool's commit that the report runs, the comment SHALL say that the repository's hook does not come from the report's commit, and SHALL quote nothing from that file.

#### Scenario: A hook from another commit than the report's is named

- **WHEN** the hook file in the merged commit differs from the hook file at the tool's commit that the report runs, as when an update moved the workflow's pin and left the hook behind
- **THEN** the comment says that the repository's hook does not come from the report's commit, and quotes nothing from the file

### Requirement: The comment shows only what the report computed

The comment, the report's job summary and what the report writes to its log SHALL hold only numbers, the report's own fixed text, and model, attribute and runner names that the price table lists, shown as code in the comment and the job summary.

#### Scenario: A runner label with markup is not shown

- **WHEN** a job's runner labels, as the jobs API gives them, hold a link, an image, an @-mention or a workflow command
- **THEN** none of that text is in the comment, the job summary or the log

### Requirement: No text from the pull request or the jobs API is quoted

The comment, the report's job summary and what the report writes to its log SHALL NOT quote ledger lines, file names, branch names, job names, runner labels the price table does not list, or any other text from the pull request or from the jobs API, so that no such text is read as Markdown in the comment or the job summary, or as a workflow command, such as `::error::`, in the log.

#### Scenario: Refused ledger lines are counted, not shown

- **WHEN** some ledger lines that the pull request adds are not valid entries
- **THEN** the comment says how many were refused, and none of them is quoted in the comment, the job summary or the log

### Requirement: A ledger line naming a model or attribute value that the price table does not list, other than the value unknown, is refused

A ledger line that names a model or an attribute value that the price table does not list, other than `unknown`, SHALL be refused.

#### Scenario: A name with markup is not shown as written

- **WHEN** a ledger line names a model with a link, an image, an @-mention or a workflow command in it
- **THEN** the line is refused, and none of that text is in the comment, the job summary or the log

### Requirement: The report reads the ledger from git, within bounds

The report SHALL read ledger files only as blobs from git, never through the working tree. It SHALL refuse an added path (see "Only the ledger files that the merge adds are counted" in `ledger`) in the ledger folder that is not a regular file, such as a symbolic link or a submodule, and SHALL learn each blob's size before reading it. It SHALL fetch what it reads: the default branch's history up to the push's commit, and the pull request's head, as `refs/pull/<number>/head`.

#### Scenario: A ledger file that is a link is refused

- **WHEN** a pull request adds a symbolic link in the ledger folder
- **THEN** the report reads nothing through it, and the comment counts it as a refused file

#### Scenario: The report reads the ledger from git, not from a working tree

- **WHEN** the report runs where a working tree holds, at the path of a ledger file that the merge adds, a file whose contents differ from that file's blob
- **THEN** the report counts the blob's entries and none of that file's

#### Scenario: The report fetches what it reads

- **WHEN** the report starts in a clone that holds neither the pull request's head nor the default branch's history before the push's commit
- **THEN** it fetches the default branch's history up to the push's commit and `refs/pull/<number>/head`, and reads the ledger files from what it fetched

### Requirement: A pull request's ledger files larger in total than the size bound are refused

The report SHALL refuse a pull request's ledger files (see "Only the ledger files that the merge adds are counted" in `ledger`) when they are larger in total than the size bound that the ledger format documents, which capture applies to each ledger file it reads, and SHALL then still report the CI cost.

#### Scenario: Ledger files too large in total are refused

- **WHEN** the ledger files that a pull request adds exceed the size bound
- **THEN** the comment says the ledger files were too large to read, and gives the CI cost

### Requirement: Ledger files that the default branch already holds are read by capture's rules

The report SHALL read the ledger files that the default branch's first-parent history held before the merge by the rules that capture applies to those it reads: it SHALL skip a path in the ledger folder that is not a regular file and a file larger than the size bound (see "A pull request's ledger files larger in total than the size bound are refused"), and SHALL skip a line that does not match the ledger format, counting it neither as an entry nor as a refused line of the pull request.

#### Scenario: An oversized ledger file that the default branch holds does not stop the report

- **WHEN** the default branch's first-parent history held, before the merge, a ledger file larger than the size bound
- **THEN** the report reads nothing of that file, and posts its comment

#### Scenario: A submodule in the default branch's ledger folder does not stop the report

- **WHEN** the default branch's first-parent history held, before the merge, a submodule or a symbolic link in the ledger folder
- **THEN** the report reads nothing through it, and posts its comment

#### Scenario: An unreadable line in an earlier ledger file does not stop the report

- **WHEN** a ledger file that the default branch held before the merge holds a line that does not match the ledger format
- **THEN** the report skips that line, counts it neither as an entry nor as a refused line of the pull request, and posts its comment

#### Scenario: An earlier ledger file's valid lines keep their calls beside an unreadable one

- **WHEN** a ledger file that the default branch held before the merge holds a line that does not match the ledger format beside valid entries, and the pull request adds an entry for one of their calls
- **THEN** the report does not count that entry

### Requirement: Ledger files that the default branch already holds are read by the version they state

The report SHALL read each ledger file that the default branch's first-parent history held before the merge by the version that its first line states, and SHALL skip one whose first line states no version or a version that it does not read, counting none of it as the pull request's and giving in its job summary how many it skipped.

#### Scenario: An earlier ledger file is read by the version it states

- **WHEN** the default branch held, before the merge, a ledger file of an earlier version that the report reads, and the pull request adds an entry for a call that it holds
- **THEN** the report reads that file's call ids by its version's rules, and does not count that entry

#### Scenario: An earlier ledger file of a version the report does not read is skipped and counted in the job summary

- **WHEN** the default branch held, before the merge, a ledger file whose first line states a version that the report does not read
- **THEN** the report reads nothing of that file, counts none of it as the pull request's, says in its job summary how many such files it skipped, and posts its comment

### Requirement: The report runs only trusted code, with the least it needs

The report SHALL run only the tool's own code, from the commit at which the calling workflow pins the tool, and SHALL read the pull request's files only as data, never running, importing or installing anything from them. It SHALL use the workflow's own token, with no permissions beyond reading the repository and its Actions data and writing pull request comments, and SHALL never write the token to its output: its log, its job summary or its comment.

#### Scenario: No secret is configured

- **WHEN** the workflow runs in a repository that has added no secret for the tool
- **THEN** the report completes

#### Scenario: Nothing from the pull request is run

- **WHEN** a merged pull request adds a Python module, a script or a requirements file
- **THEN** the report neither runs, imports nor installs any of them

#### Scenario: The token never reaches the output

- **WHEN** the report runs, whether it succeeds or fails
- **THEN** none of its log, its job summary and its comment contains the token

### Requirement: The report runs only for the push that a merge makes to the default branch

The report SHALL run only for a push that a merge makes to the default branch, and SHALL refuse every other event, including when the workflow that calls it was triggered by something else. It SHALL tell such a push by its event being `push` and its `github.ref` being `refs/heads/` followed by the default branch's name, so that neither another event that runs on the default branch nor a push of a tag named like the default branch passes.

#### Scenario: A fork's pull request gets its report

- **WHEN** a pull request opened from a fork merges
- **THEN** its report comment is posted

#### Scenario: Another event is refused

- **WHEN** the report is run for a `pull_request`, `pull_request_target`, `workflow_dispatch`, `workflow_run` or `merge_group` event, or for a push to a branch other than the default branch
- **THEN** it posts nothing, and its job fails

#### Scenario: A tag named like the default branch is refused

- **WHEN** the report is run for a push of a tag whose name is the default branch's name, such as `refs/tags/main` when the default branch is `main`
- **THEN** it posts nothing, and its job fails

### Requirement: A push gets a comment only when all its commits belong to one pull request

The report SHALL comment only when every commit that the push adds to the default branch's first-parent history belongs to one pull request. A push that merges no pull request SHALL get no comment. A push that merges more than one pull request, as a merge queue can, or that adds commits of no pull request beside a merge, SHALL get no comment either, because the report cannot tell which ledger files and runs belong to which. In each of these cases, the report SHALL say so in its job summary.

#### Scenario: A push that merges no pull request gets no comment

- **WHEN** a commit is pushed straight to the default branch, without a pull request
- **THEN** no comment is posted, the job summary says that the push merged no pull request, and the job succeeds

#### Scenario: A push that merges several pull requests gets no comment

- **WHEN** one push to the default branch merges two pull requests
- **THEN** no comment is posted, and the job summary says that the push merged more than one pull request

#### Scenario: A push that adds other commits beside a merge gets no comment

- **WHEN** one push to the default branch adds a pull request's merge and a commit that belongs to no pull request
- **THEN** no comment is posted, and the job summary says that the push holds commits of no pull request

### Requirement: The report keeps to a call budget and a time limit

The report SHALL make no more calls to GitHub's API than the call budget that the README gives, and its job SHALL have a time limit. When the budget runs out before the report can tell which pull request the push merges, it SHALL post no comment, and SHALL say so in its job summary.

#### Scenario: A push with more commits than the call budget allows gets no comment

- **WHEN** a push to the default branch adds more commits to its first-parent history than the report's call budget lets it look up
- **THEN** no comment is posted, and the job summary says that the report could not tell which pull request the push merged

### Requirement: Each ledger line is held to the ledger format

The report SHALL read each line of the ledger files that the merge adds (see "Only the ledger files that the merge adds are counted" in `ledger`) against the ledger format, and SHALL refuse every line that does not match it, among them a line with a count that is not a whole number from zero up to the ceiling, or that is `true`, `false`, not-a-number or too large to hold, a field given twice or not named by the format, nesting deeper than the format allows, or a day that is not a date.

#### Scenario: A ledger count that is not a whole number within the ceiling is refused

- **WHEN** a ledger line that the pull request adds gives a count that is negative, a fraction, text, or one more than the ceiling
- **THEN** that line is refused, counted as refused, and not counted as an entry

#### Scenario: A ledger count given as `true` or `false` is refused

- **WHEN** a ledger line that the pull request adds gives a count as `true` or as `false`
- **THEN** that line is refused, counted as refused, and not counted as an entry

#### Scenario: A ledger count given as not-a-number is refused

- **WHEN** a ledger line that the pull request adds gives a count as `NaN`, which Python's JSON reader reads as not-a-number
- **THEN** that line is refused, counted as refused, and not counted as an entry

#### Scenario: A ledger count too large to hold is refused

- **WHEN** a ledger line that the pull request adds gives a count as `1e999`, which Python's JSON reader reads as infinity, or as a whole number thousands of digits long, which it refuses to read
- **THEN** that line is refused, counted as refused, and not counted as an entry, and the report goes on

#### Scenario: A ledger line that gives a field twice is refused

- **WHEN** a ledger line that the pull request adds gives one field twice, which Python's JSON reader would read as the last of the two values
- **THEN** that line is refused, counted as refused, and not counted as an entry

#### Scenario: A ledger line with a field that the format does not name is refused

- **WHEN** a ledger line that the pull request adds holds a field that the ledger format does not name
- **THEN** that line is refused, counted as refused, and not counted as an entry

#### Scenario: A ledger line nested too deeply is refused

- **WHEN** a ledger line that the pull request adds nests arrays or objects deeper than the format allows, including so deep that Python's JSON reader raises an error on it
- **THEN** that line is refused, counted as refused, and not counted as an entry, and the report goes on

#### Scenario: A ledger day that is not a date is refused

- **WHEN** a ledger line that the pull request adds gives a day that is not a date in the calendar, such as `2026-02-30`
- **THEN** that line is refused, counted as refused, and not counted as an entry

### Requirement: The report reads each ledger file by the version it states

The report SHALL read each ledger file that the merge adds by the rules of the version of the ledger format that its first line states (see "Each ledger file states its format's version, and each version is published with a schema" in `ledger`), and SHALL count as a refused file, using none of its entries, counts or flags, a ledger file whose first line states no version or a version that the report does not read, or breaks its version's rules.

#### Scenario: A ledger file of an earlier version is read by that version's rules

- **WHEN** a pull request adds a ledger file that an earlier release's capture step wrote in an earlier version of the ledger format
- **THEN** the report reads its lines by that version's rules

#### Scenario: A ledger file of a version the report does not read is refused

- **WHEN** a ledger file that the pull request adds states a version of the ledger format that the report does not read, or states none
- **THEN** none of its entries is counted, and the comment counts it as a refused file

#### Scenario: A ledger file whose first line breaks its version's rules is refused

- **WHEN** a ledger file that the pull request adds states, on its first line, a version that the report reads, but gives a flag twice, a count above the ceiling, a field that the version does not have, or a value of another kind than the version allows
- **THEN** none of its entries, counts or flags is used, and the comment counts it as a refused file

#### Scenario: A first line anywhere but first is refused

- **WHEN** a line shaped as a ledger file's first line comes after that file's first line
- **THEN** that line is counted as a refused line, and nothing that it states is used

#### Scenario: A version is matched exactly, and chooses no code by its value

- **WHEN** a ledger file's first line states its version as `true`, as `1.0`, as a string, as the name of a module or as a number thousands of digits long
- **THEN** the file is refused, and the report imports nothing and looks nothing up by that value

### Requirement: A refused ledger line is counted as refused, and no line stops the report

A refused ledger line SHALL NOT be counted as an entry, it SHALL be counted as refused, and no line, however it is malformed, SHALL stop the report.

#### Scenario: An unreadable ledger line is counted and the report completes

- **WHEN** a ledger file that the pull request adds holds, among valid lines, a line that is not JSON or is not valid UTF-8
- **THEN** that line is counted as refused, the valid lines are counted, and the comment is posted
