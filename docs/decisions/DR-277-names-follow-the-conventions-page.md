# DR-277: Names follow the conventions page, and ruff checks Python's names

- **Type:** technical
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-27
- **Requirements:** R271
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

The owner asked on 2026-10-27 for naming conventions on a page, with records that point at it: PEP 8 names in Python, checked by ruff once its naming rules are on, and test names that state the behaviour that they check, as the tests here already do. Names followed habit rather than a written convention (B-005). On 2026-11-21 ruff's naming rules found two names here that PEP 8 does not give, both exception classes whose names do not end in `Error`.

## Decision

`docs/conventions.md` gives the conventions that names follow here, each with the requirement or record that holds it: the identifiers of requirements, records, threats, assumptions, backlog items, tasks and design decisions; file names, in lower case with hyphens, but with underscores for Python modules and where GitHub or a tool fixes a name; Python names as PEP 8 gives them, which ruff's naming rules, `N`, check, selected in `pyproject.toml` with none of them ignored; test names that state the behaviour that they check; and the names that adopters type, which the public surface holds. The two exception classes, `Refused` in `scripts/rewording.py` and `Unreadable` in `scripts/sweep_evidence.py`, are renamed to end in `Error`.

## Alternatives

- Leaving names to habit, as before: nothing tells a new contributor the form, and names that differ for one kind of thing cost each reader a moment.
- A test of every file name against its folder's form: no name out of form has reached the default branch, and such a test would change with each new kind of file, so review holds file names.
- Ignoring ruff's rule on exception names, N818, as some projects do: PEP 8 asks for the suffix on an exception that is an error, and both names here are errors.

## Consequences

- CI's `ruff check` fails on a Python name that PEP 8 does not give, and a test fails when `pyproject.toml` selects no `N` or ignores one of its rules (R271; task 1.50).
- The two exception classes are renamed, and nothing outside their scripts names them.
- A file name that no test holds, and a test name that does not state its behaviour, are for review.

## Scope

This covers the names that the project gives. The names that adopters type are part of DR-154 (The public surface is what adopters configure or depend on), and the tool's own name is DR-118 (The tool is named `agentic-pr-cost-calculator`). How the code is written beyond its names is DR-278 (The code is idiomatic Python of the oldest supported version).

## What reversing it would change

How hard it is to reverse: reversible. Turning the rules off is one line of `pyproject.toml`, and the page is one file. R271 in `project-standards` would change, with its scenarios, and so would design decision 23, task 1.50 and `docs/conventions.md`. The names that adopters type are not touched, so the change would not be a breaking one for adopters.
