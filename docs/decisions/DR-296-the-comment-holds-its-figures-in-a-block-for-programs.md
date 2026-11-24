# DR-296: The comment holds its figures in a block that a program can read

- **Type:** architecture
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the owner, 2026-11-01
- **Requirements:** R285
- **Threats:** T291, T303, T304, T305
- **Replaces:** none
- **Closed by:** none

## Context

On 2026-11-01 the owner asked how a pull request's cost is kept, and chose, from three options, a command that lists the pull requests' costs and writes a small file for each through an ordinary pull request (DR-222, B-008), over a commit that the report makes and over the comment alone. The command needs the figures exactly as the comment showed them, and the report writes nothing to the repository (DR-016).

## Decision

The comment's collapsed section ends with a fenced JSON block that holds the version of its own form, the currency in a field of its own, and every figure and count that the comment shows, written from the same values as the comment's text: each cost as its four-decimal figure, a cost under the smallest amount as zero with a flag, and a range as its two ends. The block's form is published with a JSON Schema, as the ledger format is, and says that a program reads the block only from the comment that carries the report's marker and that the report's identity posted (R285). The form and its schema are part of the public surface, and a released form's schema does not change (R122).

## Alternatives

- The command reads the comment's prose: any change of wording would break it.
- The command works the figures out again from the ledger and the jobs API: its figures could differ from those that the comment showed, through a later price row, a deleted run or a later release.

## Consequences

- The golden set holds the block from the first build, so the command writes what the comment showed.
- A block in a comment can be edited by anyone who can edit the comment, and imitated in a comment of anyone's, so the command reads it only from the report's own comment and as data, which its own change threat-models.
- A program can add the block's figures without parsing text such as "under" or a range.

## Scope

This covers what the comment holds for programs. The command itself is B-008 (An export command), and the comment's form is DR-294.

## What reversing it would change

How hard it is to reverse: reversible with work. R285 and its scenarios, the block's published form and the golden set's comments would change, and so would B-008, which reads the block.
