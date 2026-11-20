# DR-001: The tool is for teams that build pull requests with AI coding agents

- **Type:** scope
- **Boundary:** inside
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-17
- **Requirements:** R20
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

A team that builds pull requests with an AI coding agent can see what each pull request changed, but not what it cost (see the proposal's "Why"). What a pull request's work spends is recorded in different places, in raw form, and nothing adds it up per pull request.

## Decision

The tool is for teams that build pull requests with AI coding agents. It estimates what each pull request cost.

## Alternatives

None were recorded when this was decided.

## Consequences

- Usage has to reach the pull request it was spent on, as it does in the agent's own commits (DR-010), and has to be counted for that pull request alone (DR-017, DR-131).
- The comment gives each merged pull request's total cost and the parts it is made of (R20).

## Scope

This covers whom the tool is for and that it estimates each pull request's cost. Which costs the figure holds is DR-110 (The cost counts CI minutes as well as model tokens), which agent's usage it captures is DR-003 (Claude Code is the only agent `add-pr-cost-calculator` captures), what the figure means is DR-002 (The figure is an estimate at list prices, not a bill), and the cost of AI review by an app or a job in CI, which the figure leaves out, is DR-004 (The cost of AI review by an app or a job in CI is left to a later change).

## What reversing it would change

R20 in `report-comment` would change, with its scenario "The comment states the totals", and so would the proposal's "Why" and "What Changes", the README's opening and its list of what the tool will do, the opening line of `CLAUDE.md` and `docs/how-it-works.md`. The reusable workflow holds `pull-requests: write` to post each pull request's one comment, and its permissions are part of the public surface, so the change would be a breaking one for adopters (DR-096). The tasks of groups 2 to 4 in `tasks.md`, which build capture, pricing and the report, would change, and DR-002 to DR-007, DR-110 and DR-160, which narrow this scope, would be revisited. The choice bears alike on every threat that `docs/threat-model.md` gives for the tool that it defines, so the record lists none.
