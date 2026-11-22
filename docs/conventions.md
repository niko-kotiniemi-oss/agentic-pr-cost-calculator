# Conventions

The conventions that names follow in this repository, and the Python that its code is written in, each with the requirement or record that holds it (DR-277, DR-278). What no test holds is for review.

## Identifiers

Each kind of thing that the pages cite has an identifier of its own form, and keeps it. A requirement, a threat and an assumption that the default branch holds stay held or are retired (R130), a retired threat's ID is never used again (R132), and the records and the backlog items are numbered without a gap or a repeat (R124, R211).

| What | Its form | Where it is given | What holds it |
|---|---|---|---|
| A requirement | `R` and a number, as R271 | [the register](requirements.md) | R100, R130 |
| A decision record | `DR-` and at least three digits, as DR-277, in a file named `DR-`, its number, a hyphen and words | [the records](decisions/README.md) | R124, R266 |
| A threat | `T` and a number, as T262 | [the threat model](threat-model.md) | R132, R130 |
| An assumption | `A` and a number, as A14 | [the assumptions](assumptions/README.md) | R135, R130 |
| A backlog item | `B-` and three digits, as B-005, in a file named `B-`, its number, a hyphen and words | [the backlog](backlog/README.md) | R211, R216 |
| A task | its section's number, a dot and its own, as task 1.53 of `add-pr-cost-calculator` | a change's `tasks.md` | R232, R127 |
| A design decision | its number in its change's design, as design decision 23 | a change's `design.md` | R127 |

A page that names a record, a design decision, a requirement, a threat, a change or a task names one that exists, a requirement or a threat as held or retired (R127).

## File names

Files and folders are named in lower case, with a hyphen between words, as `docs/how-it-works.md` and `scripts/sync-superpowers.sh`, but for these (DR-277):

- A Python module takes underscores instead, as `scripts/risk_register.py` and `tests/test_conventions.py`, since an `import` statement names a module by an identifier.
- A file named for an identifier opens with it in its form, as each record and each backlog item does.
- A name that GitHub, Claude Code or a format fixes stays as it fixes it, as `README.md`, `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `.github/CODEOWNERS`, `.github/pull_request_template.md` and `.github/ISSUE_TEMPLATE/` for GitHub, `CLAUDE.md` for Claude Code, and `CHANGELOG.md`, which Keep a Changelog gives.

Tests hold the names of the records (R124) and of the backlog items (R211), and every tracked path's characters and its case against every other path's (R268); task 1.55 of `add-pr-cost-calculator` adds a test of what Windows can write in a path (R277). Any other name is for review. Four names predate this page and do not follow it: `tests/spec_form_openspec.json`, `vendor/superpowers/UPSTREAM.lock`, and the issue templates `.github/ISSUE_TEMPLATE/bug_report.yml` and `.github/ISSUE_TEMPLATE/feature_request.md`.

## Python names

Python names follow PEP 8 as ruff's naming rules, `N`, check them: among others, a class is named in CapWords, a function, an argument and a variable in a function in lower case with underscores, a name at a module's or a class's level not in mixed case, and an exception class with `Error` at the end of its name (DR-277). `pyproject.toml` selects the rules and ignores none of them, and a test runs them on every Python file that this repository writes, so that no comment, configuration file, ignore file, setting or folder keeps a name from them, as R271 gives it. The vendored copy of Superpowers is upstream's and keeps its own names.

## Test names

A test's name states the behaviour that it checks, as `test_a_name_kept_from_ruff_s_check_fails_the_test_of_names` does (DR-277). No test holds this: whether a name states its behaviour is for review.

## Names that adopters type

The names that adopters type, such as the opt-in key and the keys of the configuration file, are part of the public surface, which the surface manifest names (R122), so that a release that changes one raises the major number (R71, R123). This page keeps no list of them: the manifest is that list, and task 6.1 of `add-pr-cost-calculator` writes it (DR-277). A page gives such a name in code, where the glossary's words to avoid are not read, so that it keeps its spelling (R137).

## The Python that the code is written in

The tool's code, the scripts, the skeleton and the tests are written as idiomatic Python of the oldest supported version, which `requires-python` in `pyproject.toml` gives: they use what that version offers where it fits, and nothing that a later version adds (DR-278). Ruff's `UP` rules at that version, mypy at that version, and CI's runs on it and on the newest release hold what a machine can (R25, R99), and the tool's code uses the standard library alone (DR-023). Whether a construct fits its use is for review.
