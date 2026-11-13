# B-005: Conventions

- **Status:** Planned
- **Last changed:** 2026-11-13
- **Brief:** Printable ASCII in everything the project writes, diagrams as code, and naming conventions, each checked in CI.
- **Rests on:** none
- **Issue:** none
- **Pull requests:** none

## Problem

Only some pages are held to printable ASCII today, so an invisible or direction-changing character in any other file would go unseen. Nothing says how a diagram is kept, so one kept as an image cannot be reviewed in a diff, and names follow habit rather than a written convention.

## What done looks like

Everything that the project writes holds printable ASCII, and CI checks every file for invisible and direction-changing characters. Diagrams are Mermaid inside the Markdown, and a test fails on an image, a PDF or a video that no exception record names. A page gives the naming conventions, with their records, and ruff's naming rules are on.

## Postponed points

None.
