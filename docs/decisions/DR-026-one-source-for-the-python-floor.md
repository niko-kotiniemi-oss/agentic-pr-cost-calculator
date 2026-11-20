# DR-026: `requires-python` is the one source of the oldest supported Python

- **Type:** technical
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R99
- **Threats:** T55
- **Replaces:** none
- **Closed by:** none

## Context

The oldest supported Python (DR-025) is stated in many places: in the settings that ruff and mypy check the code against, in `.python-version` and the CI matrix, in documents such as the README and `CLAUDE.md`, and in the bill of materials and the hook's own guard, which tasks 6.2 and 6.5 build. Copies that disagree would tell adopters one floor and test another (T55).

## Decision

`requires-python` in `pyproject.toml` is the one source of the oldest supported version. A test holds other copies to it, and fails and names a copy that disagrees: the settings, the CI matrix and each "Python 3.N" in six documents that describe the tool now, and the bill of materials and the hook's own guard once tasks 6.2 and 6.5 build them. The change's own proposal, design and tasks, and the decision records, keep the version they were written with.

## Alternatives

None were recorded when this was decided.

## Consequences

- `tests/test_repository.py` reads the floor from `requires-python`, which it expects in the form `>=3.N`, and compares it with ruff's `target-version`, mypy's `python_version`, `.python-version` and the CI matrix.
- The same test reads six documents, among them the README, `CLAUDE.md`, the feature page and the spec of `releases-and-compatibility`, and fails when one of them states no version in the form "Python 3.N", or states one other than the floor.
- A floor written in another form, such as "older than 3.11" on the feature page, and T56's answer in `docs/threat-model.md`, which the test does not read, are not held to it, so a rise finds them only by the search for other copies (DR-146).
- It also fails when the CI matrix lacks the oldest version or `3.x`, the newest release (T55).

## Scope

This covers where the oldest supported Python is declared and how its copies are held to it. DR-025 (The oldest supported Python is 3.11) holds which version that is, and DR-134 (The oldest supported Python rises only near its end of life or for a security fix) holds when it rises.

## What reversing it would change

R99 in `releases-and-compatibility` would change, with its scenario "Declared versions that disagree are reported", and so would the design's decision 10, T55's answer, the feature page and the test in `tests/test_repository.py` that task 1.11 added. Where the floor is declared is not part of the public surface, so the change would not be a breaking one for adopters.
