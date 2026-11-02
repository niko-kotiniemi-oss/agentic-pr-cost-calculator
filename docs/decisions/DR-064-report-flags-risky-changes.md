# DR-064: The report flags changes to the switch, the hook and the workflows

- **Type:** security and privacy
- **Status:** closed
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R93
- **Threats:** T21, T25, T30, T49, T60
- **Replaces:** none
- **Closed by:** DR-186

## Context

A pull request can change `.pr-cost.json`, the workflow that runs the report and the tool commit that it pins, and its merge is then reported by what it changed (T21). Other workflows that use `GITHUB_TOKEN` comment under the report's identity and could edit its comment later (T25). A pull request can also edit the adopter's copy of the hook file, which runs on the machine of each person who works in the repository, to drop calls or scale counts in every later pull request (T60).

## Decision

When a pull request changes `.pr-cost.json`, the hook file at the path that the README gives (DR-065) or any workflow file, the report's comment says so.

## Alternatives

None were recorded when this was decided.

## Consequences

- A reviewer of the comment sees that the pull request changed how it is reported, also when it made `.pr-cost.json` unreadable (R93, T49), and a price changed by pinning another commit of the tool shows as a changed workflow (T30).
- Scripts and local actions that a workflow runs are not flagged, though they can act with the same identity: the design's risk "[A workflow runs a script or a local action that a pull request changes]" leaves them to review of the diff, as T21's and T25's residuals do.

## Scope

This covers what the comment says when a pull request changes `.pr-cost.json`, the hook file or any workflow file in the adopting repository. What it says when the merged commit's hook file is not the one at the report's own commit is DR-139 (The report names a hook that is not the report's own), where the hook file is looked for is DR-065 (The hook's path is fixed, not a setting), and a pull request that removes the calling workflow, and so goes unreported, is DR-051 (A pull request cannot turn off its own report).

## What reversing it would change

R93 in `switch-and-opt-in` would change, with its scenarios "A changed report is flagged" and "A pull request that makes the configuration unreadable is flagged". So would the answers of T21, T30, T49 and T60, T25's residual, the design's decision 7 and the risk named above, task 4.1 and the switch and opt-in feature page. DR-065, whose fixed path serves the flag on a changed hook file, would be revisited, and so would DR-021, DR-051, DR-062 and DR-139, whose consequences rest on the flag.
