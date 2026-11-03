## Purpose

Give each merged pull request one short, readable comment saying what it cost, computed by trusted code that reads the pull request's files only as data.

## ADDED Requirements

### Requirement: A merged pull request gets one report comment

When a pull request merges with the tool on, the report SHALL post one comment giving the total cost; the cost by model, by token type and by activity type; the CI minutes and their cost, and how many of those minutes ran on runners that the price table does not list; and the number of ledger entries it counted, and the number of entries and files it did not count, for each reason that this capability and `ledger` give.

#### Scenario: The comment states the totals

- **WHEN** a pull request with a ledger and CI runs merges
- **THEN** one comment is posted with the token cost, the CI cost and their total

#### Scenario: A pull request without a ledger says so

- **WHEN** a pull request merges with no ledger on its branch
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

### Requirement: A report run again updates only its own comment

When the report runs again, it SHALL update its earlier comment (see "A merged pull request gets one report comment"), and SHALL update only a comment that its own identity wrote.

#### Scenario: Running the report twice posts one comment

- **WHEN** the report runs again for a pull request that already has its comment
- **THEN** the existing comment is updated and no second one is posted

#### Scenario: A planted marker does not redirect the update

- **WHEN** a comment written by someone else carries the report's marker
- **THEN** that comment is left unchanged, and the report posts or updates its own

### Requirement: A hook that does not come from the report's commit is named, not quoted

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

#### Scenario: A ledger that is a link is refused

- **WHEN** a pull request adds a symbolic link in the ledger folder
- **THEN** the report reads nothing through it, and the comment counts it as a refused file

#### Scenario: The report reads the ledger from git, not from a working tree

- **WHEN** the report runs where a working tree holds, at the path of a ledger file that the merge adds, a file whose contents differ from that file's blob
- **THEN** the report counts the blob's entries and none of that file's

#### Scenario: The report fetches what it reads

- **WHEN** the report starts in a clone that holds neither the pull request's head nor the default branch's history before the push's commit
- **THEN** it fetches the default branch's history up to the push's commit and `refs/pull/<number>/head`, and reads the ledger files from what it fetched

### Requirement: A ledger change larger than the size bound is refused

The report SHALL refuse the ledger change when the added ledger files (see "Only the ledger files that the merge adds are counted" in `ledger`) are larger in total than the size bound that the ledger format documents, which capture applies to each ledger file it reads, and SHALL then still report the CI cost.

#### Scenario: An oversized ledger is refused

- **WHEN** the ledger files that a pull request adds exceed the size bound
- **THEN** the comment says the ledger was too large to read, and gives the CI cost

### Requirement: Ledger files that the default branch already holds are read by capture's rules

The report SHALL read the ledger files that the default branch's first-parent history held before the merge by the rules that capture applies to the ledger files it reads: it SHALL skip a path in the ledger folder that is not a regular file and a file larger than the size bound (see "A ledger change larger than the size bound is refused"), and SHALL skip a line that does not match the ledger format, counting it neither as an entry nor as a refused line of the pull request.

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
- **THEN** that line is refused, counted as refused, and its entry is not counted

#### Scenario: A ledger count given as `true` or `false` is refused

- **WHEN** a ledger line that the pull request adds gives a count as `true` or as `false`
- **THEN** that line is refused, counted as refused, and its entry is not counted

#### Scenario: A ledger count given as not-a-number is refused

- **WHEN** a ledger line that the pull request adds gives a count as `NaN`, which Python's JSON reader reads as not-a-number
- **THEN** that line is refused, counted as refused, and its entry is not counted

#### Scenario: A ledger count too large to hold is refused

- **WHEN** a ledger line that the pull request adds gives a count as `1e999`, which Python's JSON reader reads as infinity, or as a whole number thousands of digits long, which it refuses to read
- **THEN** that line is refused, counted as refused, and its entry is not counted, and the report goes on

#### Scenario: A ledger line that gives a field twice is refused

- **WHEN** a ledger line that the pull request adds gives one field twice, which Python's JSON reader would read as the last of the two values
- **THEN** that line is refused, counted as refused, and its entry is not counted

#### Scenario: A ledger line with a field that the format does not name is refused

- **WHEN** a ledger line that the pull request adds holds a field that the ledger format does not name
- **THEN** that line is refused, counted as refused, and its entry is not counted

#### Scenario: A ledger line nested too deeply is refused

- **WHEN** a ledger line that the pull request adds nests arrays or objects deeper than the format allows, including so deep that Python's JSON reader raises an error on it
- **THEN** that line is refused, counted as refused, and its entry is not counted, and the report goes on

#### Scenario: A ledger day that is not a date is refused

- **WHEN** a ledger line that the pull request adds gives a day that is not a date in the calendar, such as `2026-02-30`
- **THEN** that line is refused, counted as refused, and its entry is not counted

### Requirement: A refused ledger line is counted as refused, and no line stops the report

A refused ledger line's entry SHALL NOT be counted, the line SHALL be counted as refused, and no line, however it is malformed, SHALL stop the report.

#### Scenario: An unreadable ledger line is counted and the report completes

- **WHEN** a ledger file that the pull request adds holds, among valid lines, a line that is not JSON or is not valid UTF-8
- **THEN** that line is counted as refused, the valid lines are counted, and the comment is posted
