# DR-058: The hook file runs only when its checksum matches

- **Type:** security and privacy
- **Status:** closed
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R88, R122
- **Threats:** T59
- **Replaces:** none
- **Closed by:** DR-211

## Context

Any pull request to an adopting repository can change its copy of the hook file, which the registered command runs around every git command and at every stop (T59). The command runs the hook file in the working tree, which a checked-out branch can change, as checking out a pull request's branch to review it does, so without the check the next git command in a session would run that branch's code on the person's machine.

## Decision

The registered command carries the SHA-256 of the hook file that the adopter copied. It reads the file in the working tree once and runs what it read only when that matches the checksum, so a file that does not match runs none of its code, and the command still exits with success.

## Alternatives

- Having the script check its own checksum, which a branch that changes the script can change too.

## Consequences

- If Claude Code read its hook registrations again during a session, a branch checked out meanwhile could change the command along with the file, so the check rests on Claude Code keeping those it read at the start (see the design's context), which the threat model assumes and task 1.1 checks.
- A hook file that changes during a session stops capture for the rest of it, as the design's risk "[The hook file in the working tree changes during a session, as when the session checks out a branch that updates the hook]" says (T59), so task 4.4 has the README tell maintainers to review a pull request from another worktree or from its diff.
- The public surface takes the command by its form, not by the checksum, which changes with every change to the hook (R122).

## Scope

This covers whether the registered command runs the hook file. How the command ends is DR-031 (The registered command ends in `; exit 0`), how the adopter gets the file and its checksum is DR-022 (Adopters copy the hook file from a pinned commit), and the comment's flag for a pull request that changes the hook file is DR-064 (The report flags changes to the switch, the hook and the workflows).

## What reversing it would change

R88 in `usage-capture` would change, with its scenario "A changed hook file is not run", and so would R122 in `releases-and-compatibility`, the command in the design's decision 1 and the registration that task 2.3 documents in the README, the design's context and its risks, T59's answer, residual and assumption, and tasks 1.1, 2.3 and 4.4. Since the command's form is part of the public surface, the change would be released as a new major version (DR-096), and DR-022 and DR-031, whose update and command carry the checksum, would be revisited.
