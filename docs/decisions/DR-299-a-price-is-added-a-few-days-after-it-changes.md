# DR-299: A price is added a few days after it changes, dated the day it took effect

- **Type:** process
- **Boundary:** incoming
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-10-27 and 2026-11-24
- **Requirements:** R14, R294
- **Threats:** T30, T306, T307, T308
- **Replaces:** none
- **Closed by:** none

## Context

A vendor sometimes corrects a published price within a day or two of announcing it. A row that the price table holds can never be changed (R14, DR-020), so a row copied on the first day would keep a price that the vendor withdrew.

## Decision

A new or changed price is added to the price table a few days after it changes, dated the day it took effect, so that a correction made the next day is caught before the row is written. Each row gives the day it was added beside its effective date, and a row dated more than 30 days before the day it was added, the limit that the owner chose on 2026-11-24 from 7, 14 and 30 days, or before the newest row of its provider, model and price, names its reason, which review reads; the checks fail on one that does not. The table states the day its rows were last checked against their sources, which the comment gives as its date (R294). A routine that checks the published prices each day and opens that pull request waits for the owner's go-ahead, with a threat review of its own (B-028).

## Alternatives

- Adding a price on the day it changes: a next-day correction would need a second row, and the first would stay in the table.

## Consequences

- For a few days after a change, the table holds the earlier price, and a report in those days prices calls of the new day at the earlier price or names them as unpriced; a later report, once the row is added, prices them at the new one. An adopter's table lags until they update their pinned release, so the brief summary says when a priced call came after the table's checked day.
- Every row is backdated by design, so a row dated before the day it is added no longer stands out in review by that alone (T30); its added day and the 30-day limit make one dated further back name why, while a price change noticed weeks late still goes in without one.
- A row for an earlier change that merges after the row for a later one is allowed when it names its reason, so that its period is not left at the wrong price.

## Scope

This covers when a price row is written. How a row is dated and which row a call uses is DR-020 (Prices come from a dated price table in the repository).

## What reversing it would change

How hard it is to reverse: reversible. Only how contributors add rows would change. Nothing that adopters configure changes.
