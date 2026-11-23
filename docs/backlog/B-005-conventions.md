# B-005: Conventions

- **Status:** Done
- **Last changed:** 2026-11-23
- **Brief:** Printable ASCII in everything the project writes, line feeds in every checkout, paths that Windows can write, diagrams as code, and naming conventions, each checked in CI.
- **Rests on:** none
- **Issue:** none
- **Pull requests:** 59

## Problem

Only some pages are held to printable ASCII today, so an invisible or direction-changing character in any other file would go unseen. Nothing says how a diagram is kept, so one kept as an image cannot be reviewed in a diff, and names follow habit rather than a written convention.

## What done looks like

Everything that the project writes holds printable ASCII, and CI checks every file for invisible and direction-changing characters. Every checkout, on Linux, macOS or Windows, writes line feeds, and holds every tracked path under its own name. A file that an editor saves with Windows line endings passes every check as git will commit it, while a script that holds them, which bash cannot run, and a vendored file that holds them, which must match its pinned commit byte for byte, fail with the reason and how to write them again. Diagrams are Mermaid inside the Markdown, and a test fails on an image, a PDF or a video that no exception record names. A page gives the naming conventions, with their records, and ruff's naming rules are on.

## Postponed points

- From the threat review at implementation of pull request 29: a link from the roadmap or a backlog item may lead to any tracked file, which no check of hidden text reads, so a linked page could hold text that GitHub hides. Checking every file for such characters answers it.
