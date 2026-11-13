# B-004: Two new fields on every record

- **Status:** Planned
- **Last changed:** 2026-11-13
- **Brief:** Each decision record says which way its boundary faces and how hard it is to reverse, each in a field of its own with a column in the index.
- **Rests on:** DR-121, DR-230, T76
- **Issue:** none
- **Pull requests:** none

## Problem

A record cannot say, in a field of its own, how hard it is to reverse, or whether its decision stays inside the tool, takes something in or sends something out. A record is never edited once accepted (DR-121), so a field on every record needs a narrow rule that lets one change add it, and until then a record says how hard it is to reverse in a sentence (DR-230).

## What done looks like

A record replaces DR-121 with a rule that lets one change add a field to every record and change nothing else. Every record gains the fields Boundary, as inside, incoming or outgoing, and Reversibility, as reversible, reversible with work or a one-way door, each with a column in the index of the records and a test that holds it.

## Postponed points

- From a review of the records' checks (its findings V7.3 and V7.10): a check that a record's Decided by date is not before the repository's first commit, and a check of a new record's file mode.
- From the threat model (T76): how to recover when two records with one number reach the default branch anyway, which the owner decides.
