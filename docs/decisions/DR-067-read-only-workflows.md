# DR-067: Workflow tokens are read-only, except for releases and the report's comment

- **Type:** security and privacy
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R27
- **Threats:** T37, T68
- **Replaces:** none
- **Closed by:** none

## Context

Anyone can open a pull request here, and one from a fork runs this repository's CI with code its author chose (T37). The `pull_request_target` and `workflow_run` triggers run a workflow with this repository's token on someone else's code (`tests/test_repository.py`), and a job that holds `contents: write` and runs someone else's code hands it that token (T68).

## Decision

Every workflow in this repository declares `contents: read` for itself as a whole. None triggers on `pull_request_target` or `workflow_run`, and none reads a secret. No workflow grants a write permission but the release workflow, whose release job alone holds `contents: write`, and the report's reusable workflow, which holds `pull-requests: write` for its comment (DR-063).

## Alternatives

None were recorded when this was decided.

## Consequences

- CI's jobs neither write nor comment, and read no secret, and a run for a fork's pull request also gets GitHub's read-only token (T37).
- The one job that writes to the repository is held to a narrow form: it runs only for a pushed tag, checks the tag's form before any other step, installs nothing, keeps no checkout credentials, and leaves the tests to a separate read-only job (T68).
- `tests/test_repository.py` fails on a workflow that declares anything but `contents: read` for itself, triggers on either event, grants a write that the test's list of allowed writes does not hold for it, or has the word `secrets` anywhere in its text. The report's and the release's workflows add their writes to that list when tasks 4.3 and 6.3 build them.

## Scope

This covers the tokens, triggers and secrets of this repository's own workflows. What an adopter's calling workflow grants the report is DR-063 (The calling workflow grants only what the report needs), the repository's default workflow permissions are DR-076 (Actions' default workflow permissions are read-only), and how actions are pinned is DR-068 (Every action is pinned to a commit that its repository tagged).

## What reversing it would change

R27 in `releases-and-compatibility` would change in its clause that the release workflow checks the tag's form before any other step, with its scenario "A tag that is not a semantic version stops the workflow first", and no other requirement states this. The workflow checks in `tests/test_repository.py`, which task 1.16 added, the permissions in `.github/workflows/ci.yml`, tasks 4.3 and 6.3, the design's decision 11, the answers of T37 and T68, and the section on credentials and permissions in `docs/how-it-works.md`, with its table, would change. The reusable workflow's permissions are part of the public surface, so a change to them would be a breaking one, released as a new major version (DR-096). DR-063 and DR-076 would be revisited.
