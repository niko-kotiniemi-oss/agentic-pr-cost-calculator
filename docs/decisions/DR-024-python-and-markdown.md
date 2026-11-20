# DR-024: The tool, its release and its documentation are Python and Markdown

- **Type:** technical
- **Boundary:** inside
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the owner, 2026-10-20 and 2026-10-27
- **Requirements:** none
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

The repository holds the tool, which adopters run as a copied hook file and a reusable workflow, both on Python's standard library alone (DR-023), and the tooling that develops it. Part of that tooling is OpenSpec, which holds the specs and is installed from npm at a pinned version (DR-042), so the repository carries a Node manifest and its lock file beside its Python. Python is common and well supported, so a tool written in it is open to the most people. The owner prefers Rust, but set it aside on 2026-10-27, until deciding otherwise, so that the tool stays widely accessible.

## Decision

The tool, its release and its documentation are Python and Markdown, plus the YAML and JSON that GitHub, Claude Code's settings and the data need. The shell scripts and the configuration that develop and check the tool, such as `scripts/verify-openspec.sh`, and `pyproject.toml`, which also holds the version that a release's tag must match (DR-149), are outside this rule. OpenSpec is a Node program, so `package.json` and `package-lock.json` stay for development only, and nothing from them ships to adopters or runs in a release.

## Alternatives

- Holding the whole repository to Python and Markdown, which would leave no place for the shell scripts and configuration that only develop and check the tool, such as `scripts/verify-openspec.sh` and `package.json`.
- Writing the tool in Rust, the owner's own preference, set aside until the owner decides otherwise.

## Consequences

- The release workflow does its work in Python scripts, and its YAML only starts them (the design's decision 11).
- Node is needed only for the OpenSpec CLI, as `CONTRIBUTING.md` says: CI's `openspec` job sets Node up to run `npm ci` and `scripts/verify-openspec.sh`, and `.claude/hooks/session-start.sh` runs the same `npm ci`. `package.json` is marked private and calls itself pinned tooling, not a package.
- A release tool in Node or Go, such as one that writes the changelog from commit messages, falls outside what a release may be written in (DR-098).
- What every adopter adds to their repository keeps to this rule: the hook file, in Python; its registration in Claude Code's settings and the configuration file `.pr-cost.json`, in JSON; and a workflow that calls the tool's, in YAML. Task 4.4 has the README name what else an adopter sets, each in the format of the tool that reads it: each person's opt-in, `pr-cost.capture` in their own git configuration (DR-048), and, in some repositories, a `.pr-cost/** -text` line in `.gitattributes` where git's `core.safecrlf` is on, `.pr-cost/` left out of the repository's own git hooks, and git's sparse index turned off where it is on (DR-037).

## Scope

This covers what the tool, its release and its documentation are written in, and that nothing from OpenSpec's Node files ships to adopters or runs in a release. That the hook and the report use nothing beyond Python's standard library is DR-023 (The hook and the report use Python's standard library only), and how OpenSpec is pinned and checked is DR-042 (OpenSpec is pinned and its skills are regenerated in CI).

## What reversing it would change

The design's decision 11 would change, and so would the line of `CLAUDE.md`'s section on compatibility and releases that keeps the tool, its release and its documentation to Python and Markdown, and `CONTRIBUTING.md`'s note on Node. DR-098, whose alternative needed a Node or Go program, would be revisited. Letting another language into the release or the documentation would change nothing in the public surface, so that change would not be a breaking one for adopters; if it reached the script that writes each release's bill of materials, R28 in `releases-and-compatibility`, which names a Python script for it, would change too. Writing the tool itself in another language, such as Rust, would mean rewriting the hook and the report. It would change the requirements whose text or scenarios name the Python that they run on, or its JSON reader: R5, R12 and R13 in `usage-capture`, R35 in `report-comment`, and R25, R26, R28, R32, R99 and R122 in `releases-and-compatibility`. It would also change the design's decisions 1, 2, 6, 7 and 10, and the threats, tasks and pages that name that Python. Those requirements and threats are each listed by the records that shape them directly, such as DR-023 and DR-025, so this record lists none of them. DR-023, DR-025, DR-026, DR-027, DR-125 and DR-134, whose titles name Python, would be revisited. The Python floor is part of the public surface (R122), so that change would be a breaking one for adopters (DR-096).
