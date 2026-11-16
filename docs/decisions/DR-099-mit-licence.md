# DR-099: The licence is MIT

- **Type:** process
- **Status:** closed
- **Decided by:** the owner, 2026-10-17
- **Requirements:** R28
- **Threats:** none
- **Replaces:** none
- **Closed by:** DR-242

## Context

The repository is public, and the tool is used from other repositories: adopters copy its hook file into theirs (DR-022) and call its reusable workflow from a workflow of their own (DR-132). Anyone can open a pull request to it, a fork's included (T37).

## Decision

The repository's own work is under the MIT licence, which `LICENSE` holds and `pyproject.toml` declares as `license = "MIT"`.

## Alternatives

None were recorded when this was decided.

## Consequences

- A contribution is licensed under the same licence, as `CONTRIBUTING.md` says.
- A test holds that `LICENSE` begins with "MIT License".
- Each release's bill of materials names the MIT licence, as the scenario "The bill of materials describes the release" of R28 expects.

## Scope

This covers the licence of the repository's own work. The vendored Superpowers and OpenSpec's generated skills keep their own licences, which the bill of materials lists with their sources (R28), and how those parts are kept is DR-041 (Superpowers is vendored and compared with upstream in CI) and DR-042 (OpenSpec is pinned and its skills are regenerated in CI).

## What reversing it would change

R28's scenario "The bill of materials describes the release" in `releases-and-compatibility` would change, and so would `LICENSE`, the licence in `pyproject.toml`, the licence test in `tests/test_repository.py`, the sections on the licence in the README and `CONTRIBUTING.md`, the opening sentence of `CLAUDE.md` and the bill of materials that task 6.2 writes. DR-114, DR-115 and DR-116, whose consequences name the MIT licence, would be revisited. The licence is not part of the public surface, so the release check would not take the change for a breaking one.
