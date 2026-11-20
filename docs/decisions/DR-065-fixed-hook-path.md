# DR-065: The hook's path is fixed, not a setting

- **Type:** security and privacy
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R65, R93
- **Threats:** T60
- **Replaces:** none
- **Closed by:** none

## Context

The report compares the adopter's hook file with its own (DR-139) and flags a change to it (DR-064), so it has to know where that file is. A pull request could edit the adopter's copy to drop calls or scale counts (T60), and it can change `.pr-cost.json` as it can any other file in the repository (DR-021).

## Decision

The hook's path is the one that the README gives, not one that `.pr-cost.json` names, so that the configuration has no field more to check, and a pull request has none with which to point the comparison at another file.

## Alternatives

- A path that `.pr-cost.json` names, turned down for the two reasons that the decision gives.

## Consequences

- Every adopter copies the hook file to the one path that the README's section on adopting the tool gives (task 4.4, DR-022).
- A pull request that moves the hook file leaves that path without it, which the comment names (R65), and an edit to the file at that path is flagged (R93, T60).
- The hook file's path is part of the public surface, so moving it is a breaking change for adopters (DR-096).

## Scope

This covers where the report looks for the adopter's hook file. What the comment says about that file is DR-064 (The report flags changes to the switch, the hook and the workflows) and DR-139 (The report names a hook that is not the report's own), how adopters copy it is DR-022 (Adopters copy the hook file from a pinned commit), and the checksum that the registered command checks before it runs the file is DR-058 (The hook file runs only when its checksum matches).

## What reversing it would change

R65 in `report-comment` and R93 in `switch-and-opt-in`, which both name the hook file at the path that the README gives, would change, and so would T60's answer. A path set in `.pr-cost.json` would add a field to its format, which task 1.2 documents, and the configuration file is part of the public surface, so the change would be released as a new major version (DR-096). The design's decisions 1 and 7, which both give the hook file's path as the one that the README gives, task 4.1, the README's section on adopting the tool (task 4.4) and the report's flow in `docs/how-it-works.md` would change too, and DR-021, whose file would gain the field, DR-064 and DR-139 would be revisited.
