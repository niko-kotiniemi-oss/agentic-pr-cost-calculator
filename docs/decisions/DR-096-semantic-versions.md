# DR-096: Versions are semantic

- **Type:** process
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the owner, 2026-10-20
- **Requirements:** R27, R71, R123
- **Threats:** T44, T53, T56
- **Replaces:** none
- **Closed by:** none

## Context

The tool is consumed by other repositories, so each version is a release whose number says what an adopter must do. Adopters' update bots treat minor and patch releases as safe (T53). R71 counts any change to the public surface (DR-154) as one that adopters must act on, and the release check that task 6.1 writes holds the major number to it (DR-123).

## Decision

Versions are semantic: a breaking change raises the major number, a change that adds behaviour the minor number, and a fix alone the patch number.

## Alternatives

None were recorded when this was decided.

## Consequences

- Every part of the public surface, the store's format and the Python and git floors among them, changes only in a new major version (T44, T56).
- Whether a version's minor or patch number fits its change is left to the owner's review rather than to a test (`docs/features/releases-and-compatibility.md`).

## Scope

This covers how versions are numbered. That each release is made from a tag that carries its number is DR-148 (Each release is made from a tag), which parts make up the public surface is DR-154 (The public surface is what adopters configure or depend on), how the release check holds the major number to that surface is DR-123 (The release check compares a manifest of the public surface), and where the version is kept and how a changelog entry marks a breaking change is DR-149 (`pyproject.toml` holds the version, and the changelog has one entry per release).

## What reversing it would change

R71 in `releases-and-compatibility` would change, with its scenario, and so would R27's semantic tag, with its scenario "A tag that is not a semantic version stops the workflow first", and R123's raised major number, with its scenario. So would the design's decision 11, the answers of T44, T53 and T56, task 6.1, the version test in `tests/test_repository.py`, the release flow in `docs/how-it-works.md`, the feature page's account of versions, the proposal's list of what changes, the README, `CHANGELOG.md` and `CLAUDE.md`. The numbering itself is not part of the public surface, though what adopters' bots let through depends on it. DR-040, DR-123, DR-148, DR-149 and DR-154 would be revisited, and so would the records that cite this one when they say that reversing them would be a breaking change for adopters.
