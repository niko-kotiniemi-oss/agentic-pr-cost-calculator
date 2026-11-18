# DR-222: A command that writes each pull request's cost as a file is left to a change after the first build

- **Type:** scope
- **Status:** accepted
- **Decided by:** the owner, 2026-11-01
- **Requirements:** R206, R207
- **Threats:** T161
- **Replaces:** none
- **Closed by:** none

## Context

The owner's first brief asked that a pull request's cost be stored in a small file in the repository, optionally, and at least as a short report comment. The ledger holds usage, not cost (DR-015), and the report writes nothing to the repository (DR-016), so the cost is kept only in the comment. After a merge, only a commit to the default branch can add such a file: one that someone makes, or one that a job with write access to the default branch makes. On 2026-11-01 the owner chose a command.

## Decision

A command, built in a change of its own after the first build, lists pull requests' costs and writes each as a small Markdown file in a folder that the adopter chooses, which reaches the repository through an ordinary pull request. The report still writes nothing. The roadmap lists it under Next as planned.

## Alternatives

- An opt-in job with write access to the default branch, which would give the report's workflow a write token.
- The file written by the report itself, which DR-016 rules out.

## Consequences

- The first build does not grow by the command, and the comment stays the only place that the first version keeps a cost.
- The command's change brings its own spec and threat review, since it reads posted comments or recomputes costs and writes files that a person commits.

## Scope

This covers when and in what form a pull request's cost becomes a file. What the report writes is DR-016 (The report writes nothing to the repository).

## What reversing it would change

The roadmap's Next and design decision 12 would change, and DR-016 would be revisited if the report itself were to write the file.
