# DR-004: The cost of AI review by an app or a job in CI is left to a later change

- **Type:** scope
- **Boundary:** outgoing
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-10-18 and 2026-10-27
- **Requirements:** R20, R94
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

Besides the agent's own work, a pull request can also be reviewed by AI, by an app or by a job in CI, and that review has a cost of its own, in the tokens that it spends (see the design's non-goals). The owner decided on 2026-10-18 to leave it to a later change, which can add it once it is known where that usage can be read. A review that runs inside a session, such as `/code-review` or `/security-review`, which `CLAUDE.md`'s section on review names, is part of the agent's own work, and so are the calls of the subagents that the review starts.

## Decision

The figure that `add-pr-cost-calculator` reports leaves out the cost of AI review of the pull request by an app or a job in CI, which is left to a later change.

## Alternatives

None were recorded when this was decided.

## Consequences

- The comment's figure covers the usage in the pull request's commits and the CI runs on those commits (R94), so its total (R20) holds none of the tokens that an app or a job in CI spends reviewing the pull request.
- A review that an agent does inside its own session is recorded like its other calls, under the type of its first tool call, since review is not an activity type (DR-029).
- The cost of a review app, such as GitHub Copilot's, or of an open-source reviewer is to come in a later version, by a record that replaces this one, as the owner said on 2026-10-27.

## Scope

This covers the cost of AI review on a pull request by an app or a job in CI. How a recorded call's activity type is chosen, and why review is not one, is DR-029 (Activity types come from tool names, which are never recorded), and which agent's sessions are captured is DR-003 (Claude Code is the only agent `add-pr-cost-calculator` captures).

## What reversing it would change

R20 and R94 in `report-comment` would change, with their scenarios "The comment states the totals" and "The comment says what the figure is", and so would the design's non-goals, the proposal's "Impact", `docs/how-it-works.md`, which would name where review usage is read, and task 4.1, which builds the comment. If review became an activity type, R6 in `activity-types`, task 2.5 and DR-029 would be revisited. Added behaviour alone would raise the minor number, while a change to the public surface, such as the reusable workflow's inputs or the ledger format, would be a breaking one for adopters (DR-096).
