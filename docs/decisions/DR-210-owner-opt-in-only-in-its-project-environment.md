# DR-210: The owner's opt-in for this repository is set only in the environment of its own project

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** none
- **Threats:** T2, T32, T128
- **Replaces:** none
- **Closed by:** none

## Context

DR-207 has task 7.1 turn the tool on in this repository only from a project that holds this repository alone, so that no call made from this repository's clone on another repository of the owner's is published here. A session records calls only where it runs the capture step and finds the person's opt-in in the global git configuration where it runs (DR-202). The plugin is on the owner's account, so it loads in every session signed in with that account, terminal sessions among them, and in the threads of each project that turns it on. The opt-in follows the machine or the environment instead: a setup script's line opts in each session of its environment, and a project's threads use a default environment until another is picked. So a project of its own keeps other repositories' calls out of this one only while no other session that can reach this repository's clone beside another's finds the opt-in. The threat review at implementation found that nothing said where the owner's opt-in is set.

## Decision

The owner's opt-in for this repository is set only in the setup script of an environment that only this repository's own project uses: never in the default environment, never in an environment that another project uses, and never in a global git configuration file on a machine where the owner's sessions can reach this repository's clone beside another's. This repository is in no other project. Task 7.1 checks, in a thread of each other project of the owner's and in a terminal session where the owner runs one, that `git config --show-origin --get-all pr-cost.capture` gives no value.

## Alternatives

- Leaving where the opt-in is set to the owner, which one easy step, such as the line in the default environment's setup script, would turn into calls of private work published here.
- Turning capture off for the other repositories' folders with git's conditional includes in the owner's global configuration, which holds only where the owner has set it, and not in an environment that another project uses.

## Consequences

- Only the threads of this repository's own project record calls here, and their only clone is this repository's (T2, T32, T128).
- Any other place where the owner's opt-in is set moves or goes before task 7.1, which checks it, and the threat model lists the setting among those the owner keeps.

## Scope

This covers where the owner's own opt-in is set for this repository's sessions. Where a person's opt-in comes from is DR-202 (Capture needs an opt-in that the person sets, or that the environment they use sets), and the project is DR-207 (This repository turns the tool on only from a project that holds this repository alone).

## What reversing it would change

Task 7.1 and the owner's setting would change, and T2, T32 and T128 would again rest on where the owner happens to set the opt-in.
