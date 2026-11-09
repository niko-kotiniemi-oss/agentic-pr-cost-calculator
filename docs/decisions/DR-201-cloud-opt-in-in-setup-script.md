# DR-201: In a cloud environment, a person opts in with one line in the environment's setup script

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the owner, 2026-11-09
- **Requirements:** R1, R185
- **Threats:** T3, T134
- **Replaces:** none
- **Closed by:** none

## Context

The opt-in is `pr-cost.capture` in the global git configuration of the user who runs the session (DR-183). A cloud session runs on a machine that is built for it from its cloud environment, and the global git configuration there is written by Claude Code's own setup, not by the person. A cloud session reads neither the person's own Claude Code settings nor the settings that a plugin keeps there for its options, so neither can carry the opt-in into it. A cloud environment's setup script runs as root before Claude Code starts, the first time a session starts in the environment, and the files that it writes are the starting point of the environment's later sessions until the script changes (A71). The owner asked on 2026-11-09 for the easiest well-accepted way for a person to turn capture on, such as a setup script or a command, and the same day a new cloud thread found the line below, which the setup script of the owner's environment gave, in its global git configuration.

## Decision

In a cloud environment, a person turns capture on with one line in the environment's setup script, `git config --global pr-cost.capture true`, which writes the opt-in to the global git configuration of each new session in that environment. How capture reads the opt-in does not change (DR-183), and the line opts in only the sessions that run in that environment.

## Alternatives

- A setting of the plugin's own, which Claude Code keeps in the person's own settings, which a cloud session does not read.
- Taking the plugin's presence as the opt-in, which an organization can put there for its members (DR-202).
- An environment variable that the environment sets, which capture does not read for the opt-in, since a repository's settings can set variables for everyone who works in it (DR-183).
- A command of the tool's own that writes the opt-in, which would be one more program to install, where one git command does the same.

## Consequences

- The opt-in holds in every session that runs in the environment, in every repository that turns the tool on (DR-185), which the README says beside the line (R185).
- A machine that is resumed after a pause keeps the configuration that it was built with, so removing the line turns capture off only in sessions whose machines are built after the change, and the README says how to turn capture off in a running session with git, which ends its intervals (DR-169).
- Whoever can edit the environment decides the opt-in of its sessions: the person for an environment of their own, an Owner of the organization for a shared one (DR-202, T134).

## Scope

This covers how a person opts in within a cloud environment. Where capture reads the opt-in is DR-183 (The opt-in is read only from the person's global git configuration, and git's own reading of it can only turn capture off), and who may set it is DR-202.

## What reversing it would change

R185 in `project-standards` would change, with its scenario, and so would the design's decision 6, the README's section on cloud threads, which task 4.4 writes, the opt-in's feature page and A71. Nothing in the tool's code reads the setup script, so the change would be one of documentation.
