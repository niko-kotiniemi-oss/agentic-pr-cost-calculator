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
- post a short report comment when the pull request merges, and keep the ledger in the repository as the record;
- record a project's cloud threads too, through a Claude Code plugin that a person adds from a release's zip or from this repository as a marketplace.

A repository turns it on or off with one file, its configuration file, and each person's own opt-in, which they set themselves or which the cloud environment that they use sets, decides whether their own sessions are recorded. An organization can also set it for its members.

Usage is recorded by the directory that Claude is in when it makes each call, not by which files it touches. A call made from the repository is recorded there even when it works on another repository, so work on other repositories, private ones above all, belongs in sessions of its own.

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
- [Assumptions](docs/assumptions/README.md): what the design assumes about what lies outside the tool's own code, and how each of those facts is checked.
- [Decisions](docs/decisions/README.md): one record per decision, with why it was made, what else was considered and what reversing it would change.
- [How the project builds](docs/patterns.md): the guide, which gives, concern by concern, the principles that the project follows, each with its pattern and the anti-patterns that it steers clear of, what holds it and where the project stands.
- [Roadmap](docs/roadmap.md): what is being built now, what comes next and later, and the known limitations.
- [Glossary](docs/glossary.md): the words that the pages use, each with its meaning and the words to avoid for it.
- [Changelog](CHANGELOG.md).

## Compatibility and releases

The tool runs on Python 3.11 and every later release, with the standard library only, so it fits into other projects without pulling anything in. The oldest supported version rises only when it nears its end of life, or when a security fix needs a newer one. Versions follow [Semantic Versioning](https://semver.org/), and each release on GitHub carries a CycloneDX software bill of materials and the plugin's zip, and names the commit to pin. No version has been released yet.

## Working on this repository

Anyone may open an issue to propose a change, ask a question or report a bug, with no approval needed. An issue is public as soon as it is opened, so it holds nothing private, and a security problem goes to [`SECURITY.md`](SECURITY.md) instead. What an issue proposes is neither planned nor committed to. Proposed and planned work is kept as backlog items, so that the repository's history holds every agreement. A backlog item changes only through a pull request that the owner merges.

The work moves through these stages, each kept where the table says:

| Step | Where it lives | What it holds | Who writes it |
| --- | --- | --- | --- |
| An idea or a bug | A GitHub issue, opened as [`CONTRIBUTING.md`](CONTRIBUTING.md) says | The conversation | Anyone |
| Agreed work | A [backlog item](docs/backlog/README.md) | What and why, its status and its date | A pull request that the owner merges |
| Order | The [roadmap](docs/roadmap.md) | Which item comes when | A pull request that the owner merges |
| Delivery | An OpenSpec change, such as [`add-pr-cost-calculator`](openspec/changes/add-pr-cost-calculator/proposal.md), and its pull request | How, the tests and the reviews | The builder |
| Result | The specs, the [decision records](docs/decisions/README.md), the [threat model](docs/threat-model.md) and the [changelog](CHANGELOG.md) | What holds now, why, and what shipped | The same pull request |

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
