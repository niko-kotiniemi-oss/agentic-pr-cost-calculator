## Purpose

Hold the whole tool to the standards that make it safe to adopt: documentation that names everything it does and says how each feature is validated, connections only where that documentation says, rated threats, pull request text without private references, action pins that their repositories tagged, a record of each decision, kept so that each can be reversed on its own, the assumptions that the design rests on, a glossary of the words its documents use, and a golden set of figures that every version reproduces.

## ADDED Requirements

### Requirement: The documentation names everything the tool does

The repository SHALL keep a register of every requirement, with its kind, one page for each feature, and one page that explains the tool as a whole. That page SHALL name every credential and permission the tool uses, as a table per workflow and per job, every connection it makes to the outside world, with where to, by which protocol and why, and every flow, each drawn as a diagram. Tests SHALL fail when a flow has no diagram.

#### Scenario: A flow without a diagram fails CI

- **WHEN** a flow has no diagram
- **THEN** a test fails

### Requirement: The register matches the specs, and every requirement is on a feature page

Tests SHALL fail when the register (see "The documentation names everything the tool does") misses a requirement in the specs or names one they do not hold, and when a requirement belongs to no feature page.

#### Scenario: A requirement missing from the register fails CI

- **WHEN** a spec gains a requirement that the register does not list
- **THEN** a test fails and names the requirement

#### Scenario: A requirement without a feature fails CI

- **WHEN** a requirement belongs to no feature page
- **THEN** a test fails and names the requirement

### Requirement: Workflows are checked against the documented permissions, actions and images

Tests SHALL fail when a workflow, whether its file ends in `.yml` or `.yaml`, grants a permission in any job that the table of the page that explains the tool as a whole (see "The documentation names everything the tool does") does not give for that job, or the table gives one that the job is not granted, and when a workflow runs an action or a container or service image that the page does not name.

#### Scenario: An undocumented permission or action fails CI

- **WHEN** a job of any workflow is granted a permission that the page's table does not give for that job, or the table gives a job a permission it is not granted, or a workflow runs an action or an image that the page does not name
- **THEN** a test fails and names the workflow, the job and the permission, or the action or image

### Requirement: The tool connects only where its documentation says

The hook SHALL open no network connection. The report SHALL connect only to GitHub, over HTTPS, with the workflow's own `GITHUB_TOKEN`: to its REST API, at the address that the workflow's `GITHUB_API_URL` gives, and by git to the tool's own repository and the repository it reports on. Prices SHALL be read from the price table in the repository and never fetched.

#### Scenario: The hook opens no connection

- **WHEN** the hook runs, in any of its events
- **THEN** it opens no network connection

#### Scenario: The report connects only to GitHub

- **WHEN** the report runs
- **THEN** every connection it opens goes over HTTPS, to the host in `GITHUB_API_URL` or, by git, to the tool's own repository or the repository it reports on, and a connection anywhere else fails the test

#### Scenario: Prices are never fetched

- **WHEN** the report prices a pull request
- **THEN** it reads the price table from the tool's own commit and opens no connection for prices

### Requirement: Every threat is rated for impact and likelihood

Every threat in the threat model SHALL carry an impact and a likelihood, each from 1 to 3 with the level's name, and a risk that is their product, and the risk matrix SHALL place each threat in the one cell its ratings name. The threat model SHALL be revisited by a review independent of the design's author before a change's design is approved, and by a review of what was built before its pull request merges.

#### Scenario: A threat without both ratings fails CI

- **WHEN** a threat lacks an impact or a likelihood, or carries a risk that is not their product
- **THEN** a test fails and names the threat

#### Scenario: A threat outside its matrix cell fails CI

- **WHEN** the risk matrix leaves a threat out, places it twice or in another cell than its ratings name, or names a threat that does not exist
- **THEN** a test fails and names the threat

### Requirement: Pull request text carries no private reference

CI SHALL check a pull request's title and body against the same private patterns and name hashes that the repository's tracked files are checked against, and SHALL fail when either matches, naming the pattern and quoting none of the text. The check SHALL run when a pull request is opened, edited, reopened or updated, read the text from the event, and keep its patterns in one module that the repository's tests share.

#### Scenario: A pull request body with a private reference fails CI

- **WHEN** a pull request's title or body holds a text that one of the private patterns or name hashes matches
- **THEN** the check fails, names the pattern, and quotes none of the text

#### Scenario: An edited body is checked again

- **WHEN** a pull request's body is edited to add such a text
- **THEN** the check runs again and fails

### Requirement: Every pinned action is a commit its repository tagged

Every action and container image that a workflow uses SHALL be pinned to a full commit or a digest that a tag of its source names, and CI SHALL fail when one is pinned to anything else, such as a commit that only a fork holds.

#### Scenario: An action pinned to an untagged commit fails CI

- **WHEN** a workflow pins an action to a commit that no tag of its repository names
- **THEN** CI fails and names the action and the pin

### Requirement: Each feature's page matches its spec

Each spec SHALL have one page in `docs/features/`, named for it, listed in the folder's index, that names every requirement it holds and no other and says how the feature is validated. Tests SHALL fail on a spec without a page, a page named for another spec or for one the register does not hold, a page that leaves out a requirement of its spec or names another, a page with a missing or empty section on validation, and an index that leaves out a page or links one that does not exist.

#### Scenario: A page out of step with its spec fails CI

- **WHEN** a feature page leaves out a requirement that its spec holds, or names one that another spec holds or that the register does not hold
- **THEN** a test fails and names the requirement

#### Scenario: A spec without its own page fails CI

- **WHEN** a spec has no feature page, its page is not named for it, or a page names a spec that the register does not hold
- **THEN** a test fails and names the spec

#### Scenario: A page that does not say how its feature is validated fails CI

- **WHEN** a feature page has no section saying how the feature is validated, or an empty one
- **THEN** a test fails and names the page

#### Scenario: A page missing from the index fails CI

- **WHEN** the feature index does not link a page, or links a page that does not exist
- **THEN** a test fails and names the page

### Requirement: Each proposal says how its outcome is validated

A change's proposal SHALL list every capability that the change's specs hold, and SHALL say how each is validated, in a row of its own in a section on how the outcome is validated. Tests SHALL fail when a proposal leaves out a capability that its change's specs hold, lists one that they do not hold, or gives one no row, or an empty one, in that section.

#### Scenario: A proposal out of step with its specs fails CI

- **WHEN** a change's proposal leaves out a capability that the change's specs hold, or lists one that they do not hold
- **THEN** a test fails and names the capability

#### Scenario: A capability without its validation fails CI

- **WHEN** a change's proposal gives one of its capabilities no row, or an empty one, in its section on how the outcome is validated
- **THEN** a test fails and names the capability

### Requirement: Each decision has a record of its own, in a fixed form

Each decision about what the tool is, how it works or how it is built SHALL have a record of its own in `docs/decisions/`, holding one choice and named for its number, and the records SHALL be numbered from DR-001 without a gap or a repeat. A record SHALL give its type, status, decider, requirements, threats, the records it replaces and the one that closed it, then its context, decision, alternatives, consequences, scope and what reversing it would change, each once, in that order, none empty.

#### Scenario: A record out of form fails CI

- **WHEN** a record is named or headed outside its form, lacks a field or a section, has one twice or out of order, leaves a section empty, or gives a field a value outside its form
- **THEN** a test fails and names the record

#### Scenario: A gap or a repeat in the record numbers fails CI

- **WHEN** two records share a number, or a number between DR-001 and the highest has no record
- **THEN** a test fails and names the number

#### Scenario: A record numbered in other digits fails CI

- **WHEN** a record's file name writes its number in digits other than ASCII, or with a leading zero that padding to three does not need
- **THEN** a test fails and names the file

### Requirement: The index lists every record as the record has it

`docs/decisions/README.md` SHALL list every record once, in the order of their numbers, linking each and giving its title, type, status, decider, requirements and threats as the record gives them, and SHALL list nothing else, every line of its table, which runs to its first blank line, being a row in that form and no later line holding `|`.

#### Scenario: An index out of step with the records fails CI

- **WHEN** the index leaves a record out, lists one twice or out of order, lists one that does not exist, links a record to another file, gives a value that the record does not, holds a line in its table that is not a row in its form, or holds `|` on a line after its table
- **THEN** a test fails and names the record

### Requirement: A decision record names only what exists

Each requirement and threat that a record names SHALL be held or retired, each record, change and task that it names SHALL exist, and each date that it gives SHALL be a real one, no later than the day the tests run. A closed record SHALL name the record that closed it, which SHALL name it among those it replaces, no record SHALL name itself, and an accepted record SHALL NOT rest only on retired requirements.

#### Scenario: A record that names nothing fails CI

- **WHEN** a record names a requirement or a threat that is neither held nor retired, a record, a change or a task that does not exist, or a date that is not one or is later than the day the test runs
- **THEN** a test fails and names what it named

#### Scenario: A closed record and its closer that do not name each other fail CI

- **WHEN** a closed record names no record that closed it, an accepted one names one, a record names itself, or a record and the one that it names as its closer, or as one it replaces, do not name each other
- **THEN** a test fails and names the records

#### Scenario: An accepted record that rests only on retired requirements fails CI

- **WHEN** every requirement that an accepted record cites is retired
- **THEN** a test fails and names the record

### Requirement: No document follows a closed record

Every record and design decision that a tracked file outside `vendor/` and `tests/` names, and every requirement, threat, change and task that a Markdown file there names, SHALL exist, a requirement or a threat as held or retired. A parenthesis right after a record's ID SHALL give that record's title, and only the records, their index, the changelog and archived changes SHALL name a closed record, since a closed record no longer holds anything.

#### Scenario: A mention of nothing fails CI

- **WHEN** a tracked file names a record or a design decision that does not exist, or a Markdown file names a requirement or a threat that is neither held nor retired, or a change or a task that does not exist
- **THEN** a test fails and names the file and what it named

#### Scenario: A pattern in a data file is not read as a mention

- **WHEN** a tracked file other than Markdown holds text in the form of a requirement's or a threat's ID, a change or a task, as a lock file's hashes can
- **THEN** the test does not resolve it

#### Scenario: A record named by another title fails CI

- **WHEN** a tracked file follows a record's ID with a parenthesis that does not give that record's title
- **THEN** a test fails and names the file, the record and its title

#### Scenario: A mention of a closed record fails CI

- **WHEN** a tracked file other than a record, the index, the changelog or an archived change names a closed record
- **THEN** a test fails and names the file and the record

### Requirement: A decision record holds plain text

A record and the index SHALL hold only printable ASCII characters and line breaks, with no `&`, backslash or `@`, no fenced block, no web address, no link reference definition, no `<` or `][` outside inline code and no link but from a record's ID to that record's file, and a record SHALL hold no `|` outside inline code and no line but its headings that starts with `#`, so that a reviewer reads what an agent reads.

#### Scenario: A record that hides text or links elsewhere fails CI

- **WHEN** a record or the index holds a character other than printable ASCII or a line break, `&`, a backslash, `@`, a fenced block, a web address, a link reference definition, `<` or `][` outside inline code, or a link but from a record's ID to that record's file, or a record holds `|` outside inline code or a line other than its headings that starts with `#`
- **THEN** a test fails and names the file

### Requirement: An accepted record changes only to be closed

Tests SHALL fail when a commit removes, renames or moves a record that the base commit holds, or changes it except to close it, by its status from accepted to closed and its closer named, after which any line of text under its sections may become `[removed]`. They SHALL compare git trees with where HEAD left the default branch and with any base commit that CI names, and SHALL fail when either cannot be found, or holds the records' folder with no record in it.

#### Scenario: A record removed, renamed or changed fails CI

- **WHEN** a commit removes, renames or moves a record that the base holds, puts a link or another mode in its place, or changes anything in it but what closing it allows
- **THEN** a test fails and names the record

#### Scenario: A record closed, or cleared once closed, passes

- **WHEN** a commit changes a record's status from accepted to closed and names its closer, or replaces lines of text under a closed record's sections with `[removed]`
- **THEN** the test passes

#### Scenario: A base that cannot be found fails CI

- **WHEN** the base commit that CI names is not a full commit ID or is not in the clone, or no merge base with the default branch can be found
- **THEN** a test fails, says which, and gives the command that fetches what is missing

#### Scenario: A base whose records' folder holds no record fails CI

- **WHEN** a base commit holds `docs/decisions/` and no file in it that the tests read as a record
- **THEN** a test fails and names the base

#### Scenario: A tag never stands in for the default branch

- **WHEN** a tag carries the default branch's name
- **THEN** the test compares with the remote-tracking branch, or fails when the clone lacks it

#### Scenario: A pull request is compared with the default branch as well

- **WHEN** CI names a pull request's base commit
- **THEN** the test compares with it and with where HEAD left the default branch, and fails on a change to a record that either holds

#### Scenario: CI names the base for each event

- **WHEN** CI runs the tests for a pull request, for a change of its base, or for a push to the default branch
- **THEN** it clones the whole history and names the pull request's base commit, or the commit that the push replaced

### Requirement: IDs that the default branch holds stay held or retired

Tests SHALL fail when a requirement, threat or assumption ID that the base commit's register, threat model or assumptions' index holds or retires is neither held nor retired at HEAD, so that no record or threat comes to cite another requirement, threat or assumption.

#### Scenario: An ID that vanishes fails CI

- **WHEN** a commit drops a requirement, a threat or an assumption, or a retired ID, that the base holds, without retiring it
- **THEN** a test fails and names the ID

### Requirement: A record and the threats it lists name each other

Each threat that an accepted record lists SHALL name that record among what holds its answer, so that the change that closes the record meets the threat, and when a threat names a record that the base commit does not hold among what holds its answer, that record SHALL list the threat among its threats, so that whoever wrote the record agreed that it holds the answer.

#### Scenario: A threat that leaves out a record listing it fails CI

- **WHEN** an accepted record lists a threat whose Held by line does not name it
- **THEN** a test fails and names the record and the threat

#### Scenario: A new record that leaves out a threat citing it fails CI

- **WHEN** a threat's answer is held by a record that the base does not hold, and the record does not list the threat
- **THEN** a test fails and names the threat and the record

#### Scenario: A threat's field that runs onto another line fails CI

- **WHEN** a line of a threat is not one of its fields, as when its Held by line runs onto a second line
- **THEN** a test fails and names the threat

### Requirement: A removed threat's ID is retired, never used again

The threat model SHALL number its threats from T1 in order, and a threat that a change removes SHALL keep its number out of use in the threat model's list of retired IDs, naming that change.

#### Scenario: A gap or a reused ID in the threats fails CI

- **WHEN** the threats skip a number that no retired ID explains, a retired ID is still a threat's, or a retired ID names no change or one that does not exist
- **THEN** a test fails

### Requirement: The records' folder holds only the records and their index

`docs/decisions/` SHALL hold only the records and their index, each a file and not a link, with no folder in it, and no file elsewhere SHALL be named as a record, so that every record is one that the checks read.

#### Scenario: A file out of place fails CI

- **WHEN** `docs/decisions/` holds a folder, a link, or a file that is neither a record nor the index, or a file elsewhere is named as a record
- **THEN** a test fails and names the file

### Requirement: No attribute hides a record's diff

No attribute that the repository sets SHALL make git show a record's or the index's diff as binary, or GitHub hide it as generated, so that whoever merges a pull request reads each change that it makes to a record.

#### Scenario: An attribute that hides a record's diff fails CI

- **WHEN** the repository's attributes give a record or the index `binary`, `diff` or `linguist-generated`, in any state
- **THEN** a test fails and names the file and the attribute

#### Scenario: A person's own attributes are not read

- **WHEN** a person's global attributes file gives the records such an attribute
- **THEN** the test does not read it

### Requirement: The assumptions the design rests on are written down

The repository SHALL keep the assumptions that the specs, design, threat model and records rest on, each with what rests on it, by requirement, threat or record, and what changes if it is wrong, and each of its facts with where it is relied on and how it is checked: by a test, an observation, documentation, or not yet, with the task that will check it or why none will. A threat that rests on an assumption SHALL name it, and the assumption SHALL name the threat. Tests SHALL fail otherwise.

#### Scenario: An assumption without its check fails CI

- **WHEN** an assumption names nothing that rests on it or does not say what changes if it is wrong, or one of its facts does not say where it is relied on or how it is checked, or names a task that is done as the one that will check it
- **THEN** a test fails and names the assumption

#### Scenario: A citation of nothing fails CI

- **WHEN** an assumption or one of its facts names a requirement, a threat, a record or a task that does not exist, or a test that is not collected or that a mark skips or expects to fail
- **THEN** a test fails and names the assumption and what it names

#### Scenario: An assumption that names what does not rest on it fails CI

- **WHEN** an assumption names a requirement, a threat or a record, in what changes if it is wrong or in a fact, that it does not name as resting on it, or names as resting on it one that none of its facts is relied on by
- **THEN** a test fails and names the assumption and what it names

#### Scenario: A subject without its page fails CI

- **WHEN** a subject that the design gives a page of its own, such as Claude Code or GitHub, has no page under `docs/assumptions/`
- **THEN** a test fails and names the page

#### Scenario: An assumption and a threat that do not name each other fail CI

- **WHEN** a threat names an assumption that does not name the threat, or an assumption names a threat that does not name the assumption
- **THEN** a test fails and names both

#### Scenario: A threat that names its assumptions in prose fails CI

- **WHEN** a threat's field `Assumptions` holds text that is not an assumption's ID
- **THEN** a test fails and names the threat

### Requirement: Each fact's check can be followed

A fact whose subject no test may reach, such as Claude Code or GitHub, SHALL NOT be checked by a test alone. An observation SHALL name the file under `tests/` that reproduces what was seen, the date, and the program, version and build it was seen on, and never whose work it was seen in. Documentation SHALL be linked by its address, as a vendor's page on a host or a file at a full commit of a GitHub repository that the test lists, with the date it was read. Tests SHALL fail otherwise.

#### Scenario: A fact that no test can reach, checked by a test alone, fails CI

- **WHEN** a fact whose subject no test may reach, such as Claude Code or GitHub, gives a test as its only check
- **THEN** a test fails and names the assumption and the fact

#### Scenario: An observation that cannot be followed fails CI

- **WHEN** a fact checked by observation names no file under `tests/` that exists and holds a test that no mark skips or expects to fail, gives no date or one later than the day the test runs, or does not name the program, the version that it prints and its build
- **THEN** a test fails and names the assumption and the fact

#### Scenario: A documented fact that links elsewhere fails CI

- **WHEN** a fact checked by documentation links anything but an `https` address of a page on a vendor's documentation host that the test lists, or of a file at a full commit of a GitHub repository that it lists by a path with no `.` or `..` segment, shows link text other than its address, or gives no date or one later than the day the test runs
- **THEN** a test fails and names the assumption and the link

#### Scenario: An assumption that names a private source fails CI

- **WHEN** a page of the assumptions, or a file that a fact names as reproducing what was seen, holds a path under a home folder or a session identifier
- **THEN** a test fails and names the file and the line, and quotes neither

### Requirement: The assumptions give no other web address

No page of the assumptions SHALL give a web address but in the check of a fact checked by documentation, so that a link that no check reads cannot lead an agent elsewhere. Tests SHALL fail otherwise.

#### Scenario: A web address outside a documented check fails CI

- **WHEN** a page of the assumptions holds a web address anywhere but in the check of a fact checked by documentation
- **THEN** a test fails and names the file and the line

### Requirement: The assumptions with the most at stake come first

The assumptions SHALL be listed by the highest impact among the threats that rest on them, as the threat model rates those threats, then with the least checked first, then by the highest risk among those threats, with the assumptions that no threat rests on last. Each line of the index SHALL give that impact beside that risk. Tests SHALL fail when the list's order differs from the order that these give, or a line of the index does not give both ratings as the threat model does.

#### Scenario: An assumption out of order fails CI

- **WHEN** a threat's rating or a fact's check changes, and an assumption no longer stands in the order that they give
- **THEN** a test fails and names the assumption

#### Scenario: An assumption behind a threat of higher impact comes first

- **WHEN** one assumption rests on a threat of impact 3 and likelihood 1, and another only on threats of lower impact and higher risk
- **THEN** the first stands before the second, or a test fails and names it

#### Scenario: An index line without the impact fails CI

- **WHEN** a line of the assumptions' index gives an assumption's risk without the highest impact among the threats that rest on it, or gives a rating that differs from the threat model's
- **THEN** a test fails and names the assumption

### Requirement: The specs and pages use the glossary's words

The repository SHALL keep a glossary of each term's meaning and its words to avoid. Tests SHALL fail when a tracked Markdown file uses a word to avoid outside code, naming the file, the line and the term to use, and when they cannot read such a file whole, naming it. They SHALL NOT read decision records, archived changes, released changelog entries, vendored or generated files, or titles that an accepted record quotes, which keep their words, and SHALL fail when such a title leaves the specs.

#### Scenario: An avoided word fails CI

- **WHEN** a spec, a change's proposal, design or tasks, or another Markdown page that the repository tracks uses a word that the glossary says to avoid
- **THEN** a test fails and names the file, the line and the term to use

#### Scenario: A decision record keeps its words

- **WHEN** a decision record, an archived change, a released changelog entry, or a vendored or generated file uses a word that the glossary says to avoid
- **THEN** no test fails for it

#### Scenario: A word to avoid in code is left as written

- **WHEN** a tracked Markdown file gives a word that the glossary says to avoid inside inline code or a fenced code block
- **THEN** no test fails for it there, while the same word in the prose of that line fails

#### Scenario: A title that a record quotes keeps its words

- **WHEN** a requirement's or a scenario's title that an accepted record quotes is changed or removed in the specs
- **THEN** a test fails and names the record and the title

#### Scenario: A title that only a new record quotes is read

- **WHEN** a pull request adds a record whose status says accepted and that quotes a title holding a word to avoid
- **THEN** a test fails and names the file, the line and the term to use, since only the records that the default branch holds keep the titles that they quote

#### Scenario: A page that the test cannot read whole fails CI

- **WHEN** a tracked Markdown file that the test reads is a symbolic link, is not UTF-8, opens a fenced code block that never closes, or holds a line that GitHub reads in a fence or after it depending on whether a list item holds that fence
- **THEN** a test fails and names the file

#### Scenario: A wording check that reads nothing fails CI

- **WHEN** the glossary gives no word to avoid, or the test finds no file to read
- **THEN** a test fails

### Requirement: Each term is defined once

Tests SHALL fail when a glossary row gives no meaning, when two rows give the same term or the same word to avoid, and when a word that the glossary says to avoid is found in one of its terms or is the plural of one.

#### Scenario: A glossary row without a meaning fails CI

- **WHEN** a glossary row gives a term and no meaning
- **THEN** a test fails and names the term

#### Scenario: A term defined twice fails CI

- **WHEN** two glossary rows give the same term or the same word to avoid, or a word to avoid is found in a term or is a term's plural
- **THEN** a test fails and names the word

### Requirement: Every version reproduces the golden set

The repository SHALL hold a golden set of synthetic sessions, each with the pull request it is reported for, a price table of its own, each call of its transcripts with its entry or the scenario that leaves it out, and the figures as the comment shows them, worked out by hand from the specs with the working beside each. Tests SHALL run each session in a repository of its own, and fail when capture or the report gives another entry or figure, or a figure does not follow from its working.

#### Scenario: A result that differs from the golden set fails CI

- **WHEN** the capture step writes an entry, or the comment that the report writes shows a figure, for a session in the golden set other than the one worked out by hand
- **THEN** a test fails and names the session and the entry or the figure

#### Scenario: A golden figure that its working does not give fails CI

- **WHEN** a hand-worked figure in the golden set does not follow from the working beside it
- **THEN** a test fails and names the session and the figure

#### Scenario: A golden call that no entry or cited scenario accounts for fails CI

- **WHEN** a golden session leaves a call of its transcripts unlisted, lists one with neither a hand-worked entry nor a scenario that leaves it out, or cites a scenario that does not exist
- **THEN** a test fails and names the session and the call

#### Scenario: A golden pull request can hold ledger lines that no capture step wrote

- **WHEN** a golden session's pull request adds, removes, changes or restores ledger files, some of them holding lines that the capture step does not write
- **THEN** the test runs the report on it without the capture step, and fails when a figure, or a count that the comment gives of what the report did not count, differs from the hand-worked one

#### Scenario: The golden set leaves the clone that runs it alone

- **WHEN** the golden tests run from inside a clone of this repository whose tool is on, with the person running them opted in and a Claude Code session's calls waiting in its store
- **THEN** that clone's store, the entries of its index and its working tree are as they were before

#### Scenario: A version that does not reproduce the golden set is not released

- **WHEN** a release tag is pushed and a test of the golden set fails or is still marked as an expected failure
- **THEN** no release is published

### Requirement: A golden figure changes only with the spec that gives it

A pull request that changes an entry, a figure or a working that the golden set at its base holds SHALL either change a spec or change nothing outside the golden set, and when the latest release's tag holds that session, SHALL name the session in the changelog's unreleased section. Tests SHALL fail otherwise.

#### Scenario: A golden session changed beside other files without its spec fails CI

- **WHEN** a pull request changes an entry, a figure or a working of a session that the golden set at its base holds, and changes files outside the golden set but no spec
- **THEN** a test fails, names the session, and says that a golden figure changes with the spec that gives it or in a pull request of its own

#### Scenario: A golden session changed alone or with a spec passes

- **WHEN** a pull request changes a golden session and nothing else, or changes it together with a spec
- **THEN** no test fails for the change to the golden set

#### Scenario: A released golden figure changed without a changelog line fails CI

- **WHEN** a pull request changes or removes an entry or a figure of a golden session that the latest release's tag holds, and the changelog's unreleased section does not name the session
- **THEN** a test fails and names the session

### Requirement: The documentation says what stays published after an opt-out and what a hash does not hide

The README, the opt-in's feature page and the ledger's SHALL say that an opt-out, a removed ledger file or a removed store leaves each pushed ledger file in its branch's history, clones, forks and posted comments, and each one in a commit not yet pushed for its push to publish, and that a hashed id does not hide whose record it is, since a ledger file's commit names its author and whoever holds the transcript can match each hash. The glossary SHALL list `anonymous` as a word to avoid.

#### Scenario: A page that calls an entry `anonymous` fails the wording test

- **WHEN** a spec or a page, in its prose, calls the ledger, a ledger file or an entry `anonymous`
- **THEN** the wording test fails, naming the file and the line

#### Scenario: The opt-in's pages say what stays published

- **WHEN** the README's section on the opt-in, the opt-in's feature page and the ledger's feature page are read
- **THEN** each says that an opt-out, a removed ledger file or a removed store leaves pushed ledger files in their branch's history, in clones, forks and posted comments, that a later push publishes those in commits not yet pushed, that a force-push does not remove what GitHub keeps for the pull requests that referenced them, and that a hashed id does not hide whose record it is

### Requirement: The documentation says where an opt-in applies

The README and the opt-in's feature page SHALL say that one opt-in covers every repository that turns the tool on, those that adopt it later among them, with no notice in any of them; that a repository's own setting that turns capture off holds only in that clone; and how a person turns capture off for a folder with git's own conditional includes, and where that stops.

#### Scenario: The opt-in's pages say where an opt-in applies

- **WHEN** the README's section on the opt-in and the opt-in's feature page are read
- **THEN** each says that one opt-in covers every repository that turns the tool on, later ones too, with no notice, that a repository's own setting that turns capture off holds only in that clone, and how to turn capture off for a folder and where that stops: in a linked worktree there whose repository lies elsewhere, for a folder named through a symbolic link, and when the file that the include names is missing

### Requirement: Each ledger format that a release wrote keeps its golden figures

For each ledger format that a release's capture step wrote, the golden set SHALL keep sessions whose entries are as that release wrote them, with the figures that the report must give for them, for as long as the report reads that format. Tests SHALL fail when the report gives another figure for them.

#### Scenario: An earlier release's entries give their hand-worked figures

- **WHEN** the report reads a golden session's entries in a ledger format that an earlier release's capture step wrote
- **THEN** it gives the figures worked out by hand for them, or a test fails and names the session, the format and the figure

#### Scenario: A format that the report reads keeps a golden session

- **WHEN** a pull request removes the last golden session of a ledger format that a release wrote and the report still reads
- **THEN** a test fails and names the format
