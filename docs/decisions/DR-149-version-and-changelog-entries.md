# DR-149: `pyproject.toml` holds the version, and the changelog has one entry per release

- **Type:** process
- **Boundary:** outgoing
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R27, R71, R123
- **Threats:** T53
- **Replaces:** none
- **Closed by:** none

## Context

A release is made from a tag that carries its version number (DR-148), and the release check reads the version and the changelog at that tag: it refuses a tag whose version differs from the one the repository holds, or that has no entry (R27), and a release whose public surface changed without a raised major number and a `### Breaking` section (R123). Adopters' update bots let a minor or patch release through as safe (T53).

## Decision

`pyproject.toml` holds the version and `CHANGELOG.md` keeps one entry per release, in the Keep a Changelog form. A release's entry gathers any breaking change under a heading of its own, `### Breaking`.

## Alternatives

None were recorded when this was decided.

## Consequences

- `pyproject.toml` is the one source of the version, so the tag and the changelog entry are compared with one source, and the bill of materials names the same number (R27, R28).
- The release's own text carries the changelog entry after the release workflow's fixed words (R27).
- The release check reads the entry's `### Breaking` section, so what it finds there rests on the changelog keeping this form (T53, DR-123).
- A test holds that the version in `pyproject.toml` is three numbers separated by dots and that `CHANGELOG.md` has an `## [Unreleased]` section, which is where a change that adopters would notice gets its line before any release (DR-098).

## Scope

This covers where the version is kept and the form the changelog takes. That the entries are written by hand is DR-098 (The changelog is kept by hand), how the version number is chosen is DR-096 (Versions are semantic), how a release is made from a tag is DR-148 (Each release is made from a tag), and how the release check holds a changed public surface to a raised major number is DR-123 (The release check compares a manifest of the public surface).

## What reversing it would change

R27 in `releases-and-compatibility` would change in its clauses on `pyproject.toml` and `CHANGELOG.md`, with its scenarios "A tag that matches the version and the changelog is released" and "A tag that does not match the version is refused", and so would R71's sentence on a `### Breaking` section and R123's requirement of one, with its scenario "A changed public surface needs a major version". The design's decision 11, T53's answer, task 6.1, `CHANGELOG.md` itself, the version in `pyproject.toml`, the version and changelog test in `tests/test_repository.py`, step 4 of `CONTRIBUTING.md`, the pull request template's item for a changelog line, the line of `CLAUDE.md` that asks for one, the release flow in `docs/how-it-works.md` and the feature page's account of releases would change too. DR-098, whose entries take this form, DR-116, whose changelog follows it, DR-123, whose check reads the `### Breaking` section, and DR-148, whose release compares the tag with the version and the changelog, would be revisited. Neither the changelog nor the file that holds the version is part of the public surface, so the change would not be a breaking one for adopters.
