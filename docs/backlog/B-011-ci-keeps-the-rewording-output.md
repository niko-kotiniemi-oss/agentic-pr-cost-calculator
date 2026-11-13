# B-011: CI keeps the rewording output

- **Status:** Planned
- **Last changed:** 2026-11-13
- **Brief:** CI keeps the rewording script's output, so that no one pastes a long output into comments.
- **Rests on:** T94
- **Issue:** 16
- **Pull requests:** none

## Problem

A pull request that rewords pages to the glossary carries the output of the default branch's rewording script in its comments. One such output ran to six comments, and three of them could not be posted whole, so pasting it by hand or by an agent can fail again.

## What done looks like

CI keeps the output where a reviewer reaches it from the pull request, and the job takes the script, and the way it runs, from the default branch, never from the pull request, so that the output stays the default branch's own account (T94). The pull request template and the script's own text say where the output is.

## Postponed points

None.
