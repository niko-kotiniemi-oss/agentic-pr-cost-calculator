# DR-216: The comment says when the hook's registration does not run the hook file

- **Type:** technical
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R202
- **Threats:** T152, T157
- **Replaces:** none
- **Closed by:** none

## Context

A repository registers the hook in `.claude/settings.json` with a command that carries the SHA-256 of the hook file that the adopter copied, and the command runs the file only when it matches, with each CRLF taken as LF, and otherwise runs none of it, prints nothing and exits with success (R88, DR-211). The README at each commit gives the registration with that commit's checksum, so a maintainer who pins one release and copies the registration from the README of another, such as the one on the default branch after the hook file changed, registers a command that runs nothing, and the sessions there record nothing through it, with no sign of why (T152). The report already flags a change to `.claude/settings.json` and `.claude/settings.local.json` (DR-186), and names a hook file that does not come from its own commit (R65).

## Decision

When `.claude/settings.json` or `.claude/settings.local.json` at the merged commit registers the hook's command with a checksum other than the SHA-256 of the hook file at that commit, with each CRLF taken as LF, the comment says that the hook's registration does not run the repository's hook file, and quotes nothing from either file. The report reads each of the two files as a blob within a size bound of their own, and leaves out, without stopping, one that is not a regular file, is above that bound, is not JSON that it can read, as when its arrays nest so deep that Python's JSON reader raises an error, or is JSON in which a value on the way to a hook's command is not of the type it has in a registration, saying nothing of a registration there.

## Alternatives

- The README alone, which says to take the hook file and its registration from the README at the commit that a published release names (R203), with nothing to show a mistake.
- The capture step saying so when it starts, which it cannot do, since a command whose checksum does not match runs none of the step.

## Consequences

- A registration that runs nothing shows in the comment of the first pull request that merges after it, rather than as a figure that is too low (T152).
- The report reads both settings files as git blobs, within a size bound of their own, as data, and quotes nothing from them, and a file that it cannot read stops no report (R202, T157).
- A session that runs the plugin still records, whatever the registration says.

## Scope

This covers the registration's checksum. A hook file that does not come from the report's commit is R65, and the flags for a changed configuration, hook, registration or workflow are DR-186 (The report flags changes to the switch, the hook, its registration and the workflows).

## What reversing it would change

R202 in `report-comment` would change, with its scenarios, and so would design decision 7, task 4.1, `docs/how-it-works.md`, the feature page for `report-comment`, and the answers of T152 and T157.
