# DR-207: This repository turns the tool on only from a project that holds this repository alone

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the owner, 2026-11-09
- **Requirements:** R185
- **Threats:** T2, T32, T128
- **Replaces:** none
- **Closed by:** none

## Context

Task 7.1 turns the tool on in this repository, with the owner's own opt-in, so that its own merges carry ledger files and the report runs on them. A call is recorded in the repository that holds the directory that its transcript line names, which is Claude's current directory, whatever repository the call works on (DR-057, T2). A project's cloud thread starts in a folder that holds each of the project's clones, and once Claude moves into one clone it can read and change another through its path or with `git -C`, and those calls are recorded in the clone that Claude is in. This repository's work has been done from a project that also holds a private repository of the owner's, and `CLAUDE.md` says that this repository never holds cost figures measured on someone's private work. On 2026-11-09 the owner chose to give this repository a project of its own, over keeping the shared project with a rule that agents keep other repositories' work out of sessions here.

## Decision

Task 7.1 turns the tool on in this repository only from a project that holds this repository alone, and the owner's work on this repository moves to such a project before then. The README's section on cloud threads says that a call made from one clone counts there, whatever clone it works on, so that a project that holds a repository that turns the tool on should hold no repository whose work must stay private (R185).

## Alternatives

- The same project as now, with a rule that agents keep the other repositories' work out of sessions whose directory is in this repository, which would rest on every session following that rule, since no check over the transcript's working directories can tell such calls apart.
- Leaving the tool off here, which would leave the tool's own pull requests without a report, and task 7.1 without its check.

## Consequences

- In that project's threads, no call made from this repository's clone on another repository of the owner's can be published here, since no other repository is in that project, and DR-210 (The owner's opt-in for this repository is set only in the environment of its own project) keeps the owner's opt-in out of the other sessions that could reach this clone beside another (T2, T32).
- The calls made from the folder that holds the project's clones are still left out and flagged, as in any project (T128).
- The move is an open point for task 7.1: until the tool is on here, nothing changes.

## Scope

This covers from where this repository's own sessions run once the tool is on here. Which calls count as a repository's is DR-057 (Calls are kept by the session's working directory), and which repositories a plugin run works on is DR-198 (A plugin run works on each repository that it meets).

## What reversing it would change

Task 7.1 would change, and the README's advice to adopters would stay, since it holds for any project that holds a repository that turns the tool on.
