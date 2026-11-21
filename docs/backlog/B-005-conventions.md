# B-005: Conventions

- **Status:** Planned
- **Last changed:** 2026-11-21
- **Brief:** Printable ASCII in everything the project writes, clones that work alike on Linux, macOS and Windows, diagrams as code, and naming conventions, each checked in CI.
- **Rests on:** none
- **Issue:** none
- **Pull requests:** none

## Problem

Only some pages are held to printable ASCII today, so an invisible or direction-changing character in any other file would go unseen. Nothing says how a diagram is kept, so one kept as an image cannot be reviewed in a diff, and names follow habit rather than a written convention.

## What done looks like

Everything that the project writes holds printable ASCII, and CI checks every file for invisible and direction-changing characters. Every clone, on Linux, macOS or Windows, holds line feeds and only paths that each of them can write, and a file that an editor saves with Windows line endings passes the checks as git will commit it, while a script so saved, which bash cannot run, fails with the reason. Diagrams are Mermaid inside the Markdown, and a test fails on an image, a PDF or a video that no exception record names. A page gives the naming conventions, with their records, and ruff's naming rules are on.

## Postponed points

- From the threat review at implementation of pull request 29: a link from the roadmap or a backlog item may lead to any tracked file, which no check of hidden text reads, so a linked page could hold text that GitHub hides. Checking every file for such characters answers it.
