# DR-229: An opt-in records Claude Code alone, and each agent added later has an opt-in of its own

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R216
- **Threats:** T167
- **Replaces:** none
- **Closed by:** none

## Context

A person opts in with `pr-cost.capture` (DR-202), and one opt-in covers every repository that turns the tool on, those that adopt it later among them, with no notice in any of them (DR-185). On 2026-11-12 the owner decided that agents other than Claude Code are planned for after the first version, each in a change of its own (DR-228). The opt-in names no agent, so the change that adds one could read the same key. Its release would then record that agent's calls for every person who opted in while only Claude Code was recorded, commit them with their work and publish them when it is pushed, and tell them nothing, as nothing tells them of a repository that turns the tool on later. The release would reach them with no step of theirs, through a maintainer's update of the hook file and the pin, or through a plugin that updates with nothing to accept (T132). The design-stage review of the patterns page found this on 2026-11-12, while the opt-in key can still change without a major release, since no release has been published (T167).

## Decision

An opt-in records Claude Code's sessions alone. An agent that a later release adds is recorded only for people who opt in to that agent, by an opt-in of its own, so that no one's opt-in comes to cover an agent without a step of theirs. The README's section on the opt-in and the opt-in's feature page say so (R216).

## Alternatives

- One opt-in for every agent, now and later, so that a person needs no new step for each agent, but whose reach grows with each release without a step of theirs, as one opt-in's reach grows with each repository that turns the tool on (DR-185).
- The choice left to the change that adds the first other agent, by which time people would have opted in with no word of which agents their opt-in covers.

## Consequences

- The release that adds an agent changes the public surface, with that agent's hooks and its own opt-in key, and so raises the major number (R71, R122).
- A person who wants each agent recorded opts in to each, and the README says how for each agent that a release adds.
- Whether an organization's option can turn on an added agent's opt-in for its members, as it can turn on `pr-cost.capture` (DR-202), is for that agent's change to decide, with its own threat review.
- Whether an agent gives what capture needs, and so whether it can be recorded at all, is for its own change to check first (DR-228).

## Scope

This covers which agents an opt-in records. Whether other agents are planned is DR-228 (Agents other than Claude Code are planned for after the first version), and which repositories one opt-in covers is DR-185 (One opt-in covers every repository that turns the tool on, and a person turns capture off by folder).

## What reversing it would change

R216 in `project-standards` would change, with its scenarios, and so would design decision 6, task 4.4, the opt-in's feature page, the README's section on the opt-in that task 4.4 writes, and the answer of T167.
