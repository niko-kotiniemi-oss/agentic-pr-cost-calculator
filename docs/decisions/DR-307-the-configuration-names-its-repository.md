# DR-307: The configuration names its repository, so a fork records nothing until its owner turns the tool on there

- **Type:** security and privacy
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the owner, 2026-11-12
- **Requirements:** R296, R308, R309
- **Threats:** T313, T322
- **Replaces:** none
- **Closed by:** none

## Context

A fork copies the repository's files, its configuration among them, so a fork of a repository that turns the tool on would turn it on too: its owner's and its contributors' sessions would be recorded there, and its merges reported, though its owner never chose the tool.

## Decision

The configuration file names the repository that it turns the tool on in, as `owner/name`, under the key `repository`, which a file that enables the tool must hold in GitHub's form, compared with the case of ASCII letters alone folded (R296). Capture records nothing where that name differs from the one that the clone's `origin` remote gives, read as `git remote get-url origin` gives it, offline and without the session's `GIT_` variables, on `github.com`, and says so once a session on standard error (R308). The report posts no comment where it differs from the repository that the workflow runs in, unless GitHub gives the configured name that repository's id, as after a rename or a transfer, and quotes neither name (R309). A fork's owner turns the tool on there by naming the fork.

## Alternatives

- Leaving forks as they are: a fork would publish usage that its owner never chose to.
- Asking GitHub whether the repository is a fork: capture opens no network connection (R30), so it could not ask.

## Consequences

- After a rename or a transfer, the report still posts its comment and says that the configuration gives an earlier name, while a clone whose `origin` gives the name that the configuration does not records nothing until one of them is updated, which the README tells adopters to do.
- A contributor who works in a clone of their fork records nothing there, so their usage from a fork is not counted, as the owner chose.
- The configuration's new key, `repository`, is part of the public surface (R122), and ships in the first release.
- A GitHub Enterprise Server records nothing, as the tool is for GitHub.com alone (DR-006).

## Scope

This covers when a fork records and is reported. How a person opts in is the opt-in's own records.

## What reversing it would change

How hard it is to reverse: reversible with work. R296 and its scenarios, the configuration's format and the surface manifest would change, and the README's short start would no longer ask adopters to name their repository.
