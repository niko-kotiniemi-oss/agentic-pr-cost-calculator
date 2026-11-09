# DR-198: A plugin run works on each repository that it meets

- **Type:** architecture
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R54, R76, R180
- **Threats:** T2, T129
- **Replaces:** none
- **Closed by:** none

## Context

A run of the hook file's registration works on one repository, the one that holds the project directory that Claude Code gives the hook, whatever directory Claude has moved to, since the hook belongs to that repository and its settings register it. The plugin belongs to the person instead, and runs in every session that loads it (DR-197). A project's cloud thread starts in a folder that holds each of its clones directly inside it, and that folder is in no repository, so no repository holds its project directory (A70), and a run that worked only on that repository would work on none. Capture keeps a call for a repository when the working directory that its transcript line names is in that repository (DR-057).

## Decision

A run of the plugin works on the repository that holds the project directory or, when no repository holds it, on each repository whose top level is directly inside it; on the repository that holds the hook input's working directory; and, before or after a commit, on the repository where the commit runs. It finds each by reading the git files on the way itself, as a run finds its own repository, before it starts any program. In each of them it does what a run of the hook file's registration does in its own repository: it reads both switches there, begins and ends that repository's intervals, records only the calls made from that repository, and stages, takes back and puts back there, and it never starts a git that the working trees or the git common directory of any of them holds. A run of the hook file's registration still works only on the repository that holds the project directory.

## Alternatives

- Working only on the repository that holds the project directory, as the hook file's registration does, which in a project's cloud thread is none.
- Working on every repository anywhere below the project directory, which would have a run walk a folder tree of any size within its time budget.
- Working only on the repository that holds the hook input's working directory, which in a project's cloud thread is none until Claude moves into a clone, so that the start run would begin no interval and the thread's first calls in a clone would be left out.

## Consequences

- In a project's cloud thread, the start run begins an interval in each clone that turns the tool on, and when it comes before the thread's first prompt is written, as it did twice in the threads seen on 2026-11-09 (A70), the calls that the thread then makes in that clone are recorded from its first turn.
- A repository elsewhere, or deeper inside the project directory, is met only by a run whose working directory is in it or whose commit runs in it, so the calls that the session made there before that run are left out, and flagged for consent (DR-200).
- In each repository, only the calls whose line gives a working directory in it are recorded (DR-057), so a run that works on several repositories records each call in one repository at most, and a call made in one repository is never published in another's ledger (T2).
- With the plugin, the person's opt-in covers every repository that turns the tool on where Claude works or commits in any of their sessions, not only those whose own settings register the hook, which the README says (DR-185, T129).
- A run that works on several repositories shares one time budget among them, leaving what it has not read for a later run.

## Scope

This covers which repositories a run of the plugin works on. Which calls count as a repository's is DR-057 (Calls are kept by the session's working directory), what happens to a call whose repository cannot be told is DR-199 (A call whose repository cannot be told is left out), and how the step finds git is DR-188 (The hook starts only git, by absolute path, from a safe folder, without the session's git variables).

## What reversing it would change

R180 in `usage-capture` would be removed or changed, with its scenarios, and so would R76 and R54, the design's decision 17, T2's answer, T129, the README's section on cloud threads, which task 4.4 writes, and the tasks that build and check the plugin. A plugin that works only on the repository that holds the project directory would record nothing in a project's cloud threads.
