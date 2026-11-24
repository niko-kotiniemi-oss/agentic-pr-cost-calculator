# DR-303: The comment and the job summary hold no dollar sign and no tilde outside inline code

- **Type:** technical
- **Boundary:** outgoing
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R286
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

GitHub reads text between two dollar signs as a formula and text between tildes as struck through, so a comment that writes amounts with a dollar sign can show them as neither, as issue 18 found.

## Decision

The comment and the report's job summary hold no dollar sign and no tilde outside inline code and code blocks fenced with backticks, hold no code block fenced with tildes, and write each currency by its code (R286). GitHub renders no formula inside a fenced block, so the block for programs may name its schema with `$schema`.

## Alternatives

- Escaping each dollar sign: GitHub's handling of an escaped dollar sign has changed before, and an escape can be lost when the text is copied.

## Consequences

- Amounts read as `USD 1.23` rather than with a symbol.

## Scope

This covers two characters in the comment. The comment's own words are R21's and R97's.

## What reversing it would change

How hard it is to reverse: reversible. R286 and its scenario would change. Nothing that adopters configure changes.
