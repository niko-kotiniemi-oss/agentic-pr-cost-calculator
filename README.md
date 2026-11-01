# Agentic PR cost calculator

An open-source tool to estimate what a GitHub pull request cost when it was built with an AI coding agent.

**Status: proposal.** None of the tool's code exists yet. The design is an OpenSpec change under
[`openspec/changes/`](openspec/changes/), and code starts once it is approved.

## What it will do

For each pull request, the tool will:

- capture the tokens the agent spent while its session was working in the repository, per model and by type: input, output, cache writes and cache reads, and carry them to the pull request with the agent's own commits;
- price them from a dated price table kept in the tool's own repository, so the estimate uses the price that applied on the day the tokens were spent;
- add the GitHub Actions minutes the pull request's CI used, priced at GitHub's published rate;
- where the data allows, split the cost by activity: code generation, file reading, tooling, MCP calls, subagents and conversation, with any tool it does not know counted as other;
- post a short report comment when the pull request merges, and keep the ledger in the repository as the record.

A repository turns it on or off with one file, its configuration file, and each person decides for themselves whether their own sessions are recorded.

Usage is recorded by the directory the session is in, not by which files it touches. A session in the repository is recorded there even for work it does on another repository from there, so work on other repositories, private ones above all, belongs in sessions of its own.

The figure is an **API-equivalent estimate**, meaning what the same tokens would cost at list prices. It is not a bill: subscription plans and included CI minutes change what you actually pay.

## Not supported in this first version

- Commands sent through Claude Code's PowerShell tool, which is on by default on Windows for claude.ai and Console accounts: capture does not see a commit or a change of branch made through that tool ([DR-007](docs/decisions/DR-007-powershell-tool-out-of-scope.md)).
- Agents other than Claude Code, such as Gemini or Codex ([DR-003](docs/decisions/DR-003-claude-code-only.md)).
- GitHub Enterprise Server ([DR-006](docs/decisions/DR-006-github-com-only.md)).
- Repository and CI services other than GitHub, such as GitLab or Gitea ([DR-160](docs/decisions/DR-160-github-only.md)).

Each line links the decision record that leaves it out. A later version may add any of these, by a new record that replaces that one.

## Documentation

- [How it works](docs/how-it-works.md): the tool as a whole, with its flows, how a cost is computed, and every credential, permission and outside connection it uses.
- [Features](docs/features/README.md): one page per feature, with its expected behaviour, its requirements and how it is validated.
- [Requirements](docs/requirements.md): every functional, behavioural and non-functional requirement, indexed to the specs that hold them.
- [Threat model](docs/threat-model.md): what could go wrong, each threat rated for impact and likelihood, and what answers it.
- [Decisions](docs/decisions/README.md): one record per decision, with why it was made, what else was considered and what reversing it would change.
- [Changelog](CHANGELOG.md).

## Compatibility and releases

The tool runs on Python 3.11 and every later release, with the standard library only, so it fits into other projects without pulling anything in. The oldest supported version rises only when it nears its end of life, or when a security fix needs a newer one. Versions follow [Semantic Versioning](https://semver.org/), and each release on GitHub carries a CycloneDX software bill of materials and names the commit to pin. No version has been released yet.

## Working on this repository

How to contribute is in [`CONTRIBUTING.md`](CONTRIBUTING.md), and the rules for contributors, human or agent, are in [`CLAUDE.md`](CLAUDE.md). Everyone taking part follows the [code of conduct](CODE_OF_CONDUCT.md). In short: tests come first, every figure in prose is computed rather than recalled, and scope is never narrowed silently.

Setup for a local clone:

```sh
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
npm ci --ignore-scripts
.venv/bin/pytest
.venv/bin/ruff check . && .venv/bin/ruff format --check . && .venv/bin/mypy
scripts/verify-openspec.sh
```

A cloud session of Claude Code that has this repository alone, outside a project's threads, runs the same setup automatically through `.claude/hooks/session-start.sh`.

Two tools are pinned here:

- [OpenSpec](https://github.com/Fission-AI/OpenSpec), installed at an exact version from `package-lock.json`. It holds what the tool must do.
- [Superpowers](https://github.com/obra/superpowers), vendored under `vendor/superpowers/` at the commit `UPSTREAM.lock` names. It guides how the code is built. CI checks that the copy matches upstream.

## Security

See [`SECURITY.md`](SECURITY.md) for reporting a vulnerability, and [`docs/threat-model.md`](docs/threat-model.md) for the threats the design answers.

## Licence

[MIT](LICENSE).
