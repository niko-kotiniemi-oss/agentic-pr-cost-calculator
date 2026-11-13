# B-012: Windows home folder variables

- **Status:** Planned
- **Last changed:** 2026-11-13
- **Brief:** A check, on Windows, of whether a project's Claude Code settings can set the variables that name the home folder, from which the opt-in is read.
- **Rests on:** DR-183, T119, A5
- **Issue:** 15
- **Pull requests:** none

## Problem

On Windows, where no home variable is set, the capture step and git find the home folder, and so the configuration that holds a person's opt-in, from three other variables. Claude Code's documentation names the variables that a project's settings cannot set, and names none of these three, so the opt-in relies on a fact that is not yet checked (A5, DR-183, T119).

## What done looks like

The check is run on Windows, and assumption A5 says what it showed. If a project's settings can set those variables, a change weighs how the home folder is read, while still reading the file that git reads.

## Postponed points

- From the security review of pull request 13 (its finding 1), as issue 15 gives it.
