# DR-300: The price table can list a model with no price

- **Type:** scope
- **Boundary:** incoming
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-10-27
- **Requirements:** R287
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

On 2026-10-27 the owner asked that the price table be able to list a model with no price, such as a self-hosted open-source one, so that its tokens are counted under its name. Capture records a model's name only when the price table lists it (R77), so an unlisted model is recorded as `unknown`.

## Decision

The price table can list a model with no price. Capture records its name, and the report counts its tokens under that name, leaves them out of the cost and says that the model has no price, which the comment tells apart from an unknown model (R287).

## Alternatives

- Recording such a model as unknown: its tokens would be counted, but its name, which the person chose to use, would be lost.

## Consequences

- Listing a model is a pull request to the price table, so its name is checked by review before any ledger holds it.

## Scope

This covers a listed model with no price. An unlisted model is R17's and DR-155's.

## What reversing it would change

How hard it is to reverse: reversible. R287 and its scenario, the price table's form and the report would change.
