# DR-158: A record names other things by ID, number or path, and its change by name

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R126, R127
- **Threats:** T75
- **Replaces:** none
- **Closed by:** none

## Context

A record rests on requirements, threats, other records, its change's design decisions, the tasks that build what it decided, and files of the repository, and a record that the default branch holds can never be corrected, only closed (DR-121). A link to a path or a heading breaks when a change is archived or the design is restructured (T75). The records name tasks, design decisions and paths, and the sentences that moved out of the design into them name them as the design did.

## Decision

A record names requirements, threats and other records by ID, its change by name, and that change's design decisions and tasks by number. It may name a file by its path, in a code span. Within a record, the design, the proposal and the tasks that it names without naming a change are those of the change that added the record.

## Alternatives

- Taking task numbers, design decision numbers and paths out of every record, which would cut the sentences that moved out of the design and leave a reader unable to find what a record rests on.
- Naming the change with every task and design decision, which those moved sentences, written as the design's own, do not do.

## Consequences

- `tests/test_decisions.py` fails on a record or a design decision that does not exist, and on a parenthesis right after a record's ID that does not give that record's title, in every tracked file outside `vendor/` and `tests/`, and, in every Markdown file there, the records among them, on a requirement or a threat that is neither held nor retired and on a change or a task that does not exist (R126, R127; task 1.18). It reads a name as a change's where the words "the change" come before it, and finds a task or a design decision named without its change in any change, active or archived, so it cannot tell whether that one is the record's own (T75). No test resolves a path that a record names in a code span.
- A name resolves in an archived change too, so a record keeps its meaning once its change is archived.
- A file that is moved or renamed, and a task renumbered while its change is open, leave a record naming a path or a number that no longer points at what it meant, which no test sees, so a record describes the repository as it stood when the record was accepted (T75).

## Scope

This covers how a record names what it rests on. The characters and the links that a record may hold are DR-152 (A record is plain text and links only to other records), that requirement IDs stay held or retired is DR-106 (Requirement IDs are stable and never reused), that threat IDs are retired rather than renumbered is DR-120 (Threat IDs are retired, never renumbered), and that a held record is only ever closed is DR-121 (A record is never edited once accepted, only closed by a record that replaces it).

## What reversing it would change

R126 and R127 in `project-standards` would change, with their scenarios "A record that names nothing fails CI", "A mention of nothing fails CI" and "A record named by another title fails CI", and so would the citation and mention checks in `tests/test_decisions.py`, task 1.18, the design's decision 13 and T75's answer and residual. Every record that names a task, a design decision or a path would then hold what the rule no longer allows, and such a record changes only by being closed, so DR-121 and DR-152 would be revisited. Records are not part of the public surface, so the change would not be a breaking one for adopters.
