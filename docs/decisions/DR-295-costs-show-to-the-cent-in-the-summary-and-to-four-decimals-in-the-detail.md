# DR-295: Costs show to the cent in the summary and to four decimals in the detail

- **Type:** scope
- **Boundary:** outgoing
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-11-24
- **Requirements:** R284
- **Threats:** T89, T292, T297, T301
- **Replaces:** none
- **Closed by:** none

## Context

The design left open how the comment shows a cost: the unit it names, the precision, the rounding, how a cost above zero but below the precision is written, and that each figure is rounded from its own exact cost. Every acceptance test of the report that checks a figure, and the golden set, wait on it. On 2026-11-24 the owner chose, from three options, cents in the summary and four decimals in the detail.

## Decision

Each cost is shown in the price table's currency, written as its code, to two decimals in the brief summary and to four in the collapsed section and the job summary. Each figure, the total among them, is rounded half up from its own exact cost, never summed from rounded figures, and every cost is worked out from rates read as exact decimals, never in binary floating point. A cost above zero that rounds to zero is shown as under the smallest amount at that precision, a cost of zero as zero, and the brief summary says, beside the total, that a total can differ from the sum of its shown parts (R284).

## Alternatives

- Cents everywhere: simplest, but many detail lines, such as cache reads or a short CI job, would read as under a cent.
- Four decimals everywhere: nothing small is hidden, but the brief summary is harder to read at a glance.

## Consequences

- The report reads each rate as an exact decimal, computes each cost exactly, and rounds only when it writes a figure, so a figure does not depend on the order in which costs were added, and a half cent is not lost to a binary float: read as a float, a rate of 0.30 per million tokens prices 50000 tokens just under 0.015, which rounds down.
- A total can differ from the sum of its shown parts by more than one unit of its last digit: four parts of 0.005 each show 0.01, and their total 0.02. The comment says that they can differ, with no bound.
- The job summary shows each cost as the collapsed section does, so that the two never disagree.

## Scope

This covers how a cost is written. Which costs the comment shows, and where, is DR-294 (The comment opens with a brief summary and keeps the detail in a collapsed section), and the currency is DR-298 (The price table states one currency, USD).

## What reversing it would change

How hard it is to reverse: reversible. R284 and its scenarios, the golden set's figures and the report comment's feature page would change. Nothing that adopters configure changes.
