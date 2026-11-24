# DR-301: The ledger's day field is named `utc_day`

- **Type:** technical
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R290
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

An entry records its call's UTC day (DR-052), and the documentation calls it the UTC day, but the ledger format had not named the field. B-007's What done looks like asks that it be named so that it says UTC.

## Decision

Each ledger entry gives its call's day in a field named `utc_day`, as a date with no time (R290).

## Alternatives

- A field named `day` or `date`: a reader of a ledger file could take it for a local date.

## Consequences

- The field's name is part of the ledger format, which the public surface holds, so it is fixed before the first release writes one.

## Scope

This covers the day field's name. Recording the UTC day is DR-052.

## What reversing it would change

How hard it is to reverse: reversible with work. R290, the ledger format's document and schema, capture and the report would change. Once a release has written the format, renaming the field is a new version of the format.
