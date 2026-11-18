# B-018: The PowerShell tool

- **Status:** Open to feedback and contributions
- **Last changed:** 2026-11-13
- **Brief:** Commands sent through Claude Code's PowerShell tool, which capture does not see.
- **Rests on:** DR-007
- **Issue:** none
- **Pull requests:** none

## Problem

Claude Code's PowerShell tool is on by default on Windows for some accounts, and capture does not see a commit or a change of branch made through it (DR-007), so the calls before such a commit can be missed or misplaced.

## What done looks like

Capture sees commits and changes of branch made through the PowerShell tool, as it does those made through the shell.

## Postponed points

None.
