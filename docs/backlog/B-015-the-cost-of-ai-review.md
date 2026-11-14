# B-015: The cost of AI review

- **Status:** Planned
- **Last changed:** 2026-11-13
- **Brief:** The cost of AI review by an app or a job in CI, which the first version leaves out.
- **Rests on:** DR-004
- **Issue:** none
- **Pull requests:** none

## Problem

A pull request's review by an AI app or by a job in CI uses model tokens too, but the first version counts only the calls that an agent makes while it works (DR-004), so a pull request's figure leaves review out.

## What done looks like

A pull request's figure can include the cost of its AI review, by an app or a job in CI, shown apart from the agent's own calls.

## Postponed points

None.
