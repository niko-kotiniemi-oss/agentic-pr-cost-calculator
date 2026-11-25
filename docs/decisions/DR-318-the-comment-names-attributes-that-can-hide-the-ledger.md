# DR-318: The comment names the attributes that can hide the ledger, as git reads them from the repository alone

- **Type:** technical
- **Boundary:** outgoing
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R302
- **Threats:** T16, T323
- **Replaces:** none
- **Closed by:** none

## Context

A pull request's ledger files are in its diff, where a reviewer can see an edited count (T16), but attributes can hide them: `linguist-generated`, `-diff` and `binary` collapse or hide a file, a `diff` driver changes what is shown, and a `filter` such as Git LFS's stores a pointer in the file's place, which the report cannot read (T323). GitHub showed the reviewer the diff at the pull request's head, which a last push can change, and git on a runner also reads attributes from the runner's own files.

## Decision

The report runs `git check-attr --source` at the merged commit and at the pull request's head, reading no global, system or `info` attributes, so that only the repository's own files count, and macros are read as git reads them. Where either gives a ledger file that the pull request adds `linguist-generated`, `-diff`, `binary`, a `diff` driver or a `filter`, the comment says that GitHub may hide the ledger files or show a pointer in their place, and quotes nothing from any attributes file (R302). A pointer is counted as a refused file.

## Alternatives

- Reading the attribute files in Python: macros and git's order of files would be read otherwise than git reads them.
- The merged commit alone: an attribute that the reviewer met at the head and that a last push removed would not be named.

## Consequences

- An attribute set only in a push between the first commit and the head, and a diff that GitHub collapses for its size, are not named.
- `--source` needs git 2.40 or later on the runner, which the floor of 2.43 covers.

## Scope

This covers what the comment says of attributes. Whether the ledger's edits are accepted is DR-257.

## What reversing it would change

How hard it is to reverse: reversible. R302 and its scenarios would change, and T16's disclosure and T323's answer would lose the comment's line.
