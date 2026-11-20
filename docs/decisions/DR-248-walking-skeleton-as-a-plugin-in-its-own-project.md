# DR-248: The walking skeleton runs as a plugin of its own, in a project that holds only its scratch repository

- **Type:** security and privacy
- **Boundary:** inside
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-14
- **Requirements:** R235, R243
- **Threats:** T185, T192
- **Replaces:** none
- **Closed by:** none

## Context

A project's cloud threads, where the owner works, run none of the hooks that a repository's settings register, and they do run a plugin's hooks, as a test plugin saw on 2026-11-09 (design decision 17, A61, A69). DR-236 puts the skeleton's real run in a repository made for it, from a project that holds no other repository, with the owner's own opt-in. A line in an environment's setup script reaches the global git configuration of each new session there (A71), and this repository's own opt-in at task 7.1 is set only in the environment of its own project, never in the default one (DR-210). Uploading a zip adds a plugin to the person's account (A72). The owner approved on 2026-11-15 a summary of this design that put the run in such a project's cloud thread, through a plugin.

## Decision

The skeleton's capture runs as a plugin named `pr-cost-skeleton`, apart from the tool's own plugin, built as a zip from `skeleton/`. The owner creates a private scratch repository and a project that holds only it, with an environment that only that project uses, whose setup script holds the opt-in, never the Default environment, and uploads the plugin's zip, built from a commit that the run names, after checking its SHA-256. An upload adds the plugin to the account, so it can load in other projects, where the skeleton records nothing, since it records only where a repository's `.pr-cost.json` holds its own key, `walking_skeleton`, which the tool's reader refuses, and only the calls made in that repository (R235). The plugin declares nothing but its command hooks (R243). Once the run is recorded, the owner removes the plugin from the account and the project, and the opt-in's line from the environment, and task 7.1 checks that no `pr-cost-skeleton` plugin is left.

## Alternatives

- A terminal session on the owner's computer, where the repository's hooks run: it needs Claude Code installed there and would not meet the cloud path that the owner uses.
- The plugin in the scratch project's settings only: no route that the assumptions record adds an uploaded zip to a project alone (A72).
- The opt-in in the owner's Default environment: it would opt in every project that uses that environment, which DR-210 rules out for this repository's own opt-in.

## Consequences

- The run meets the facts about plugins in cloud threads as well as those about transcripts and hooks (A69, A70, A71).
- The plugin loads in other projects while it is on the account, where it records nothing while no repository there holds the skeleton's key (T185).
- The owner removes it once the run is recorded, and a change to settings reaches new threads only, so the run's own thread is not used again (A69).

## Scope

This covers how and from where the skeleton's run happens. What the run keeps here is DR-247, and the bounds on the run are DR-236.

## What reversing it would change

How hard it is to reverse: reversible, until the run. One pull request can change it. R235 and R243 in `project-standards` would change, with their scenarios, and so would design decision 18, tasks 1.34, 1.36 and 7.1 and the answers of T185 and T192.
