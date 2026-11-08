# DR-186: The report flags changes to the switch, the hook, its registration and the workflows

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R93
- **Threats:** T21, T25, T30, T49, T60
- **Replaces:** DR-064
- **Closed by:** none

## Context

A pull request can change `.pr-cost.json`, the workflow that runs the report and the tool commit that it pins, and its merge is then reported by what it changed (T21). Other workflows that use `GITHUB_TOKEN` comment under the report's identity and could edit its comment later (T25). A pull request can also edit the adopter's copy of the hook file, which runs on the machine of each person who works in the repository, to drop calls or scale counts in every later pull request (T60). DR-064 flagged a change to those three kinds of file. The hook runs only as the project settings register it, though, in `.claude/settings.json` or in a `.claude/settings.local.json` that the repository tracks, which Claude Code applies over the first and reads hooks and variables from too, and a pull request that changes that registration, its events, its matchers or its command, changes when and how the hook runs as much as one that changes the hook file. The design-stage review of the change's revision of consent and the store found that DR-064 left such a change unflagged, and a review of the change's later commits, in a context separate from the one that wrote them, found that the flag named the first of the two files alone.

## Decision

When a pull request changes `.pr-cost.json`, the hook file at the path that the README gives (DR-065), `.claude/settings.json` or `.claude/settings.local.json`, the project settings files that can register it and set its environment, or any workflow file, the report's comment says so. This restates DR-064 and adds the registration.

## Alternatives

- Keeping DR-064's three kinds of file, which would let a pull request change when the hook runs, or stop it running, with no word in the comment.
- Flagging only a change to the hook's own entries in the project settings files, which would need the report to read and compare the settings, while a change elsewhere in a file, such as to the variables that it sets for the hook, can change what the hook does too.
- Flagging `.claude/settings.json` alone, which would leave unflagged a `.claude/settings.local.json` that a pull request adds, whose hooks and variables Claude Code applies over the first file's.

## Consequences

- A reviewer of the comment sees that the pull request changed how it is reported or recorded, also when it made `.pr-cost.json` unreadable (R93, T49), and a price changed by pinning another commit of the tool shows as a changed workflow (T30).
- A pull request that changes any other setting in either file, such as a permission rule, is flagged too, so the flag says that a file changed, not that the hook did.
- Scripts and local actions that a workflow runs are not flagged, though they can act with the same identity: the design's risk "[A workflow runs a script or a local action that a pull request changes]" leaves them to review of the diff, as T21's and T25's residuals do.

## Scope

This covers what the comment says when a pull request changes `.pr-cost.json`, the hook file, the settings files that can register it or any workflow file in the adopting repository. What it says when the merged commit's hook file is not the one at the report's own commit is DR-139 (The report names a hook that is not the report's own), where the hook file is looked for is DR-065 (The hook's path is fixed, not a setting), and a pull request that removes the calling workflow, and so goes unreported, is DR-051 (A pull request cannot turn off its own report).

## What reversing it would change

R93 in `switch-and-opt-in` would change, with its scenarios "A changed report is flagged", "A pull request that makes the configuration unreadable is flagged" and "A changed registration is flagged". So would the answers of T21, T30, T49 and T60, T25's residual, the design's decision 7 and the risk named above, task 4.1 and the switch and opt-in feature page. DR-065, whose fixed path serves the flag on a changed hook file, would be revisited, and so would DR-021, DR-051, DR-062 and DR-139, whose consequences rest on the flag.
