# DR-278: The code is idiomatic Python of the oldest supported version

- **Type:** technical
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-27
- **Requirements:** R26
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

The owner asked on 2026-10-27 for idiomatic code of the given version, which the plan of that day read as idiomatic Python of the oldest version that the tool supports, 3.11 by DR-025. `pyproject.toml` already sets ruff's target and mypy's version to 3.11, ruff's rules for upgrading code, `UP`, rewrite what that version writes otherwise, and CI runs on 3.11 and on the newest release (task 1.11).

## Decision

The tool's code, the scripts, the skeleton and the tests are written as idiomatic Python of the oldest supported version: they use what that version offers where it fits, and nothing that a later version adds. `docs/conventions.md` says so, with what holds it: ruff's `UP` rules at the 3.11 target, mypy at 3.11, and CI's runs on 3.11 and on the newest release.

## Alternatives

- Writing for the newest release: the tool supports 3.11 and every later release (DR-025), so code that used a later feature would fail on 3.11.
- Leaving idiom to review alone: ruff's upgrade rules already rewrite what the target writes otherwise, so a machine holds part of it.

## Consequences

- No new check: what holds it is in place since task 1.11, and what no rule checks, such as whether a construct fits its use, is for review.
- When the oldest supported version rises (DR-134), what is idiomatic rises with it.

## Scope

This covers how the code is written. Which version is the oldest is DR-025 (The oldest supported Python is 3.11), and when it rises is DR-134 (The oldest supported Python rises only near its end of life or for a security fix). Names are DR-277 (Names follow the conventions page, and ruff checks Python's names).

## What reversing it would change

How hard it is to reverse: reversible. Only `docs/conventions.md` and this record say it, and the checks that hold it belong to DR-025. Nothing that adopters configure or depend on changes, so the change would not be a breaking one for adopters.
