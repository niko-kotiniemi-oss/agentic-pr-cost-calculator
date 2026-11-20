# DR-124: What the price table does not price is named, never guessed

- **Type:** technical
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R14, R17, R20, R61, R63
- **Threats:** T9, T17, T26, T27
- **Replaces:** none
- **Closed by:** none

## Context

Prices come only from the dated price table at the tool's own commit (DR-020), which can lack a model newer than itself, a rate for an attribute value or for a combination of modifiers, a runner, or any price for a day before a model's first one (T9, T17).

## Decision

Whatever the price table cannot price is left out of the cost and shown in the report, never priced by a guess. Calls with an unpriced model, attribute value or combination of modifiers are counted in tokens and named, or their model is said to be unknown; an entry dated before its model's first price is named with its model and day; and the minutes on runners that the table does not list are counted.

## Alternatives

None were recorded when this was decided.

## Consequences

- The cost can leave out part of the usage, but the report says what it left out, and the rest can still be recomputed, as the design's goals ask (T27).
- The table lists web fetches at no charge, so that a call that made them is still priced (T9; see the design's decision 4).
- Calls of a new model are left out of the cost while the hook's copy of the table does not list it or the report's does not price it, as the design's risks "[Prices go stale, or a new model appears]" and "[An adopter updates the hook and the workflow pin at different times]" say.

## Scope

This covers what the report does with usage that its price table cannot price. How the hook records a name that its table does not list is DR-054 (Names the price table does not list are recorded as `unknown`), and usage that a transcript gives only in part is DR-032 (A call with no stop reason is read from its last line, as a lower bound) and DR-135 (A call with an unknown usage field is counted from the fields capture knows). A cache write of unknown lifetime, priced as a range (R15), is outside it: that is DR-155 (A cache write of unknown lifetime is priced as a range).

## What reversing it would change

R14's clause on an entry whose day has no price, R17 and R61 in `pricing`, R63 in `ci-minutes` and R20's count of minutes on unlisted runners in `report-comment` would change, with their scenarios, and so would the purpose of the `pricing` spec, the design's decision 7 on such runners and the two risks above, the answers of T9, T17, T26 and T27, tasks 3.2 and 3.3, and the `pricing` and `ci-minutes` feature pages. DR-054 would be revisited. The comment is not part of the public surface, so the change would not be a breaking one for adopters.
