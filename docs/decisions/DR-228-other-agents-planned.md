# DR-228: Agents other than Claude Code are planned for after the first version

- **Type:** scope
- **Status:** accepted
- **Decided by:** the owner, 2026-11-12
- **Requirements:** none
- **Threats:** none
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
- The patterns page lists a ledger format and a price table shaped for one provider among the anti-patterns to fix before the build, so that adding an agent can be a minor release (DR-096), since a change to the ledger format after a release is a breaking one for adopters (DR-003).
- Each agent's change starts by checking what that agent gives: its hooks, and where it gives each call's token counts.

## Scope

This covers whether other agents are planned. Which agent the first version captures is DR-003 (Claude Code is the only agent `add-pr-cost-calculator` captures).

## What reversing it would change

The roadmap's item under Later would change its mark, and the anti-pattern on the patterns page that rests on this record would be revisited.
