# DR-308: GitHub's code scanning for Python runs in its default setup

- **Type:** security and privacy
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-11-12
- **Requirements:** none
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

The repository's checks are its own tests, ruff and mypy. GitHub's code scanning (CodeQL) adds a data-flow analysis of the Python code at no cost for a public repository, as a setting that the owner turns on.

## Decision

GitHub's code scanning for Python is on in its default setup, a repository setting that the owner turns on and keeps (Settings, then Advanced Security, then Set up beside CodeQL analysis, then Default). A private, commercial repository would need GitHub Code Security, a paid product, so there code scanning would likely be off, and deterministic CI gates, starting with Semgrep Community Edition, Bandit, Ruff and pip-audit, would take its place, giving useful coverage but not CodeQL's deeper data-flow analysis; Ruff already offers many of Bandit's checks as its `S` rules.

## Alternatives

- No code scanning: the data-flow analysis would be lost while it costs nothing here.
- An advanced setup in a workflow of this repository: it adds a workflow and its pins to keep, for no gain over the default setup.

## Consequences

- Code scanning's alerts reach the owner, who decides what follows from each; an agent never posts a finding of a vulnerability in released code.
- The setting is the owner's, so no test holds it, and the threat model's settings that the owner keeps list it.

## Scope

This covers code scanning here. How vulnerabilities in dependencies are found is the scope and visual documentation's records.

## What reversing it would change

How hard it is to reverse: reversible. The owner turns the setting off, and the list of settings that the owner keeps would change.
