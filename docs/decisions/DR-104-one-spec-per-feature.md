# DR-104: Each feature is one spec

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-25
- **Requirements:** R73
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

The specs hold what the tool must do, one folder per capability (DR-079). Each feature has a page that names its requirements and says how it is validated (DR-101).

## Decision

Each feature is one spec. A capability of a change and a feature of the product are the same thing.

## Alternatives

None were recorded when this was decided.

## Consequences

- A page is named for its spec, and tests fail on a spec without a page, a page named for another spec, and a page that leaves out a requirement of its spec or names one of another's (R73).
- The register gives each requirement's spec as its capability, so each requirement belongs to one feature (`docs/requirements.md`).
- Task 1.17 made each feature of `add-pr-cost-calculator` one spec.

## Scope

This covers how features map to specs. What a proposal says about validating a change's capabilities is DR-150 (Each proposal says how its capabilities are validated), what a page holds is DR-101 (Each feature has a page), and what one requirement may state, and at what length, are DR-105 (Each requirement states one behaviour) and DR-113 (Each requirement is 500 characters or fewer).

## What reversing it would change

R73 in `project-standards` would change, with its scenarios. So would the design's decision 12, the specs of `add-pr-cost-calculator` and the pages in `docs/features/`, the note in `docs/requirements.md` that each capability is one feature, the proposal's section on capabilities, the checks of pages in `tests/test_documentation.py`, and task 1.17. DR-101 and DR-150 would be revisited.
