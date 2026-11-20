# DR-023: The hook and the report use Python's standard library only

- **Type:** technical
- **Boundary:** incoming
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R12, R25
- **Threats:** T28
- **Replaces:** none
- **Closed by:** none

## Context

Adopters run two parts of the tool: the capture hook and the report's reusable workflow. The hook runs on whatever machine the session uses, and the workflow runs on a stock runner. With no dependencies, both run with nothing to install, and nothing in the supply chain has to be pinned for users. Anything the tool depended on would also be one more place from which a malicious change could reach adopters (T28).

## Decision

The hook and the report import nothing beyond Python's standard library, so the code that adopters run has no runtime dependency.

## Alternatives

None were recorded when this was decided.

## Consequences

- The hook can be one file that runs under `python3 -I` and that adopters copy whole (R12, DR-022, DR-125).
- Having no runtime dependency is part of T28's answer. It also keeps the bill of materials short, and a dependency that crept in would show there at once (DR-097).
- The code keeps to the language and standard library of Python 3.11, the oldest supported version, and a change that uses something newer fails in CI (R25, DR-025).

## Scope

This covers the code that adopters run. The development tools, such as pytest, ruff and mypy, are outside it: `requirements-dev.txt` pins them, and how they and their own dependencies are locked is DR-126 (Development dependencies are locked with hashes). Which languages the tool, its release and its documentation are written in is DR-024 (The tool, its release and its documentation are Python and Markdown), and which Python versions the code supports is DR-025 (The oldest supported Python is 3.11).

## What reversing it would change

R12 in `usage-capture` and R25 in `releases-and-compatibility` would change, and so would the design's decision 2, T28's answer, the rule in `CLAUDE.md` that the tool uses the standard library only, the statements that it does in the README, the proposal and the `releases-and-compatibility` feature page, `docs/how-it-works.md`, which calls the hook a standard-library Python file, and task 2.3. A runtime dependency would enter the bill of materials (DR-097), and DR-022, whose single copied file rests on this, would be revisited.
