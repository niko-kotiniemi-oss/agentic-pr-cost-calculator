# B-003: Context files and the rules agents follow

- **Status:** Planned
- **Last changed:** 2026-11-13
- **Brief:** Rules that load only for the files they concern, a shorter `CLAUDE.md`, and rules on how reviews are reported and how files are staged.
- **Rests on:** DR-134
- **Issue:** none
- **Pull requests:** none

## Problem

`CLAUDE.md` loads into every session in full and grows with each rule, so an agent reads rules for files that it never touches. Some practices that the project follows, such as how review findings are reported and how files are staged for a commit, are kept nowhere that an agent loads.

## What done looks like

Path-scoped rules, which Claude Code loads only when an agent works on the files that they name, point agents to the parts of the long pages that they need, and `CLAUDE.md` is shorter. Rules, each with its record, say that a review's findings and their resolutions go on the pull request as separate comments, with an index, and that files are staged by name, never all at once. The Renovate configuration keeps the Python that the project develops on at the oldest supported release (DR-134), and says that an update of OpenSpec or Superpowers has its generated files refreshed on its branch once its diff has been read. `CONTRIBUTING.md` says that a contributor needs neither Claude Code nor Superpowers.

## Postponed points

- From the threat review at design of the change's first pull request (pull request 1, its item 8): how an agent reads the pull request and issue templates and `CONTRIBUTING.md`.
