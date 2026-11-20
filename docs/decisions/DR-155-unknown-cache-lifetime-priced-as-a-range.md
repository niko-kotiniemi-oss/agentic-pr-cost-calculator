# DR-155: A cache write of unknown lifetime is priced as a range

- **Type:** technical
- **Boundary:** outgoing
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R15
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

A transcript's usage block splits cache-write tokens into five-minute and one-hour lifetimes (see the design's context). Prices come from the dated price table (DR-020), where cache writes of each lifetime have a rate of their own, so cache writes that do not say their lifetime could be priced at either rate. The design's risk "[Cache writes recorded without their lifetime]" names that case.

## Decision

When a ledger entry's cache writes do not say their lifetime, the report prices them at each of the two lifetimes' rates and shows their cost as the range between the two, a low and a high figure.

## Alternatives

None were recorded when this was decided.

## Consequences

- Both ends of the range come from rates that the table holds, so the range can be recomputed from the ledger and the table like every other figure (see the design's goals).
- Such cache writes stay in the cost, as a range, unlike usage that the table cannot price at all, which is counted in tokens, left out of the cost and named (DR-124).

## Scope

This covers cache writes whose lifetime a ledger entry does not give. Where prices come from is DR-020 (Prices come from a dated price table in the repository), and usage that the table cannot price at all is DR-124 (What the price table does not price is named, never guessed).

## What reversing it would change

R15's last sentence in `pricing` would change, with its scenario "An unknown lifetime gives a range". So would the design's risk "[Cache writes recorded without their lifetime]", the sentence on an unknown cache lifetime under "How a cost is computed" in `docs/how-it-works.md`, the `pricing` feature page and task 3.2, which builds the range. The comment is not part of the public surface, so the change would not be a breaking one for adopters.
