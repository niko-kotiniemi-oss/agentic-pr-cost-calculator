# DR-102: A page explains how the tool works as a whole

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the owner, 2026-10-20
- **Requirements:** R29, R101
- **Threats:** T57
- **Replaces:** none
- **Closed by:** none

## Context

DR-117 holds the tool to doing nothing that its documentation leaves out. The tool's parts run in different places: the hook on the machine that runs a session, and the report and the release workflow on GitHub Actions runners (see the design's decisions 1, 7 and 11).

## Decision

`docs/how-it-works.md` explains the tool as one product: its inputs and outputs, how a cost is computed and from where, one diagram per flow, every credential and permission, and every connection to the outside world, with where to, by which protocol and why.

## Alternatives

None were recorded when this was decided.

## Consequences

- `tests/test_documentation.py` holds the page to the workflows. It fails when a job's permissions in the page's table and in its workflow differ, either way, or when a workflow runs an action or an image that the page does not name (R101), which is T57's answer, and when a flow has no diagram (R29).
- Once the tool's code exists, task 5.3 checks the page against every network call and environment variable that the code reads.

## Scope

This covers the page on the tool as a whole. The pages for each feature are DR-101 (Each feature has a page), and the register is DR-100 (A register lists every requirement with its kind).

## What reversing it would change

R29 and R101 in `project-standards` would change, with their scenarios "A flow without a diagram fails CI" and "An undocumented permission or action fails CI". So would the design's decision 12, `docs/how-it-works.md`, its checks in `tests/test_documentation.py`, T57's answer, tasks 1.12 and 5.3, the README's list of documentation, the proposal's sections on what changes and on capabilities, `CLAUDE.md`'s section on documentation, the step on documentation in `CONTRIBUTING.md` and the pull request template's checklist. DR-103 and DR-117 would be revisited.
