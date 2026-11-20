# DR-100: A register lists every requirement with its kind

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the owner, 2026-10-20
- **Requirements:** R29, R73, R100, R130
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

Each requirement's text and scenarios are in the spec of its feature (DR-104), so what the product must do is spread over the specs. The documentation sets out to let a developer say how the tool works (DR-117).

## Decision

`docs/requirements.md` registers every requirement in the specs, once, with its kind: functional, for what the tool does; behavioural, for how it responds to conditions, failures and inputs it must refuse; non-functional, for the qualities it must keep, such as privacy, compatibility, security and its release. The specs stay the source of each requirement's text and scenarios, and the register is their index.

## Alternatives

None were recorded when this was decided.

## Consequences

- What the product must do can be read in one place, and each requirement has an ID that the feature pages cite (DR-106).
- `tests/test_documentation.py` fails when a spec holds a requirement that the register leaves out, when the register names one that no spec holds or lists one twice, and when a kind is not one of the three (R100).
- A pull request that adds a requirement adds its row to the register too (DR-103).

## Scope

This covers the register. The pages for each feature are DR-101 (Each feature has a page), how the IDs are kept is DR-106 (Requirement IDs are stable and never reused), and what one requirement may state, and at what length, are DR-105 (Each requirement states one behaviour) and DR-113 (Each requirement is 500 characters or fewer).

## What reversing it would change

R29, R73, R100 and R130 in `project-standards` would change, with R100's scenario "A requirement missing from the register fails CI" and the references to the register in R73 and R130. So would the design's decision 12, `docs/requirements.md`, the register's checks in `tests/test_documentation.py`, tasks 1.12 and 5.3, the feature pages, which name requirements by their IDs, the README's list of documentation, `CLAUDE.md`'s section on documentation, the step on documentation in `CONTRIBUTING.md`, the pull request template's checklist and the proposal's list of what changes. DR-106 would be closed, and DR-101 and DR-103 revisited.
