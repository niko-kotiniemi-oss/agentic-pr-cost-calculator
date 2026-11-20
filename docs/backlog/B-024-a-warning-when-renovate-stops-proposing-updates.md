# B-024: A warning when Renovate stops proposing updates

- **Status:** Planned
- **Last changed:** 2026-11-20
- **Brief:** A daily check that tells the owner when Renovate seems to have stopped proposing updates, because an update it should have proposed is overdue or it has been quiet for five days.
- **Rests on:** R263, DR-265, DR-267
- **Issue:** none
- **Pull requests:** none

## Problem

Renovate opened no pull request in this repository from 2026-11-09 until the owner turned it on again on 2026-11-20, while updates that had passed its wait were left unproposed. Nothing told the owner: the dependency dashboard only stopped changing, which looks the same as a week with nothing to update.

## What done looks like

The owner learns, without looking, within days of Renovate stopping: a scheduled run fails and says which update is overdue or how long Renovate has been quiet, and the owner has seen such a warning arrive once. The check holds no write permission and reads no secret, and its tests use no network.

## Postponed points

None.
