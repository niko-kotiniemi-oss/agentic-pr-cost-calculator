# DR-139: The report names a hook that is not the report's own

- **Type:** security and privacy
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R65
- **Threats:** T54, T60
- **Replaces:** none
- **Closed by:** none

## Context

Adopters copy the hook file from the commit that their calling workflow pins (DR-022). Bots that follow tags can propose a new commit for the calling workflow's pin but cannot change the copied hook file, so the hook and the report drift apart: models are recorded as `unknown` and ledger lines are refused, with nothing to say why (T54). A pull request can also edit the adopter's copy of the hook file, to drop calls or scale counts in every later pull request (T60).

## Decision

When the merged commit has no hook file at the path that the README gives (DR-065), or one that differs from the hook file at `job.workflow_sha`, the tool's commit that the report runs, the report's comment says that the repository's hook does not come from the report's commit. It quotes nothing from that file.

## Alternatives

None were recorded when this was decided.

## Consequences

- An adopter who moves only the pin gets a comment that says the hook does not come from the report's commit, not a fixed hook (R65, T54), and the README's section on adopting the tool, which task 4.4 writes, tells adopters to update the hook file, its checksum and the pin in one pull request, as the design's risk "[An adopter updates the hook and the workflow pin at different times]" says.
- The comment looks at the hook file in the merged commit, not at what the pull request changed, so a hook that a pull request edits is named in that pull request's comment and in each later one for as long as it differs, beside the flag that DR-064 gives the change itself (T60).
- The comment does not say how the file differs: like the rest of the comment, it quotes no text from the pull request (R97).

## Scope

This covers what the comment says when the repository's hook file is missing or is not the one at the report's own commit. The flag on a pull request that changes the hook file is DR-064 (The report flags changes to the switch, the hook and the workflows), where the report looks for the file is DR-065 (The hook's path is fixed, not a setting), and how adopters copy and update it is DR-022 (Adopters copy the hook file from a pinned commit).

## What reversing it would change

R65 in `report-comment` would change, with its scenario "A hook from another commit than the report's is named", and so would T54's answer and residual and T60's answer, the design's decisions 1 and 7 where they say that the report names such a hook, the design's risk "[An adopter updates the hook and the workflow pin at different times]", task 4.1, the report's flow and inputs in `docs/how-it-works.md`, and the report comment feature page. DR-065, whose fixed path serves this comparison, would be revisited.
