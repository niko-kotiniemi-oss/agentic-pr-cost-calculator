# DR-118: The tool is named `agentic-pr-cost-calculator`

- **Type:** scope
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the owner, 2026-10-17
- **Requirements:** none
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

The tool estimates what a GitHub pull request cost when it was built with an AI coding agent (see the README), for teams that build pull requests with AI coding agents (DR-001). Its repository holds a Python project and the Node tooling that installs OpenSpec for development, and adopters take the hook file and the reusable workflow from it (DR-022; see the design's decision 7).

## Decision

The tool and its repository are named `agentic-pr-cost-calculator`.

## Alternatives

None were recorded when this was decided.

## Consequences

- `pyproject.toml` names the project `agentic-pr-cost-calculator`, and `package.json` names the development tooling `agentic-pr-cost-calculator-tooling`, which is private and installs the OpenSpec CLI at an exact version.
- The README spells the name out in its heading as the Agentic PR cost calculator.
- The issue templates' link to private vulnerability reporting names the repository.
- The names that adopters configure are not the tool's name: the opt-in key `pr-cost.capture`, the ledger path `.pr-cost/` and the configuration file `.pr-cost.json` are parts of the public surface in their own right (see the design's decision 11).

## Scope

This covers the name of the tool and of its repository. Whom the tool is for is DR-001 (The tool is for teams that build pull requests with AI coding agents), and that the repository is public and open source is DR-114 (The tool is open source, in a public repository).

## What reversing it would change

A new name would change `pyproject.toml`, `package.json`, `package-lock.json` and the link in `.github/ISSUE_TEMPLATE/config.yml`. The design's decision 11 puts the reusable workflow's path on the public surface, and adopters' calling workflows reach that workflow in this repository, so a new name for the repository would be a breaking change for adopters (DR-096). A new name for the Python project alone would not reach the public surface, and the `pr-cost` names would not change. No requirement's text would have to change.
