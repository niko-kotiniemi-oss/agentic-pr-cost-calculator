# DR-244: This repository keeps from the skeleton's run only a transcript's shape with no values, and what was observed

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the owner, 2026-11-14
- **Requirements:** R236
- **Threats:** T186
- **Replaces:** none
- **Closed by:** none

## Context

`CLAUDE.md` says that this public repository never holds session transcripts, and DR-236 says that it keeps from the skeleton's run only what the skeleton's pull request asks the owner to keep. The guide's entry on fixtures asks for the shape of a real transcript, with no values, so that each fixture can be compared with it (B-007, B-021). The third choice of the plan that the owner approved on 2026-11-14 was what this repository keeps from the run.

## Decision

This repository keeps from the run two things only: the shape of the run's transcripts, `tests/fixtures/transcript-shape.json`, which gives paths of field names and the JSON type at each and no path below a tool's input, a tool's result or a message's text (R236), and what was observed, written into the assumptions and the specs. It keeps no count, no cost, no identifier and no text from the run. The shape is the one exception that `CLAUDE.md`'s privacy section names to its rule against transcripts.

## Alternatives

- The run's ledger files and the comment's figure kept as an example: they are counts measured on the owner's work, which `CLAUDE.md` keeps out of this repository.
- Nothing kept but the written observations: fixtures would have no recorded shape to be compared with, which the guide names as a gap.

## Consequences

- `CLAUDE.md`'s privacy section names the shape as its one exception, in the same pull request (DR-244).
- A test fails on an entry of the shape that gives a value or a path below a tool's input, a tool's result or a message's text (R236, task 1.31).
- Whether a field name itself tells something private rests on review (T186).

## Scope

This covers what this repository keeps from the skeleton's run. Where the run happens is DR-236 and DR-245.

## What reversing it would change

How hard it is to reverse: reversible. The shape is a file that one pull request can remove, though what a pushed commit published stays published. R236 in `project-standards` would change, with its scenarios, and so would `CLAUDE.md`'s privacy section, design decision 18, tasks 1.31 and 1.36 and the answer of T186.
