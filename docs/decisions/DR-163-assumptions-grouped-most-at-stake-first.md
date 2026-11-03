# DR-163: The assumptions are grouped, and listed with the most at stake first

- **Type:** process
- **Status:** accepted
- **Decided by:** the owner, 2026-10-28
- **Requirements:** R136
- **Threats:** T92
- **Replaces:** none
- **Closed by:** none

## Context

A review that read the specs, the design, the documentation pages, the threat model and every record found the design resting on more facts than a person can read and adjust in one list, most of them parts of a larger assumption. The owner chose on 2026-10-28 between listing every fact, grouping the facts into assumptions that a person can read, and listing only the facts behind a threat of the highest risk, and chose the grouped list, riskiest first. The threat reviews at design then found that the threat model rates each threat with its answer in place (DR-112), so an assumption that keeps a serious threat unlikely takes that threat's low risk and would be listed late. The owner chose on 2026-10-28 to list first what is at stake if an assumption is wrong.

## Decision

The facts are grouped into assumptions, and the assumptions are listed by the highest impact among the threats that rest on them, as the threat model rates those threats, then with the least checked first, then by the highest risk among those threats, with the assumptions that no threat rests on last (R136).

## Alternatives

- Listing every fact on its own, which leaves nothing out but is too long to read and adjust.
- Listing only the facts behind a threat of the highest risk, which would leave the rest where nobody keeps them current.
- Listing by the highest risk among the threats alone, as first chosen, which puts last the assumptions whose answers hold best, since a threat's risk is rated with its answer in place.
- Rating each assumption on its own, which would add ratings that nothing checks against the threat model.

## Consequences

- An index lists every assumption in order, one line each, with the highest impact and the highest risk among its threats, and a page per subject holds each one in full, so that a reader, or an agent, reads only the subject it needs.
- The order comes from the threat model's ratings and from how each fact is checked, which the test reads, so a changed rating or check changes the order, and no assumption is rated on its own.
- An assumption is as checked as its least checked fact, from not yet, through documented and observed, to tested.
- Within one impact, the order still follows the risk that remains with each assumption true, and many assumptions can share the highest impact.

## Scope

This covers how the assumptions are grouped and ordered. What each one says is DR-162 (The design's assumptions are written down, each with what rests on it and how it is checked).

## What reversing it would change

R136 in `project-standards` would change, with its scenarios, and so would the design's decision 14, the index in `docs/assumptions/` and its check in `tests/test_assumptions.py`, task 1.19, the threat model's answer to T92 and the feature page for `project-standards`. The assumptions are not part of the public surface, so the change would not be a breaking one for adopters.
