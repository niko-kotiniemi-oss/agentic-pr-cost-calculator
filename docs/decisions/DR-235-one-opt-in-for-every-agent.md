# DR-235: One opt-in records every agent, those that later releases add among them

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the owner, 2026-11-12
- **Requirements:** R122, R186, R199, R224, R225
- **Threats:** T171, T175, T176
- **Replaces:** none
- **Closed by:** none

## Context

A person opts in with `pr-cost.capture` (DR-202), and one opt-in covers every repository that turns the tool on, those that adopt it later among them, with no notice in any of them (DR-185). On 2026-11-12 the owner decided that agents other than Claude Code are planned for after the first version, each in a change of its own (DR-234). The opt-in names no agent, so the change that adds one can read the same key. Its release then records that agent's calls for every person who opted in while only Claude Code was recorded, commits them with their work and publishes them when it is pushed, and reaches them with no step of theirs, through a maintainer's update of the hook file and the pin, or through a plugin that updates with nothing to accept (T132). The design-stage review of 2026-11-12 found this (T171), and the change proposed an opt-in of its own for each agent that a later release adds. Asked that day, the owner chose one opt-in for every agent.

## Decision

One opt-in, `pr-cost.capture`, records every agent that the tool records: Claude Code alone in the first version, and each agent that a later release adds, with no further step of the person's (R225). The README says so before any step that opts anyone in, and has an organization tell its members so before it opts them in (R199, R224, R186).

## Alternatives

- An opt-in of its own for each agent that a later release adds, which the change proposed, so that no one's opt-in comes to cover an agent without a step of theirs, at the cost of one more step for each agent for people who want them all recorded.
- The choice left to the change that adds the first other agent, by which time people would have opted in with no word of which agents their opt-in covers.

## Consequences

- An opt-in's reach grows with each agent that a release adds, as it grows with each repository that turns the tool on (DR-185), so a person who opted in without reading the warning, who has forgotten it, or whose opt-in someone else set, has an added agent's calls recorded and published once they use it in a repository that turns the tool on (T171, T176).
- No opt-in leaves one agent out, so a person who does not want an added agent recorded turns capture off where they use it: in a clone, for a folder (DR-185) or everywhere. A member whose organization opts them in from a shared environment keeps it off for good only in an environment of their own (R186).
- The surface manifest names each agent that the opt-in records (R122), so the release that adds one changes the public surface and raises the major number, with a `### Breaking` section (R71), while the opt-in key stays as it is. That section says that every opt-in now records that agent, which rests on that change's own review, since no test can read a release that does not exist yet.
- The change that adds an agent shows first, in its own threat review, that the answers to T2, T3, T4 and T119 hold for that agent, and that nothing that a repository holds can write the opt-in where it runs, and records that agent only where they hold (T175), besides checking whether the agent gives what capture needs at all (DR-234).

## Scope

This covers which agents an opt-in records. Whether other agents are planned is DR-234 (Agents other than Claude Code are planned for after the first version), and which repositories one opt-in covers is DR-185 (One opt-in covers every repository that turns the tool on, and a person turns capture off by folder).

## What reversing it would change

How hard it is to reverse: reversible, with work. Before a release adds a second agent, an opt-in of its own for each agent changes the requirements and the README; after one has, it also changes the public surface, so its release raises the major number, and what every opt-in recorded of that agent until then stays published. R199, R224 and R186 in `project-standards` would change, with their scenarios, and so would R225 in `switch-and-opt-in` and R122 in `releases-and-compatibility`, design decisions 6 and 12, tasks 1.28, 4.4 and 6.1, the opt-in's feature page and the README's sections that task 4.4 writes, the answers of T171 and T176, and the change that adds an agent, which would add an opt-in key of its own.
