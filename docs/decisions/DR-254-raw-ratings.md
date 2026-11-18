# DR-254: Each threat is also rated as if its answer were not built, by reviewers who did not write it

- **Type:** process
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-29
- **Requirements:** R244
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

A threat's likelihood is rated with its answer in place (DR-112), so the threat model shows how much risk remains, but not how much each answer removes. A reader cannot tell which answers carry the most weight, and a matrix in which every answer is taken as built can show nothing as high. The owner asked on 2026-10-29 for a risk document with raw and adjusted ratings.

## Decision

Each threat also carries a raw impact and a raw likelihood, rated as if nothing that its Answer and its Held by cite were built, while the rest of the design stands, and a raw risk that is their product (R244). The threat's impact, likelihood and risk stay as they are, rated with the answer in place (DR-112). Both kinds of rating stay in the threat model, so that each lives in one place.

The raw ratings are first made by reviewers who did not write the threat model's ratings, one per trust boundary, each in a context of its own, as the threat model's method has reviewers model threats. Each reviewer reads the method and each threat's kind, what could happen and its answer, but not its ratings, so that the rating with the answer in place does not anchor the raw one. A raw rating below the rating with the answer in place is a disagreement that a second reviewer settles, and the pull request lists each.

An answer can lower an impact as well as a likelihood, such as a comment that says that its figure is a lower bound, so the raw impact is rated too, and neither raw rating may be lower than its rating with the answer in place.

## Alternatives

- A raw likelihood alone, with the impact taken as it stands: simpler, but it would count as raw an impact that an answer has already lowered.
- Raw ratings made by the author of the threat model's ratings: quicker, but rated by someone who already knows the answer and its rating, which the raw rating exists to set aside.
- Raw ratings kept on the risk register rather than in the threat model: each threat's ratings would then live in two files.

## Consequences

- The threat model's method defines the raw rating, and each threat gives its raw impact, raw likelihood and raw risk after its risk.
- A threat that a later change adds is given its raw ratings with its other ratings, by the reviews that model the threats at design and at implementation (DR-095).
- The comparison of the reviewers' raw ratings with the ratings with the answers in place is also a check of the latter, where a disagreement shows one of them to be wrong.

## Scope

This covers the raw rating and who makes it. What a likelihood with the answer in place is rated against is DR-112, the scale DR-094, the bands DR-253, and the register that shows both DR-256.

## What reversing it would change

How hard it is to reverse: easy. The raw fields would leave the threat model, with R244 and its checks, and the risk register would show one rating; nothing that the tool does rests on them.
