# DR-298: The price table states one currency, USD

- **Type:** technical
- **Boundary:** incoming
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-27
- **Requirements:** R288
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

On 2026-10-27 the owner asked that the price table state its currency, which no file did. Anthropic and GitHub publish their prices in US dollars.

## Decision

The price table states the one currency of all its prices, by its ISO 4217 code, `USD`, and every cost is written in it, by its code. The tool's checks fail on a table that states no currency or gives a price in another (R288).

## Alternatives

- A currency on each row: a pull request could mix currencies, and the report would need exchange rates, which it would have to fetch, against R30.
- No stated currency: a reader could not tell what the figures are in.

## Consequences

- Adding a provider that publishes prices in another currency needs a decision of its own.

## Scope

This covers the price table's currency. How a cost is written is DR-295.

## What reversing it would change

How hard it is to reverse: reversible with work. R288 and its scenarios, the price table's form and the report would change.
