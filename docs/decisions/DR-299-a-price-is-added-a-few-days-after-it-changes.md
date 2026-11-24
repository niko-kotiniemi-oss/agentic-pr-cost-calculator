# DR-299: A price is added a few days after it changes, dated the day it took effect

- **Type:** process
- **Boundary:** incoming
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-10-27 and 2026-11-24
- **Requirements:** R14, R295
- **Threats:** T30, T307, T308
- **Replaces:** none
- **Closed by:** none

## Context

A vendor sometimes corrects a published price within a day or two of announcing it. A row that the price table holds can never be changed (R14, DR-020), so a row copied on the first day would keep a price that the vendor withdrew.

## Decision

A new or changed price is added to the price table a few days after it changes, dated the day it took effect, so that a correction made the next day is caught before the row is written. Each row gives the day it was added beside its effective date, a day no earlier than the commit that it is compared with and no later than the day the checks run, and a row dated more than 30 days before the day it was added, the limit that the owner chose on 2026-11-24 from 7, 14 and 30 days, names its reason, which review reads; the checks fail on one that does not (R295). A row dated on or before the newest row of its provider, model and price is refused, as DR-020 gives it. A routine that checks the published prices each day and opens that pull request waits for the owner's go-ahead, with a threat review of its own (B-028).

## Alternatives

- Adding a price on the day it changes: a next-day correction would need a second row, and the first would stay in the table.

## Consequences

- For a few days after a change, the table holds the earlier price, and a report in those days prices calls of the new day at the earlier price or names them as unpriced; a later report, once the row is added, prices them at the new one. An adopter's table lags until they update their pinned release, which DR-306 (The price table states the day it was last checked) makes visible.
- Every row is backdated by design, so a row dated before the day it is added no longer stands out in review by that alone (T30); its added day and the 30-day limit make one dated further back name why, while a price change noticed weeks late still goes in without one.
- A row for an earlier price change that merges after the row for a later one is refused, as DR-020 gives it, so the period between them keeps the price before both; keeping the rows immutable and ordered is worth that rare loss.

## Scope

This covers when a price row is written. How a row is dated and which row a call uses is DR-020 (Prices come from a dated price table in the repository).

## What reversing it would change

How hard it is to reverse: reversible. Only how contributors add rows would change. Nothing that adopters configure changes.
