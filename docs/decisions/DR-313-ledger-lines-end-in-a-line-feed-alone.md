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

The capture step ends every line of a ledger file with a line feed alone, on every system, and the report refuses a ledger line that ends otherwise and counts it as refused. The README gives adopters whose git has `core.safecrlf` on the attribute line `.pr-cost/** -text`, and this repository's own attributes get it when task 7.1 turns the tool on here (R306).

## Alternatives

- Reading both endings: two forms of one file would make a ledger line's bytes depend on where it was written.

## Consequences

- A ledger line that someone edits on Windows with an editor that writes CRLF is refused, and the comment counts it.

## Scope

This covers a ledger file's line endings. The ledger's form is the ledger's own records.

## What reversing it would change

How hard it is to reverse: reversible with work. R306 and the ledger format, which is part of the public surface, would change.
