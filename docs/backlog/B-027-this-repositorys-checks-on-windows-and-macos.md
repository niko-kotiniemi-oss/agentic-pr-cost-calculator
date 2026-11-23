# B-027: This repository's checks on Windows and macOS

- **Status:** Open to feedback and contributions
- **Last changed:** 2026-11-21
- **Brief:** This repository's own checks, scripts and hooks run on Windows and macOS as they do on Linux, so that a contributor on either can work on the tool, and CI shows it.
- **Rests on:** R276, R277, DR-281, DR-282, A4
- **Issue:** none
- **Pull requests:** none

## Problem

Every job of CI runs on Linux, and nothing has run this repository's tests, scripts or hooks on Windows or macOS. A test of the specs' form plants a path that holds a line feed and a carriage return, which Windows cannot hold; the scripts are written for bash; and both start commands of `.claude/settings.json` are written for a POSIX shell, while on Windows without Git Bash, Claude Code runs a hook's command in PowerShell (A4). B-005 makes each checkout write line feeds and hold only paths that Windows can write, and the tool's own trials on Windows cover what adopters run, but neither runs this repository's checks there.

## What done looks like

This repository's checks pass on Windows and macOS as they do on Linux, the session's start hooks and the scripts among them, and CI shows it on each pull request; a check that cannot run on one of them says so, and why.

## Postponed points

- From the threat review at design of pull request 59, as the owner chose on 2026-11-21: that the tests plant a path that Windows cannot hold while CI runs on Linux alone (D8 of boundary 7), and that the start commands of `.claude/settings.json` are written for a POSIX shell (boundary 9).
