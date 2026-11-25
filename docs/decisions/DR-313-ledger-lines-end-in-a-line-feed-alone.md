# DR-313: Ledger lines end in a line feed alone on every system

- **Type:** technical
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-21
- **Requirements:** R306
- **Threats:** T316
- **Replaces:** none
- **Closed by:** none

## Context

Python on Windows writes a carriage return before each line feed unless it is told otherwise, so a ledger file written there would differ from one written elsewhere, and git may convert or refuse it. The owner asked on 2026-11-21 that no design break with Windows line endings.

## Decision

The capture step ends every line of a ledger file with a line feed alone, on every system. The report splits each ledger file's bytes on line feeds before it decodes them, for the files that a pull request adds and those that the default branch held alike, and takes a line that holds a carriage return anywhere, or a last line that no line feed ends, as breaking the format, so that such a first line makes its file refused. The README gives every adopter `.pr-cost/** -text -filter -linguist-generated` as the last line of the root `.gitattributes`, since a later line would rank above it, and this repository's own attributes get it when task 7.1 turns the tool on here (R306).

## Alternatives

- Reading both endings: two forms of one file would make a ledger line's bytes depend on where it was written.
- Splitting decoded text as Python's `splitlines` does: it also splits on a lone carriage return, U+0085 and U+2028, so the count of lines would depend on what a line holds.

## Consequences

- A ledger line that someone edits on Windows with an editor that writes CRLF is refused, and the comment counts it.

## Scope

This covers a ledger file's line endings. The ledger's form is the ledger's own records.

## What reversing it would change

How hard it is to reverse: reversible with work. R306 and the ledger format, which is part of the public surface, would change.
