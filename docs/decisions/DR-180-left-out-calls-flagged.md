# DR-180: A ledger file flags calls left out, with no count

- **Type:** technical
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-02
- **Requirements:** R155, R157
- **Threats:** T106
- **Replaces:** none
- **Closed by:** none

## Context

Capture now leaves out a call that it cannot show was made inside an interval when both switches were on (DR-168), or from this repository (DR-179), and the owner asked on 2026-11-02 that the incompleteness that follows be reported where appropriate. A count of the calls left out, or their times, would say how much the person worked while capture was off, or on another repository, which is what leaving them out protects (T106).

## Decision

When a run leaves out a call made in this repository because it fell outside every interval, or a call whose repository could not be told, the next ledger file that holds a call of that session says so, by one of two flags, for consent or for the repository, with no count, time or other fact about the calls left out. Calls left out because they were made in another repository raise no flag here. The report's comment says, for each flag that a pull request's ledger files raise, that calls were left out and that the token cost is then a lower bound.

## Alternatives

- Counting the calls left out, which would show how much is missing, and how much the person did outside consent or outside the repository.
- Saying nothing, which would present a figure that is too low as if it were whole.

## Consequences

- A reader learns that a figure is too low, not by how much.
- A session that leaves out calls and never commits again in this repository raises no flag, since no ledger file of its follows.
- A flag says that, in some session, calls were left out for consent or for their repository, which is the least that reporting the gap can say (T106).

## Scope

This covers how the gap that left-out calls make is reported. Which calls are left out is DR-168 and DR-179, and the ledger format that carries the flags is DR-181.

## What reversing it would change

R155 in `usage-capture` and R157 in `report-comment` would change, with their scenarios, and so would the design's decisions 6 and 16, T106, and tasks 1.2, 2.4 and 4.2. The flags are part of the ledger format, which is part of the public surface, so the change would be a breaking one for adopters (DR-096).
