# DR-098: The changelog is kept by hand

- **Type:** process
- **Boundary:** outgoing
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** none
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

`CHANGELOG.md` keeps one entry per release, in the Keep a Changelog form, and the release check reads those entries (DR-149). The tool, its release and its documentation keep to Python and Markdown (DR-024).

## Decision

The changelog's entries are written by hand: every change that an adopter would notice gets a line under `## [Unreleased]` in the pull request that makes it.

## Alternatives

- A release tool that writes the changelog from commit messages, which needs a Node or Go program and the commit-message conventions to go with it.

## Consequences

- The changelog needs no convention for commit messages, and no program beyond the repository's own Python.
- The pull request template asks for the line, but no check reads whether a change that adopters would notice has one. The release check reads only that the version has an entry, and how its `### Breaking` section fits the major number and the surface manifest.

## Scope

This covers how the entries are written. Where the version is kept and the form the entries take is DR-149 (`pyproject.toml` holds the version, and the changelog has one entry per release), how the version number is chosen is DR-096 (Versions are semantic), and how the release check finds a breaking change is DR-123 (The release check compares a manifest of the public surface).

## What reversing it would change

No requirement would change: the form that DR-149 sets can be written by a program as well as by hand. The design's decision 11, the line of `CLAUDE.md` that asks for a changelog line, step 4 of `CONTRIBUTING.md` and the pull request template's item for it would change, since the line would then come from a commit message rather than from the pull request that makes the change. A tool in Node or Go would also mean revisiting DR-024. The changelog is not part of the public surface, so the change would not be a breaking one for adopters.
