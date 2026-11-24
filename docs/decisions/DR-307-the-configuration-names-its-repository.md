# DR-307: The configuration names its repository, so a fork records nothing until its owner turns the tool on there

- **Type:** security and privacy
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the owner, 2026-11-12
- **Requirements:** R296
- **Threats:** T313
- **Replaces:** none
- **Closed by:** none

## Context

A fork copies the repository's files, its configuration among them, so a fork of a repository that turns the tool on would turn it on too: its owner's and its contributors' sessions would be recorded there, and its merges reported, though its owner never chose the tool.

## Decision

The configuration file names the repository that it turns the tool on in, as `owner/name`. Capture records nothing where that name differs from the one that the clone's `origin` remote gives, read from git's configuration with no network, and the report posts no comment where it differs from the repository that the workflow runs in, and says so in its job summary (R296). A fork's owner turns the tool on there by naming the fork.

## Alternatives

- Leaving forks as they are: a fork would publish usage that its owner never chose to.
- Asking GitHub whether the repository is a fork: capture opens no network connection (R30), so it could not ask.

## Consequences

- A repository that is renamed turns the tool off until its configuration names it again, and the report's job summary says why.
- A contributor who works in a clone of their fork records nothing there, so their usage from a fork is not counted, as the owner chose.
- The configuration's new key is part of the public surface (R122).

## Scope

This covers when a fork records and is reported. How a person opts in is the opt-in's own records.

## What reversing it would change

How hard it is to reverse: reversible with work. R296 and its scenarios, the configuration's format and the surface manifest would change, and the README's short start would no longer ask adopters to name their repository.
