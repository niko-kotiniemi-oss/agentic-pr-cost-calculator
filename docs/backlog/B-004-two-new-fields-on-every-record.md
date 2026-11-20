# B-004: Two new fields on every record

- **Status:** Done
- **Last changed:** 2026-11-20
- **Brief:** Each decision record says which way its boundary faces and how hard it is to reverse, each in a field of its own with a column in the index.
- **Rests on:** DR-230, DR-268, T76
- **Issue:** none
- **Pull requests:** 56

## Problem

A record cannot say, in a field of its own, how hard it is to reverse, or whether its decision stays inside the tool, takes something in or sends something out. A record was never edited once accepted, which DR-268 restates, so a field on every record needs a narrow rule that lets one change add it, and until then a record says how hard it is to reverse in a sentence (DR-230).

## What done looks like

A record supersedes the rule that a record changes only by being closed with a narrower one: one change may extend the form of every record by a field and change nothing else, while a decision still changes only by being superseded by a record that replaces it, which may close it. Every record gains the fields Boundary, as inside, incoming or outgoing, and Reversibility, as reversible, reversible with work or a one-way door, each with a column in the index of the records and a test that holds it.

## Postponed points

- From earlier reviews of the records' checks: a check that a record's Decided by date is not before the repository's first commit, and a check of a new record's file mode.
- From the threat model (T76): how to recover when two records with one number reach the default branch anyway, which the owner decides.
