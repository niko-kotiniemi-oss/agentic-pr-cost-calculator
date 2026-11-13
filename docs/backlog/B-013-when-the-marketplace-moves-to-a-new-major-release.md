# B-013: When the marketplace moves to a new major release

- **Status:** Planned
- **Last changed:** 2026-11-13
- **Brief:** A decision on when the marketplace moves to a new major release, so that repositories can move their pins first.
- **Rests on:** DR-204, DR-208, A72
- **Issue:** 23
- **Pull requests:** none

## Problem

A person who adds this repository as a marketplace gets each new version of its plugin, and the plugin's release writes the ledger files (DR-208). A major release can change the ledger format, which reports pinned to an earlier major release refuse, so once the marketplace moves, repositories that have not moved their pins lose those files from their figures (DR-204).

## What done looks like

The README and each major release's notes say when the marketplace moves to that release, and the pull request that moves it comes at that time.

## Postponed points

- From the threat review at design of pull request 22 (its threat 10), as issue 23 gives it.
