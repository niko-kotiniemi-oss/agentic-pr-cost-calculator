# DR-108: Each decision has a record of its own, in an index

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the owner, 2026-10-26
- **Requirements:** R124, R125, R126, R127, R133, R134
- **Threats:** T72, T73, T74, T76, T78, T79, T81
- **Replaces:** none
- **Closed by:** none

## Context

Each decision is meant to be reversible or replaceable on its own, and linked to the requirements it shapes (see the proposal's "What Changes"). The design's decisions mixed how the tool works, why, and what was not chosen (T78).

## Decision

Each decision about what the tool is, how it works or how it is built has a record of its own in `docs/decisions/`, holding one choice, and `docs/decisions/README.md` indexes every record. A record's fields give its type, who decided it and the requirements and threats it shapes.

## Alternatives

None were recorded when this was decided.

## Consequences

- `tests/test_decisions.py` checks the form, the numbering, the folder, the index, the citations and the mentions of records, and that no attribute that the repository sets hides a record's diff (R124 to R127, R133 and R134; task 1.18; T81).
- A record's ID is `DR-` and its number in ASCII digits, padded to three, and the records are keyed by their numbers (R124; T79). `docs/decisions/` holds only the records and their index, each a file and not a link, with no folder in it, and no file elsewhere is named as a record, so a file that is neither fails the check wherever it is (R133; T79).
- Every line of the index's table, which runs to its first blank line, other than its header and the delimiter under it, is read as a row against the record it names, and a later line that holds a vertical bar fails (R125; T79).
- The index's column of deciders puts every attribution in one diff for the owner to read before merging, but no machine can tell whether the owner made a decision (T72).
- A record describes and never instructs, and its last section says what reversing the decision would change, not how (T73). Where a record and `CLAUDE.md` disagree, `CLAUDE.md` steers, as its paragraph on records being data says.
- An accepted record whose cited requirements are all retired fails CI, so the change that retires them closes it (R126; T74).
- The design's reasons moved into records word for word (T78).
- A record whose choice touches every threat in the same way, as the rating of threats does, lists none in its threats and gives that reason in its last section (DR-094, DR-112).
- Whether a record holds one choice and says what its sources say is left to review.

## Scope

This covers that each decision has a record, what a record gives, and the index. The forms that a decider takes are DR-151 (A record's decider takes one of three forms), the characters and the links a record may hold are DR-152 (A record is plain text and links only to other records), how a record names what it rests on is DR-158 (A record names other things by ID, number or path, and its change by name), that a record and the threats it lists name each other is DR-159 (A record and the threats it lists name each other), and that an accepted record is only closed, never edited, is DR-121 (A record is never edited once accepted, only closed by a record that replaces it).

## What reversing it would change

R124 to R127, R133 and R134 in `project-standards` would change, with their scenarios, and so would the design's decision 13 and its lists of records, `docs/decisions/`, `tests/test_decisions.py`, task 1.18, the answers of T72 to T74, T76, T78, T79 and T81, `CLAUDE.md`'s lines on decision records, the README, the first step in `CONTRIBUTING.md`, the feature page for `project-standards` and the proposal. DR-119, DR-120, DR-121, DR-151, DR-152, DR-153, DR-158 and DR-159 would be revisited, and since records are not part of the public surface, the change would not be a breaking one for adopters.
