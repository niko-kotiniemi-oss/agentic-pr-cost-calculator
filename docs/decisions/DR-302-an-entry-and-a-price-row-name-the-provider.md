# DR-302: A ledger entry names its agent and its provider, and a price row its provider

- **Type:** architecture
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-14
- **Requirements:** R289, R290
- **Threats:** T293
- **Replaces:** none
- **Closed by:** none

## Context

On 2026-11-14 the owner planned agents other than Claude Code (DR-234), and the guide names a ledger format and a price table shaped for one provider as a gap that B-007 closes. One model can be bought from more than one provider, such as Anthropic's API, Amazon Bedrock or Google Vertex AI, at rates that can differ.

## Decision

Each ledger entry names the agent that made its call, in this version always Claude Code, and the provider that the price table lists for its model, or `unknown` where the table lists the model under more than one provider and the call's lines do not tell which (R290). Each price row names its provider beside its model, and a call is priced by the row whose provider and model are its entry's (R289).

## Alternatives

- Adding the fields when a second agent or provider comes: the change would need a new version of a ledger format that a release wrote, which the public surface holds (R122).

## Consequences

- Whether Claude Code's transcript tells a call's provider is checked by task 1.1; until it does, a model that the table lists under one provider takes that provider.

## Scope

This covers the fields that name an agent and a provider. Which agents are planned is DR-234 (Agents other than Claude Code are planned for after the first version).

## What reversing it would change

How hard it is to reverse: reversible with work. R289, R290 and their scenarios, the ledger format and the price table's form would change, before the first release at no cost to adopters, and after it as a new version of the format.
