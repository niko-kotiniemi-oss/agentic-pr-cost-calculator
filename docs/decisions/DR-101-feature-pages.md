# DR-101: Each feature has a page

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the owner, 2026-10-20 and 2026-10-25
- **Requirements:** R29, R73, R100
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

Each feature's requirements and their scenarios are in its spec (DR-079, DR-104). The documentation sets out to let a developer say how the tool works (DR-117).

## Decision

`docs/features/` has one page per feature, from the user's side: what it does and how it is expected to behave, which requirements it holds, and how it is validated.

## Alternatives

- One long document, in which a feature's behaviour and the product's logic are harder to find.

## Consequences

- `tests/test_documentation.py` fails on a spec without a page, a page that leaves out a requirement of its spec or names another, a page with no section on validation, a page that the index does not link, and a requirement that is on no page (R73, R100).
- While the tool is designed and not built, each page describes the behaviour that its spec requires, and it changes in the same pull request as its feature (see `docs/features/README.md`, and DR-103).

## Scope

This covers the pages for each feature. Which spec each page is for is DR-104 (Each feature is one spec), and the tool as a whole is DR-102 (A page explains how the tool works as a whole).

## What reversing it would change

R29, R73 and R100 in `project-standards` would change, with R73's scenarios and R100's scenario "A requirement without a feature fails CI". So would the design's decision 12, `docs/features/` and its index, the checks of the pages in `tests/test_documentation.py`, tasks 1.12, 1.17 and 5.3, the README's list of documentation, the proposal's list of what changes and its section on capabilities, `CLAUDE.md`'s section on documentation, the step on documentation in `CONTRIBUTING.md` and the pull request template's checklist. DR-104 would be revisited.
