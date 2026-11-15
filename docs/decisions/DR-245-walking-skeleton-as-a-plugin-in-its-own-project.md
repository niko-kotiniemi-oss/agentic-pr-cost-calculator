# DR-245: The walking skeleton runs as a plugin of its own, in a project that holds only its scratch repository

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-14
- **Requirements:** R235
- **Threats:** T185
- **Replaces:** none
- **Closed by:** none

## Context

A project's cloud threads, where the owner works, run none of the hooks that a repository's settings register, and they do run a plugin's hooks, as a test plugin saw on 2026-11-09 (design decision 17, A61, A69). DR-236 puts the skeleton's real run in a repository made for it, from a project that holds no other repository, with the owner's own opt-in. The owner's Default environment already opts in with one line of its setup script (A71). The owner approved on 2026-11-15 a summary of this design that put the run in such a project's cloud thread, through a plugin.

## Decision

The skeleton's capture runs as a plugin named `pr-cost-skeleton`, apart from the tool's own plugin, built as a zip from `skeleton/`. The owner creates a private scratch repository and a project that holds only it, adds the plugin in that project's settings only and not to the account, and uses an environment whose setup script holds the opt-in. The skeleton records only where the repository's switch and the person's opt-in are both on (R235).

## Alternatives

- A terminal session on the owner's computer, where the repository's hooks run: it needs Claude Code installed there and would not meet the cloud path that the owner uses.
- The plugin added to the owner's account: it would load in every thread of every project, this repository's among them.

## Consequences

- The run meets the facts about plugins in cloud threads as well as those about transcripts and hooks (A69, A70, A71).
- A plugin added to the account by mistake loads in other projects, where it records nothing while no repository there holds a switch (T185).
- The owner removes the plugin from the project's settings once the run is recorded.

## Scope

This covers how and from where the skeleton's run happens. What the run keeps here is DR-244, and the bounds on the run are DR-236.

## What reversing it would change

How hard it is to reverse: reversible, until the run. One pull request can change it. R235 in `project-standards` would change, with its scenarios, and so would design decision 18, tasks 1.34 and 1.36 and the answer of T185.
