# DR-066: A ledger edited by hand is an accepted risk

- **Type:** security and privacy
- **Boundary:** incoming
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** none
- **Threats:** T16
- **Replaces:** none
- **Closed by:** none

## Context

Whoever can push to a pull request's branch writes its ledger files, the author of a pull request from a fork included, so a contributor can lower or raise the reported cost by editing them (T16). The files travel in the pull request's own commits (DR-010), and the figure that the report gives is an estimate at list prices, not a bill (DR-002).

## Decision

The tool makes no attempt to tell an edited ledger from a recorded one. The threat model accepts T16 instead, for two reasons: a reviewer sees the ledger files in the pull request's diff, as any other change, and what the report gives is an estimate, not a bill.

## Alternatives

None were recorded when this was decided.

## Consequences

- The reported cost is only as sound as the review of the ledger files in the pull request's diff.
- The checks that hold each line to the ledger format, count a call once and refuse names that the price table does not list (R35, R59, R98) stop a malformed or hostile line (T17), not a count changed to another valid one.
- Removing a ledger file before the merge removes its calls from the cost, as the ledger's feature page says.
- T16 keeps its rating, likely and of medium impact, which places it among the threats with a risk of 6 or more that the threat model lists.

## Scope

This covers ledger files that a pull request adds and that someone edited by hand before the merge. Earlier ledger files that a pull request removes or changes are flagged and not counted, under DR-017 (A pull request's usage is the ledger files its merge adds), an edited hook file is flagged under DR-064 (The report flags changes to the switch, the hook and the workflows), and a changed price is held by DR-020 (Prices come from a dated price table in the repository).

## What reversing it would change

No requirement's text holds this acceptance, so a reversal would add requirements, in whichever specs held the new check, rather than change one. T16 would get an answer and be rated again (DR-094), and the design's risk "[A ledger edited by hand changes the reported cost]" and the ledger's feature page, which says that the ledger is visible in review, would change. A check that needed new fields in a ledger entry would change the ledger format, which is part of the public surface, so it would be released as a new major version (DR-096).
