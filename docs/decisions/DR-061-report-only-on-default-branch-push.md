# DR-061: The report runs only for a push to the default branch

- **Type:** security and privacy
- **Boundary:** incoming
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R68
- **Threats:** T23, T29
- **Replaces:** none
- **Closed by:** none

## Context

The report is a reusable workflow that an adopter's own workflow calls (DR-132), and a reusable workflow is handed the event of the workflow that calls it (see the design's context). An adopter could call the report from `pull_request_target` or from any other trigger (T29), and the report would then run with a token that can write before the owner has merged the pull request (T23). An event other than a push can still carry a `github.ref` that names the default branch, and a tag can be given the default branch's name, so that its `github.ref_name` is that name too.

## Decision

The report checks the event itself, whatever triggered the workflow that calls it, and goes on only when the event's name is `push` and its `github.ref` is the default branch's full ref: `refs/heads/` followed by the branch's name. For any other event, it posts nothing and its job fails.

## Alternatives

None were recorded when this was decided.

## Consequences

- A `pull_request`, `pull_request_target`, `workflow_dispatch`, `workflow_run` or `merge_group` event, a push to another branch and a push of a tag named like the default branch each end in a failed job and no comment (R68).
- An adopter who calls the report from the wrong trigger gets a failed job, not a report that runs with a write token before the merge (T29).
- The check lives in the reusable workflow, not in the caller's, so it holds whatever trigger the caller names (task 4.3). That the report sees its caller's event at all rests on GitHub behaving as its documentation says (see the threat model's Assumptions).

## Scope

This covers which events the report goes on for. The trigger that adopters are given is DR-018 (The report runs on the push that a merge makes to the default branch), the code that runs once the check passes is DR-062 (The report runs its own pinned code), and the permissions it runs with are DR-063 (The calling workflow grants only what the report needs).

## What reversing it would change

R68 in `report-comment` would change, with its scenarios "Another event is refused" and "A tag named like the default branch is refused", and so would the answers of T23 and T29. The design's decision 7, which describes the check, task 4.3 and its tests for each refused event, the report comment feature page and the proposal's row for `report-comment` in how the outcome is validated, which both name those tests, and the report's flow in `docs/how-it-works.md` would change too. The events that the report accepts are not part of the public surface (DR-154). DR-018 would be revisited, since its consequence that the report runs only after the merge rests on this check.
