# DR-247: This repository keeps from the skeleton's run only a transcript's shape with no values, and what was observed

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the owner, 2026-11-14
- **Requirements:** R236
- **Threats:** T186, T190
- **Replaces:** none
- **Closed by:** none

## Context

`CLAUDE.md` says that this public repository never holds session transcripts, and DR-236 says that it keeps from the skeleton's run only what the skeleton's pull request asks the owner to keep. The guide's entry on fixtures asks for the shape of a real transcript, with no values, so that each fixture can be compared with it (B-007, B-021). The third choice of the plan that the owner approved on 2026-11-14 was what this repository keeps from the run.

## Decision

This repository keeps from the run two things only: the shape of the run's transcripts, `tests/fixtures/transcript-shape.json`, which gives the paths of the field names of each kind of line at its top level, in its `message` object and in `message.usage`, with the JSON type at each, and every other object and array as its type alone (R236), and what was observed, written in words into the assumptions and the specs. It keeps no value, count, cost, identifier, time or text from the run, in its files or in its pull request's text. A fact that the run observed becomes `observed` only through a test whose fixture is written by hand to the kept shape; otherwise it keeps its check and its statement says what the run saw and when. The owner reads the shape and the observations in the scratch repository before they come here. The shape is the one exception that `CLAUDE.md`'s privacy section names to its rule against transcripts.

## Alternatives

- The run's ledger files and the comment's figure kept as an example: they are counts measured on the owner's work, which `CLAUDE.md` keeps out of this repository.
- Nothing kept but the written observations: fixtures would have no recorded shape to be compared with, which the guide names as a gap.

## Consequences

- `CLAUDE.md`'s privacy section names the shape as its one exception, in the same pull request (DR-247).
- A test fails on an entry of any kept shape that gives a value, a name below another object than the line, its `message` and `message.usage`, or a name of an identifier's form, and fails when no shape exists once the run is recorded (R236, task 1.31), and the private-reference check knows the identifiers that a transcript carries (task 1.31, T190).
- Whether a field name itself, or an observation's words, tells something private rests on the owner's reading and on review (T186, T190).

## Scope

This covers what this repository keeps from the skeleton's run. Where the run happens is DR-236 and DR-248.

## What reversing it would change

How hard it is to reverse: reversible. The shape is a file that one pull request can remove, though what a pushed commit published stays published. R236 in `project-standards` would change, with its scenarios, and so would `CLAUDE.md`'s privacy section, design decision 18, tasks 1.31 and 1.36 and the answer of T186.
