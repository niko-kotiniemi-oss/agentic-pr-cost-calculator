# DR-022: Adopters copy the hook file from a pinned commit

- **Type:** architecture
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R12, R53, R72, R88
- **Threats:** T28, T54, T59, T60, T69
- **Replaces:** none
- **Closed by:** none

## Context

The hook runs on the machine of everyone who works in an adopting repository, so how its code reaches them is part of T28. Python's isolated mode keeps it to a single file, as the design's decision 1 says, and the report comes from the commit that the adopter's calling workflow pins (DR-062).

## Decision

The hook reaches adopters as one file, which each adopter copies into their repository, at the path that the README gives, from the full commit that their calling workflow pins, and checks against the SHA-256 checksum that the README at that commit gives. The copy is then reviewed and versioned as the adopter's own code, and a newer release is taken in one pull request that changes the file, the checksum that its registration carries and the workflow's pin at once.

## Alternatives

- Delivering the script as a Claude Code plugin, which a repository's own session hook can install for everyone, as this repository's hook installs Superpowers, so it would give no stronger consent than the opt-in.
- Publishing to PyPI, which adds an account and a token to protect for a tool that adopters copy one file of.
- Copying the file from a tag rather than a full commit, since a tag can be moved (T28).

## Consequences

- A matching checksum shows only that the copy is complete. Trust in the commit rests on the adopter's choice of it, as it does for the workflow, which T28's residual accepts.
- Update bots can move the pin and leave the copy behind, so the hook and the report can come from different commits, as the design's risk "[An adopter updates the hook and the workflow pin at different times]" says (T54). The file's first line names its release (R53).
- A fix to the hook reaches only the adopters who copy the new file, and no advisory process for security fixes is designed yet (T54).

## Scope

This covers how the hook file reaches an adopter and how the copy is updated. How the report's code runs is DR-062 (The report runs its own pinned code), how releases are made is DR-148 (Each release is made from a tag), and where the copy sits is DR-065 (The hook's path is fixed, not a setting).

## What reversing it would change

R12, R53 and R88 in `usage-capture` would change, R88 for the checksum that the registered command carries, and so would R72's clause in `releases-and-compatibility` that compares a release's hook checksum with the hook file's and the README's. So would the design's decisions 1 and 11, T28's answer and residual, the answers of T54, T59, T60 and T69, the proposal's impact, the parts table and the merge and price-update flows in `docs/how-it-works.md`, and tasks 2.3 and 4.4, which build the file and the README's section on adopting the tool. The hook's path and registered command are part of the public surface, so the change would be a breaking one for adopters (DR-096), and DR-027, DR-040, DR-058, DR-064, DR-065 and DR-139, which rest on a copied file, would be revisited.
