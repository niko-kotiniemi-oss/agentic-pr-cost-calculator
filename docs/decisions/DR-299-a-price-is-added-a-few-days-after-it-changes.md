# DR-299: A price is added a few days after it changes, dated the day it took effect

- **Type:** process
- **Boundary:** incoming
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-10-27
- **Requirements:** R14
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

A vendor sometimes corrects a published price within a day or two of announcing it. A row that the price table holds can never be changed (R14, DR-020), so a row copied on the first day would keep a price that the vendor withdrew.

## Decision

A new or changed price is added to the price table a few days after it changes, dated the day it took effect, so that a correction made the next day is caught before the row is written. A routine that checks the published prices each day and opens that pull request waits for the owner's go-ahead.

## Alternatives

- Adding a price on the day it changes: a next-day correction would need a second row, and the first would stay in the table.

## Consequences

- For a few days after a change, the table holds the earlier price, and a report in those days prices calls of the new day at the earlier price or names them as unpriced; a later report, once the row is added, prices them at the new one.

## Scope

This covers when a price row is written. How a row is dated and which row a call uses is DR-020 (Prices come from a dated price table in the repository).

## What reversing it would change

How hard it is to reverse: reversible. Only how contributors add rows would change. Nothing that adopters configure changes.
