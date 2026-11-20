# DR-095: Threats are modelled twice in every change

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-10-18 and 2026-10-20
- **Requirements:** R31
- **Threats:** T74, T78, T80
- **Replaces:** none
- **Closed by:** none

## Context

Every change revisits the threat model, and in the change `add-pr-cost-calculator` it was written before any code, so its answers are requirements and tasks (see the threat model's introduction). Each likelihood is rated with the answer in place as designed (DR-112).

## Decision

The threat model is revisited twice in each change. Before the design is approved, reviewers who did not write it read the design and the specs, boundary by boundary, find the threats that are missing, and rate likelihood; their findings change the design where they need to, and the change records what they found. Before the pull request merges, a review of what was built rates each threat again against the code and adds the threats that the code itself brings (task 5.2).

## Alternatives

None were recorded when this was decided.

## Consequences

- In `add-pr-cost-calculator`, the review at design found T38 to T69, the design-stage review of the decision records found T70 to T78, and the implementation-stage review of those records and their checks found T79 to T81, which the threat model lists after T37 under a heading for each boundary, as its introduction says. Task 1.10 rated T1 to T69 after the first of those reviews.
- Since `tests/test_threat_model.py` checks only that a citation resolves, whether it still says what holds the answer rests on these reviews (DR-085).
- The review against the code also carries three residuals: whether a record that a citation now names holds the answer (T78), whether revisiting a threat after its record closed changed the right thing (T80), and whether a change that alters a decided behaviour without retiring a requirement has left a record wrong, which rests as well on the rule that such a change adds its record (T74).
- Neither review is a test: the feature page for `project-standards` lists both as validated by review.
- Each change takes a review for each trust boundary before its design is approved, and a further review before it merges.
- That review runs in a context separate from the one that built it (task 5.2), as a change's other reviews before it merges do (DR-093).

## Scope

This covers when the threat model is revisited, and by whom. How each threat is rated is DR-094 (Threats are rated for impact and likelihood), and the review of a change's code before the merge is DR-093 (Every change is reviewed in a separate context before it merges).

## What reversing it would change

R31 in `project-standards` would change, in its sentence on the two reviews. So would the design's decision 9, the threat model's method, the residuals of T74, T78 and T80, `CLAUDE.md`'s section on the threat model, the steps on threats at design and at implementation in `CONTRIBUTING.md`, the pull request template's checklist, the proposal's list of what changes and its conditions for success, the feature page for `project-standards`, and tasks 1.10 and 5.2. DR-094 and DR-112, whose ratings the review of what was built checks, and DR-085, which leaves what a citation says to these reviews, would be revisited.
