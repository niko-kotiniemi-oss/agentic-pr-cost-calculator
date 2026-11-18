# B-006: Scope and visual documentation

- **Status:** Planned
- **Last changed:** 2026-11-13
- **Brief:** Records on what the project takes from elsewhere, a section of the page on how the tool works that lists everything incoming and outgoing, and diagrams in the README and the feature pages.
- **Rests on:** T94
- **Issue:** none
- **Pull requests:** none

## Problem

What the project takes from elsewhere, and what crosses its boundaries, is spread over many records and pages, so a reader cannot see it in one place. The pages explain the tool's flows in prose alone.

## What done looks like

Records say that nothing comes in from repositories or tools outside this one, that tests are built here, and that an adopter never needs to clone the whole repository, and a record says how vulnerabilities are found. The README says what the tool is for and which uses to avoid, and opens with the quickest way to start. The page on how the tool works has a section that lists everything incoming and outgoing, each with its record, and the README and the feature pages hold diagrams.

## Postponed points

- From the reviews of pull request 7 (its finding 1.3, T94): a requirement and a test that the README says what opting in records and publishes.
- From the reviews of pull request 1 (its finding 13): the threat model's diagram of the data flows gains the report's git fetches.
