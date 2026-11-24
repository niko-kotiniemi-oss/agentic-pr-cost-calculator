# DR-297: The comment ends with a note that a subscription may include the usage

- **Type:** scope
- **Boundary:** outgoing
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-10-27
- **Requirements:** R282
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

On 2026-10-27 the owner asked that the comment end with a note that a subscription may include this usage. The figure is what the usage would cost at the API's list prices (DR-002), while many people run Claude Code on a subscription that already pays for it.

## Decision

The comment ends by saying that a subscription may include this usage, so that the figure is what the same usage would cost through the API (R282).

## Alternatives

None were recorded when this was decided.

## Consequences

- A reader on a subscription is not led to think that the figure was billed to them.

## Scope

This covers the comment's last line. What the figure is, an estimate and not a bill, is DR-002 (The figure is an estimate at list prices, not a bill).

## What reversing it would change

How hard it is to reverse: reversible. R282 and its scenario, and the golden set's comments, would change. Nothing that adopters configure changes.
