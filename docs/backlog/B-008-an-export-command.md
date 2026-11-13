# B-008: An export command

- **Status:** Planned
- **Last changed:** 2026-11-13
- **Brief:** A command that lists pull requests' costs and writes each one as a small Markdown file in a folder that the adopter chooses. The file reaches the repository through an ordinary pull request, while the report itself still writes nothing.
- **Rests on:** DR-222, DR-016, B-007
- **Issue:** none
- **Pull requests:** none

## Problem

A pull request's cost is kept only in its comment: the ledger holds token counts, not cost, and the report writes nothing to the repository (DR-016). An adopter who wants each pull request's cost kept beside the code has no way to do it.

## What done looks like

A command writes each listed pull request's cost as a small Markdown file, with exactly the figures that its comment showed, read from the block for programs that the item on the tool's requirements (B-007) adds to the comment, into a folder that the adopter chooses. The adopter commits the files through an ordinary pull request, and no job gains write access to the default branch (DR-222).

## Postponed points

None.
