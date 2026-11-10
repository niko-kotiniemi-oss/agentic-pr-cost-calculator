# DR-198: A plugin run works on each repository that it meets

- **Type:** architecture
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R54, R76, R180, R197
- **Threats:** T2, T19, T46, T108, T129, T144
- **Replaces:** none
- **Closed by:** none

## Context

A run of the hook file's registration works on one repository, the one that holds the project directory that Claude Code gives the hook, whatever directory Claude has moved to, since the hook belongs to that repository and its settings register it. The plugin belongs to the person instead, and runs in every session that loads it (DR-197). A project's cloud thread starts in a folder that holds each of its clones directly inside it, and that folder is in no repository, so no repository holds its project directory (A70), and a run that worked only on that repository would work on none. Capture keeps a call for a repository when the working directory that its transcript line names is in that repository (DR-057), and a run comes before each git command, so that a call goes to the branch that was checked out when it was made, not to one that the command checks out (DR-012, DR-030).

## Decision

A run of the plugin works first on the repository where each git command of its input that the hook's condition matches runs, read as a run reads where a commit runs, then on the repository that holds the hook input's working directory, then on the repository that holds the project directory or, when no repository holds it, on each repository whose top level is directly inside it, in the order of their paths. It finds each by reading the git files on the way itself, as a run finds its own repository, before it starts any program, and leaves out one whose files it cannot read, saying so on standard error in its own words. In each of the others it does what a run of the hook file's registration does in its own repository: it reads both switches there, begins and ends that repository's intervals, records only the calls made from that repository, and stages, takes back and puts back there, and it never starts a git that the working trees or the git common directory of any of them holds, or that the folder of one that it left out holds. Outside the repository that holds the project directory, it starts a git command that reads a repository's index or attributes, as staging, a take-back and a put-back do, only where a git command of its input runs, or to take back a ledger file that its own session staged there, and leaves any other take-back or put-back to the first run that may make it. A run of the hook file's registration still works only on the repository that holds the project directory.

## Alternatives

- Working only on the repository that holds the project directory, as the hook file's registration does, which in a project's cloud thread is none.
- Working on every repository anywhere below the project directory, which would have a run walk a folder tree of any size within its time budget.
- Working only on the repository that holds the hook input's working directory, which in a project's cloud thread is none until Claude moves into a clone, so that the start run would begin no interval and the thread's first calls in a clone would be left out.
- Meeting a git command's repository only for a commit, which would let `git -C <path> switch` in another repository send that repository's waiting calls to the new branch.
- Stopping the whole run when one repository's files cannot be read, which would let one unusual clone stop every record, stage and take-back in the others.
- Reading the index in each repository that a run meets, as a run of the hook file's registration does in its own, which would have git start a program that the configuration of a clone where the session never ran git names, such as `core.fsmonitor`, from the session's start run on (T144).
- Reading the index also in the repository that holds Claude's current directory, which a folder that Claude only moves into, such as one unpacked from an archive, would reach the same way.

## Consequences

- In a project's cloud thread, the start run begins an interval in each clone that turns the tool on, and when it comes before the thread's first prompt is written, as a test plugin saw on 2026-11-09, which A70 records as not yet checked until task 7.2 checks it, the calls that the thread then makes in that clone are recorded from its first turn.
- A git command's repository comes first, so a command that changes the branch of another repository, as `git -C <path> switch` does, finds that repository's waiting calls recorded on the branch checked out before it, within the run's time budget (T19, T108).
- A repository elsewhere, or deeper inside the project directory, is met only by a run whose working directory is in it or whose git command runs in it, so the calls that the session made there before that run are left out, and flagged for consent (DR-200).
- In each repository, only the calls whose line gives a working directory in it are recorded (DR-057), so a run that works on several repositories records each call in one repository at most: the one that holds the directory that its line names, which is Claude's current directory, whatever repository the call works on (T2).
- The repositories that a project directory holds come in the order of their paths, so that what a run reaches within its budget does not depend on the order in which the system lists them, and one whose files the run cannot read is left out while the others are served, with the `PATH` entries inside its folder still skipped, though not those inside its linked worktrees elsewhere, which the run cannot know (T46).
- With the plugin, the person's opt-in covers every repository that turns the tool on where Claude works or runs git in any of their sessions, not only those whose own settings register the hook, which the README says (DR-185, T129).
- A run that works on several repositories shares one time budget among them, leaving what it has not read for a later run, and a line that a whole budget cannot read is skipped by the next run and counted as refused in each repository that it works on.
- A ledger file that a run staged for a refused commit in a repository that the session then leaves stays staged until a later run of that session meets that repository, or a session runs git there, and the README says how to look for one and take it back.
- A repository that the session only meets, or moves into without running git there, has git start none of the programs that its configuration names, such as `core.fsmonitor`, since the git commands that read the opt-in and find the store start none (A21), so its intervals still begin and its calls are still recorded, while another session's ledger file left staged there waits for a run before or after a git command of a session there (T144).

## Scope

This covers which repositories a run of the plugin works on, and in what order. Which calls count as a repository's is DR-057 (Calls are kept by the session's working directory), what happens to a call whose repository cannot be told is DR-199 (A call whose repository cannot be told is left out), and how the step finds git is DR-188 (The hook starts only git, by absolute path, from a safe folder, without the session's git variables).

## What reversing it would change

R180 and R197 in `usage-capture` would be removed or changed, with their scenarios, and so would R76 and R54, the design's decision 17, the answers of T2, T19, T46, T108, T129 and T144, the README's section on cloud threads, which task 4.4 writes, and the tasks that build and check the plugin. A plugin that works only on the repository that holds the project directory would record nothing in a project's cloud threads.
