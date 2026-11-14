# DR-234: Agents other than Claude Code are planned for after the first version

- **Type:** scope
- **Status:** accepted
- **Decided by:** the owner, 2026-11-12
- **Requirements:** none
- **Threats:** T171, T175
- **Replaces:** none
- **Closed by:** none

## Context

The first version captures Claude Code only (DR-003), and agents other than Claude Code were open to feedback and contributions, as the backlog item B-017 gives them (DR-226). On 2026-11-12 the owner said that capturing other agents, such as GitHub Copilot, OpenAI's Codex and Google's Gemini, and later agents that run open-source models, is clearly wanted. Of the change's requirements on that day, 11 of the 66 in `usage-capture` name Claude Code, as do 4 in `project-standards`, 1 in `report-comment` and 1 in `switch-and-opt-in`, while none of those in `ledger`, `pricing`, `activity-types` and `ci-minutes` does. Yet a ledger entry names no agent and no provider, its token types are those that Anthropic's usage gives, and the price table finds a price by a model's name and the day, with no word of a provider.

## Decision

Agents other than Claude Code are planned: the backlog item B-017 is `Planned`, and the roadmap lists it under Later. The first version still captures Claude Code only, as DR-003 says, and each other agent comes in a change of its own after it, by a record that replaces DR-003.

## Alternatives

- The item left open to feedback and contributions, which would no longer say what the owner wants.

## Consequences

- B-017 becomes `Planned` in the pull request that holds this record, as DR-226 says an item becomes planned, through a pull request that the owner merges.
- The guide names a ledger format and a price table shaped for one provider as an anti-pattern, a gap whose item the owner chooses before the guide is written, since either item would take on work that its What done looks like does not yet name (DR-239): the corrected requirements (B-007), which would close it before the build, so that the change that adds an agent need not also change a ledger format that a release wrote, which the public surface holds (R122), or the item on other agents (B-017), whose change for the first of them would then change that format too. The release that adds an agent changes that surface either way, since it names each agent that the opt-in records (R122, DR-235), and so raises the major number (R71).
- That anti-pattern comes from the owner's question rather than from the three reviews of 2026-11-12, so its recognised name and its source are the guide's own, and the build's review checks them (T170).
- One opt-in records every agent that the tool records, those that later releases add among them, as the owner chose (DR-235), so the README's short start warns of it before any step that opts anyone in (R199, T171).
- Each agent's change starts by checking what that agent gives: its hooks, and where it gives each call's token counts, which is not yet known for any of them (A68), so that a planned agent may turn out not to be one that the tool can record. For an agent that works on this repository, it also checks whether that agent reads `CLAUDE.md`, on which the rules for agents here rest (A16). Before the agent joins the opt-in, the change shows that the answers to T2, T3, T4 and T119 hold for it, and that nothing that a repository holds can write the opt-in where it runs (T175, DR-235).

## Scope

This covers whether other agents are planned. Which agent the first version captures is DR-003 (Claude Code is the only agent `add-pr-cost-calculator` captures).

## What reversing it would change

How hard it is to reverse: reversible. The plan is B-017's status, which one pull request can change until an agent's own change is built. B-017 would change, the guide's entry that rests on this record would be revisited, and so would DR-235 and the answer of T171.
