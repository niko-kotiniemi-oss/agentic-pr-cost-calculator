# DR-107: The proposal's reviews stopped after the twenty-fifth

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-10-20
- **Requirements:** none
- **Threats:** T2, T8, T10
- **Replaces:** none
- **Closed by:** none

## Context

Independent reviews read the proposal one after another, and from the third to the twenty-fifth each was answered in a commit of its own. From the seventh on, each read the previous commit against git's real behaviour, and from the twelfth on none found a high finding. The last rounds were about git's own behaviour in detail, such as its sparse checkouts, its index and its worktrees. The twenty-fifth asked whether task 4.4's tests should run on git 2.43 itself, and the task was changed to do so.

## Decision

The proposal's independent reviews stop after the twenty-fifth. The remaining details of git's behaviour are settled by task 4.4's tests against real git, rather than by more rounds of review.

## Alternatives

None were recorded when this was decided.

## Consequences

- What the design says of git's behaviour rests, for the details that the reviews did not reach, on task 4.4's tests, which run with the CI runner's git and, in one more job, with git 2.43 from an image pinned to its digest.
- Those details are settled only when the tests run, after the proposal is approved, and what they find can change the README's section on adopting the tool, the design's risks and the residuals of T2, T8 and T10, which describe that behaviour.

## Scope

This covers the rounds of independent review of the proposal before its approval. The threat model's review at design and against the code is DR-095 (Threats are modelled twice in every change), and the review of what was built, before the change merges, is DR-093 (Every change is reviewed in a separate context before it merges).

## What reversing it would change

Further rounds of review would read the proposal again, and what they found would be answered in the design, in the README's section that task 4.4 writes and in the residuals of T2, T8 and T10. Task 4.4's tests would still run. No requirement and no part of the public surface is involved.
