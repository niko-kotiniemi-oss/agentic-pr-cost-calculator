# DR-294: The comment opens with a brief summary and keeps the detail in a collapsed section

- **Type:** scope
- **Boundary:** outgoing
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-11-09
- **Requirements:** R283
- **Threats:** T290
- **Replaces:** none
- **Closed by:** none

## Context

On 2026-11-09 the owner gave the direction for how the comment shows a cost: for an ordinary user, the default is a brief summary of the end results, each model with its input, output and cached tokens and its price, and the detailed figures stay available for when they are needed. The comment's earlier form gave every figure at once (R20).

## Decision

The comment opens with a brief summary: for each model, its input, output and cached tokens and its cost, then the CI cost and the total, and a line whenever a figure is a lower bound or something was not counted. Every other figure is in one collapsed section after it, in the same comment, which gives each token type's tokens, rate, currency and cost (R283).

## Alternatives

- Every figure at once, as before: the comment is long, and the result that most readers want is lost among the counts.
- The detail only through a separate command or run: a reader would need to run something to see what the comment counted, and the detail could differ from what the summary gave.

## Consequences

- The summary keeps every warning that a figure is a lower bound or that something was not counted, so a reader who never opens the collapsed section still learns that the figure is incomplete (R283).
- The collapsed section is part of the comment, so the detail needs no second run and always matches the summary.

## Scope

This covers the comment's form. How precisely it shows a cost is DR-295 (Costs show to the cent in the summary and to four decimals in the detail), and the block for programs is DR-296 (The comment holds its figures in a block that a program can read).

## What reversing it would change

How hard it is to reverse: reversible. R283 and its scenarios, the report comment's feature page and the golden set's comments would change. Nothing that adopters configure changes, but a program that reads the comment's text would read a new form, so the change would be noted in the changelog.
