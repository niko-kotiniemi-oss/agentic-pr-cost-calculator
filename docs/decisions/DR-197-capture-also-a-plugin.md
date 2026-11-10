# DR-197: The capture step also comes as a Claude Code plugin, beside the hook file that adopters copy

- **Type:** architecture
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-01
- **Requirements:** R12, R90, R179, R188
- **Threats:** T8, T59, T131, T135, T141
- **Replaces:** none
- **Closed by:** none

## Context

Capture runs as a hook that the repository's own settings register, from a hook file that adopters copy into the repository (DR-022, DR-172). A cloud thread of a project loads only a repository's `CLAUDE.md` files and its rules, and runs none of the hooks that the repository's settings register, so a project's cloud threads record nothing (A61). The owner said on 2026-11-01 that capture in a project's cloud threads is a key feature, to be supported. Claude Code loads into each new cloud thread of a project the plugins that the person adds in the project's settings, and into the person's terminal sessions signed in with claude.ai the plugins turned on for their claude.ai account, those that their organization turns on among them. A test plugin on 2026-11-09 saw its hooks run in a project's cloud threads, at the same events as a repository's hooks, with the hook condition `Bash(git *)` holding, which A69 records as not yet checked until task 7.2 checks it.

Claude Code copies most plugins into its cache, and runs a copied plugin's hooks with the copy's folder as `CLAUDE_PLUGIN_ROOT`, but it loads some in place, as with `--plugin-dir`, from a skills folder or from a marketplace added by a local path, and gives those their source folder. A plugin's manifest can also declare MCP servers, monitors and plugins that it depends on, and its hooks file can hold HTTP hooks as well as commands (A69).

## Decision

The tool also ships its capture step as a Claude Code plugin, beside the hook file that adopters copy. The plugin's hooks run the same file, from the plugin's own folder, for the same events, with the same condition and timeouts as the hook file's registration, through a command that names the plugin form, carries the SHA-256 of the plugin's capture step and runs it only when it matches, with each CRLF taken as LF, exits with success and prints nothing on standard output, in each shell that Claude Code runs a hook's command in. The plugin declares nothing but those hooks: its manifest holds only its name, version, description, author, licence and repository, its hooks are all command hooks, and each commit builds it with the hook file, byte for byte, as its capture step, never from the folder that the marketplace serves (DR-204). Its run at a session's end keeps within the budget that Claude Code gives a plugin's `SessionEnd` hooks, which a plugin's own timeout does not raise. The plugin records nothing unless the repository turns the tool on and the opt-in holds, as for the hook file (DR-202). A repository that turns the tool on still copies the hook file, so that the sessions of everyone who works in it run capture, whether or not they have the plugin.

## Alternatives

- The plugin alone, in place of the hook file, which would leave a repository's contributors who do not have the plugin unrecorded in every session, and would leave the report no hook file of the repository's own to compare with the report's commit.
- A hook that the environment's setup script writes into the person's own Claude Code settings, which a cloud session does not read.
- The hook file alone, which leaves a project's cloud threads unrecorded.
- A plugin command with no checksum, since a copied plugin's folder is not the working tree, which would run whatever a plugin loaded in place from a clone holds once a branch checked out there changes it.
- A manifest that may declare more than the hooks, which would let the plugin run what neither its zip's list of files, its checksum nor the bill of materials shows.

## Consequences

- A project's cloud threads, and the person's terminal sessions in repositories that register no hook, run capture when the person has the plugin.
- A copied plugin runs the step from a folder that no checked-out branch changes, while one loaded in place runs it from its source folder, so the plugin's command carries the step's checksum, as the hook file's registration does (DR-211), and runs none of a changed file, and the README says to install the plugin only from a release's zip or from this repository's GitHub address (T59).
- CI and the release workflow fail where, in the plugin that a commit builds, the manifest holds another key, a hook is not a command or the capture step differs from the hook file, so that the plugin runs only the step that the zip's checksum and the bill of materials name (T141).
- A plugin's session-end run has less time than the hook file's can have, so it takes back and puts back first, as every run does, and leaves to a later run what it cannot read within that budget.
- In a project's cloud thread, a machine that pauses after a turn resumes with its files, the store among them, while one that cannot be resumed continues from a fresh clone, which holds no store, so the calls that waited for a commit there are lost (T131).
- Claude Code registers the hooks of one plugin per name: the copy that managed settings turn on, or else the copy that it loads first, so a plugin of the same name from another origin, such as one that a repository's settings turn on, can run in place of the person's copy (T135).

## Scope

This covers how capture reaches a session that runs no repository hook, and what the plugin declares. Which repositories a run of the plugin works on is DR-198 (A plugin run works on each repository that it meets), whose opt-in it needs is DR-202, how the plugin is installed is DR-203, and how a session that runs both the plugin and the hook file records each call once is DR-206 (Two copies of the capture step in one session share the store). How adopters copy the hook file is DR-022 (Adopters copy the hook file from a pinned commit).

## What reversing it would change

R179 in `usage-capture` and R188 in `releases-and-compatibility` would be removed, with their scenarios, and R90 and R12 would change, and so would the design's decision 17, DR-198, DR-203, DR-204, DR-205, DR-206 and DR-207, which would be closed or revisited, T8's residual, T59's answer, T131, T135, T141 and boundary 9 of the threat model, the README's sections on cloud threads and on installing the plugin, and the tasks that build and check the plugin. The plugin's name and its hooks are part of the public surface, so removing the plugin would be a breaking change for adopters (DR-096).
