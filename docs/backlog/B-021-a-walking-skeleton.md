# B-021: A walking skeleton

- **Status:** Planned
- **Last changed:** 2026-11-14
- **Brief:** The thinnest path from a session's calls through capture and a ledger file in a commit to the report's figure, run once in a real Claude Code session. It comes right after the guide and before the other items that prepare the build.
- **Rests on:** DR-233, DR-236, R223
- **Issue:** none
- **Pull requests:** none

## Problem

The design is long and none of the tool's code runs yet, so its riskiest assumptions, those about Claude Code's transcripts and hooks, would first be met by the build, after the requirements had been corrected without what a running path would show.

## What done looks like

A pull request of its own, whose design the owner approves before it is built, builds the thinnest path that runs end to end and runs it once in a real Claude Code session, and what the run shows goes into the specs and the assumptions first (DR-232, DR-233). The path builds a test seam, which the corrected requirements then name in the design (B-007). The run gives a record of a real transcript's shape, with no values, as a named exception to the rule in `CLAUDE.md` against transcripts, with a record of its own and a test that holds it, so that the fixtures have a real case to be compared with (B-007). The run happens in a repository made for it, from a project that holds no other repository, and records nothing without that repository's switch and the person's own opt-in, while this repository keeps from it only what that pull request asks the owner to keep (DR-236).

## Postponed points

- From the assessment of 2026-11-12, with the owner's answers that day: a scratch repository that calls the reusable workflow once, kept to that use.
