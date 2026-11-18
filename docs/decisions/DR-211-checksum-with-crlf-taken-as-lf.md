# DR-211: The capture step runs only when its checksum matches, with each CRLF taken as LF

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R88, R122, R179
- **Threats:** T59, T143
- **Replaces:** DR-058
- **Closed by:** none

## Context

Any pull request to an adopting repository can change its copy of the hook file, which the registered command runs around every git command and at every stop (T59). The command runs the hook file in the working tree, which a checked-out branch can change, as checking out a pull request's branch to review it does, so without a check the next git command in a session would run that branch's code on the person's machine. The plugin's command runs the capture step from the plugin's own folder, which a checkout changes too where Claude Code loads the plugin in place (DR-197). DR-058 has the registered command run what it read only when that matches the checksum that it carries.

Git writes Windows line endings on checkout where the person's git has `core.autocrlf` set to `true`, or where an attribute gives a file `eol=crlf`, and Claude Code clones a marketplace that a person adds from its command line with the person's own git (A72). A checkout can so give the capture step other bytes than those whose checksum the command carries, in their line endings alone, and a command that compares the bytes as they are then runs none of the step, with no store, no ledger file and no flag (T143). Python reads each CRLF in a source file as LF, inside a triple-quoted string as well, as Python 3.11 and 3.13 did on 2026-11-10, so a step whose text matches once each CRLF is taken as LF runs as the program whose checksum was taken. This record restates DR-058 with that rule, for both commands.

## Decision

The registered command carries the SHA-256 of the hook file that the adopter copied, reads the file in the working tree once, and runs what it read only when that, with each CRLF taken as LF, matches the checksum. The plugin's command does the same with the SHA-256 of the plugin's capture step, in the plugin's own folder. So a checkout that changes only the step's line endings still runs it, while a file that differs in any other byte, a lone carriage return among them, runs none of its code, and the command still exits with success.

## Alternatives

- Comparing the bytes as they are, as DR-058 had it, which stops capture with no flag wherever a checkout writes Windows line endings, the clone of a marketplace that a person's git makes among them.
- Attributes that keep git from converting the plugin's files, with a README step that has adopters add one for their copy of the hook file, which leaves out every adopter who skips the step and every clone that a person's own configuration converts.
- Taking a lone carriage return as a line end too, which no checkout that this answers writes, and which would run more files than those that a checkout gives.
- Having the script check its own checksum, which a branch that changes the script can change too.

## Consequences

- A checkout that changes only the step's line endings runs it, so a person whose git writes Windows line endings is recorded, while any other change to the file runs none of its code (T59, T143).
- If Claude Code read its hook registrations again during a session, a branch checked out meanwhile could change the command along with the file, so the check rests on Claude Code keeping those it read at the start (A25), which task 1.1 checks.
- A hook file that changes during a session stops capture for the rest of it, as the design's risk "[The hook file in the working tree changes during a session, as when the session checks out a branch that updates the hook]" says (T59), so task 4.4 has the README tell maintainers to review a pull request from another worktree or from its diff.
- A filter that a person's own attributes file gives the step's path changes its bytes in another way, which no check here reads, and still stops that person's capture without a flag (T143).
- The public surface takes the command by its form, not by the checksum, which changes with every change to the hook (R122).

## Scope

This covers whether the registered command and the plugin's command run the capture step. How the command ends is DR-031 (The registered command ends in `; exit 0`), how the adopter gets the file and its checksum is DR-022 (Adopters copy the hook file from a pinned commit), the plugin is DR-197 (The capture step also comes as a Claude Code plugin, beside the hook file that adopters copy), and the comment's flag for a pull request that changes the hook file is DR-064 (The report flags changes to the switch, the hook and the workflows).

## What reversing it would change

R88 in `usage-capture` would change, with its scenarios "A changed hook file is not run" and "A hook file checked out with Windows line endings still runs", and so would R179, with its scenario "The plugin runs its step from a checkout with Windows line endings", R122 in `releases-and-compatibility`, the command in the design's decisions 1 and 17, T59's and T143's answers, and tasks 1.1, 2.3, 2.6 and 4.4. Since the command's form is part of the public surface, the change would be released as a new major version (DR-096), and DR-022 and DR-031, whose update and command carry the checksum, would be revisited.
