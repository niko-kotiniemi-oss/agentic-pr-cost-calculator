# DR-191: The report says when a merge leaves the tool off

- **Type:** technical
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R172
- **Threats:** T49, T123
- **Replaces:** none
- **Closed by:** none

## Context

The report runs for a merge when the configuration before it or after it turns the tool on, and a file that is missing, disables the tool or cannot be read as a valid configuration leaves the tool off at its commit (DR-051). A pull request that changes the file is flagged (DR-186), in the same words whatever the change. Since a key that the tool does not know makes the file not valid (DR-190), a misspelt key, or a key that a later version adds, can turn the tool off at a merge whose comment says only that the configuration changed, and after it every pull request merges with no comment and no record of its calls. A repository that adopts the tool with such a file gets no comment at all. A check of DR-190's commit, in a context separate from the one that wrote it, found that nothing said that the tool was off.

## Decision

When the configuration before a merge turns the tool on and the configuration after it does not, the comment says, in the report's own words, that the tool is off after the merge, and whether the file there is missing, disables the tool or cannot be read as a valid configuration. When neither turns the tool on, the report posts no comment, and its job summary says the same of the file after the merge.

## Alternatives

- Leaving the flag on a changed configuration as the only sign, which reads the same for any edit of the file, and gives nothing for a repository that adopts the tool with a file that is not valid.
- Posting a comment for a merge that finds the tool off at both commits, which would comment in repositories that keep the tool off, against R19's scenario "Disabled means silent".
- Posting a short comment when the file after the merge sets `enabled` to true but is not valid, which would give a repository that adopts the tool with such a file a comment on its pull request without commenting where the tool is kept off, but would have the report act on part of a file that it takes to be not valid, against reading strictly what crosses into the tool (DR-044), and could not say what a file that is not JSON, or that gives `enabled` twice, sets.

## Consequences

- Whoever reads the comment of the pull request that turns the tool off, by a misspelt key or on purpose, sees that later pull requests go unreported until a pull request turns it on again (T49).
- Where every report finds the tool off, as after a key that the report's version does not know, each push's job summary says why, and so does the summary for a repository that adopts the tool with a file that is not valid (T123), or that keeps the tool off, which still gets no comment.
- The words are the report's own and quote nothing from the file, as with everything that the report writes (DR-044).
- The comment speaks for the report's version of the tool: where the repository's hook file is a later version that knows a key that the report's version does not, capture goes on recording while the comment says that the tool is off (T123).

## Scope

This covers what the report says when the configuration leaves the tool off. When the report runs is DR-051 (A pull request cannot turn off its own report), the flag on a changed configuration is DR-186 (The report flags changes to the switch, the hook, its registration and the workflows), and which files are valid is DR-021 (One file, `.pr-cost.json`, turns the tool on or off) and DR-190 (A configuration file with a key that the tool does not know is not valid).

## What reversing it would change

R172 in `switch-and-opt-in` would be removed, with its scenarios "A pull request after which the tool is off is told so", "A pull request that removes the configuration file is told that it is missing", "A pull request that disables the tool is told so", "A merge with the tool off at both commits says why in its job summary" and "A merge after which the tool is on says nothing of it being off", and so would its row in `docs/requirements.md`, and the scenarios "Disabled means silent" and "A key that the tool does not know turns the report off after the pull request that adds it" would say nothing of the job summary. The answers and residuals of T49 and T123, and T21's residual, would change, and so would DR-190's first consequence, the design's decisions 6 and 7, task 4.1, the report's steps in `docs/how-it-works.md`, A58, the feature pages of the switch and opt-in and of the report comment, and the changelog's line.
