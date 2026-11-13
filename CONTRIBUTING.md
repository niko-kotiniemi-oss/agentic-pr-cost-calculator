# Contributing

Thank you for helping. This page says how a change gets made here. The rules for anyone working on the repository, person or agent, are in [`CLAUDE.md`](CLAUDE.md), and they apply to every contribution.

## Before you start

- For a bug, open an issue with the bug report template. For a security problem, don't open an issue: follow [`SECURITY.md`](SECURITY.md).
- For a new feature or a change of behaviour, open an issue first, where it is discussed. A proposal is agreed by a pull request, which the owner merges, that makes its backlog item planned, and an item is built only once it is planned. The README's [briefing on how work flows](README.md#working-on-this-repository) gives the stages. What the tool must do is written as an OpenSpec change under `openspec/changes/`, and code follows an approved change.

## Setting up

```sh
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
npm ci --ignore-scripts
```

The tool supports Python 3.11 and later, so use Python 3.11 locally if you can: CI tests on 3.11 and on the newest release. Node is needed only for the OpenSpec CLI, which is a development tool.

## Making a change

1. **The change first.** Update or add the OpenSpec change that says what must hold, with its requirements and scenarios. A change that makes or reverses a decision adds its record to [`docs/decisions/`](docs/decisions/README.md), and closes the record of any decision it reverses; a record that the default branch holds is never edited otherwise, except that a closed record's lines may become `[removed]`.
2. **Threats at design.** Read [`docs/threat-model.md`](docs/threat-model.md) against the change. Add the threats it brings, each rated for impact and likelihood, with its answer.
3. **Tests first.** Write the failing test, see it fail for the expected reason, then make it pass. Every change has positive and negative tests.
4. **Documentation with the code.** Update [`docs/requirements.md`](docs/requirements.md), the feature's page in [`docs/features/`](docs/features/README.md) and [`docs/how-it-works.md`](docs/how-it-works.md) in the same pull request, and the backlog item and [`docs/roadmap.md`](docs/roadmap.md) when the change finishes, adds or moves one of its items, and add a line to `CHANGELOG.md` under `## [Unreleased]` for anything an adopter would notice.
5. **Threats at implementation.** Before asking for review, read the threat model again against what you built, and update the ratings and answers.
6. **Run the checks.** All of these must pass:

   ```sh
   .venv/bin/pytest
   .venv/bin/ruff check . && .venv/bin/ruff format --check . && .venv/bin/mypy
   scripts/verify-openspec.sh
   ```

7. **Open the pull request** with the template, and keep it to one change.

## What a pull request may not contain

This repository is public. Never commit session transcripts, session identifiers, cost figures measured on someone's private work, internal names or secrets. Test data is synthetic.

## Licence

By contributing you agree that your contribution is licensed under the [MIT licence](LICENSE) of this repository.
