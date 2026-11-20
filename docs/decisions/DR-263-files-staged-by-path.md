# DR-263: Files are staged by their paths, never by a folder, a pattern or all at once

- **Type:** security and privacy
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-27
- **Requirements:** none
- **Threats:** T32
- **Replaces:** none
- **Closed by:** none

## Context

On 2026-10-27 the owner asked that agents never stage files with `git add *`, and backlog item B-003 asks for a rule, with its record, that files are staged by name, never all at once. This repository is public, and a working tree holds files that no commit should take: a scratch file, a tool's output, a file in a folder that git does not ignore, or a personal `CLAUDE.local.md`. A command that stages a folder, a pattern or everything takes such a file with the change, and a commit pushed to a branch here is public at once, before any check of the pull request runs (T32).

## Decision

An agent stages each file by its path, never a folder, a pattern or everything at once: no `git add .`, `-A`, `-u` or `*`, and no `git commit -a`. The root `CLAUDE.md` gives this rule in its section on what an agent never does here.

## Alternatives

- A rule against `git add *` alone: `git add .`, `git add -A` and `git commit -a` take the same files.
- A check in CI of what a commit adds: it runs only after the push, when the file is already public.
- A hook that refuses such a command: a project's cloud thread runs none of the hooks that the repository's settings register (A61), and the owner's sessions here run in such threads.

## Consequences

- A commit holds only the files that the agent named, and a file that it did not mean to commit stays out of the commit.
- A change of many files names each, which also shows in the session what the commit takes.

## Scope

This covers how an agent stages files for a commit here. What the repository may hold is DR-069 (The public repository holds no private data).

## What reversing it would change

How hard it is to reverse: reversible. The rule is a sentence of the root `CLAUDE.md`, and the answer of T32 would change.
