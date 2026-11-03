# DR-190: A configuration file with a key that the tool does not know is not valid

- **Type:** technical
- **Status:** accepted
- **Decided by:** the owner, 2026-11-03
- **Requirements:** R92, R122, R171
- **Threats:** T49, T123
- **Replaces:** none
- **Closed by:** none

## Context

`.pr-cost.json` holds one key, `enabled`, which turns the tool on or off in the repository (DR-021). Capture reads the file in the working tree and the report reads it at the default branch's commits before and after the merge, and both take a file that is missing, is not a regular file, is larger than its size bound or is not valid to leave the tool off, without stopping the report (R92), whose comment flags a pull request that changes the file (R93). Nothing said whether a file that holds a key besides `enabled` is valid. A person can misspell a key, and a later version can add one. The configuration file is part of the public surface, so a release that changes its format raises the major number (DR-096). The check of the fixes made after the review of the change's revision of consent and the store found the case undecided, and the owner was asked.

## Decision

A configuration file that holds a key that the configuration's format does not document, in the version of the tool that reads it, is not valid, whatever that key's value and whatever `enabled` says. So capture records nothing while the file in the working tree holds one, and the report takes the file to leave the tool off at a commit where it holds one, as it does any file that is not valid (R92).

## Alternatives

- Passing over a key that the format does not document, which the change recommended: an earlier version would keep working when a later version's key is added to the file, and such a key could never turn capture on for anyone, but a misspelt key would go unnoticed, and the tool would do what the file's author did not mean.

## Consequences

- A misspelt key leaves the tool off, and the pull request that adds it still gets its report, flagged, when the file before the merge turned the tool on, while the pull requests after it get none as long as the file holds it (R171, T49). The change adds that this comment says that the tool is off after the merge, and that each later job summary says why (DR-191).
- A key that a later version adds turns every earlier version off where the file holds it: the report at a pin of an earlier version, and capture in a working tree whose hook file is earlier. A key that a later version no longer documents turns that version off where the file still holds it. The change answers this (T123): since the configuration file is part of the public surface (DR-154), the surface manifest names each key that the format documents, with the values that each takes, so that the release check refuses a release that adds or drops one without a raised major number and a `### Breaking` section (R122, DR-096), and the README's section on adopting the tool, which task 4.4 writes, says to add such a key only with or after the pull request that moves the hook file and the calling workflow's pin to that version, and to drop one that a later version no longer documents before or with it.
- If an organization mode, which DR-189 leaves to a later change, adds a key, an earlier version takes a file that holds it to be not valid, and leaves the tool off rather than running without the mode.

## Scope

This covers which keys a valid configuration file holds. What the file turns on, and where capture reads it, is DR-021 (One file, `.pr-cost.json`, turns the tool on or off), how the report reads it at the commits before and after the merge, and what a file that is not valid does there, is DR-051 (A pull request cannot turn off its own report), and the flag on a pull request that changes the file is DR-186 (The report flags changes to the switch, the hook, its registration and the workflows).

## What reversing it would change

R171 in `switch-and-opt-in` would keep only its clauses on a key given twice and on `enabled` (DR-192), and would lose its scenarios "A key that the tool does not know turns capture off" and "A key that the tool does not know turns the report off after the pull request that adds it", and the configuration's format, which task 1.2 documents in `docs/ledger-format.md`, would say that such a key is passed over, and R171's row in `docs/requirements.md` would change with its title. T49's answer would change, T123 would be retired, and a threat that a misspelt key goes unnoticed would be added. The design's decision 6, tasks 2.4, 4.1 and 4.4, `docs/how-it-works.md`, the switch and opt-in feature page, A23's note of T123 and the changelog's line would change too. R122's scenario "The surface manifest names the configuration's keys" would stay, since a key that a version adds changes the public surface either way. A file that one version takes to be not valid would turn the tool on in another, so the change would be a breaking one for adopters (DR-096).
