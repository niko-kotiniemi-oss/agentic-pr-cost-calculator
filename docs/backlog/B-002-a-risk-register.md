# B-002: A risk register

- **Status:** Planned
- **Last changed:** 2026-11-13
- **Brief:** Each threat rated as if its answer were not built, beside its rating with the answer in place, on a page generated from the threat model. Every high or critical risk gets a further answer.
- **Rests on:** DR-112
- **Issue:** none
- **Pull requests:** none

## Problem

Each threat's likelihood is rated with its answer in place (DR-112), so the threat model shows how much risk remains, but not how much each answer removes. A reader cannot tell which answers carry the most weight, and nothing asks that the highest risks get more than one answer.

## What done looks like

A page, generated from the threat model so that each rating lives in one place, gives each threat its raw rating, made by reviewers of their own as if its answer were not built, beside its rating with the answer in place, with what answers it and the assumptions it rests on. A test fails when the page and the threat model disagree. A record sets the bands of low, medium, high and critical risk, and says what happens to a risk that no answer brings below high. Every high or critical risk has a further answer, which the item on the tool's requirements (B-007) builds.

## Postponed points

None.
