# DR-038: CI minutes come from job times, rounded up per job

- **Type:** technical
- **Boundary:** incoming
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R18, R62
- **Threats:** T22
- **Replaces:** none
- **Closed by:** none

## Context

The start and end of every job are available from GitHub's jobs API with no more than `actions: read`, though the API lists only each job's latest attempt unless it is asked for all of them, and gives a job that has not finished no end time (see the design's context). Counting only the latest attempts would leave out every re-run (T22).

## Decision

The report computes CI minutes from the start and end times that the jobs API gives for every attempt of every job it counts, and rounds each attempt's duration up to a whole minute.

## Alternatives

- The "billable" timing that GitHub gives for each run, which has been seen to return zero (see the design's context).

## Consequences

- A job that ran for 61 seconds counts as two minutes, and a job whose run was re-run counts the minutes of both attempts (R18, R62).
- Every minute in the comment can be recomputed from the jobs API, as the design's goals ask of every number in a report.
- A run that has not finished when the report runs has none of its jobs counted, and makes the CI cost incomplete (R64).
- The minutes are priced at GitHub's list rate, so included minutes and plan discounts are not modelled (DR-002).

## Scope

This covers how the minutes of a counted job are found and rounded. Which runs are counted is DR-019 (CI minutes come from the runs on the pull request's own commits), the rate that prices each minute, by runner type and day, is DR-020 (Prices come from a dated price table in the repository), and how many calls the report may spend reading runs and jobs is DR-039 (The report keeps to a call budget and a time limit).

## What reversing it would change

R18 in `ci-minutes` would change, with its scenario "A job's minutes are rounded up", and so would R62's count of every attempt, with its scenario "A re-run job counts every attempt". The design's context, which says why minutes come from job times, T22's answer, the CI cost formula in `docs/how-it-works.md`, the CI minutes feature page and task 3.3 would change too, and DR-019 and DR-039 would be revisited.
