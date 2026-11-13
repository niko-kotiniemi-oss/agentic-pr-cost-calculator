# B-010: Every reader finds the specs at any depth

- **Status:** Planned
- **Last changed:** 2026-11-13
- **Brief:** Every reader of the specs finds them at any depth, as the test of the specs' form does.
- **Rests on:** R177, T124
- **Issue:** 19
- **Pull requests:** none

## Problem

The test of the specs' form reads a spec at any depth, as OpenSpec does (R177), and names it by OpenSpec's ID, but the repository's other readers of the specs look one folder down, or name a spec by the folder that holds it. No spec is nested today, so nothing fails now, but a nested spec would be read one way by OpenSpec and another by those checks (T124).

## What done looks like

Every test and script that reads the specs finds them as the test of the specs' form does and names them by the same ID, each with a test that plants a spec two folders deep.

## Postponed points

- From the threat review at implementation of pull request 17, and the answer to its simplify review: the documentation test names a spec by the folder that holds it, the threat model's and the assumptions' tests read specs one folder down only, and the glossary's and the records' tests find a commit's specs by a pattern that matches one folder down only.
