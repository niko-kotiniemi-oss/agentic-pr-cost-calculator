# DR-217: The report runs its own pinned code

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R24, R203
- **Threats:** T23, T28, T30
- **Replaces:** DR-062
- **Closed by:** none

## Context

The report runs in the adopter's CI with a token that can write pull request comments (DR-063), and the pull request it reports on is untrusted, like everything that crosses into the tool (DR-044). Code from a pull request that runs with a write token is T23. The `github` context that a reusable workflow receives is its caller's, while the `job` context gives the reusable workflow's own repository and commit (see the design's context).

DR-062 has the report run only the tool's own code, from the commit that the calling workflow pins. One of its consequences says that the calling workflow that the README's section on adopting the tool gives pins a full commit that a release names. That no longer holds: the README gives the calling workflow with its pin left for the adopter to fill with the full commit that a published release of the tool names, since a commit cannot name itself (R203). On 2026-11-11 the owner chose to have DR-062 replaced rather than left with that consequence, so this record restates its decision, which the change made, with that consequence corrected, and names DR-186, which closed DR-064, for the comment's flag on a changed workflow.

## Decision

The report checks out and runs only the tool's own code, from the repository and the commit that `job.workflow_repository` and `job.workflow_sha` give, never the caller's, and runs it with `python3 -I`. It reads the adopter's repository, the merged pull request included, only as data, and never runs, imports or installs anything from it.

## Alternatives

None were recorded when this was decided.

## Consequences

- A merged pull request that adds a Python module, a script or a requirements file changes nothing that the report runs (R24, T23).
- The price table comes with the tool's commit, so an adopting repository changes its prices only by pinning another commit of the tool, which the comment flags as a changed workflow (T30, DR-186).
- What runs is only as honest as the commit that the adopter pins. The README's section on adopting the tool, which task 4.4 writes, gives the calling workflow with its pin left for the adopter to fill with the full commit that a published release of the tool names, never a branch or a tag (R203, DR-156), and the threat model leaves the rest to the adopter's choice of commit (T28).
- The `job` context values that this rests on are missing from GitHub Enterprise Server, which the tool does not support (DR-006).

## Scope

This covers whose code the report runs and how it treats the adopter's repository. Which event it goes on for is DR-061 (The report runs only for a push to the default branch), what its token may do is DR-063 (The calling workflow grants only what the report needs), and what the comment says about a changed pin is DR-186 (The report flags changes to the switch, the hook, its registration and the workflows).

## What reversing it would change

R24 in `report-comment` would change, with its scenario "Nothing from the pull request is run", and so would the answers of T23 and T30 and T28's answer and residual. The design's decision 7, its non-goal of GitHub Enterprise Server, task 4.3, the calling workflow in the README (task 4.4), and the report's flow and connections in `docs/how-it-works.md` would change too. The reusable workflow's path, inputs and permissions are public surface, so a reversal that changed any of them would be released as a new major version (DR-096). DR-006, whose reason is the `job` context, and DR-139, which compares the adopter's hook file with the one at the report's own commit, would be revisited.
