# DR-213: The README keeps its detail, folded below its short start

- **Type:** process
- **Status:** accepted
- **Decided by:** the owner, 2026-11-10
- **Requirements:** R200
- **Threats:** T145, T151
- **Replaces:** none
- **Closed by:** none

## Context

The README's short start leaves the detail to the sections that it links (DR-212). The requirements name those sections as the README's own (R159, R164, R185 to R187, R194 to R196), and 13 accepted records say in their decision that the README gives such a detail: DR-022, DR-039, DR-063, DR-065, DR-132, DR-139, DR-156, DR-182, DR-186, DR-201, DR-203, DR-207 and DR-208. Accepted records, among them DR-050 and DR-202, say that the README's section on adopting the tool gives the opt-in's detail. A record that the default branch holds changes only by being closed by a record that replaces it and restates whatever still holds (DR-121). GitHub shows the text of a `<details>` element closed, under its `<summary>`, until a reader opens it, and open from the start only with the `open` attribute, and it shows nothing of an HTML comment, which the raw file still holds (A9), while agents that set the tool up read the raw file.

## Decision

The README keeps its sections on adopting the tool, on the opt-in, on installing the plugin, on a project's cloud threads, on organizations and on turning capture off, after its short start, each with its heading shown and its text folded in a `<details>` element of its own, so that the README first shows the short start and a list of what the detail covers. The section on the opt-in sits inside the section on adopting the tool, under a heading of its own.

## Alternatives

- A setup page of its own that holds the detail, which the README links: the README would be shorter, but each of the 13 records would be closed and replaced by one that restates it with the setup page in place of the README, as would the records that say so outside their decision, and each requirement, threat's answer and task that names one of the README's sections would change, while what each of them decided stays the same.
- The detail shown in full below the short start, which keeps every word in view and makes the README long.

## Consequences

- Every requirement, record and threat's answer that says the README gives a detail still holds, the opt-in's detail within the section on adopting the tool among them, and the short start links each section by its heading (R198).
- A test fails when a section of detail shows its text outside a `<details>` element, gives that element the `open` attribute, or comes before the short start (R200).
- A test fails when the README holds text that GitHub hides, as R200 lists it, so that an agent that reads the raw file reads nothing that a reader of GitHub's page cannot open (T151).
- Folded text is still in the file, so an agent or a tool that reads the README reads all of it, and the tests of task 4.4 read each section's text whole.
- A person who opens no section relies on what the short start says (T145).

## Scope

This covers where the README's detail lives and how it shows. What the short start says is DR-212 (The README opens with a short start).

## What reversing it would change

R200 in `project-standards` would change, with its scenarios, and so would design decision 12, task 4.4, the answers of T145 and T151, assumption A9 and the feature page for `project-standards`. A setup page of its own would also close the records that say the README gives the detail, as the alternatives say.
