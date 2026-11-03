# DR-165: A golden set of hand-worked sessions holds the tool's figures

- **Type:** process
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-28
- **Requirements:** R139, R141, R142
- **Threats:** T83, T84, T85, T87, T89, T91, T98
- **Replaces:** none
- **Closed by:** none

## Context

The owner asked on 2026-10-28 about reusable testing patterns, golden datasets and A/B testing. The tool's figures come from rules spread over several specs: what capture records, how a cost is priced, how CI minutes are counted and what the report adds up. The acceptance tests hold each scenario (DR-084), property-based tests hold the invariants (DR-088), and the end-to-end tests run the whole flow (DR-092), but nothing fixes what the figures must be for a whole session, worked out without the tool's code. The threat reviews at design found that a set built from transcripts alone would hold only ledgers that capture wrote, that its entries apply rules rather than arithmetic, that running the capture step from the clone that runs the tests acts on that clone, that no spec says how the comment shows a figure, and that a newer report can price an older hook's entries otherwise with nothing saying so.

## Decision

A golden set of synthetic sessions, each with the pull request it is reported for, a price table of its own, each call of its transcripts with its entry or the scenario that leaves it out, and the figures as the comment shows them, worked out by hand from the specs with the working beside each, which every version must reproduce (R139). A golden figure changes only with the spec that gives it, and one that a release holds with a line in the changelog (R141), and for each ledger format that a release wrote, the set keeps sessions with their figures for as long as the report reads that format (R142).

## Alternatives

- A/B testing, which compares two variants in live use and suits a system whose outputs vary from one use to the next. The tool is deterministic: one input always gives one figure. Once the tool runs on this repository (DR-147), it could compare two ways of working, which would be a decision of its own.
- Expected figures written by running the tool, which would hold whatever the code computes, its defects included.
- Running the capture step as the README registers it, from the clone that runs the tests, which makes that clone the step's repository and can withhold the calls of the session that runs them.
- Giving a run its time through an environment variable, which a repository's settings could set for every session in it.

## Consequences

- The set is built from task 1.1's fixtures, once `report-comment` states how a cost is shown and before the code that it checks (task 1.21).
- Its tests are acceptance tests, so they are never rewritten to make an implementation pass (DR-084), and each names as its expected error one that only a missing capture step or report raises.
- The tests run each session in a temporary repository of its own and call the capture step's and the report's entry points in their own process, giving each run its time and the report its day, so that no run reads the opt-in of the person running them, nothing sets a run's time through the environment, and the clone that runs them is left as it was. They never run a command from a fixture through a shell.
- The test works out each figure's working on its own, so a slip in the set's arithmetic is caught as well as a defect in the code, and each call of a session is accounted for by an entry or a cited scenario.
- A session joins the set with each rule that changes an entry, a figure or a count that the comment gives.

## Scope

This covers the fixed figures that every version must reproduce. The tests of each scenario are DR-084 (Acceptance tests come first), the invariants are DR-088 (Invariants get property-based tests), the tests of the whole flow are DR-092 (The hook and the report are tested end to end), and what a release's tests must pass is DR-167 (A release needs every acceptance test to pass).

## What reversing it would change

R139, R141 and R142 in `project-standards` would change, with their scenarios, and so would the design's decision 14, tasks 1.21 and 6.4, `tests/golden/` and the feature page for `project-standards`. The golden set is not part of the public surface, so the change would not be a breaking one for adopters.
