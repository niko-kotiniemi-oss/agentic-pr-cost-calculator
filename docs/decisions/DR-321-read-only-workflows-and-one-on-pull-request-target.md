# DR-321: Workflow tokens are read-only, except for releases and the report's comment, and only the base commit's checks run on `pull_request_target`

- **Type:** security and privacy
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-24
- **Requirements:** R27, R321
- **Threats:** T37, T68, T240, T287, T320
- **Replaces:** DR-067
- **Closed by:** none

## Context

Anyone can open a pull request here, and one from a fork runs this repository's CI with code its author chose (T37). The `pull_request_target` and `workflow_run` triggers run a workflow with this repository's token on someone else's code (`tests/test_repository.py`), and a job that holds `contents: write` and runs someone else's code hands it that token (T68). DR-067 let no workflow trigger on either event. The owner chose on 2026-11-24 that the base commit's checks run from the base branch's own workflow, so that a pull request cannot drop or weaken them (DR-312), and only `pull_request_target` runs the base's copy of a workflow for a pull request.

## Decision

Every workflow in this repository declares `contents: read` for itself as a whole. None triggers on `workflow_run`, and only the workflow of the base commit's checks triggers on `pull_request_target`, granting only `contents: read` to itself and its job, checking out only the base's commit, giving the pull request's number and commits to a command only through `env:` and restoring and saving no cache (R321). None reads a secret. No workflow grants a write permission but the release workflow, whose release job alone holds `contents: write`, and the report's reusable workflow, which holds `pull-requests: write` for its comment (DR-063).

## Alternatives

- No workflow on `pull_request_target`, as DR-067 had it: a pull request that also changes the workflow of the base commit's checks would drop them, leaving only the owner's review (DR-312).

## Consequences

- CI's jobs neither write nor comment, and read no secret, and a run for a fork's pull request also gets GitHub's read-only token (T37).
- The job of the base commit's checks runs for a fork's pull request without the approval that DR-078 asks for, since it runs the base's code alone and reads the pull request's tree only from git's objects (R317, T320).
- The one job that writes to the repository is held to a narrow form: it runs only for a pushed tag, checks the tag's form before any other step, installs nothing, keeps no checkout credentials, and leaves the tests to a separate read-only job (T68).
- `tests/test_repository.py` fails on a workflow that declares anything but `contents: read` for itself, triggers on `workflow_run`, triggers on `pull_request_target` unless it is the workflow of the base commit's checks held as R321 gives, grants a write that the test's list of allowed writes does not hold for it, or has the word `secrets` anywhere in its text. The report's and the release's workflows add their writes to that list when tasks 4.3 and 6.3 build them.
- DR-067 is closed, and this record holds what it decided. R27, T37, T68, T240 and T287, which rested on it, rest on this record, and the threat model, the assumptions, the guide and the design cite it in DR-067's place; records that name DR-067 keep their text.

## Scope

This covers the tokens, triggers and secrets of this repository's own workflows. What an adopter's calling workflow grants the report is DR-063 (The calling workflow grants only what the report needs), the repository's default workflow permissions are DR-076 (Actions' default workflow permissions are read-only), and how actions are pinned is DR-068 (Every action is pinned to a commit that its repository tagged).

## What reversing it would change

How hard it is to reverse: reversible. R27 in `releases-and-compatibility` would change in its clause that the release workflow checks the tag's form before any other step, with its scenario "A tag that is not a semantic version stops the workflow first", and R321 in `project-standards` with its scenarios. The workflow checks in `tests/test_repository.py`, which task 1.16 added, the permissions in `.github/workflows/ci.yml` and the workflow of the base commit's checks, tasks 4.3 and 6.3, the design's decision 11, the answers of T37, T68 and T320, and the section on credentials and permissions in `docs/how-it-works.md`, with its table, would change. The reusable workflow's permissions are part of the public surface, so a change to them would be a breaking one, released as a new major version (DR-096). DR-063, DR-076 and DR-312 would be revisited.
