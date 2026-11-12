# DR-229: One opt-in records every agent, those that later releases add among them

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the owner, 2026-11-12
- **Requirements:** R216
- **Threats:** T167
- **Replaces:** none
- **Closed by:** none

## Context

A person opts in with `pr-cost.capture` (DR-202), and one opt-in covers every repository that turns the tool on, those that adopt it later among them, with no notice in any of them (DR-185). On 2026-11-12 the owner decided that agents other than Claude Code are planned for after the first version, each in a change of its own (DR-228). The opt-in names no agent, so the change that adds one can read the same key. Its release then records that agent's calls for every person who opted in while only Claude Code was recorded, commits them with their work and publishes them when it is pushed, and reaches them with no step of theirs, through a maintainer's update of the hook file and the pin, or through a plugin that updates with nothing to accept (T132). The design-stage review of the patterns page found this on 2026-11-12 (T167), and the change proposed an opt-in of its own for each agent that a later release adds. Asked that day, the owner chose one opt-in for every agent.

## Decision

One opt-in, `pr-cost.capture`, records every agent that the tool records: Claude Code alone in the first version, and each agent that a later release adds, with no further step of the person's. The README warns of this before anyone opts in (R216).

## Alternatives

- An opt-in of its own for each agent that a later release adds, which the change proposed, so that no one's opt-in comes to cover an agent without a step of theirs, at the cost of one more step for each agent for people who want them all recorded.
- The choice left to the change that adds the first other agent, by which time people would have opted in with no word of which agents their opt-in covers.

## Consequences

- An opt-in's reach grows with each agent that a release adds, as it grows with each repository that turns the tool on (DR-185), so a person who opted in without reading the warning, or who has forgotten it, has an added agent's calls recorded and published once they use it in a repository that turns the tool on (T167).
- No opt-in leaves one agent out, so a person who does not want an added agent recorded turns capture off where they use it: in a clone, for a folder (DR-185) or everywhere.
- An organization's option that turns the opt-in on for its members (DR-202) covers the agents that later releases add too, so the README's section on organizations warns as well.
- The release that adds an agent changes the public surface with that agent's hooks, and so raises the major number (R71, R122), while the opt-in key stays as it is. Its changelog says that every opt-in now records that agent.
- Whether an agent gives what capture needs, and so whether it can be recorded at all, is for its own change to check first (DR-228).

## Scope

This covers which agents an opt-in records. Whether other agents are planned is DR-228 (Agents other than Claude Code are planned for after the first version), and which repositories one opt-in covers is DR-185 (One opt-in covers every repository that turns the tool on, and a person turns capture off by folder).

## What reversing it would change

R216 in `project-standards` would change, with its scenarios, and so would design decision 6, tasks 1.27 and 4.4, the opt-in's feature page, the README's sections on the opt-in and on organizations that task 4.4 writes, the answer and rating of T167, and the change that adds an agent, which would add an opt-in key of its own.
