# DR-302: A ledger entry names its agent and its provider, and a price row its provider

- **Type:** architecture
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-14
- **Requirements:** R2, R4, R77, R98, R289, R290
- **Threats:** T1, T31, T293, T294, T295, T296
- **Replaces:** none
- **Closed by:** none

## Context

On 2026-11-14 the owner planned agents other than Claude Code (DR-234), and the guide names a ledger format and a price table shaped for one provider as a gap that B-007 closes. One model can be bought from more than one provider, such as Anthropic's API, Amazon Bedrock or Google Vertex AI, at rates that can differ.

## Decision

Each ledger entry names, in `agent`, the agent that made its call, in this version always `claude-code`, and, in `provider`, the provider that a metadata field of the call's lines names, as the capture step's price table names it, where that table lists it, and `unknown` otherwise, never taken from message content, tool data, the environment, the hook's input or settings (R290). A provider that the table does not list reaches no ledger file, as a model name does not (R4, R77), and the report refuses a line whose provider the table does not list or whose agent its format's version does not name (R98). Each price row names its provider beside its model, and a call is priced by its own provider's row, or, when its provider is `unknown`, by its model's only provider on its day or by the one that a dated statement names as its default on that day, which the comment says was taken from the table (R289). A default is a dated statement, as a combination of modifiers is, so that adding a second provider's rows changes no row and reprices no earlier call. No field records how a call was paid.

## Alternatives

- Adding the fields when a second agent or provider comes: the change would need a new version of a ledger format that a release wrote, which the public surface holds (R122).
- Capture records the provider that the table lists for the model, or `unknown` where it lists more than one: adding a second provider's row would turn every call of that model into one with no price, and a guess would read in the ledger as observed.
- Taking the provider from the environment, such as a variable that turns on Amazon Bedrock: a repository's settings can set such a variable for everyone, and a run reads calls after they were made, under whatever the environment then says.

## Consequences

- Whether Claude Code's transcript tells a call's provider is checked by task 1.1, and recorded in words with no value. Until it is shown to, every entry's provider may be `unknown`, and every call is priced at its model's only or default provider's rates, which the comment says; a call made through another provider is then priced at the default's rates (T293).
- A field that recorded how a call was paid, such as by a subscription, would publish a person's plan, so none is written; one would come only with a change and a threat review of its own.

## Scope

This covers the fields that name an agent and a provider. Which agents are planned is DR-234 (Agents other than Claude Code are planned for after the first version).

## What reversing it would change

How hard it is to reverse: reversible with work. R289, R290 and their scenarios, the ledger format and the price table's form would change, before the first release at no cost to adopters, and after it as a new version of the format.
