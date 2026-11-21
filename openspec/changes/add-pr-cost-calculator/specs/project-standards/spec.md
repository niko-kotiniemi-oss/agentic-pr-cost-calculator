## Purpose

Hold the whole tool to the standards that make it safe to adopt: documentation that names everything it does and says how each feature is validated, connections only where that documentation says, rated threats, pull request text without private references, action pins that their repositories tagged, a record of each decision, kept so that each can be reversed on its own, the assumptions that the design rests on, a glossary of the words its documents use, specs that OpenSpec reads as they are written, and a golden set of figures that every version reproduces.

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

### Requirement: The tests of the specs' form read every spec that OpenSpec reads

Tests SHALL read as specs each `spec.md` in a folder at any depth below `openspec/specs/`, or below the `specs/` folder of each folder in `openspec/changes/` but `archive`, that no folder whose name starts with a dot holds, and SHALL fail when a file or a folder in `openspec/` outside `openspec/changes/archive/` is a symbolic link, which they never follow, or when a file is named `spec.md` in any case and is not one of those specs.

#### Scenario: A spec in a deeper folder is read

- **WHEN** a spec two folders below `openspec/specs/` or below a change's `specs/` folder, or in a change that has no proposal, holds a scenario with no THEN line
- **THEN** a test fails and names that spec

#### Scenario: A spec that the tests do not read fails CI

- **WHEN** a file named `spec.md` in any case stands in `openspec/`, outside `openspec/changes/archive/`, where the tests do not read it, as at the top of a `specs/` folder, in a change's own folder or in a folder whose name starts with a dot
- **THEN** a test fails and names the file

#### Scenario: A symbolic link among the specs fails CI

- **WHEN** a file or a folder in `openspec/`, outside `openspec/changes/archive/`, is a symbolic link
- **THEN** a test fails and names it, and no test reads what it points to

### Requirement: Each requirement's text keeps OpenSpec's form

Tests SHALL fail when a requirement that a spec they read gives under `## Requirements`, `## ADDED Requirements` or `## MODIFIED Requirements` has no scenario, or has text, between its heading and its first scenario, that holds neither SHALL nor MUST as a word, is longer than 500 characters, measured on its lines that are not blank, each trimmed and joined by line breaks, or holds a line that starts with a bold label and a colon, and when they read no requirement or no scenario.

#### Scenario: A requirement with no SHALL or MUST fails CI

- **WHEN** a requirement's text holds neither SHALL nor MUST as a word, as when it gives them in lower case or in its heading alone
- **THEN** a test fails and names the spec and the requirement

#### Scenario: A requirement longer than 500 characters fails CI

- **WHEN** a requirement's text is longer than 500 characters, whether a main spec gives it or a change adds or modifies it
- **THEN** a test fails and names the spec, the requirement and its length

#### Scenario: A requirement with no scenario fails CI

- **WHEN** a requirement that a main spec gives, or that a change adds or modifies, has no scenario
- **THEN** a test fails and names the spec and the requirement

#### Scenario: A label line in a requirement's text fails CI

- **WHEN** a requirement's text holds a line that starts with a bold label and a colon, such as `**Note**:`, which OpenSpec leaves out of the text when other lines remain
- **THEN** a test fails and names the spec, the requirement and the line

#### Scenario: A requirement that a change removes or renames is not read for its text

- **WHEN** a change removes a requirement, giving its heading with its reason and its migration and no scenario, or renames one
- **THEN** the test passes it

#### Scenario: A test that reads no requirement or no scenario fails

- **WHEN** the test finds no spec, or specs that give no requirement or no scenario
- **THEN** it fails and says what it did not read

### Requirement: Each scenario of the specs keeps OpenSpec's form

Tests SHALL fail when a scenario in a spec that they read holds other than one `- **WHEN**` line and then one `- **THEN**` line, each followed by any `- **AND**` lines, when it has the name of another scenario in that spec, and when a requirement's text holds a line that starts as a scenario's lines do.

#### Scenario: A scenario out of form fails CI

- **WHEN** a scenario has no `- **WHEN**` line or no `- **THEN**` line, gives one of them twice or its THEN first, or holds another line, such as a later scenario's heading made plain text or bold
- **THEN** a test fails and names the spec, the requirement, the scenario and the line

#### Scenario: A scenario that takes another's name fails CI

- **WHEN** two scenarios in one spec have the same name, under one requirement or under two
- **THEN** a test fails and names the spec and the name

#### Scenario: A scenario's line in a requirement's text fails CI

- **WHEN** a `- **WHEN**`, `- **THEN**` or `- **AND**` line stands in a requirement's text, as when its first scenario's heading is made plain text
- **THEN** a test fails and names the spec and the line

#### Scenario: A scenario with AND lines passes

- **WHEN** a scenario gives `- **AND**` lines after its WHEN line and after its THEN line
- **THEN** the test passes it

### Requirement: Each heading and line of the specs is read as GitHub shows it

Tests SHALL fail when a spec that they read gives text other than a title before its sections; a heading other than that title, the sections that OpenSpec reads, and `### Requirement:` and `#### Scenario:` headings with a name, the second under a requirement; another line that, after any spaces, tabs or list or quote markers, starts with `#` or three backticks or tildes, or holds only `=` or `-` signs and spaces or tabs; or a line before the first requirement of a section that gives their text.

#### Scenario: A heading out of form or out of place fails CI

- **WHEN** a requirement's or a scenario's heading is at another level, or lacks `Requirement:` or `Scenario:` or its name, a scenario's heading stands before any requirement, or a spec gives a title after its first section, a section that OpenSpec does not read or any other heading
- **THEN** a test fails and names the spec and the line

#### Scenario: A line that OpenSpec or GitHub alone reads as a fence or a heading fails CI

- **WHEN** a line, after any spaces, tabs or list or quote markers, starts with three backticks or three tildes, as a fence's opening line or a code span does, inside an HTML comment or not, starts with `#` and is not a heading in form, such as `###Requirement:` with no space or `- ### Requirement:` in a list item, or holds only `=` or `-` signs and spaces or tabs, with which GitHub makes the line above it a heading
- **THEN** a test fails and names the spec and the line

#### Scenario: A line before a section's first requirement fails CI

- **WHEN** a line stands before the first requirement of a section that gives their text, as when that requirement's heading is made plain text
- **THEN** a test fails and names the spec and the line

#### Scenario: A line before a spec's first section fails CI

- **WHEN** a line of text other than a title stands before a spec's first section, where GitHub shows it and OpenSpec reads no text
- **THEN** a test fails and names the spec and the line

#### Scenario: A spec in OpenSpec's own form passes

- **WHEN** a main spec opens with the title that archiving a change gives it, then `## Purpose` and `## Requirements`, and a change's spec gives the sections of OpenSpec's template
- **THEN** the test passes it

### Requirement: The specs hold only text that GitHub shows as it is

Tests SHALL fail when a spec that they read holds a character other than printable ASCII and line breaks, a run of backticks that no run as long closes on its line, or, outside inline code, a `<`, an `&`, a backslash, a `|`, a `](`, a `]:`, a `$` or a `~`, with which GitHub would show the spec otherwise than OpenSpec and agents read it.

#### Scenario: Text that GitHub would hide or show otherwise fails CI

- **WHEN** a spec holds a character other than printable ASCII and line breaks, such as a carriage return, a byte-order mark or a line separator, bytes that are not UTF-8, inline code that does not close on its line, or, outside inline code, an HTML comment, a character reference, an escaped character, a table, a link, a link reference definition, a mathematical expression or struck-through text
- **THEN** a test fails and names the spec, the line and what it holds

#### Scenario: Inline code may hold those marks

- **WHEN** a spec gives `<`, `&`, `|`, `](`, `]:`, `$`, `~` or a backslash inside inline code that closes on its line
- **THEN** the test passes it

### Requirement: CI checks that the tests read each spec as OpenSpec does

CI SHALL fail when the specs and changes that the tests of the specs' form read, or the requirements that they read from each, in order, each with its operation in a change, its name, its text and its scenarios' names and lines, differ from what the pinned OpenSpec CLI lists and shows for them, and when it compares none.

#### Scenario: A spec that the tests read otherwise than OpenSpec fails CI

- **WHEN** the pinned OpenSpec CLI lists a spec or a change that the tests do not read, or the other way round, or shows a requirement's operation, name, text or scenarios otherwise than the tests read them, as for a requirement that a fence hides from OpenSpec
- **THEN** CI fails and names the spec and the first difference

#### Scenario: A comparison of nothing fails CI

- **WHEN** the comparison finds no requirement to compare
- **THEN** CI fails and says so

#### Scenario: Readings that agree pass

- **WHEN** the tests and the pinned CLI read the same specs and changes, and the same requirements in each
- **THEN** the comparison passes

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

Every record and design decision that a tracked file outside `vendor/` and `tests/`, or a context file, names, and every requirement, threat, change and task that a Markdown file there names, SHALL exist, a requirement or a threat as held or retired. A parenthesis right after a record's ID SHALL give that record's title, and only the records, their index, the changelog, archived changes and the mapping of B-022 SHALL name a closed record, since a closed record holds nothing.

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

- **WHEN** a tracked file other than a record, the index, the changelog, an archived change or the mapping of B-022 names a closed record
- **THEN** a test fails and names the file and the record

#### Scenario: A context file under `tests/` is read

- **WHEN** `tests/CLAUDE.md` names a record that does not exist, or a closed one
- **THEN** a test fails and names the file and the record, while the other files under `tests/` stay unread

#### Scenario: The mapping of B-022 may name a closed record

- **WHEN** `docs/evidence/B-022-mapping.md` names a closed record in the text that it quotes
- **THEN** the test does not report it, and still reports a record that it names and that does not exist

### Requirement: A decision record holds plain text

A record and the index SHALL hold only printable ASCII characters and line breaks, with no `&`, backslash or `@`, no fenced block, no web address, no link reference definition, no `<` or `][` outside inline code and no link but from a record's ID to that record's file, and a record SHALL hold no `|` outside inline code and no line but its headings that starts with `#`, so that a reviewer reads what an agent reads.

#### Scenario: A record that hides text or links elsewhere fails CI

- **WHEN** a record or the index holds a character other than printable ASCII or a line break, `&`, a backslash, `@`, a fenced block, a web address, a link reference definition, `<` or `][` outside inline code, or a link but from a record's ID to that record's file, or a record holds `|` outside inline code or a line other than its headings that starts with `#`
- **THEN** a test fails and names the file

### Requirement: An accepted record changes only to be closed

Tests SHALL fail when a commit removes, renames or moves a record that the base commit holds, or changes it except to close it, by its status set to closed and its closer named, after which any line of text under its sections may become `[removed]`, or as the next two requirements allow. They SHALL compare git trees with where HEAD left the default branch and with any base commit that CI names, and SHALL fail when either cannot be found, or holds the records' folder with no record in it.

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

### Requirement: A field added to every record leaves the rest of each record as it was

A commit MAY change the records that the base commit holds by adding to every one of them the lines of the fields Boundary and Reversibility that its copy lacks, each in its place, and nothing else, a record that it closes included. Tests SHALL fail when such a commit adds another field, adds them to some of those records and not to others, or changes any other line of a record beyond what closing it allows.

#### Scenario: A field added to every record passes

- **WHEN** a commit adds to each record that the base holds the lines of Boundary and Reversibility that its copy lacks, and changes nothing else in it, or only closes it as well
- **THEN** the test passes

#### Scenario: A field added together with another edit fails CI

- **WHEN** a commit adds such a field to a record that the base holds and also changes, adds or removes another line of it
- **THEN** a test fails and names the record

#### Scenario: A field that the form does not give fails CI

- **WHEN** a commit adds to a record that the base holds a line of a field other than Boundary and Reversibility, or a field line that the base's copy already has
- **THEN** a test fails and names the record

#### Scenario: A field added to some held records and not to others fails CI

- **WHEN** a commit adds Boundary and Reversibility to some of the records that the base holds and leaves others without them
- **THEN** a test fails and names a record left without them

### Requirement: A record number held twice is mended by renumbering the later record

When each base commit other than HEAD holds two records with one number, a commit MAY move the one that the base's first-parent history added later to the number after the base's highest, changing only its heading's number, and replace the old number with the new one, mention by mention, in the records that the same commit of that history added and in the Closed by of each record that it replaces. Tests SHALL fail on any other removal or renaming, and on a repeat that this cannot mend.

#### Scenario: The later of two records with one number renumbered passes

- **WHEN** the base holds two records with one number, and a commit moves the one that the base's first-parent history added later to the number after the base's highest, changing only its heading's number, and changes the other records added with it only by that number
- **THEN** the test passes

#### Scenario: The earlier of two records with one number renumbered fails CI

- **WHEN** the base holds two records with one number, and a commit moves the one that the base's first-parent history added earlier
- **THEN** a test fails and names the record

#### Scenario: A renumbering that changes more fails CI

- **WHEN** a commit moves the later record but changes its text beyond its heading's number, takes another number than the one after the base's highest, or changes a record added with it in another way
- **THEN** a test fails and names the record

#### Scenario: A record renumbered when no number is held twice fails CI

- **WHEN** the base holds no number twice and a commit moves a record that it holds to another number, or only a base that the pull request chose holds it twice
- **THEN** a test fails and names the record

#### Scenario: The later record renumbered, with each record that it closed naming it anew, passes

- **WHEN** the moved record replaces records that another merge added, and the commit changes only their Closed by from the old number to the new one
- **THEN** the test passes

#### Scenario: A mend merged to the default branch passes there

- **WHEN** a push to the default branch merges such a mend, so that HEAD, one of the bases, no longer holds the repeat
- **THEN** the test passes

#### Scenario: A repeat that renumbering cannot mend fails CI

- **WHEN** a base holds a number three times, two numbers twice each, or two records with one number that one commit of its first-parent history added
- **THEN** a test fails, names the records and says that the owner decides how to mend them

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

`docs/decisions/` SHALL hold only the records and their index, each a file of git's mode 100644 and not a link or an executable file, with no folder in it, and no file elsewhere SHALL be named as a record, so that every record is one that the checks read.

#### Scenario: A file out of place fails CI

- **WHEN** `docs/decisions/` holds a folder, a link, or a file that is neither a record nor the index, or a file elsewhere is named as a record
- **THEN** a test fails and names the file

#### Scenario: A record committed as executable fails CI

- **WHEN** HEAD's tree or the index gives a file in `docs/decisions/` a mode other than 100644
- **THEN** a test fails and names the file and its mode

### Requirement: No attribute hides the diff of a record, the README, a file that steers, the guide, the threat model, a change's tasks or what the marketplace serves, or changes the plugin's checkout

No attribute that the repository sets SHALL make git show as binary, or GitHub hide as generated, the diff of a record, the index, the README, a file that steers or a test that holds one, the guide, the threat model, a change's `tasks.md`, the root marketplace file or a file in the plugin folder that it names, so that whoever merges reads each change to them, nor make git's checkout of the hook file or of a file in that folder write more than other line endings.

#### Scenario: An attribute that hides a record's diff fails CI

- **WHEN** the repository's attributes give a record or the index `binary`, `diff` or `linguist-generated`, in any state
- **THEN** a test fails and names the file and the attribute

#### Scenario: An attribute that hides the marketplace's diff fails CI

- **WHEN** the repository's attributes give the root marketplace file, or a file in the plugin folder that it names, `binary`, `diff` or `linguist-generated`, in any state
- **THEN** a test fails and names the file and the attribute

#### Scenario: An attribute that hides the README's diff fails CI

- **WHEN** the repository's attributes give `README.md` `binary`, `diff` or `linguist-generated`, in any state
- **THEN** a test fails and names the file and the attribute

#### Scenario: An attribute that hides the guide's diff fails CI

- **WHEN** the repository's attributes give `docs/patterns.md` `binary`, `diff` or `linguist-generated`, in any state
- **THEN** a test fails and names the file and the attribute

#### Scenario: An attribute that hides the threat model's diff fails CI

- **WHEN** the repository's attributes give `docs/threat-model.md` `binary`, `diff` or `linguist-generated`, in any state
- **THEN** a test fails and names the file and the attribute

#### Scenario: An attribute that hides `CLAUDE.md`'s diff fails CI

- **WHEN** the repository's attributes give `CLAUDE.md` `binary`, `diff` or `linguist-generated`, in any state
- **THEN** a test fails and names the file and the attribute

#### Scenario: An attribute that hides a folder file's diff fails CI

- **WHEN** the repository's attributes give `docs/CLAUDE.md` or `tests/CLAUDE.md` `binary`, `diff` or `linguist-generated`, in any state
- **THEN** a test fails and names the file and the attribute

#### Scenario: An attribute that hides the diff of another file that steers fails CI

- **WHEN** the repository's attributes give `.claude/settings.json`, a file under `.claude/hooks/` or `.claude/skills/`, a workflow, `renovate.json`, `tests/test_context_files.py` or `tests/test_repository.py` `binary`, `diff` or `linguist-generated`, in any state
- **THEN** a test fails and names the file and the attribute

#### Scenario: An attribute that hides a change's tasks' diff fails CI

- **WHEN** the repository's attributes give a change's `tasks.md`, active or archived, `binary`, `diff` or `linguist-generated`, in any state
- **THEN** a test fails and names the file and the attribute

#### Scenario: An attribute that changes the plugin's checkout fails CI

- **WHEN** the repository's attributes give the hook file, or a file in the plugin folder that the root marketplace file names, `working-tree-encoding`, `ident` or `filter`, in any state
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

The README, the opt-in's feature page and the ledger's SHALL say that an opt-out, a removed ledger file or a removed store leaves each pushed ledger file in its branch's history, clones, forks and posted comments, and each one in a commit not yet pushed for its push to publish, that a force-push does not remove what GitHub keeps for the pull requests that referenced a commit, and that a hashed id does not hide whose record it is. The glossary SHALL list `anonymous` as a word to avoid.

#### Scenario: A page that calls an entry `anonymous` fails the wording test

- **WHEN** a spec or a page, in its prose, calls the ledger, a ledger file or an entry `anonymous`
- **THEN** the wording test fails, naming the file and the line

#### Scenario: The opt-in's pages say what stays published

- **WHEN** the README's section on the opt-in, the opt-in's feature page and the ledger's feature page are read
- **THEN** each says that an opt-out, a removed ledger file or a removed store leaves pushed ledger files in their branch's history, in clones, forks and posted comments, that a later push publishes those in commits not yet pushed, that a force-push does not remove what GitHub keeps for the pull requests that referenced them, and that a hashed id does not hide whose record it is

### Requirement: The documentation says where an opt-in applies

The README and the opt-in's feature page SHALL say that one opt-in covers every repository that turns the tool on, those that adopt it later among them, with no notice in any of them, and with the plugin each one where the person's sessions work or commit, whether or not it registers the hook; that a repository's own setting that turns capture off holds only in that clone; and how a person turns capture off for a folder with git's own conditional includes, and where that stops.

#### Scenario: The opt-in's pages say where an opt-in applies

- **WHEN** the README's section on the opt-in and the opt-in's feature page are read
- **THEN** each says that one opt-in covers every repository that turns the tool on, later ones too, with no notice, and with the plugin each one where the person's sessions work or commit, whether or not it registers the hook, that a repository's own setting that turns capture off holds only in that clone, and how to turn capture off for a folder and where that stops: in a linked worktree there whose repository lies elsewhere, for a folder named through a symbolic link, and when the file that the include names is missing

### Requirement: The documentation says how capture covers a project's cloud threads

The README and the capture's feature page SHALL say that a project's cloud threads run capture only through the plugin, give the setup script's line, which opts in each session in that environment in every repository that turns the tool on, and say that calls from the folder that holds the clones are left out and flagged, that a call from a clone counts there whatever clone it works on, how to keep a session in a repository, and that a machine not resumed loses calls that no commit took.

#### Scenario: The pages say how a cloud thread is covered

- **WHEN** the README's section on cloud threads and the capture's feature page are read
- **THEN** each says that a project's cloud threads run capture only through the plugin, which is added in the project's settings and loads into the threads that start afterwards, gives the setup script's line and says that it opts in each session in that environment, in every repository that turns the tool on, says that calls made from the folder that holds the clones are left out and flagged, that a call made from one clone counts there whatever clone it works on, so that a project that holds a repository that turns the tool on should hold no repository whose work must stay private, says how to keep a session inside a repository, and that one `cd` into a clone does not keep it there, since Claude's current directory can go back to the thread's folder, and says that a machine that cannot be resumed loses the calls that no commit took

### Requirement: The documentation says how to turn capture off in a session that is running, and how to check it

The README SHALL say that removing the setup script's line, or using another environment, reaches only the sessions that start, or whose machines are rebuilt, afterwards; that `git config --global pr-cost.capture false` in a session turns capture off there, and the variables `GIT_CONFIG_COUNT=1`, `GIT_CONFIG_KEY_0=pr-cost.capture` and `GIT_CONFIG_VALUE_0=false` on an environment from each session's next restore; what can undo each; and how to see a session's opt-in.

#### Scenario: The README says how to turn capture off in a running session

- **WHEN** the README's section on turning capture off is read
- **THEN** it says that removing the setup script's line, or using another environment, reaches only sessions that start, or whose machines are rebuilt, afterwards, gives `git config --global pr-cost.capture false` for a running session and the three `GIT_CONFIG_` variables for an environment, which each of its sessions reads at its next restore, says that the first holds until something writes the opt-in again, as the setup script does on a machine that is rebuilt and an organization's hook can at a session's start or resume, or after `/clear` or a compaction, and the variables unless a settings file that the session loads sets `GIT_CONFIG_COUNT` itself, says that the three are for an environment that sets no other `GIT_CONFIG_` variable and how one that does adds the pair, gives `git config --show-origin --get-all pr-cost.capture` to see each value of a session's opt-in and where it comes from, says that `git config --global --get pr-cost.capture` shows only the global file's value, gives `/hooks` to see the hooks that run, and says that a repository whose `.claude/settings.json` sets `remote.defaultEnvironmentId` chooses the environment of the cloud sessions that `claude --cloud` starts from its clone, over the person's own pick, which the person keeps with the same key in the clone's `.claude/settings.local.json`

### Requirement: The documentation says how an organization turns capture on for its members

The README SHALL say how an organization turns the plugin on for its members, with no `ref`, and puts the opt-in's line in a shared environment, which sessions it reaches, that sharing an environment shares its line, that a member cannot change it, how managed settings opt members in only in cloud sessions and what a hook without that limit leaves, that it tells members first and what is published, how a member sees and stops capture, and that Team and Enterprise plans have no Projects yet.

#### Scenario: The README says what an organization's option does

- **WHEN** the README's section on organizations is read
- **THEN** it says how an organization turns the plugin on for its members, registering this repository's marketplace with no `ref`, since a release's own tag holds the release before it, and puts the opt-in's line in a shared environment, which sessions each reaches, that a member who has not picked an environment uses the organization's default, that sharing an environment, or making it the default, shares the line in its setup script with every member who uses it and with a Claude Tag channel's sessions, so that an Owner takes their own line out first, that a member sees a shared environment read-only, so that an opt-out in a session there holds only until its machine is rebuilt and a member refuses the line for good only by working in an environment of their own, and keeps an agent that a later release adds out only by turning all capture off, since no opt-in leaves one agent out, that the organization's managed settings can also opt members in, with a hook that writes the opt-in only when `CLAUDE_CODE_REMOTE` is `true`, which it is in cloud sessions alone, and `git config --global --get pr-cost.capture` does not already give `true`, since the hook runs again after `/clear` and a compaction, and a write of the person's global configuration ends every interval, that a hook without the first condition writes the opt-in into a member's own git configuration on their own computer, where it stays after the hook goes and after they leave, and records each agent that later releases add, so that an organization that stops tells its members to turn capture off on each computer, that the organization tells its members first what is then published, and that its opt-in also records each agent that a later release adds, with no step of theirs, that a person's own line belongs in an environment of their own, how a member sees what turns capture on, with git's `--show-origin` and `/hooks`, and turns it off, and that Projects are not offered on Team or Enterprise plans yet

### Requirement: The documentation gives both ways to install the plugin, the zip first

The README SHALL give the release's zip first, with the command that checks its SHA-256 against the README at the release's commit, then this repository as a marketplace, saying when its updates arrive and that nothing needs accepting once one has synced, that a fixed release comes from its zip, since a release's tag holds an earlier plugin, that a zip follows no address, that a plugin loaded in place runs whatever its folder holds, and that a repository still copies the hook file.

#### Scenario: The README gives the zip first and the marketplace second

- **WHEN** the README's section on installing the plugin, and its section on adopting the tool, are read
- **THEN** the section on installing the plugin gives the release's zip first, with the command that checks its SHA-256, then the repository as a marketplace, on claude.ai or with Claude Code's command, says that a marketplace's update arrives when the person checks for updates, or by itself once they turn on syncing, with nothing to accept once it has synced, that a fixed release comes from its zip and not from a marketplace pinned to the release's tag, which holds an earlier release's plugin or none, since the marketplace's folder moves only after a release, that a zip follows no address, that the plugin is installed only from a release's zip or from this repository's GitHub address, since one loaded in place runs whatever its folder holds, and that a repository still copies the hook file, and the section on adopting the tool names the plugin and points to that section

### Requirement: The documentation says which release of the plugin runs, and what that changes

The README SHALL say that the release of the plugin that a session runs, not the repository's pinned report, writes that session's ledger files, what a later or an earlier plugin then does, as an earlier copy leaving a session or a store to a later one, that a repository keeps its pin current and a person keeps their plugin current, that one copy of a plugin's name runs its hooks, how to see which, and that a tag with no published release is not a version.

#### Scenario: The README says which release of the plugin runs

- **WHEN** the README's section on installing the plugin is read
- **THEN** it says that the plugin's release, not the repository's pinned report, writes the ledger files of the sessions that run it, what a later plugin's ledger files do to an earlier report and what an earlier plugin does beside a later copy or store, that a repository keeps its pin current and a person keeps their plugin current, that only one copy of a plugin's name runs its hooks, how to see which one in a terminal session and what a cloud session shows, and that a tag with no published release is not a version to pin or install

### Requirement: The documentation says where the plugin leaves a staged ledger file

The README SHALL say that a plugin run meets a repository only through the project directory, Claude's directory or a git command run there, and outside the repository that holds the project directory takes back another session's file only where its own session runs git, so that a ledger file that a refused commit staged in a repository that the session then leaves stays staged until a later run of that session meets it, or a session runs git there, and how to look for one and take it back.

#### Scenario: The README says how to find a ledger file left staged in a repository that a session left

- **WHEN** the README's section on installing the plugin is read
- **THEN** it says that a ledger file that a refused commit staged in a repository that the session then left stays staged until a later run of that session meets that repository, or a session runs git there, and how to look for one with `git status` and take it back

### Requirement: The README opens with a short start

The README SHALL open, after its first paragraph and its status, with a short start of at most 200 words outside code, with no HTML, that says how a repository turns the tool on, pinned to a published release, how a person opts in, also in a cloud environment only they use, and adds the plugin for a project's cloud threads, from a release's zip checked against its README or from this repository's marketplace, how an organization opts its members in, and how to stop, linking each step's detail.

#### Scenario: The README opens with its short start

- **WHEN** the README is read from its top
- **THEN** the first section after its first paragraph and its status is the short start, which holds no HTML and at most 200 words outside code, counted as the runs of letters or digits, with any apostrophe or hyphen inside them, that are left once its heading, its code blocks, its inline code and each link's brackets and target are taken out, and says how a repository turns the tool on, pinned to a published release, how a person opts in on each machine, that a cloud environment that only they use takes the same line in its setup script, that a project's cloud threads also need the plugin, added in the project's settings, from the latest release's zip after checking its checksum against that release's README, or from this repository's marketplace, named by its address, whose updates need no approval, that an organization tells its members, then turns the plugin on and opts them in, and how to stop, on each machine and in each running session, and in a setup script or with another environment, and that an organization that opted a person in can do so again, linking for each step the README's section that gives its detail

#### Scenario: A short start that grows, moves, holds HTML or links elsewhere fails a test

- **WHEN** the short start holds more than 200 words outside code, counted as the runs of letters or digits, with any apostrophe or hyphen inside them, that are left once its heading, its code blocks, its inline code and each link's brackets and target are taken out, a section comes before it, the `.github` folder holds a README, which GitHub shows on the repository's page in place of this one, it holds HTML, such as a `<details>` element, an HTML comment or any other element, or one of its links names anything but a heading of the README or this repository's latest release by its full address
- **THEN** a test fails and names what it found

#### Scenario: A command of the short start that the detail or the specs do not give fails a test

- **WHEN** a command in the short start's code is not given, as written, in the README's section that the short start links for that step, its opt-in's line in both the section on the opt-in and the section on cloud threads, its opt-in is not `git config --global pr-cost.capture true`, its way to stop is not `git config --global pr-cost.capture false`, or the marketplace's address that it gives is not the one that the section on installing the plugin gives
- **THEN** a test fails and names the command

### Requirement: The README's short start says what an opt-in records and publishes

Before any step that opts anyone in, the short start SHALL say that the tool records only opted-in people's sessions, that one opt-in covers every repository that turns the tool on and every agent, later ones too, that a call counts in the repository it is made from, whatever it works on, and that what a session spends is committed with its work, traceable to the person, published once pushed, even after an opt-out, and stays published, and SHALL tell an organization to tell its members first.

#### Scenario: The short start says what an opt-in records and publishes

- **WHEN** the README's short start is read as GitHub shows it
- **THEN** before any step that opts anyone in, it says that turning the tool on in a repository records only the sessions of people who are opted in, that one opt-in covers every repository that turns the tool on and every agent that the tool records, later ones too, that a call counts in the repository that it is made from, whatever repository it works on, that what a session spends is committed with its work and can be traced to the person, that pushing that work publishes it, even after an opt-out, and that it stays published, and its step for an organization says to tell its members before it opts them in

#### Scenario: A short start that leaves out what an opt-in publishes, or says it late, fails a test

- **WHEN** the README's short start, as GitHub shows it, leaves out that turning the tool on records only the sessions of people who are opted in, that one opt-in covers every repository that turns the tool on and every agent that the tool records, later ones too, that a call counts in the repository that it is made from, whatever repository it works on, that what a session spends is committed with its work and can be traced to the person, or that it is published when pushed, even after an opt-out, and stays published, gives one of these only after a step that opts anyone in, or tells an organization to tell its members only after it opts them in
- **THEN** a test fails and names what is missing or late

### Requirement: The README folds the detail that follows its short start

The README's sections on adopting the tool, on the opt-in, on installing the plugin, on a project's cloud threads, on organizations and on turning capture off SHALL follow its short start, each with its heading shown and its text folded until a reader opens it, so that the README shows first its short start and a list of what the detail covers, and the README SHALL hold only printable ASCII and line breaks, and no other text that GitHub hides.

#### Scenario: The detail is folded under headings that show

- **WHEN** the README is read as GitHub shows it
- **THEN** its sections on adopting the tool, on the opt-in, on installing the plugin, on a project's cloud threads, on organizations and on turning capture off come after the short start, each heading shows, and the text of each section is inside a `<details>` element that stays closed until a reader opens it

#### Scenario: A section of detail that shows its text, or text that GitHub hides, fails a test

- **WHEN** one of those sections holds text, other than its heading, outside a `<details>` element, gives that element or its `<summary>` element an attribute, such as `open`, or comes before the short start, or the README holds a character other than printable ASCII and a line break, such as a zero-width space, a bidirectional control or a variation selector, a code block whose opening fence gives anything but a language on the test's list, which holds none that GitHub draws as a diagram, a map, a model or mathematics, such as `mermaid` or `math`, or, outside code, a `<` that does not open or close one of the `<details>` and `<summary>` elements that fold those sections, as in an HTML comment, any other element, a processing instruction, a declaration or a CDATA section, a `]:`, as in a link reference definition or a footnote's definition, a character reference, a mathematical expression, an image, a link with a title, or a link whose target holds a query or a fragment that names no heading of the README
- **THEN** a test fails and names the section, or the line and what it holds

### Requirement: The README sends people only to this repository and to addresses that its test lists

Every link, autolink and web address in the README, prose and code alike, and every repository that it names as `owner/repo`, SHALL name a heading of the README, a file of this repository by a relative path, an address on a list that its test keeps, or, on GitHub, only this repository, its latest release, or a release, a release's file, a file or a folder at a release's tag or a placeholder, since GitHub also serves under this repository's address what others write.

#### Scenario: The README's addresses are this repository's or on the test's list

- **WHEN** every link, autolink, web address and `owner/repo` in the README is read, in its opening, its short start, its folded detail and its code, an `owner/repo` being read where a `uses:` line, a marketplace's command or setting, or a `gh` command names a repository
- **THEN** each names a heading of the README, a file of this repository by a relative path, an address on the test's list, or, at `github.com` or `raw.githubusercontent.com`, this repository, its latest release, or a release, a release's file, a file or a folder at a tag of the form `vMAJOR.MINOR.PATCH` or at a placeholder, such as `<commit>`

#### Scenario: An address elsewhere, or a commit named by its ID, fails a test

- **WHEN** the README gives, anywhere in it, a link, an autolink, a web address or an `owner/repo` that names another repository or site that the test's list does not hold, or anything else under this repository's address, such as a commit by its ID, a branch, a pull request's ref, such as `refs/pull/1/head`, a pull request, an issue or a comparison
- **THEN** a test fails and names the address

### Requirement: The README's section on adopting the tool takes the tool from a published release's commit

The README's section on adopting the tool SHALL say to take the hook file, its registration and the calling workflow from the README at the commit that a published release names, SHALL give the calling workflow with its pin left for that commit, and SHALL say that a tag with no published release is not a version to pin, so that a pin, an update bot's included, is taken only once a published release names its commit.

#### Scenario: The section on adopting the tool takes the tool from a published release's commit

- **WHEN** the README's section on adopting the tool is read
- **THEN** it says to take the hook file, its registration and the calling workflow from the README at the commit that a published release names, gives the calling workflow with a placeholder for its pin and says to fill it with that commit, and says that a tag with no published release is not a version to pin, so that a pin, an update bot's included, is taken only once a published release names its commit

#### Scenario: A calling workflow pinned in the README, or a section that leaves out where the tool comes from, fails a test

- **WHEN** the README's calling workflow gives a commit, a tag or a branch for its pin in place of the placeholder, or the section on adopting the tool leaves out that the hook file, its registration and the calling workflow come from the README at a published release's commit, or that a tag with no published release is not a version to pin
- **THEN** a test fails and names what it found

### Requirement: The README leaves each opt-in to the person, or to their organization

The README's sections on the opt-in, on a project's cloud threads and on organizations SHALL say that a person sets their own opt-in, or their organization does once it has told them, and that an agent that sets the tool up turns capture on for no one, in a git configuration file, a setup script, an environment's variables or managed settings, and leaves the opt-in to whoever asked it.

#### Scenario: The README leaves the opt-in to the person

- **WHEN** the README's sections on the opt-in, on cloud threads and on organizations are read
- **THEN** each says that a person sets their own opt-in, or their organization does once it has told them, and that an agent that sets the tool up turns capture on for no one, in a git configuration file, a setup script, an environment's variables or managed settings, and leaves the opt-in to whoever asked it

### Requirement: The README's status says when this repository's marketplace does not serve the plugin yet

While this repository's root marketplace file is missing, or holds no entry for the tool's plugin, the README's status SHALL say that this repository's marketplace does not serve the plugin yet.

#### Scenario: The README's status says that the marketplace does not serve the plugin yet

- **WHEN** this repository's root marketplace file is missing, or holds no entry for the tool's plugin, and the README is read
- **THEN** its status says that this repository's marketplace does not serve the plugin yet

#### Scenario: A status that leaves out that the marketplace does not serve the plugin fails a test

- **WHEN** this repository's root marketplace file is missing, or holds no entry for the tool's plugin, as the file that lists the vendored Superpowers holds none, and the README's status does not say that this repository's marketplace does not serve the plugin yet
- **THEN** a test fails and names the root marketplace file

### Requirement: The roadmap says what is now, next and later

The repository SHALL keep a roadmap, `docs/roadmap.md`, linked from the README's list of documentation, with the sections Now, Next, Later, Known limitations and Known bugs in that order. It SHALL open by saying that it describes, that an item on it is neither a promise nor a date, and that it is not a request to start work, and Now SHALL end with one line on the build that links the change's proposal and tasks. Tests SHALL fail otherwise.

#### Scenario: The roadmap gives its sections in order

- **WHEN** the README's list of documentation and `docs/roadmap.md` are read
- **THEN** the list links the roadmap, the roadmap opens by saying that it describes, that an item is neither a promise nor a date and that it is not a request to start work, its sections are Now, Next, Later, Known limitations and Known bugs, in that order, and Now ends with the line on the build

#### Scenario: A roadmap without its link, its opening, a section or the line on the build fails a test

- **WHEN** `docs/roadmap.md` is missing, it does not open with what it says of its items, a section is missing or out of order, the README's list of documentation does not link it, or Now does not end with the line on the build
- **THEN** a test fails and names what is missing

### Requirement: Each backlog item says how far it is from being built

Each backlog item SHALL give one of five statuses: `Open to feedback and contributions`, `Planned`, `In progress`, `Done` or `Dropped`. An item that is `In progress` or `Done` SHALL name at least one pull request, and an item that is `Dropped` SHALL have a section that says why. Tests SHALL fail otherwise.

#### Scenario: Each item gives one of five statuses

- **WHEN** the backlog items are read
- **THEN** each gives one of the five statuses, each that is `In progress` or `Done` names a pull request, and each that is `Dropped` says why

#### Scenario: An item without one of the five statuses fails a test

- **WHEN** an item gives no status, or a status other than the five, such as `Planned.` with a stop or `Agreed`
- **THEN** a test fails and names the item

#### Scenario: An item in progress or done that names no pull request fails a test

- **WHEN** an item that is `In progress` or `Done` gives `none` in its field Pull requests, or an item that is `Dropped` has no section that says why
- **THEN** a test fails and names the item

### Requirement: Every risk of the design is listed as a known limitation

Each risk that the risks and trade-offs of any change's design give, active or archived, SHALL be listed, by its title as that design gives it, under the roadmap's Known limitations or in the section on known limitations and the roadmap of a page in `docs/features/` that is named for a spec. Each such page SHALL have that section, linking the roadmap, and Known limitations SHALL say that it is a short list and link each of those sections. Tests SHALL fail otherwise.

#### Scenario: Every risk is listed

- **WHEN** the risks and trade-offs of every change's design, the roadmap's Known limitations and the feature pages are read
- **THEN** each risk's title, as its design gives it, is listed in at least one of them, and Known limitations says that it is a short list and links each feature page's section

#### Scenario: A risk that no page lists fails a test

- **WHEN** a risk of a design is listed neither under the roadmap's Known limitations nor on any feature page, a feature page has no section on known limitations and the roadmap, that section does not link the roadmap, or Known limitations does not link it
- **THEN** a test fails and names the risk or the page

#### Scenario: A listed title that no design gives fails a test

- **WHEN** the roadmap's Known limitations or a feature page lists as a risk of the design a title that no change's design gives
- **THEN** a test fails and names the page and the title

#### Scenario: The risks are read from an archived change too

- **WHEN** the change whose design gives a risk is archived
- **THEN** the risk is still read from its archived design, and a page that no longer lists it fails a test

### Requirement: The roadmap and the backlog link only this repository's own files

Every link, image, autolink, web address, host and `owner/repo` in the roadmap, `docs/backlog/` and each feature page's section on known limitations and the roadmap, prose and code alike, SHALL name a heading of its own page or, by a relative path inside this repository, a tracked file of it outside `vendor/` and `.claude/skills/`. They SHALL name issues and pull requests by number alone, and give no `@`, commit ID, fenced or indented code, or space in inline code. Tests SHALL fail otherwise.

#### Scenario: The roadmap's and the backlog's links stay within this repository's files

- **WHEN** every link, autolink, web address and `owner/repo` in the roadmap, in the files in `docs/backlog/` and in those sections is read, each link from its `](` whatever its text holds, in prose and in inline code alike
- **THEN** each names a heading of its own page, or a tracked file of this repository outside `vendor/` and `.claude/skills/` by a relative path that, resolved from the page's folder, stays inside the repository

#### Scenario: A link elsewhere fails a test

- **WHEN** the roadmap, a file in `docs/backlog/` or such a section gives a web address, a host such as `example.org`, in prose or in inline code, that is not a tracked file's path or a name that the test lists as not a host, among them, in prose, one that emphasis marks split, as `evil.*example*` is, which GitHub shows as one name, and four numbers joined by dots, as an IP address is, an image, an `@`, an `owner/repo`, a commit ID, read as seven or more hexadecimal digits that hold both a digit and a letter, a fenced or indented code block, inline code that holds a space, as a command such as `git config --global pr-cost.capture true` does, a relative path that leaves the repository or names no tracked file, as `../../../issues/15` does, or a link into `vendor/` or `.claude/skills/`, whose files others write
- **THEN** a test fails and names the file and the line

#### Scenario: A name that only looks like a host passes when the test lists it

- **WHEN** the roadmap, a file in `docs/backlog/` or such a section gives, in prose or in inline code, a name that reads as a host, as two or more labels joined by dots whose last is made of letters, and that the test lists, with its reason, among the names that are not hosts, such as the git configuration key `core.autocrlf`
- **THEN** the test passes it, and fails on that name once it is taken off the list

### Requirement: The roadmap, the backlog and the feature pages' roadmap sections hold no hidden text

The roadmap, each file in `docs/backlog/`, and each feature page's section on known limitations and the roadmap, SHALL hold only printable ASCII and line feeds, and nowhere, inline code included, a `<`, a `&`, a backslash, a `]:`, a `|` or a link with a title, so that what GitHub shows of them is all that an agent reads. Tests SHALL fail otherwise.

#### Scenario: Text that GitHub hides fails a test

- **WHEN** the roadmap, a file in `docs/backlog/` or such a section holds a character other than printable ASCII and a line feed, such as a carriage return, a zero-width space or a bidirectional control, or, inline code included, a `<`, as in an HTML comment, a `&`, as in a character reference, a backslash, as in an escape, a `]:`, as in a link reference definition, a `|`, as in a table whose row holds a cell more than its header, or a link with a title
- **THEN** a test fails and names the file, the line and what it holds

### Requirement: A backlog item has its form

Each backlog item SHALL be a file `docs/backlog/B-NNN-words.md`, numbered from B-001 without a gap or a repeat, and the folder SHALL hold nothing else but `README.md`, which gives the form. An item SHALL open with `# B-NNN: title` and the fields Status, Last changed, Brief, Rests on, Issue and Pull requests, in that order, and then give the sections Problem, What done looks like and Postponed points, each once and in that order. Tests SHALL fail otherwise.

#### Scenario: Each backlog item has its form

- **WHEN** the files in `docs/backlog/` are read
- **THEN** each but `README.md` is an item named `B-NNN-words.md`, numbered from B-001 without a gap, with its heading, its six fields in order, a date as `YYYY-MM-DD` in Last changed, a brief of one to three sentences, IDs or `none` in Rests on, a number or `none` in Issue and numbers or `none` in Pull requests, and its sections in order

#### Scenario: An item out of form fails a test

- **WHEN** an item's file name, heading, fields or sections are missing, repeated, out of order or in another form, its brief holds more than three sentences, its date is not a date, the numbers have a gap or a repeat, or the folder holds another file, a folder or a symbolic link
- **THEN** a test fails and names the file and what is wrong

### Requirement: The README briefs developers on how work flows

The README's section on working here SHALL open, before its setup, with a briefing: anyone may open an issue with no approval needed; an issue is public at once and holds nothing private; what it proposes is not planned or committed to; and a backlog item changes only by a pull request that the owner merges. It SHALL give the stages of work in one table, which no other Markdown file gives, and `CONTRIBUTING.md` and `docs/backlog/README.md` SHALL link the section. Tests SHALL fail otherwise.

#### Scenario: The README opens its section on working here with the briefing

- **WHEN** the README's section on working on this repository is read
- **THEN** before its setup it says that anyone may open an issue with no approval needed, that an issue is public at once and holds nothing private, a security problem going to `SECURITY.md` instead, that what an issue proposes is neither planned nor committed to, and that a backlog item changes only through a pull request that the owner merges, and it gives the table of stages, with the columns Step, Where it lives, What it holds and Who writes it, and the rows An idea or a bug, Agreed work, Order, Delivery and Result, in that order, each row linking a page of this repository

#### Scenario: A briefing out of form, or a second copy of its table, fails a test

- **WHEN** the briefing is missing or follows the setup, leaves out one of those statements, its table lacks a column or a row, or gives them out of order, a row links no page, another tracked Markdown file gives the table's header, or `CONTRIBUTING.md` or `docs/backlog/README.md` does not link the section
- **THEN** a test fails and names what is wrong

### Requirement: The roadmap is the index of the open backlog items

Now, Next and Later SHALL give one line for each backlog item that is `Open to feedback and contributions`, `Planned` or `In progress`, in the order of the work, linking its file and giving its ID, title, status, date and brief as the item gives them, and no line for an item that is `Done` or `Dropped`. Now SHALL list only items that are `Planned` or `In progress`, and each item listed under Next or Later SHALL name at least one ID in Rests on. Tests SHALL fail otherwise.

#### Scenario: The roadmap lists each open item as the item gives it

- **WHEN** the roadmap's Now, Next and Later and the backlog items are read
- **THEN** each item that is `Open to feedback and contributions`, `Planned` or `In progress` is listed once, by a line that links its file and gives its ID, title, status, date and brief as the item gives them, and no item that is `Done` or `Dropped` is listed

#### Scenario: A line that differs from its item fails a test

- **WHEN** a line under Now, Next or Later gives a title, a status, a date or a brief that differs from its item's, links no backlog item's file, or is in another form
- **THEN** a test fails and names the line

#### Scenario: An open item missing or listed twice, or a closed one still listed, fails a test

- **WHEN** an item that is `Open to feedback and contributions`, `Planned` or `In progress` is listed in none of Now, Next and Later, or more than once, or an item that is `Done` or `Dropped` is listed
- **THEN** a test fails and names the item

#### Scenario: An item under Now that is not agreed fails a test

- **WHEN** an item listed under Now is `Open to feedback and contributions`
- **THEN** a test fails and names the item

#### Scenario: An item under Next or Later that rests on nothing fails a test

- **WHEN** an item listed under Next or Later gives `none` in its field Rests on
- **THEN** a test fails and names the item

### Requirement: Later says how work on an item starts

Later SHALL open by saying that work on an item that is open to feedback and contributions starts with an issue, that an item is built only once it is `Planned`, which only a pull request that the owner merges makes it, and that some items need a spec, a threat review and the owner's decision first. Each record that the README's list of what the first version does not support links SHALL be named in Rests on by an item listed under Later. Tests SHALL fail otherwise.

#### Scenario: Later opens with how work on an item starts

- **WHEN** the roadmap's Later is read
- **THEN** it opens, before its first line, with its sentence on how work on an item starts, and each record that the README's list of what the first version does not support links is named in Rests on by an item listed under Later

#### Scenario: Later without its opening fails a test

- **WHEN** Later does not open, before its first line, with its sentence on how work on an item starts
- **THEN** a test fails and names the section

#### Scenario: A record that the README leaves out and Later does not name fails a test

- **WHEN** the README's list of what the first version does not support links a record that Rests on of no item listed under Later names
- **THEN** a test fails and names the record

### Requirement: A backlog item names only what exists, and is not stale

Rests on SHALL hold only `none` or requirements (`R` and digits), records (`DR-` and three digits), threats (`T` and digits), assumptions (`A` and digits), backlog items (`B-` and three digits) and tasks (`task`, its number, `of` and its change's name as code), each of which SHALL exist, in active and archived changes alike. No item SHALL name a closed record, and an open item SHALL name no tasks that are all ticked. Tests SHALL fail otherwise.

#### Scenario: An item that names what does not exist fails a test

- **WHEN** an item's Rests on holds anything but `none` and those forms, or names a requirement that the register does not hold, a record that `docs/decisions/` does not hold, a threat that the threat model does not hold, an assumption that `docs/assumptions/` does not hold, a backlog item that `docs/backlog/` does not hold, or a task by a change and number that no change's `tasks.md`, active or archived, holds
- **THEN** a test fails and names the item and what it names

#### Scenario: A stale item fails a test

- **WHEN** an item names a closed record, or an item that is neither `Done` nor `Dropped` names tasks that are all ticked in their change's `tasks.md`
- **THEN** a test fails and names the item

### Requirement: A backlog item keeps its file, and its date moves with its text

Compared with the base commit that the records' check uses, no backlog item SHALL be removed, renamed or moved, an item whose text a branch changes SHALL give a later date in Last changed than the base's copy, or the same date when that is the day on which the test runs, and no item SHALL give a date later than that day, in UTC. Tests SHALL fail otherwise.

#### Scenario: An item changed without a new date fails a test

- **WHEN** a branch changes an item's text and leaves its date before the date that the base commit's copy gives, or at that date when it is not the day on which the test runs, or an item gives a date later than that day
- **THEN** a test fails and names the item

#### Scenario: A second change to an item on the day of the first passes

- **WHEN** the base commit's copy of an item gives the day on which the test runs, and a branch changes the item again and gives the same date
- **THEN** no test fails for its date

#### Scenario: An item removed or renamed fails a test

- **WHEN** the base commit holds an item that the branch removes, renames or moves
- **THEN** a test fails and names the item, so that every link to an item still leads to it once it is done or dropped

### Requirement: The backlog's page says what an item is and is not

`docs/backlog/README.md` SHALL give an item's form, link the roadmap, and say that an item describes, that it is neither a promise nor a date, that it is not a request to start work, what each of the five statuses means, and that `Done` means that its pull requests have merged to the default branch, while `CHANGELOG.md` names the release that holds it. Tests SHALL fail otherwise.

#### Scenario: The backlog's page says what an item is and is not

- **WHEN** `docs/backlog/README.md` is read
- **THEN** it links the roadmap, gives the form, and says that an item describes, is neither a promise nor a date and is not a request to start work, what each status means, and that `Done` means merged, with `CHANGELOG.md` naming the release

#### Scenario: A backlog page that leaves one out fails a test

- **WHEN** `docs/backlog/README.md` is missing, does not link the roadmap, or leaves out one of those statements or a status
- **THEN** a test fails and names what is missing

### Requirement: An item becomes agreed only by a change to its status

Compared with the base commit that the records' check uses, an item that the base does not hold SHALL be `Open to feedback and contributions` or `Planned`, and an item that the base gives as `Open to feedback and contributions` or `Dropped` SHALL NOT become `In progress` or `Done`, so that an item is agreed by its status line before it is built. The check SHALL be skipped while no base holds `docs/backlog/`. Tests SHALL fail otherwise.

#### Scenario: An item that skips agreement fails a test

- **WHEN** a branch adds an item that is `In progress`, `Done` or `Dropped`, or moves an item that the base gives as `Open to feedback and contributions` or `Dropped` to `In progress` or `Done`
- **THEN** a test fails and names the item and the two statuses

#### Scenario: The first items pass before any base holds the backlog

- **WHEN** no base commit holds `docs/backlog/`
- **THEN** the check of status changes examines nothing and passes, and once a base holds it, the check reads every item

### Requirement: The guide says how the project builds, concern by concern

A guide, `docs/patterns.md`, SHALL be linked from the README's list of documentation, and `CLAUDE.md` SHALL give the sentence on the guide's rank that the first scenario gives. The guide SHALL open with the text that the scenario gives, word for word, and a last line that names the assessment, by its date, or the release, by its version, for which its entries were last read, and SHALL then give the sections that the scenario names, each holding one or more entries. Tests SHALL fail otherwise.

#### Scenario: The guide opens with its text and gives its concerns in order

- **WHEN** the README's list of documentation, `CLAUDE.md` and `docs/patterns.md` are read
- **THEN** the list links the guide; `CLAUDE.md` gives the sentence "The guide is not one of the pages that only describe, but it steers below the specs and this file: where it differs from either, they win, so tell the owner, and it never widens what this file lets you do."; the guide opens, before its first section, with these lines, word for word, each followed by a blank line: "# How the project builds", "This guide says how the project builds, concern by concern: the principles that the project follows, each with the pattern that it applies and the anti-patterns that it steers clear of, what holds it, and where the project stands.", "The specs decide what the tool does, `CLAUDE.md` what an agent may do, and this guide how the project builds. Where the guide differs from the specs or `CLAUDE.md`, they win, and the owner is told. It never widens what `CLAUDE.md` lets an agent do, and an entry cites the requirement or the rule of `CLAUDE.md` that it rests on rather than stating it again. Where an entry and a step of a Superpowers skill differ, the step is followed, and the owner is told.", "The guide steers as the default branch holds it: an entry that a branch adds or changes is a proposal until the owner merges it, and a principle is added, removed, changed or moved to another concern only when the owner asks for it, in a pull request that changes nothing outside `docs/`, `openspec/`, the context files and `CHANGELOG.md`. It speaks to work on this repository, not to setting the tool up, which is the README's section on adopting it: an agent that sets the tool up turns capture on for no one.", "Where we stand gives where the default branch stands, and a release's guide is the copy at its tag. It opens with `Followed.` when the default branch's code and checks hold the principle, `Designed.` when its specs and tasks hold it before it is built, `Knowingly accepted.` with the record that gives the reason, or `Gap.` with the backlog item that closes it, as `Gap. Before the build.` when the owner asked for it to be closed before the build." and "A gap is not, by being there, a request to start work: it closes only through the backlog item that it names, and work outside that item leaves what the gap concerns as it stands. A principle knowingly accepted is accepted only where its record says."; then a last line that is "The entries are read again at each assessment and before each release, and were last read for " followed by "the assessment of " and a date as `YYYY-MM-DD`, or by "release " and a version as `MAJOR.MINOR.PATCH`, and a full stop; and its sections are Architecture and integration, Security, Privacy, Identity and credentials, Supply chain and releases, Testing, Decisions and documentation, Working with agents, and Conventions, in that order, each holding one or more entries

#### Scenario: A guide without its links, its opening or a concern fails a test

- **WHEN** `docs/patterns.md` is missing, the README's list of documentation does not link it, `CLAUDE.md` does not give that sentence, the text before the guide's first section differs from that text or names no assessment or release in its last line, or a section is missing, repeated, out of order or holds no entry
- **THEN** a test fails and names what is missing, or the first line that differs

### Requirement: Each entry of the guide gives its principle and where the project stands

Each entry SHALL be a `###` heading that names a principle, followed by the fields Statement, Rationale, Implications, Pattern, Anti-patterns, Held by, Rests on and Where we stand, each once, in that order, and nothing else, an entry under Working with agents citing `CLAUDE.md` in Held by. Where we stand SHALL open with `Followed.`, `Designed.`, `Knowingly accepted.` or `Gap.`, as "Where the guide says the project stands is held true" holds them. Tests SHALL fail otherwise.

#### Scenario: Each entry gives its fields in order

- **WHEN** the guide's entries are read
- **THEN** each is a `###` heading followed by the fields Statement, Rationale, Implications, Pattern, Anti-patterns, Held by, Rests on and Where we stand, each once, in that order, none of them empty, and each section holds its entries and nothing else

#### Scenario: An entry out of form fails a test

- **WHEN** an entry leaves out a field, repeats one, gives them out of order or leaves one empty, or a section holds text outside its entries
- **THEN** a test fails and names the entry, or the section and the line

#### Scenario: An entry that does not say where the project stands fails a test

- **WHEN** an entry's Where we stand opens with none of `Followed.`, `Designed.`, `Knowingly accepted.` and `Gap.`
- **THEN** a test fails and names the entry

#### Scenario: An entry on working with agents that does not cite `CLAUDE.md` fails a test

- **WHEN** an entry under Working with agents does not cite `CLAUDE.md` in its Held by, so that an entry there could stand in for a rule of `CLAUDE.md`
- **THEN** a test fails and names the entry

### Requirement: The guide links only this repository's own files and holds no hidden text

The guide SHALL hold to the rules that "The roadmap and the backlog link only this repository's own files" and "The roadmap, the backlog and the feature pages' roadmap sections hold no hidden text" give the roadmap, apart from inline code with a space in its opening, which is fixed word for word, and SHALL give no `$` and no `~` outside inline code and cite no file under `vendor/` or `.claude/skills/` in Held by, so that it leads no one to what others write or hide. Tests SHALL fail otherwise.

#### Scenario: A link elsewhere in the guide fails a test

- **WHEN** the guide gives a web address, a host such as `example.org`, in prose or in inline code, that is not a tracked file's path or a name that the test lists as not a host, among them, in prose, one that emphasis marks split and four numbers joined by dots, an image, an `@`, an `owner/repo`, a commit ID, a fenced or indented code block, inline code that holds a space after its opening, a relative path that leaves the repository or names no tracked file, or a link into `vendor/` or `.claude/skills/`, or an entry's Held by cites a file there, whose text others write
- **THEN** a test fails and names the line

#### Scenario: The guide's opening keeps its fixed words in inline code

- **WHEN** the guide's opening, which is fixed word for word, gives `Knowingly accepted.` and `Gap. Before the build.` in inline code
- **THEN** the test passes them, and fails on inline code that holds a space anywhere after the opening

#### Scenario: Text that GitHub hides in the guide fails a test

- **WHEN** the guide holds a character other than printable ASCII and a line feed, or, inline code included, a `<`, a `&`, a backslash, a `]:`, a `|` or a link with a title, or, outside inline code, a `$` or a `~`, with which GitHub shows mathematics or struck-through text
- **THEN** a test fails and names the file, the line and what it holds

### Requirement: Each entry of the guide gives its source, what holds it and what it rests on

An entry's Pattern SHALL give its recognised name and, after `Source:`, its source by author or body and work. Held by SHALL cite what holds the entry as the threat model's Held by does, or say after `Review:` what review checks, or both. Rests on SHALL hold IDs, in the forms of a backlog item's Rests on, that exist and name no closed record. Clean Code, PEP 8, OWASP's secure coding practices and OpenSSF's Scorecard SHALL each be named in a Pattern. Tests SHALL fail otherwise.

#### Scenario: Each entry gives its source, what holds it and what it rests on

- **WHEN** the guide's entries are read
- **THEN** each Pattern gives text after `Source:`, each Held by cites scenarios, tasks, decisions, records or files that exist, or gives text after `Review:`, or both, each Rests on names one or more requirements, records, threats, assumptions, backlog items or tasks that exist and no closed record, and Clean Code, PEP 8, OWASP's secure coding practices and OpenSSF's Scorecard are each named in an entry's Pattern

#### Scenario: An entry with no source fails a test

- **WHEN** an entry's Pattern gives no `Source:` or nothing after it
- **THEN** a test fails and names the entry

#### Scenario: An entry whose Held by holds nothing that resolves fails a test

- **WHEN** an entry's Held by cites a scenario, a task, a design decision, a record or a file that does not exist, or neither cites anything nor gives text after `Review:`
- **THEN** a test fails and names the entry and what it cites

#### Scenario: An entry that rests on nothing, or on what does not exist, fails a test

- **WHEN** an entry's Rests on gives `none` or an ID in another form, or names a requirement that the register does not hold, a record that `docs/decisions/` does not hold or that is closed, a threat that the threat model does not hold, an assumption that `docs/assumptions/` does not hold, a backlog item that `docs/backlog/` does not hold, or a task by a change and number that no change's `tasks.md`, active or archived, holds
- **THEN** a test fails and names the entry and what it names

#### Scenario: A named practice left out of the guide fails a test

- **WHEN** no entry's Pattern names one of Clean Code, PEP 8, OWASP's secure coding practices and OpenSSF's Scorecard
- **THEN** a test fails and names the practice

### Requirement: Where the guide says the project stands is held true

`Followed.` SHALL be given only while every task that the entry's Held by cites is ticked, and `Designed.` only while one is not. `Knowingly accepted.` SHALL name an accepted record, and `Gap.` a backlog item that is not `Done` or `Dropped`. Under Security, Privacy, Identity and credentials, and Supply chain and releases, a record so named SHALL give the owner as its decider, and an item so named SHALL be `Planned` or `In progress`. Tests SHALL fail otherwise.

#### Scenario: A principle followed or designed as its tasks give passes

- **WHEN** an entry's Where we stand opens with `Followed.` and every task that its Held by cites is ticked, or with `Designed.` and one of them is not
- **THEN** the test passes it

#### Scenario: A principle said to be followed before it is built fails a test

- **WHEN** an entry's Where we stand opens with `Followed.` and its Held by cites a task that is not ticked, or with `Designed.` and its Held by cites no task that is not ticked
- **THEN** a test fails and names the entry, and the task that is not ticked

#### Scenario: A principle knowingly accepted without its record fails a test

- **WHEN** an entry's Where we stand opens with `Knowingly accepted.` and names no record, or names only records that `docs/decisions/` does not hold or that are closed
- **THEN** a test fails and names the entry

#### Scenario: A gap without an open backlog item fails a test

- **WHEN** an entry's Where we stand opens with `Gap.` and names no backlog item, or it names a backlog item that `docs/backlog/` does not hold or that is `Done` or `Dropped`
- **THEN** a test fails and names the entry and the item, so that the pull request that finishes or drops an item says again where the project stands

#### Scenario: A risk that adopters rely on, accepted without the owner, fails a test

- **WHEN** an entry under Security, Privacy, Identity and credentials, or Supply chain and releases opens Where we stand with `Knowingly accepted.`, and a record that it names does not give the owner in Decided by
- **THEN** a test fails and names the entry and that record

#### Scenario: A gap that adopters rely on, without an agreed item, fails a test

- **WHEN** an entry under Security, Privacy, Identity and credentials, or Supply chain and releases opens Where we stand with `Gap.`, and names a backlog item that is not `Planned` or `In progress`
- **THEN** a test fails and names the entry and that item

### Requirement: A gap to close before the build holds the build back

While an entry's Where we stand opens with `Gap.` and names a backlog item that the roadmap lists under Now, no task of `add-pr-cost-calculator` numbered 1.1 to 1.9, 1.13 to 1.15 or 1.21, or in a section after the first, SHALL be ticked in that change's `tasks.md`, active or archived, so that what the owner asked to be fixed before the build is fixed first, and an entry that opens with `Gap. Before the build.` SHALL name such an item. Tests SHALL fail otherwise.

#### Scenario: A gap to close before the build, with its item under Now, passes

- **WHEN** an entry's Where we stand opens with `Gap. Before the build.` and names an item that the roadmap lists under Now, and no task of `add-pr-cost-calculator` numbered 1.1 to 1.9, 1.13 to 1.15 or 1.21, or in a section after the first, is ticked
- **THEN** the test passes it

#### Scenario: A gap to close before the build whose item is not under Now fails a test

- **WHEN** an entry's Where we stand opens with `Gap. Before the build.` and names no item that the roadmap lists under Now
- **THEN** a test fails and names the entry and the items that it names

#### Scenario: A build task ticked while a gap to close before it is open fails a test

- **WHEN** an entry's Where we stand opens with `Gap.` and names an item that the roadmap lists under Now, whether or not it goes on with `Before the build.`, and a task of `add-pr-cost-calculator` numbered 1.1 to 1.9, 1.13 to 1.15 or 1.21, or in a section after the first, is ticked
- **THEN** a test fails and names the entry, the item and the task

### Requirement: A principle of the guide changes alone

Compared with the base that the records' check uses, a pull request that adds or removes a guide entry, moves one to another concern, or changes an entry's Statement, Rationale, Implications, Pattern or Anti-patterns, SHALL change no file outside `docs/`, `openspec/`, the context files and `CHANGELOG.md`, so that one diff cannot both weaken a principle and add the work that the principle forbade. The check SHALL be skipped while no base holds the guide. Tests SHALL fail otherwise.

#### Scenario: A principle changed beside other work fails a test

- **WHEN**, compared with the base, a pull request adds or removes an entry of the guide, or changes an entry's Statement, Rationale, Implications, Pattern or Anti-patterns, and also changes a file outside `docs/`, `openspec/`, the context files and `CHANGELOG.md`
- **THEN** a test fails and names the entry and the file

#### Scenario: An entry moved to another concern beside other work fails a test

- **WHEN**, compared with the base, a pull request moves an entry of the guide from one concern to another, as from Security, where only a record that the owner decided accepts it, to Conventions, and also changes a file outside `docs/`, `openspec/`, the context files and `CHANGELOG.md`
- **THEN** a test fails and names the entry, both concerns and the file

#### Scenario: A principle changed alone passes

- **WHEN**, compared with the base, a pull request that changes a principle so changes no file outside them, or one that changes no principle changes an entry's Held by, Rests on or Where we stand beside other work
- **THEN** the test passes it

#### Scenario: A principle changed beside a folder file's rules passes

- **WHEN**, compared with the base, a pull request changes a principle of the guide and, outside `docs/`, `openspec/` and `CHANGELOG.md`, changes only the root `CLAUDE.md` and `tests/CLAUDE.md`
- **THEN** the test passes it

#### Scenario: The guide's first entries pass before any base holds the guide

- **WHEN** no base commit holds `docs/patterns.md`
- **THEN** the check of changes to the guide's principles examines nothing and passes, and once a base holds it, the check reads every entry

### Requirement: A gap given to an agreed item changes that item

Compared with the base that the records' check uses, a pull request that makes an entry of the guide name as a gap a backlog item that the base gives as `Planned` or `In progress` SHALL change that item's What done looks like, so that what an agreed item takes on shows in its own text, which changes only on the owner's words. The check SHALL be skipped while no base holds the guide. Tests SHALL fail otherwise.

#### Scenario: A gap given to an agreed item without a change to that item fails a test

- **WHEN**, compared with the base, an entry comes to name as a gap a backlog item that the base gives as `Planned` or `In progress`, and that item's What done looks like is as the base gives it
- **THEN** a test fails and names the entry and the item

#### Scenario: A gap given to an agreed item with a change to that item passes

- **WHEN**, compared with the base, an entry comes to name as a gap a backlog item that the base gives as `Planned` or `In progress`, and that item's What done looks like differs from the base's, or it comes to name an item that the base gives with another status or does not hold
- **THEN** the test passes it

#### Scenario: The guide's first gaps pass before any base holds the guide

- **WHEN** no base commit holds `docs/patterns.md`
- **THEN** the check of gaps given to agreed items examines nothing and passes, and once a base holds it, the check reads every entry's gap

### Requirement: A gap of the guide closes only with its item

Compared with the base that the records' check uses, a pull request in which an entry of the guide, known by its heading, stops being a gap, or its gap stops naming a backlog item that the base's gap names, SHALL leave that item `Done` or `Dropped`, so that a gap closes, or passes to other work, only through its item, and not in the pull request whose work it holds back. The check SHALL be skipped while no base holds the guide. Tests SHALL fail otherwise.

#### Scenario: A gap closed while its item is open fails a test

- **WHEN**, compared with the base, an entry that the base gives as `Gap.` no longer opens Where we stand with `Gap.`, and a backlog item that the base's gap names is neither `Done` nor `Dropped`, or `docs/backlog/` does not hold it
- **THEN** a test fails and names the entry and the item

#### Scenario: A gap that stops naming its open item fails a test

- **WHEN**, compared with the base, an entry that the base gives as `Gap.` still opens Where we stand with `Gap.`, but no longer names a backlog item that the base's gap names, and that item is neither `Done` nor `Dropped`, or `docs/backlog/` does not hold it
- **THEN** a test fails and names the entry and the item

#### Scenario: A gap closed with its item done or dropped passes

- **WHEN**, compared with the base, each backlog item that the base's gap names is `Done` or `Dropped`, or is still named by the entry's gap, whatever other items the gap comes to name
- **THEN** the test passes it

#### Scenario: The guide's first standings pass before any base holds the guide

- **WHEN** no base commit holds `docs/patterns.md`
- **THEN** the check of gaps closed examines nothing and passes, and once a base holds it, the check reads every entry that the base gives as a gap

### Requirement: This repository holds no switch and no ledger file before its own capture is turned on

This repository SHALL track no `.pr-cost.json` and no file under `.pr-cost/` at its root, whatever the case of their letters, while task 7.1 of `add-pr-cost-calculator`, which turns the tool on here, is not ticked in that change's `tasks.md`, active or archived, so that no capture records here before then. A test SHALL fail and name the file otherwise.

#### Scenario: A switch or a ledger file here before task 7.1 fails a test

- **WHEN** task 7.1 of `add-pr-cost-calculator` is not ticked, and this repository tracks `.pr-cost.json` or a file under `.pr-cost/` at its root, whatever the case of their letters, since a file system that ignores case opens such a file by those names
- **THEN** a test fails and names the file

#### Scenario: A switch and ledger files here after task 7.1 pass

- **WHEN** task 7.1 of `add-pr-cost-calculator` is ticked, and this repository tracks `.pr-cost.json` and files under `.pr-cost/` at its root
- **THEN** that test passes them

#### Scenario: A switch or a ledger file below the root passes before task 7.1

- **WHEN** task 7.1 of `add-pr-cost-calculator` is not ticked, and this repository tracks `.pr-cost.json` or files under `.pr-cost/` only in a folder below its root, as a golden session in `tests/golden/` can
- **THEN** that test passes them

### Requirement: This repository holds no reusable workflow before the one that refuses other events

No tracked file under `.github/workflows/` SHALL declare `workflow_call` while task 4.3 of `add-pr-cost-calculator`, which adds the reusable workflow that refuses every event but a push to the default branch, is not ticked in that change's `tasks.md`, active or archived, so that no workflow here can be called from another repository before that guard exists. A test SHALL fail and name the file otherwise.

#### Scenario: A reusable workflow here before task 4.3 fails a test

- **WHEN** task 4.3 of `add-pr-cost-calculator` is not ticked, and a tracked file under `.github/workflows/` declares `workflow_call`
- **THEN** a test fails and names the file

#### Scenario: A reusable workflow after task 4.3 passes this test

- **WHEN** task 4.3 of `add-pr-cost-calculator` is ticked, and the reusable workflow that it adds declares `workflow_call`
- **THEN** that test passes it, and the checks of task 4.3 hold its events and permissions

### Requirement: Each change's tasks are read as GitHub shows them

Each change's `tasks.md`, active or archived, SHALL give each task once, on a line that opens with `- [ ]` or `- [x]`, a space, its number and a space, and SHALL hold no other line with a checkbox, no fenced code, front matter, byte-order mark or carriage return without a line feed after it, no `<` before a letter, `/`, `!` or `?` outside inline code on its line, and no line that opens with `$$` after any spaces, so that the checks read what GitHub shows the owner. Tests SHALL fail otherwise.

#### Scenario: A task list read as GitHub shows it passes

- **WHEN** each line of a change's `tasks.md` that holds a checkbox is a task as the checks read it, no task is given twice, and the file holds none of the text that GitHub does not show in a task list
- **THEN** the test passes it

#### Scenario: A checkbox that the checks do not read as a task fails a test

- **WHEN** a line of a change's `tasks.md` holds a checkbox, `[ ]`, `[x]` or `[X]`, and is not a task as the checks read it, such as one indented, given with another bullet, with two spaces or a tab after its box, with its number in bold or followed by a colon, or numbered in three parts or in digits other than 0 to 9
- **THEN** a test fails and names the file and the line

#### Scenario: Text that GitHub does not show in a task list fails a test

- **WHEN** a change's `tasks.md` holds a `<` before a letter, `/`, `!` or `?`, at the start of a line or after other text, that is not in inline code that opens and closes on its line, with which Markdown starts HTML, such as a comment, that can hide the lines after it; fenced code, in which GitHub shows a tick as code; a line that opens with `$$` after any spaces, with which GitHub starts a math block; front matter, which a first line of `---` opens; a byte-order mark; or a carriage return without a line feed after it, which Markdown reads as the end of a line where the checks read none
- **THEN** a test fails and names the file and the line

#### Scenario: A task given twice fails a test

- **WHEN** a change's `tasks.md` gives one task number on two lines, ticked or not
- **THEN** a test fails and names the file, the task and both lines

### Requirement: The documentation says which agents an opt-in records

The README's section on the opt-in and the opt-in's feature page SHALL name each agent that the release records, and say that one opt-in also records each agent that a later release adds, with no further step, and that no opt-in leaves one agent out, so that a person who does not want an added agent recorded turns capture off where they use it. Tests SHALL fail otherwise.

#### Scenario: The opt-in's pages say which agents an opt-in records

- **WHEN** the README's section on the opt-in and the opt-in's feature page are read
- **THEN** each names each agent that the surface manifest says the release records, and says that one opt-in also records each agent that a later release adds, with no further step, and that no opt-in leaves one agent out, so that a person who does not want an added agent recorded turns capture off where they use it

#### Scenario: An opt-in's page that does not say which agents it records fails a test

- **WHEN** the README's section on the opt-in or the opt-in's feature page leaves out an agent that the surface manifest says the release records, says that it records an agent that the manifest does not name, or leaves out that one opt-in also records each agent that a later release adds, with no further step, that no opt-in leaves one agent out, or that a person who does not want an added agent recorded turns capture off where they use it
- **THEN** a test fails and names the page and what is missing

### Requirement: Each ledger format that a release wrote keeps its golden figures

For each ledger format that a release's capture step wrote, the golden set SHALL keep sessions whose entries are as that release wrote them, with the figures that the report must give for them, for as long as the report reads that format. Tests SHALL fail when the report gives another figure for them.

#### Scenario: An earlier release's entries give their hand-worked figures

- **WHEN** the report reads a golden session's entries in a ledger format that an earlier release's capture step wrote
- **THEN** it gives the figures worked out by hand for them, or a test fails and names the session, the format and the figure

#### Scenario: A format that the report reads keeps a golden session

- **WHEN** a pull request removes the last golden session of a ledger format that a release wrote and the report still reads
- **THEN** a test fails and names the format

### Requirement: Nothing here registers the walking skeleton

No tracked file under `.claude/`, `.claude-plugin/` or `.github/` SHALL hold the word `skeleton`, whatever the case of its letters, so that no setting, hook script, marketplace or workflow here registers, installs or runs the walking skeleton, whatever way it names `skeleton/`. A test SHALL fail and name the file otherwise.

#### Scenario: A file that names the skeleton where it could register it fails a test

- **WHEN** a tracked file under `.claude/`, `.claude-plugin/` or `.github/`, such as a settings file, the session-start hook script, a marketplace file or a workflow, holds `skeleton` in any case, as `./skeleton`, `skeleton/` or `Skeleton`
- **THEN** a test fails and names the file

#### Scenario: The skeleton's own files pass

- **WHEN** only files outside `.claude/`, `.claude-plugin/` and `.github/` name `skeleton/`
- **THEN** that test passes

### Requirement: The walking skeleton records only with its own switch and the opt-in

The walking skeleton's capture SHALL record a call only for a repository whose top-level `.pr-cost.json` holds `enabled` and `walking_skeleton` both `true`, while git gives its own opt-in, `pr-cost-skeleton.capture`, never the tool's, as `true` from the person's global files alone, read without the session's git variables or `XDG_CONFIG_HOME`, never a repository's own; and SHALL keep a call only when its line's working directory lies in that repository's working tree. Tests SHALL drive each way.

#### Scenario: A switch without the skeleton's key records nothing

- **WHEN** the skeleton's capture runs in a repository whose `.pr-cost.json` holds `enabled` set to `true` and no `walking_skeleton` set to `true`, and the person has opted in
- **THEN** it writes no store, stages no ledger file and exits with success

#### Scenario: No switch means the skeleton records nothing

- **WHEN** the skeleton's capture runs where no repository holds a `.pr-cost.json`, or where one's `enabled` is not `true`, and the person has opted in
- **THEN** it writes no store, stages no ledger file and exits with success

#### Scenario: No opt-in means the skeleton records nothing

- **WHEN** the skeleton's switch is on, and git, reading the person's global configuration files, does not give `pr-cost-skeleton.capture` as `true`, though the repository's own configuration does, or the session's `GIT_CONFIG_` or `XDG_CONFIG_HOME` variables do, or though the tool's own opt-in, `pr-cost.capture`, is `true`
- **THEN** it writes no store, stages no ledger file and exits with success

#### Scenario: A call made in another repository is not recorded

- **WHEN** the switch and the opt-in are on, and the transcript holds a call whose line gives a working directory outside the repository's working tree, or in another repository inside it, or none
- **THEN** no ledger file that the skeleton stages holds that call

### Requirement: The walking skeleton never stalls or steers the agent

Each hook command of the walking skeleton's plugin SHALL run its capture script with `python3 -I` and end in `; exit 0`, and the script SHALL print nothing on standard output, whatever it meets, so that no run of it blocks a command, sends the agent back to work or gives Claude text. A test SHALL fail otherwise.

#### Scenario: A missing or failing capture script still exits with success

- **WHEN** a hook command of the skeleton's plugin runs while its capture script is missing, or while the script raises an error
- **THEN** the command exits with success and prints nothing on standard output

#### Scenario: A hook command without its guard fails a test

- **WHEN** a hook command in the skeleton's plugin does not run `python3 -I` or does not end in `; exit 0`
- **THEN** a test fails and names the hook

### Requirement: The walking skeleton stages only for a commit it recognises

The walking skeleton SHALL stage a ledger file only before a command whose parts, joined by two ampersands, are `cd` to a written path or `git add` with written paths, then a `git commit` with only `-m` and a quoted message, which may repeat, `-a` or `-q`, in the repository of each `git add`, each git with at most one written `-C`, and only when the commit would commit something without the file; and SHALL take back a file that the command did not commit, its calls waiting.

#### Scenario: A recognised commit after calls holds one ledger file

- **WHEN** the switch and the opt-in are on, calls made in the repository wait, and the agent runs `cd` to the clone, `git add` with a path and `git commit -m` with a message, joined by two ampersands
- **THEN** the commit holds the agent's change and one ledger file with those calls' counts by model, and no text of the transcript but the model's name

#### Scenario: A commit in another form gets no ledger file

- **WHEN** the agent commits with any other command, such as one with `--amend`, a pathspec, a pipe or a semicolon
- **THEN** the skeleton stages nothing, and the calls wait

#### Scenario: A commit with nothing to commit stays empty

- **WHEN** the agent runs a recognised `git commit` with no `git add` before it, no `-a`, and nothing staged
- **THEN** the skeleton stages nothing, and the commit fails as it would without it

#### Scenario: A commit in another repository than its adds gets no ledger file

- **WHEN** the agent runs `git add` in one repository and, in the same command, `git commit` in another
- **THEN** the skeleton stages nothing, and the calls wait

#### Scenario: A commit with repeated messages gets its ledger file

- **WHEN** the agent's recognised commit gives `-m` with a quoted message more than once, as for trailer lines
- **THEN** the commit holds one ledger file

#### Scenario: A file that a commit did not take is taken back

- **WHEN** the skeleton staged a ledger file and the command then failed, or succeeded without committing the file
- **THEN** the file is gone from the index and the working tree, and its calls wait for a later commit

### Requirement: The kept transcript shape holds no values

Each transcript shape kept from the walking skeleton's run, a tracked file under `tests/` whose name begins with `transcript-shape`, SHALL hold only field names at a line's top level that the recorder's list names, in its `message` and in `message.usage`, each with its JSON type, and every other object and array as its type alone; each name of letters, digits and underscores, at most 40 long and not of an identifier's form. A test SHALL fail and name the entry otherwise.

#### Scenario: A value in the kept shape fails a test

- **WHEN** an entry of a kept shape gives anything but a field path and a JSON type name, or a name with a character other than a letter, a digit or an underscore, or longer than 40 characters
- **THEN** a test fails and names the file and the entry

#### Scenario: A name below another object fails a test

- **WHEN** an entry of a kept shape gives a field name below an object other than the line, its `message` object and `message.usage`, as below `message.content`, a tool's input, a tool's result or a map keyed by identifiers
- **THEN** a test fails and names the file and the entry

#### Scenario: A top-level name outside the recorder's list fails a test

- **WHEN** an entry of a kept shape gives a name at a line's top level that the list shared by the shape recorder and its check does not name
- **THEN** a test fails and names the file and the entry

#### Scenario: A name of an identifier's form fails a test

- **WHEN** an entry of a kept shape gives a name that is a lower-case prefix, an underscore and a token of 8 or more letters and digits that holds a digit or an upper-case letter, so that a field name such as `stop_sequence` is not taken for one
- **THEN** a test fails and names the file and the entry

#### Scenario: A shape of names and types passes

- **WHEN** every entry of each kept shape gives a path of names at those levels only, and a JSON type name
- **THEN** that test passes

#### Scenario: No kept shape after the run fails a test

- **WHEN** task 1.36 of `add-pr-cost-calculator` is ticked, and no tracked file under `tests/` has a name that begins with `transcript-shape`
- **THEN** a test fails and says that the shape is missing

### Requirement: The skeleton's workflow can do no more than post its comment

The skeleton's workflow, `skeleton/workflow.yml`, SHALL run only on a push to `main`, ask only to read contents and write pull requests, use no action but `actions/checkout` pinned to a full commit with `persist-credentials: false`, fetch no commit but the push's `before` and `after`, read no secret, put no `${{` inside a `run:`, and set `timeout-minutes`. A test SHALL fail and name what differs otherwise.

#### Scenario: Another event, permission or action in the skeleton's workflow fails a test

- **WHEN** `skeleton/workflow.yml` runs on an event other than a push to `main`, asks for a permission other than reading contents and writing pull requests, or uses an action other than `actions/checkout` or one that a full commit does not pin
- **THEN** a test fails and names what differs

#### Scenario: A secret, a kept credential, an expression in a command or no time limit fails a test

- **WHEN** `skeleton/workflow.yml` reads a secret, checks out without `persist-credentials: false`, puts `${{` inside a `run:`, fetches a ref other than the push's `before` and `after`, or sets no `timeout-minutes`
- **THEN** a test fails and names what differs

#### Scenario: The skeleton's workflow as designed passes

- **WHEN** `skeleton/workflow.yml` runs only on a push to `main`, with those two permissions, `actions/checkout` alone pinned to a full commit without kept credentials, the push's two commits fetched by SHA, no secret, no expression in a command and a time limit
- **THEN** that test passes

### Requirement: The skeleton's report counts one merged pull request's calls once, at a test price

Only when GitHub's API gives exactly one merged pull request for a push and its `before` is not all zeros, the skeleton's report SHALL read the ledger files that the push added, count each call's key once, sum each model's tokens at the test price that `skeleton/` holds, and write the figure, saying that it is at a test price and not a real cost, to the job summary and as one comment; otherwise it SHALL post no comment and say why in the job summary.

#### Scenario: One call in two ledger files is counted once

- **WHEN** two ledger files that the push added hold the same call's key
- **THEN** the report counts that call once

#### Scenario: A merge, a squash and a rebase give the figure of the files that the push added

- **WHEN** a pull request is merged by a merge commit, by squash, or by rebase of two commits that each add a ledger file
- **THEN** the report reads every ledger file that the push added and none that the default branch held before it

#### Scenario: A push with no single merged pull request posts no comment

- **WHEN** the push's `before` is all zeros, or GitHub's API gives no merged pull request for `after`, or more than one
- **THEN** the report posts no comment, and its job summary says why

#### Scenario: The comment says that its figure is not a real cost

- **WHEN** the report posts its figure
- **THEN** the comment and the job summary say that it is at a test price and is not a real cost

### Requirement: The walking skeleton says what it is

Each file under `skeleton/` that can hold a comment SHALL open with one that says it is the walking skeleton and not the tool or a release, the plugin's manifest SHALL say so in its `description`, and while `skeleton/` exists the README's status SHALL name it as the walking skeleton and say that it is not the tool. A test SHALL fail and name the file otherwise.

#### Scenario: A skeleton file that does not say what it is fails a test

- **WHEN** a Python or YAML file under `skeleton/` does not open with a comment that says that it is the walking skeleton and not the tool, or the plugin's manifest's `description` does not say so
- **THEN** a test fails and names the file

#### Scenario: A README silent on the skeleton fails a test

- **WHEN** `skeleton/` exists, and the README's status does not name it as the walking skeleton
- **THEN** a test fails

### Requirement: The skeleton's plugin declares nothing but its command hooks

The walking skeleton's plugin manifest SHALL hold only its name, `pr-cost-skeleton`, a version and a description, and its hooks SHALL all be command hooks; its zip SHALL hold only the manifest, the hooks file and the capture script, and SHALL be built the same, byte for byte, from the same commit. A test SHALL fail and name what differs otherwise.

#### Scenario: A plugin that declares more fails a test

- **WHEN** the skeleton's manifest holds another key, as one naming an MCP server, or a hook of another type than a command, or the zip holds another file, as an `.mcp.json`
- **THEN** a test fails and names it

#### Scenario: Two builds of one commit give the same zip

- **WHEN** the skeleton's zip is built twice from one commit
- **THEN** the two zips are the same, byte for byte

### Requirement: No release holds the walking skeleton

The release workflow SHALL refuse a tag whose tree holds a `skeleton/` folder, so that the build removes the walking skeleton before the first release and no adopter takes it for the tool.

#### Scenario: A tag that holds the skeleton is refused

- **WHEN** a tag's tree holds a `skeleton/` folder
- **THEN** the release workflow refuses it and names the folder

#### Scenario: A tag without the skeleton passes this check

- **WHEN** a tag's tree holds no `skeleton/` folder
- **THEN** this check of the release workflow passes it

### Requirement: Every threat is also rated as if its answer were not built

Every threat in the threat model SHALL carry, beside its ratings with its answer in place, a raw impact and a raw likelihood, each from 1 to 3 with the level's name as the threat model's method defines them, rated as if what its Answer, its Held by and any further answer cite were not built, and a raw risk that is their product. Neither raw rating SHALL be lower than its rating with the answer in place. Tests SHALL fail otherwise.

#### Scenario: A threat without its raw ratings fails CI

- **WHEN** a threat lacks a raw impact or a raw likelihood, gives either without its level's name or with another level's name, or carries a raw risk that is not their product
- **THEN** a test fails and names the threat

#### Scenario: A raw rating below the rating with the answer in place fails CI

- **WHEN** a threat's raw impact is lower than its impact, or its raw likelihood is lower than its likelihood
- **THEN** a test fails and names the threat and the rating

#### Scenario: A threat whose raw ratings equal its ratings passes

- **WHEN** a threat's answer lowers neither its impact nor its likelihood, and its raw ratings equal its ratings
- **THEN** this check passes it

### Requirement: The risk register is written from the threat model

The repository SHALL keep a risk register, `docs/risk-register.md`, that a script here writes from the threat model, the specs and the register of requirements alone, and CI SHALL fail when the page differs from what the script writes. The page SHALL open by saying that the script writes it, and that a rating with the answer in place takes the answer as built as specified, before any code is built.

#### Scenario: A register that differs from the threat model fails CI

- **WHEN** a rating, a band, a title or a row of the committed register differs from what the script writes, or the register leaves out a threat or lists one that the threat model does not hold
- **THEN** a test fails and names the threat, or the line, that differs

#### Scenario: A scenario that no requirement holds stops the script

- **WHEN** a threat's Held by cites a scenario that the specs and the register of requirements cannot place under a requirement
- **THEN** the script writes nothing, fails and names the threat and the scenario

#### Scenario: A symbolic link on the way to a file of the register stops the script

- **WHEN** the threat model, the register of requirements or the page, or a folder on the way to one of them, is a symbolic link
- **THEN** the script reads and writes nothing through it, fails and names the file

#### Scenario: The page says what its ratings take as built

- **WHEN** the script writes the register
- **THEN** its opening says that the script writes it from the threat model, that it is not edited by hand, and that each rating with the answer in place takes the answer as built as specified, until the review of what was built rates it again

### Requirement: The risk register holds no hidden text

The risk register SHALL hold to the rule that "The roadmap, the backlog and the feature pages' roadmap sections hold no hidden text" gives the roadmap, but for the `|` of its tables, each row of which holds as many cells as its header, and SHALL link only this repository's own files. The script SHALL write nothing and fail on a threat's title that holds a character that the rule forbids. Tests SHALL fail otherwise.

#### Scenario: Text that GitHub hides in the register fails a test

- **WHEN** the register holds, outside its tables' cell separators, a character or a form that the roadmap's rule forbids, a table row whose cells differ in number from its header's, or a link to anything but a file of this repository
- **THEN** a test fails and names the line

#### Scenario: A title that the rule forbids stops the script

- **WHEN** a threat's title holds a `|`, a `<`, a `&`, a backslash or a character that is not printable ASCII
- **THEN** the script writes nothing, fails and names the threat

### Requirement: The risk register gives each risk its band

The risk register SHALL give the bands of the overall risk severity of OWASP's Risk Rating Methodology, read for each score of impact times likelihood: 1 note, 2 low, 3 and 4 medium, 6 high and 9 critical; how many threats each band holds, raw and with the answers in place; a matrix of the raw ratings and one of the ratings with the answers in place; and each high and critical risk with its further answer or its acceptance.

#### Scenario: A band follows its score

- **WHEN** the script writes a risk of 1, 2, 3, 4, 6 or 9
- **THEN** it gives it the band note, low, medium, medium, high or critical

#### Scenario: Each band's count adds up to the threats

- **WHEN** the script writes how many threats each band holds, raw and with the answers in place
- **THEN** each set of counts adds up to the number of threats in the threat model

#### Scenario: A threat in the wrong cell of a matrix fails a test

- **WHEN** the script places a threat in a cell of either matrix other than the one that its ratings name, or leaves it out of one
- **THEN** a test fails and names the threat and the matrix

### Requirement: The risk register gives a row for each threat

The risk register SHALL give a row for each threat, the highest risk with its answer in place first, then the highest raw risk, then by ID, with its ID linked to the threat, its title, its trust boundary, its kind, its raw rating and its rating with the answer in place, each with its band, what answers it by ID, and the assumptions that it rests on.

#### Scenario: A threat's row names what answers it by ID

- **WHEN** the script writes the row of a threat whose Held by cites scenarios, records, tasks and files
- **THEN** the row gives, once each and in order, the requirement that holds each scenario, each record, each task and each file, and the assumptions that the threat names

#### Scenario: The rows follow the risk

- **WHEN** two threats differ in their risk with the answer in place, or share it and differ in their raw risk
- **THEN** the one with the higher risk comes first, and threats that share both come in the order of their IDs

### Requirement: Every high or critical risk has a further answer

A threat whose risk with its answer in place is high or critical SHALL carry a further answer citing what holds it beyond its Held by, or an agreed backlog item whose What done looks like names the threat; or, for a high risk only, an acceptance citing an owner's record that lists the threat. A further answer that cites an item SHALL change only with that item. Neither line, on any threat, SHALL hold text that the roadmap's rule forbids. Tests SHALL fail otherwise.

#### Scenario: A high or critical risk with neither a further answer nor an acceptance fails CI

- **WHEN** a threat whose risk with its answer in place is 6 or 9 carries neither a further answer nor an acceptance
- **THEN** a test fails and names the threat

#### Scenario: A further answer that adds nothing fails CI

- **WHEN** a further answer cites nothing that resolves, nothing that the threat's Held by does not already cite, or a backlog item that the base, or the tag in a release's tests, or the tree checked does not give as `Planned` or `In progress`, or whose What done looks like does not name the threat by its ID
- **THEN** a test fails and names the threat and the citation

#### Scenario: A further answer rewritten while its item stands fails CI

- **WHEN** compared with the base, a pull request adds or changes a further answer that cites a backlog item, and leaves that item's text as the base holds it
- **THEN** a test fails and names the threat and the item

#### Scenario: An acceptance that the owner did not give for the threat fails CI

- **WHEN** an acceptance cites no record, a closed record, a record whose decider is not the owner, or a record whose Threats do not list the threat
- **THEN** a test fails and names the threat and the citation

#### Scenario: An accepted critical risk fails CI

- **WHEN** a threat whose risk with its answer in place is 9 carries an acceptance
- **THEN** a test fails and names the threat

#### Scenario: Hidden text in a further answer or an acceptance fails CI

- **WHEN** a further answer or an acceptance, on a threat of any risk, holds a character or a form that the roadmap's rule forbids, a link with a title or a web address among them
- **THEN** a test fails and names the threat

### Requirement: A high or critical risk is lowered only with what lowers it

Compared with the base that the records' check uses, a pull request that rates a threat that the base gives a high or critical risk lower, raw or with its answer in place, SHALL also change that threat's What could happen, Answer, Held by or further answer, so that the reason shows in the same diff; a further answer removed, or one that is a plan (DR-255), is no such reason. Tests SHALL fail otherwise.

#### Scenario: A rating lowered alone fails CI

- **WHEN** a pull request lowers the likelihood or the impact of a threat that the base rates 6 or 9, and changes none of its What could happen, Answer, Held by and further answer
- **THEN** a test fails and names the threat

#### Scenario: A rating lowered on a plan or on a removed further answer fails CI

- **WHEN** a pull request lowers such a rating and changes only the threat's further answer, by removing it or to one that cites a backlog item
- **THEN** a test fails and names the threat

#### Scenario: A rating lowered with its reason passes

- **WHEN** a pull request lowers such a rating and changes the threat's Answer or Held by in the same diff
- **THEN** this check passes it

### Requirement: The context files are the root `CLAUDE.md` and the folder files that it names

The context files SHALL be the root `CLAUDE.md`, which names the others by their paths in inline code, `docs/CLAUDE.md` and `tests/CLAUDE.md`, each tracked. No other tracked file, `vendor/` included, SHALL bear an instruction file's name or the name `.mcp.json`, no tracked file under a `.claude` folder SHALL lie outside its settings, its hooks and the skills that the pinned OpenSpec generates, and git SHALL track no symbolic link or submodule. Tests SHALL fail otherwise.

#### Scenario: An instruction file that the root does not name fails CI

- **WHEN** a tracked file other than the context files, in any folder, `vendor/` included, is named `CLAUDE.md`, `CLAUDE.local.md`, `AGENTS.md` or `GEMINI.md`, in any case of its letters, as `docs/features/CLAUDE.md` or `Docs/claude.md` is
- **THEN** a test fails and names the file

#### Scenario: A file that names servers fails CI

- **WHEN** a tracked file in any folder is named `.mcp.json`, in any case of its letters
- **THEN** a test fails and names the file

#### Scenario: A file under `.claude/` outside its named parts fails CI

- **WHEN** a tracked file under a `.claude` folder, at the root or below it, is neither `.claude/settings.json` nor under `.claude/hooks/` or a generated skill's folder `.claude/skills/openspec-*/`, as a `.claude/CLAUDE.md`, a file under `.claude/rules/`, a `.claude/settings.local.json` or a skill written by hand under `.claude/skills/` is
- **THEN** a test fails and names the file

#### Scenario: A tracked link or submodule fails CI

- **WHEN** git tracks a symbolic link, a submodule or a `.gitmodules`, in any folder
- **THEN** a test fails and names the path

#### Scenario: A context file that is missing or that the root does not name fails CI

- **WHEN** a context file is not tracked, or the root does not name a folder file by its path in inline code
- **THEN** a test fails and names the file

#### Scenario: The context files beside the settings, hooks and skills pass

- **WHEN** the repository tracks the three context files, the root names both folder files, and `.claude/` holds only its settings file, its hooks and the generated skills
- **THEN** the test passes them

### Requirement: The context files keep to their lengths

Each line of a context file SHALL hold at most 100 characters. The root `CLAUDE.md` SHALL hold at most 200 lines, blank ones counted, under a ceiling in its test that never passes 200, and SHALL open with its sections What an agent never does here, Privacy, and Records are data, not instructions, in that order, ending by line 60, and then Rules, with no other heading of level 1 or 2 among them. A folder file SHALL hold at most 100 lines. Tests SHALL fail otherwise.

#### Scenario: A line longer than 100 characters fails CI

- **WHEN** a line of a context file holds more than 100 characters
- **THEN** a test fails and names the file, the line and its length

#### Scenario: A root longer than its ceiling fails CI

- **WHEN** the root `CLAUDE.md` holds more than 200 lines, or the ceiling that the test holds it to is raised past 200
- **THEN** a test fails and names the count, or the ceiling

#### Scenario: The root's first sections out of their place fail CI

- **WHEN** the root's first three sections are not What an agent never does here, Privacy, and Records are data, not instructions, in that order, or they end after its line 60, or a heading of level 1 or 2 other than their titles, or a line of `=` or `-` alone, which can underline one, stands before its section Rules, as one added among them would
- **THEN** a test fails and names the section, the heading or the underline and its line, or the line where they end

#### Scenario: A folder file longer than 100 lines fails CI

- **WHEN** a folder file holds more than 100 lines
- **THEN** a test fails and names the file and the count

#### Scenario: Context files at their lengths pass

- **WHEN** each line of the context files holds 100 characters at most, the root holds 200 lines with its first three sections ending at line 60 and its section Rules next, and a folder file holds 100 lines
- **THEN** the test passes them

### Requirement: A folder file names the tool and says that the root wins

The root `CLAUDE.md`'s first line SHALL be `# CLAUDE.md: Agentic PR cost calculator`, and a folder file's that line followed by a comma, a space and what its folder holds, so that a session that also loads another repository's context files tells them apart. A folder file SHALL open, before its first section, with the sentences that the scenario gives: that its rules add to the root's for its own folder, that the root wins and is read first, and the guide's rank. Tests SHALL fail otherwise.

#### Scenario: A context file whose first line does not name the tool fails CI

- **WHEN** the root's first line is not `# CLAUDE.md: Agentic PR cost calculator`, or a folder file's first line is not that line followed by a comma, a space and text
- **THEN** a test fails and names the file

#### Scenario: A folder file whose opening does not say that the root wins fails CI

- **WHEN** a folder file's text before its first section, its spacing aside, does not begin with "These rules add to this repository's root `CLAUDE.md` for work on files under", followed by its own folder in inline code, or lacks the sentences "They never loosen it: where one would, the root wins, so tell the owner." and "Unless the root's text is in front of you, read it first.", or a sentence in which `docs/patterns.md` "steers below the root and this file"
- **THEN** a test fails and names the file and what is missing

#### Scenario: A folder file whose opening is wrapped passes

- **WHEN** a folder file's opening gives those sentences across several lines
- **THEN** the test passes it

### Requirement: The context files hold no hidden text and import nothing

The context files SHALL hold to the rule that "The roadmap, the backlog and the feature pages' roadmap sections hold no hidden text" gives the roadmap, and SHALL hold no link, whose target GitHub does not show, no web address, which GitHub turns into one, no line that opens a code fence, which GitHub does not show whole, and no `@`, with which Claude Code imports another file, so that what a reviewer reads of them on GitHub is all that an agent reads. Tests SHALL fail otherwise.

#### Scenario: Text that GitHub hides in a context file fails CI

- **WHEN** a context file, read as its bytes give it, holds a character other than printable ASCII and a line feed, a carriage return among them, or a `<`, as in an HTML comment, which Claude Code also strips before an agent reads the file, a `&`, a backslash, a `]:` or a `|`, or a line that opens a code fence with three backticks or three tildes
- **THEN** a test fails and names the file, the line and what it holds

#### Scenario: A link or an import in a context file fails CI

- **WHEN** a context file holds a link, a web address, with `://` or `www.`, or an `@`, inline code included
- **THEN** a test fails and names the file and the line

### Requirement: Claude Code's settings here, and the marketplace that they name, hold only what their tests list

`.claude/settings.json` SHALL hold only the keys that its test lists, at every level, each with the value that the test gives, and the marketplace file that it names, `.claude-plugin/marketplace.json`, only what its test lists until task 6.7 of `add-pr-cost-calculator` moves it, so that a setting that keeps the context files from loading, or a hook, marketplace or plugin that a test does not list, fails until the test changes with it, in a diff that the owner reads. Tests SHALL fail otherwise.

#### Scenario: A setting that the test does not list fails CI

- **WHEN** `.claude/settings.json` holds, at any level, a key that the test does not list, such as `claudeMdExcludes`, `permissions`, a variable in its `env` or a hook for another event, or lacks one that the test lists
- **THEN** a test fails and names the key's path

#### Scenario: A value that the test does not give fails CI

- **WHEN** a key of `.claude/settings.json` holds a value other than the one that the test gives, such as another hook command, another marketplace folder or a plugin turned off
- **THEN** a test fails and names the key's path and the value

#### Scenario: A marketplace entry that the test does not list fails CI

- **WHEN** the marketplace file that `.claude/settings.json` names holds, at any level, a key, a value or an entry that its test does not list, such as a plugin taken from another folder
- **THEN** a test fails and names the key's path and the value

#### Scenario: The settings that the test lists pass

- **WHEN** `.claude/settings.json` holds the keys and values that the test lists and no other, and the marketplace file that it names holds what its test lists
- **THEN** the test passes it

### Requirement: Git ignores a personal instruction file and the worktree folders

The repository's ignore files SHALL make git ignore `CLAUDE.local.md` in any folder, and the folders `.worktrees` and `.claude/worktrees`, where another branch's worktree is made, before they exist and with every file under them, SHALL make it ignore no context file and SHALL take none of these back, with no other file of ignore rules read, so that neither a personal instruction file nor another branch's files reach a commit by mistake. Tests SHALL fail otherwise.

#### Scenario: A personal instruction file or a worktree that git would add fails CI

- **WHEN**, with only the repository's ignore files read, git does not ignore `CLAUDE.local.md` at the root or in a folder that holds a tracked file, the folder `.worktrees` or `.claude/worktrees` before it exists, or a file of any name under one
- **THEN** a test fails and names the path

#### Scenario: An ignore rule that takes a personal file or a worktree back fails CI

- **WHEN** an ignore file of the repository holds a rule that starts with `!` and names `CLAUDE.local.md` or a worktree folder
- **THEN** a test fails and names the file and the rule

#### Scenario: An ignored context file fails CI

- **WHEN** the repository's ignore files make git ignore a context file
- **THEN** a test fails and names the file

### Requirement: The README and `CONTRIBUTING.md` say where a session starts

The README's section on working on this repository and `CONTRIBUTING.md` SHALL each give the sentence that the scenario gives, so that a Claude Code session on this repository starts where it loads the root `CLAUDE.md` and the repository's settings from the start, rather than in a folder above the clone. Tests SHALL fail otherwise.

#### Scenario: A page that does not say where a session starts fails CI

- **WHEN** the README's section on working on this repository, or `CONTRIBUTING.md`, does not give, whitespace aside, the sentence "Start a Claude Code session for this repository in the clone's own folder, so that it loads this repository's `CLAUDE.md` and settings from the start."
- **THEN** a test fails and names the file

### Requirement: Each record gives its boundary and how hard it is to reverse

Each record SHALL give, right after its type, its boundary, as `inside`, `incoming` or `outgoing`, and its reversibility, as `reversible`, `reversible with work` or `one-way door`, and the index SHALL give both, in columns of their own right after the type. A record from DR-268 on SHALL open its section on what reversing it would change with "How hard it is to reverse: " and its reversibility, which MAY become `[removed]` once the record is closed. Tests SHALL fail otherwise.

#### Scenario: A record with its boundary and its reversibility passes

- **WHEN** a record gives each of the two fields once, right after its type, with a value from its list, and the index gives the same values in its two columns
- **THEN** the test passes it

#### Scenario: A record without its boundary or its reversibility fails CI

- **WHEN** a record lacks either field, gives one twice or out of its place, or gives a value outside its list
- **THEN** a test fails and names the record

#### Scenario: An index without the two columns fails CI

- **WHEN** the index's table lacks the column of either field, holds it out of its place, or gives a value that the record does not
- **THEN** a test fails and names the record

#### Scenario: A reversibility sentence that disagrees with its field fails CI

- **WHEN** a record from DR-268 on does not open its section on what reversing it would change with "How hard it is to reverse: " followed by its reversibility and a full stop
- **THEN** a test fails and names the record

### Requirement: A record's decider gives no date before the owner's first brief

Each date that a record's decider gives SHALL be no earlier than 2026-10-17, the day of the owner's first brief for the tool, before the repository's first commit, and no later than the day the tests run. Tests SHALL fail otherwise.

#### Scenario: A decider's date before the first brief fails CI

- **WHEN** a record's decider gives a date earlier than 2026-10-17
- **THEN** a test fails and names the record and the date

#### Scenario: A decider's date on the day of the first brief passes

- **WHEN** a record's decider gives 2026-10-17
- **THEN** the test passes it

### Requirement: The files that this repository writes hold only printable ASCII

Every tracked file that this repository writes SHALL hold only printable ASCII and line feeds, and declare no encoding but UTF-8 where Python reads it, and every tracked path only printable ASCII but the space, unlike any other in more than case, so that no character that cannot be seen, reorders text or passes for an ASCII one reaches code, pages or names. Others write the files under `vendor/superpowers/` but its root lock, and under `.claude/skills/openspec-*/`. Tests SHALL fail otherwise.

#### Scenario: A character beyond printable ASCII in a file that this repository writes fails CI

- **WHEN** a tracked file that this repository writes holds a character other than printable ASCII and a line feed, such as a tab, a carriage return, a byte-order mark, a zero-width space, a direction-changing character, a non-breaking space, an em dash, an arrow or an accented letter
- **THEN** a test fails and names the file, the line, the column and the character by its code point and its name, never by the character itself

#### Scenario: A path beyond printable ASCII fails CI

- **WHEN** a tracked path, of any file, holds a character other than printable ASCII, or a space
- **THEN** a test fails and names the path, with each such character by its code point, never by the character itself

#### Scenario: Two tracked paths that differ only in case fail CI

- **WHEN** two tracked paths are the same once the case of their letters is set aside, such as `.claude-plugin/Marketplace.json` beside `.claude-plugin/marketplace.json`, which a file system that ignores case keeps as one file
- **THEN** a test fails and names both paths

#### Scenario: A Python file that declares an encoding other than UTF-8 fails CI

- **WHEN** a tracked file that this repository writes and that Python reads as source, by the extension `.py` or `.pyi` or by a first line that runs Python, declares on its first or second line an encoding other than UTF-8, such as `# -*- coding: utf-7 -*-` or `# coding: unicode_escape`, with which a line that reads as a comment can run as code
- **THEN** a test fails and names the file and the encoding

#### Scenario: Printable ASCII and line feeds pass

- **WHEN** every tracked file that this repository writes holds only printable ASCII and line feeds, and declares no encoding but UTF-8 where Python reads it as source, and every tracked path holds only printable ASCII other than the space, unlike every other path in more than case
- **THEN** the test passes them

### Requirement: The pages that this repository writes hold no text that GitHub hides

Each Markdown file that this repository writes SHALL hold, outside code, no HTML comment or other raw HTML, no character reference, no link or footnote definition, no image, no `$` and no table row with more cells than its header, and draw no block but Mermaid, with no entity code or comment in it, so that what GitHub shows is what checks and agents read. A template under `.github/` may hold comments, and the README the elements that fold its sections of detail. Tests SHALL fail otherwise.

#### Scenario: Text that GitHub hides in a page fails CI

- **WHEN** a Markdown file that this repository writes holds, outside inline code and fenced blocks, an HTML comment, an element other than those with which the README folds its sections of detail, a declaration or a processing instruction, a character reference such as `&#x202E;` or `&nbsp;`, a link or footnote definition, an image, a `$`, with which GitHub starts a mathematical expression, or a table row with more cells than its header
- **THEN** a test fails and names the file, the line and what it holds

#### Scenario: A drawn block that can hide text fails CI

- **WHEN** a Markdown file that this repository writes holds a fenced block that GitHub draws other than Mermaid, such as `math` or `geojson`, or a Mermaid block that holds an entity code, such as `#8238;`, or a comment, which starts with `%%`
- **THEN** a test fails and names the file, the line and what it holds

#### Scenario: A template's comment passes

- **WHEN** a template under `.github/`, such as the pull request template, holds an HTML comment
- **THEN** the test passes it

#### Scenario: The README's folds pass

- **WHEN** the README folds its sections of detail in `<details>` and `<summary>` elements without attributes, as "The README folds the detail that follows its short start" gives them
- **THEN** the test passes those elements, and fails on such an element in any other page

#### Scenario: Those marks in code pass

- **WHEN** a page gives those marks inside inline code, or inside a fenced block that GitHub shows as code
- **THEN** the test passes them

### Requirement: The test of characters reads every file as git holds it, and prints only printable ASCII

The test of characters SHALL read each tracked file as git's index holds it, and also as the working tree holds it wherever that holds a file, and a link as the path that it holds, never followed, and SHALL print only printable ASCII and line feeds, so that neither an attribute that rewrites a checkout nor an edit not yet staged hides a character from it, and no failure of its own shows a character that it refuses. Tests SHALL fail otherwise.

#### Scenario: A character that only git's index holds fails CI

- **WHEN** git's index holds a character beyond printable ASCII in a file that this repository writes, while the working tree holds that file in printable ASCII alone, as an attribute such as `working-tree-encoding=UTF-7` makes a checkout write it
- **THEN** a test fails and names the file, the line, the column and the character by its code point and its name

#### Scenario: An edit not yet staged is read

- **WHEN** the working tree holds a character beyond printable ASCII in a tracked file that this repository writes, while git's index holds that file in printable ASCII alone
- **THEN** a test fails and names the file, the line, the column and the character by its code point and its name

#### Scenario: A file that the test cannot read as text fails CI

- **WHEN** a tracked file that no exception lets in holds bytes that are not UTF-8, in git's index or in the working tree, or a tracked path is neither a file nor a link, such as a submodule
- **THEN** a test fails and names the path

#### Scenario: A link is read as the path that it holds

- **WHEN** a tracked link holds a path beyond printable ASCII, or names a file outside the repository that holds such a character
- **THEN** the test fails on the first, names the link and its path's characters by their code points, and reads nothing through either

#### Scenario: Everything that the test of characters prints is printable ASCII

- **WHEN** the test fails on each defect that its scenarios plant, among them a path that holds a line feed, a carriage return, an escape character, a tag character or a variation selector, a link whose path holds them, and a character to which Python's Unicode database gives no name
- **THEN** everything that the run prints, pytest's own report included, is printable ASCII and line feeds, each path gives every other character by its code point, and a character without a name is named by its code point and a fixed phrase

#### Scenario: A check of characters that reads no file fails

- **WHEN** git lists no tracked file, or the test reads none
- **THEN** the test fails and says that it read nothing

### Requirement: The repository's attributes set nothing but line endings

The repository's attributes SHALL give a tracked file no attribute but `text` and `eol`, and each check of them SHALL read them as git's index holds them and also as the working tree holds them, and never a person's own, so that no attribute makes a checkout, an archive or GitHub's diff give other text than git holds, or folds a diff that the owner reads, and no attributes file hides from the checks by re-encoding itself. Tests SHALL fail otherwise.

#### Scenario: An attribute other than `text` and `eol` fails CI

- **WHEN** the repository's attributes give a tracked file any attribute other than `text` and `eol`, in any state, such as `working-tree-encoding`, `filter`, `ident`, `export-subst`, `export-ignore`, `binary`, `diff` or `linguist-generated`
- **THEN** a test fails and names the file and the attribute

#### Scenario: An attributes file that a checkout re-encodes is read as git holds it

- **WHEN** git's index holds a `.gitattributes` that gives itself `working-tree-encoding` and gives tracked files other attributes, while the working tree holds that file as a fresh clone writes it
- **THEN** the test of attributes, and each check that "No attribute hides the diff of a record, the README, a file that steers, the guide, the threat model, a change's tasks or what the marketplace serves, or changes the plugin's checkout" gives, fails and names each file and its attribute

#### Scenario: Line endings alone pass

- **WHEN** the repository's attributes give tracked files only `text` and `eol`, or nothing
- **THEN** the test passes them

#### Scenario: A person's own attributes are not read as the repository's

- **WHEN** a person's global attributes file gives a tracked file an attribute other than `text` and `eol`
- **THEN** the test of attributes does not read it

### Requirement: The files that others write hold no character that a reader cannot see

Each file that others write SHALL hold, as itself or by an escape, only printable ASCII, tabs, line feeds and the visible characters that its test lists for Markdown or any file, by code point and Unicode name, with variation selector 16 only right after a character listed for it, and the list SHALL give only punctuation and symbols, none that shows as blank, so that an update brings none that cannot be seen, and a visible one only once its pull request lists it. Tests SHALL fail otherwise.

#### Scenario: A character that a reader cannot see in a file that others write fails CI

- **WHEN** a file that others write holds a character that is not printable ASCII, a tab, a line feed or a listed character, such as a carriage return, a zero-width space, a right-to-left override, a byte-order mark, a non-breaking space or a tag character, or holds variation selector 16 right after a character that the list does not give for it
- **THEN** a test fails and names the file, the line, the column and the character by its code point and its name, never by the character itself

#### Scenario: A visible character that the list does not give fails CI

- **WHEN** a file that others write holds a visible character beyond printable ASCII that the test does not list, such as a Cyrillic letter that looks like a Latin one
- **THEN** a test fails, names the file, the line, the column and the character by its code point and its name, and says that the owner decides whether the list gives it, with no step for adding it

#### Scenario: A character listed for Markdown alone fails in another file

- **WHEN** a file that others write and that is not Markdown, such as a script, holds a character that the list gives for Markdown alone
- **THEN** a test fails and names the file, the line, the column and the character by its code point and its name

#### Scenario: A character written by an escape is held as the character

- **WHEN** a file that others write holds an escape that writes a character that the file may not hold, `\u` and four hexadecimal digits, `\U` and eight or `\x` and two, or a skill's front matter, read as YAML, gives a value that holds such a character, as an escape such as `\e` or `\_` writes it
- **THEN** a test fails and names the file, the line and the character by its code point and its name

#### Scenario: The characters that the list gives pass

- **WHEN** a file that others write holds only printable ASCII, tabs, line feeds and the characters that the list gives for its kind of file, with variation selector 16 only right after a character listed for it
- **THEN** the test passes it

#### Scenario: A list that gives a character that cannot be seen fails CI

- **WHEN** the test's list gives a character that is not punctuation or a symbol by its Unicode category, such as a letter, a digit or a combining mark, one that shows as blank, such as the blank Braille pattern, or a name other than the one that Unicode gives it
- **THEN** a test fails and names the entry

#### Scenario: A listed character that the oldest supported Python does not know is checked on a later one

- **WHEN** the Unicode database of the Python that runs the test assigns no character to a code point that the list gives
- **THEN** on the oldest supported Python the list's check passes over that entry, and on every later one it fails and names the entry

### Requirement: The vendored copy of Superpowers holds only what its pinned commit gives

CI SHALL compare every path under `vendor/superpowers/`, whatever its name, with the files that the sync script copies from the commit that `vendor/superpowers/UPSTREAM.lock` pins, leaving out that lock alone, by its path, so that no file there passes as upstream's unless that commit gives it as it is. Tests SHALL fail otherwise.

#### Scenario: A vendored file that the pinned commit does not give fails CI

- **WHEN** a file or folder below `vendor/superpowers/`, other than `vendor/superpowers/UPSTREAM.lock`, is not among what the pinned commit gives, whatever its name, `UPSTREAM.lock` included
- **THEN** the vendor check fails and names it

#### Scenario: A vendored file that differs from the pinned commit's fails CI

- **WHEN** a file below `vendor/superpowers/`, other than `vendor/superpowers/UPSTREAM.lock`, holds other bytes than the pinned commit gives
- **THEN** the vendor check fails and names it

#### Scenario: The vendored copy as the pinned commit gives it passes

- **WHEN** every path below `vendor/superpowers/` but its lock is what the pinned commit gives
- **THEN** the vendor check passes

### Requirement: An image, a PDF or a video is tracked only with a record that names it

A tracked file with the extension of an image, a PDF or a video SHALL be one that the test's list of exceptions gives with its object id and an accepted record whose text names its path in a code span, and the list SHALL give no other file, so that a diagram stays text, what a diff cannot show enters only with a record that the owner reviews, and a changed file needs a changed entry. The test of characters SHALL still read a listed file whose bytes are UTF-8. Tests SHALL fail otherwise.

#### Scenario: An image, a PDF or a video that no record names fails CI

- **WHEN** a tracked file has the extension of an image, a PDF or a video, such as `.png`, `.jpg`, `.gif`, `.svg`, `.webp`, `.ico`, `.pdf`, `.mp4`, `.mov` or `.webm`, in any case, and the list of exceptions does not give it with its object id and an accepted record that names its path in a code span
- **THEN** a test fails and names the file

#### Scenario: A file that the list gives with its record passes

- **WHEN** the list of exceptions gives such a file with the object id that git holds for it and an accepted record that names its path in a code span
- **THEN** the test passes it

#### Scenario: A listed file of text is still read by the test of characters

- **WHEN** the list of exceptions gives a file whose bytes are UTF-8, such as an SVG
- **THEN** the test of characters reads it as it reads any file of its writer, and fails on a character beyond what that writer may use

#### Scenario: A listed file whose bytes changed fails CI

- **WHEN** git holds a file that the list of exceptions gives with another object id than its entry gives
- **THEN** a test fails and names the file and the entry

#### Scenario: An exception out of its form fails CI

- **WHEN** the list of exceptions gives a path that git does not track, a file whose extension is not that of an image, a PDF or a video, whatever its bytes, an entry without an object id, a record that does not exist or is closed, or a record whose text does not name the path in a code span
- **THEN** a test fails and names the entry

### Requirement: Python names follow PEP 8, as ruff's naming rules check them

`pyproject.toml` SHALL select ruff's naming rules, `N`, and ignore none of them, and every Python file that this repository writes SHALL pass them when ruff runs them with no configuration, no `noqa` comment and no ignore file, so that a name in the tool's code, the scripts, the skeleton or the tests that PEP 8 does not give, such as an exception class whose name does not end in `Error`, fails CI however a setting or a comment would keep it from the rules. Tests SHALL fail otherwise.

#### Scenario: Ruff's configuration without the naming rules fails CI

- **WHEN** `pyproject.toml` selects no `N` among ruff's rules, or ignores one of them, for every file or for some
- **THEN** a test fails and names the setting

#### Scenario: A name that PEP 8 does not give fails ruff's check

- **WHEN** a Python file that `ruff check` reads with the repository's configuration names a class in lower case, a function in mixed case, or an exception class without `Error` at its end
- **THEN** `ruff check` fails and names the rule and the line

#### Scenario: A name kept from the naming rules fails CI

- **WHEN** a Python file that this repository writes gives a name that PEP 8 does not give, which a `noqa` comment, a configuration file in its folder, an ignore file, a setting of the naming rules or a folder named `vendor` keeps from `ruff check`
- **THEN** a test that runs ruff's naming rules on every such file, with no configuration, no `noqa` and no ignore file, fails and names the file, the line and the rule

#### Scenario: Names that PEP 8 gives pass ruff's check

- **WHEN** a Python file that `ruff check` reads with the repository's configuration gives only names that PEP 8 gives
- **THEN** `ruff check` passes it
