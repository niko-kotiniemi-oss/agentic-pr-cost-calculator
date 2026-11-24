# DR-306: The price table states the day it was last checked

- **Type:** technical
- **Boundary:** incoming
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R294
- **Threats:** T306
- **Replaces:** none
- **Closed by:** none

## Context

A price is added a few days after it changes (DR-299), and an adopter's report prices calls with the table of the release that they pinned, so a report can price calls made after a price change at the earlier price. The comment named "the price table's date", which no requirement defined, and a row added later with an earlier effective date means that the newest effective date does not say how current the table is.

## Decision

The price table states the UTC day on which its rows were last checked against their sources. The comment gives that day as the price table's date, and when a priced call's day is after it, the brief summary says that prices may have changed since then. The checks fail on a table that states no such day, or one after the day they run (R294).

## Alternatives

- The newest effective date as the table's date: a row added later with an earlier date would leave it unchanged, so it would not say when the table was last checked.
- No date at all: a reader could not tell that the figure may use an outdated price.

## Consequences

- Each pull request that checks the prices updates the day, and review reads that change with the rows.
- Moving the day without checking the prices clears the summary's warning; only review catches it (T306).

## Scope

This covers the day that the table states and what the comment says of it. When a price is added is DR-299 (A price is added a few days after it changes, dated the day it took effect).

## What reversing it would change

How hard it is to reverse: reversible with work. R294 and its scenarios, the price table's form and the comment's line on the table's date would change.
