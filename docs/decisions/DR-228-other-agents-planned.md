# DR-228: Agents other than Claude Code are planned for after the first version

- **Type:** scope
- **Status:** accepted
- **Decided by:** the owner, 2026-11-12
- **Requirements:** none
- **Threats:** T167
- **Replaces:** none
- **Closed by:** none

## Context

The first version captures Claude Code only (DR-003), and the roadmap's Later listed agents other than Claude Code as open to feedback and contributions (DR-219). On 2026-11-12 the owner said that capturing other agents, such as GitHub Copilot, OpenAI's Codex and Google's Gemini, and later agents that run open-source models, is clearly wanted. Of the change's requirements on that day, 11 of the 66 in `usage-capture` name Claude Code, as do 4 in `project-standards`, 1 in `report-comment` and 1 in `switch-and-opt-in`, while none of those in `ledger`, `pricing`, `activity-types` and `ci-minutes` does. Yet a ledger entry names no agent and no provider, its token types are those that Anthropic's usage gives, and the price table finds a price by a model's name and the day, with no word of a provider.

## Decision

Agents other than Claude Code are planned, and the roadmap's item for them under Later opens with **Planned.** The first version still captures Claude Code only, as DR-003 says, and each other agent comes in a change of its own after it, by a record that replaces DR-003.

## Alternatives

- The item left open to feedback and contributions, which would no longer say what the owner wants.

## Consequences

- The roadmap's item changes its mark, as DR-219 says an item moves.
- The patterns page lists a ledger format and a price table shaped for one provider among the anti-patterns to fix before the build, so that the change that adds an agent need not also change a ledger format that a release wrote, which the public surface holds (R122). The release that adds an agent still changes that surface with the agent's hooks, and so raises the major number (R71).
- That anti-pattern comes from the owner's question rather than from the three reviews of 2026-11-12, so its recognised name and its source are the patterns page's own, and the build's review checks them (T166).
- An agent that a later release adds is recorded only for people who opt in to that agent (DR-229), so that no one's opt-in comes to cover an agent without a step of theirs (T167).
- Each agent's change starts by checking what that agent gives: its hooks, and where it gives each call's token counts, which is not yet known for any of them (A68), so that a planned agent may turn out not to be one that the tool can record. For an agent that works on this repository, it also checks whether that agent reads `CLAUDE.md`, on which the rules for agents here rest (A16).

## Scope

This covers whether other agents are planned. Which agent the first version captures is DR-003 (Claude Code is the only agent `add-pr-cost-calculator` captures).

## What reversing it would change

The roadmap's item under Later would change its mark, the anti-pattern on the patterns page that rests on this record would be revisited, and so would DR-229 and the answer of T167.
