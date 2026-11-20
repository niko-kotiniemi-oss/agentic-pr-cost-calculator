# DR-002: The figure is an estimate at list prices, not a bill

- **Type:** scope
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R94
- **Threats:** T16, T27
- **Replaces:** none
- **Closed by:** none

## Context

What a team actually pays for a pull request's tokens and CI minutes depends on its subscription plans and on the CI minutes that its plan includes (see the README). The tool prices usage from a dated price table kept in the repository, which gives each row's source (DR-020).

## Decision

The report's figure is an API-equivalent estimate: what the recorded tokens and CI minutes would cost at list prices. It is not a bill, and the tool does not reconcile it with one, so it models no subscription plan, discount or included minutes.

## Alternatives

None were recorded when this was decided.

## Consequences

- The comment says that its figure is an API-equivalent estimate and not a bill, so that no reader takes it for one (R94, T27).
- A ledger edited by hand is an accepted risk partly because the report is an estimate and not a bill (the design's risk "[A ledger edited by hand changes the reported cost]", T16, DR-066).

## Scope

This covers what the figure means and at which prices it is computed. Where the prices come from, and how they are dated, is DR-020 (Prices come from a dated price table in the repository), and which costs the figure holds is DR-110 (The cost counts CI minutes as well as model tokens).

## What reversing it would change

R94 in `report-comment` would change, with its scenario "The comment says what the figure is", and so would the design's non-goals, the purpose of the `pricing` spec, which calls the cost API-equivalent, the README's paragraph on the figure, the feature pages of the report comment and of CI minutes, T27's answer and T16's reason for accepting the risk. Modelling plans, discounts or included minutes would also change how tokens and minutes are priced, in tasks 3.1 to 3.3, and DR-020, DR-038 and DR-066 would be revisited. The comment's wording is not part of the public surface, so a change to it alone would not be a breaking one for adopters (DR-096).
