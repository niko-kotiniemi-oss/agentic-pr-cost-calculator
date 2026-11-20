# DR-006: GitHub.com only, not GitHub Enterprise Server

- **Type:** scope
- **Boundary:** incoming
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** none
- **Threats:** T23
- **Replaces:** none
- **Closed by:** none

## Context

The report learns where its own code comes from through GitHub's `job` context: it checks out `job.workflow_repository` at `job.workflow_sha` (DR-062). In a reusable workflow, those values give the reusable workflow's own repository and commit rather than its caller's (see the design's context). The report also compares the adopter's hook file with the one at `job.workflow_sha` (DR-139). GitHub Enterprise Server does not provide those values (see the design's non-goals).

## Decision

The change `add-pr-cost-calculator` supports repositories on GitHub.com, and leaves GitHub Enterprise Server out of its scope.

## Alternatives

None were recorded when this was decided.

## Consequences

- The report relies on `job.workflow_repository` and `job.workflow_sha` to run only its own code, from the commit that the calling workflow pins, which is part of T23's answer, and to name a hook file that does not come from its own commit (R65).
- On GitHub Enterprise Server, which lacks those values, the report as designed could do neither.
- The README lists GitHub Enterprise Server near its top among what this first version does not support.

## Scope

This covers which GitHub the tool supports. How the report runs its own pinned code is DR-062 (The report runs its own pinned code), and how it names a hook file that is not its own is DR-139 (The report names a hook that is not the report's own).

## What reversing it would change

Supporting GitHub Enterprise Server would need another way for the report to learn its own repository and commit. The design's non-goals and decision 7 would change, and so would the README's list of what this first version does not support, T23's answer, which names the `job` context, the flow "A merge and its report" in `docs/how-it-works.md`, and tasks 4.1 and 4.3, which compare the hook file with the one at `job.workflow_sha` and check out the tool's code by it. R24 and R65 in `report-comment` would keep their text but be met another way, and DR-062 and DR-139 would be revisited. Added behaviour alone would raise the minor number, while a change to the public surface, such as the reusable workflow's inputs, would be a breaking one for adopters (DR-096).
