# DR-197: The capture step also comes as a Claude Code plugin, beside the hook file that adopters copy

- **Type:** architecture
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-01
- **Requirements:** R12, R90, R179
- **Threats:** T8, T131, T135
- **Replaces:** none
- **Closed by:** none

## Context

Capture runs as a hook that the repository's own settings register, from a hook file that adopters copy into the repository (DR-022, DR-172). A cloud thread of a project loads only a repository's `CLAUDE.md` files and its rules, and runs none of the hooks that the repository's settings register, so a project's cloud threads record nothing (A61). The owner said on 2026-11-01 that capture in a project's cloud threads is a key feature, to be supported. Claude Code loads into each new cloud thread of a project the plugins that the person adds in the project's settings, and into the person's terminal sessions signed in with claude.ai the plugins turned on for their claude.ai account, those that their organization turns on among them. A test plugin on 2026-11-09 showed its hooks running in a project's cloud threads, at the same events as a repository's hooks, with the hook condition `Bash(git *)` holding.

## Decision

The tool also ships its capture step as a Claude Code plugin, beside the hook file that adopters copy. The plugin's hooks run the same file, from the plugin's own folder, for the same events and with the same condition as the hook file's registration, through a command that names the plugin form, exits with success and prints nothing on standard output, in each shell that Claude Code runs a hook's command in. Its run at a session's end keeps within the budget that Claude Code gives a plugin's `SessionEnd` hooks, which a plugin's own timeout does not raise. The plugin records nothing unless the repository turns the tool on and the opt-in holds, as for the hook file (DR-202). A repository that turns the tool on still copies the hook file, so that the sessions of everyone who works in it run capture, whether or not they have the plugin.

## Alternatives

- The plugin alone, in place of the hook file, which would leave a repository's contributors who do not have the plugin unrecorded in every session, and would leave the report no hook file of the repository's own to compare with the report's commit.
- A hook that the environment's setup script writes into the person's own Claude Code settings, which a cloud session does not read.
- The hook file alone, which leaves a project's cloud threads unrecorded.

## Consequences

- A project's cloud threads, and the person's terminal sessions in repositories that register no hook, run capture when the person has the plugin.
- The plugin runs the step from its own folder, which a checked-out branch does not change, so its command carries no checksum, while the hook file's registration still does (DR-058).
- A plugin's session-end run has less time than the hook file's can have, so it takes back and puts back first, as every run does, and leaves to a later run what it cannot read within that budget.
- In a project's cloud thread, a machine that pauses after a turn resumes with its files, the store among them, while one that cannot be resumed continues from a fresh clone, which holds no store, so the calls that waited for a commit there are lost (T131).
- Claude Code loads one plugin of a given name, and a plugin of the same name from another origin, such as one that a repository's settings turn on, comes before the copy synced from the person's claude.ai account (T135).

## Scope

This covers how capture reaches a session that runs no repository hook. Which repositories a run of the plugin works on is DR-198 (A plugin run works on each repository that it meets), whose opt-in it needs is DR-202, how the plugin is installed is DR-203, and how a session that runs both the plugin and the hook file records each call once is DR-206 (Two copies of the capture step in one session share the store). How adopters copy the hook file is DR-022 (Adopters copy the hook file from a pinned commit).

## What reversing it would change

R179 in `usage-capture` would be removed, with its scenarios, and R90 and R12 would change, and so would the design's decision 17, DR-198, DR-203, DR-204, DR-205 and DR-206, which would be closed or revisited, T8's residual, T131, T135 and boundary 9 of the threat model, the README's sections on cloud threads and on installing the plugin, and the tasks that build and check the plugin. The plugin's name and its hooks are part of the public surface, so removing the plugin would be a breaking change for adopters (DR-096).
