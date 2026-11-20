# DR-112: Likelihood is rated with the answer in place

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** none
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

Each threat in the threat model carries an impact and a likelihood, each from 1 to 3, and a risk that is their product (DR-094). The model was written before any code, so its answers are requirements and tasks rather than code (see the threat model's introduction), and how likely a threat is depends on whether its answer is in place.

## Decision

The likelihood is rated for the threat with its answer in place as designed, so the matrix shows the risk that remains if the answer is built as specified, and the review of what was built checks that it was.

## Alternatives

- Rating likelihood before the answer, which shows why the answer is needed but not what remains.

## Consequences

- The threat model's method, in its step on ratings, defines likelihood with the answer in place and names this record.
- The review of what was built is task 5.2. In a context separate from the builder's, it rates each threat's likelihood again against the code, adds the threats that the code brings and records what changed.
- Until that review, every likelihood is a judgment of a design rather than of code.

## Scope

This covers what a likelihood is rated against. The scale, the risk and the matrix are DR-094 (Threats are rated for impact and likelihood), and when the threat model is revisited, and by whom, is DR-095 (Threats are modelled twice in every change).

## What reversing it would change

The threat model's method would define likelihood another way, and every threat's likelihood would be rated again, with its risk, the risk matrix and the list of the threats with the highest risks. The design's decision 9, which names this record, and task 5.2, whose review checks the ratings against what was built, would change, and DR-094 and DR-095 would be revisited. No requirement's text would have to change, since R31 asks for a likelihood without saying what it is rated against. This choice touches every threat in the same way, so the record lists none in its threats, and reversing it would change the likelihood of each (DR-108). The threat model is not part of the public surface, so the change would not be a breaking one for adopters.
