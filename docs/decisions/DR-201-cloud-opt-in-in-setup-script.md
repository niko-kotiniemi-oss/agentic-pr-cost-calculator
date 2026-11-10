# DR-201: In a cloud environment, a person opts in with one line in the environment's setup script

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the owner, 2026-11-09
- **Requirements:** R1, R185, R194
- **Threats:** T3, T134
- **Replaces:** none
- **Closed by:** none

## Context

The opt-in is `pr-cost.capture` in the global git configuration of the user who runs the session (DR-183). A cloud session runs on a machine that is built for it from its cloud environment, and the global git configuration there is written by Claude Code's own setup, not by the person. A cloud session reads neither the person's own Claude Code settings nor the settings that a plugin keeps there for its options, so neither can carry the opt-in into it. A cloud environment's setup script runs as root before Claude Code starts, the first time a session starts in the environment, and the files that it writes are the starting point of the environment's later sessions until the script changes. It does not run again when a paused machine is restored, so a change to it reaches a session that is running only once its machine is rebuilt, while the environment's variables are read again at each restore (A71). The owner asked on 2026-11-09 for the easiest well-accepted way for a person to turn capture on, such as a setup script or a command, and the same day a new cloud thread found the line below, which the setup script of the owner's environment gave, in its global git configuration.

## Decision

In a cloud environment, a person turns capture on with one line in the environment's setup script, `git config --global pr-cost.capture true`, which writes the opt-in to the global git configuration of each new session in that environment. How capture reads the opt-in does not change (DR-183), and the line opts in only the sessions that run in that environment. Since removing the line reaches only the sessions that start, or whose machines are rebuilt, afterwards, the README gives two opt-outs that reach a session that is running: `git config --global pr-cost.capture false` in that session, which holds until something writes the opt-in again, as the setup script does on a machine that is rebuilt and an organization's hook can at a session's start or resume, and the environment's variables `GIT_CONFIG_COUNT=1`, `GIT_CONFIG_KEY_0=pr-cost.capture` and `GIT_CONFIG_VALUE_0=false`, which each of its sessions reads at its next restore, which git's reading of the opt-in in the session's own environment finds, and which hold unless a settings file that the session loads sets `GIT_CONFIG_COUNT` itself, as long as the `GIT_CONFIG_` variables that a cloud session sets for itself leave them in force (A71). The README gives them for an environment that sets no other such variable, and says what can undo each.

## Alternatives

- A setting of the plugin's own, which Claude Code keeps in the person's own settings, which a cloud session does not read.
- Taking the plugin's presence as the opt-in, which an organization can put there for its members (DR-202).
- An environment variable that the environment sets as the opt-in, which capture does not read to turn capture on, since a repository's settings can set variables for everyone who works in it (DR-183), though git's reading of such a variable can turn capture off.
- A command of the tool's own that writes the opt-in, which would be one more program to install, where one git command does the same.

## Consequences

- The opt-in holds in every session that runs in the environment, in every repository that turns the tool on (DR-185), which the README says beside the line (R185).
- Removing the line, or moving to another environment, turns capture off only in the sessions that start, or whose machines are rebuilt, afterwards, while an idle thread can still wake to fix its pull request and commit. The README says so, gives the two opt-outs that reach a running session, either of which ends its intervals and empties the store at the next run (DR-169, DR-171), and says how a person sees a session's opt-in and where it comes from (R194).
- Whoever can edit the environment decides the opt-in of its sessions: the person for an environment of their own, an Owner of the organization for a shared one or the organization's default (DR-202, T134).

## Scope

This covers how a person opts in, and out, within a cloud environment. Where capture reads the opt-in is DR-183 (The opt-in is read only from the person's global git configuration, and git's own reading of it can only turn capture off), and who may set it is DR-202.

## What reversing it would change

R185 and R194 in `project-standards` would change, with their scenarios, and so would the design's decision 6, the README's sections on cloud threads and on turning capture off, which task 4.4 writes, the opt-in's feature page and A71. Nothing in the tool's code reads the setup script, so the change would be one of documentation.
