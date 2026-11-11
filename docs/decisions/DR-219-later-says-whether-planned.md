# DR-219: Each item under Later says whether it is planned

- **Type:** process
- **Status:** accepted
- **Decided by:** the owner, 2026-11-11
- **Requirements:** R207
- **Threats:** T161
- **Replaces:** none
- **Closed by:** none

## Context

What the first version leaves out is of two kinds. Some is planned for a later change, such as the cost of AI review by an app or a job in CI (DR-004). Some is left to the future for feedback and contributions to call for, such as a mode in which an organization turns its members' capture on and they cannot turn it off (DR-189), other agents than Claude Code (DR-003) and services other than GitHub (DR-006, DR-160). A public list headed Later can read as a promise of all of them.

## Decision

The roadmap keeps one list under Later, and each of its items opens by saying whether it is planned or open to feedback and contributions. Each record that the README's list of what the first version does not support links is linked by an item under Later, so that what the README leaves out has its place on the roadmap.

## Alternatives

- Later holding only what is planned, with a fourth list for what is open to contributions.
- Every item that the first version leaves out under Later, with no mark, which reads as a promise of each.

## Consequences

- A test fails when an item under Later opens with neither mark, and when a record that the README's list links is linked by no item under Later (R207).
- An item moves from open to planned only by a pull request that changes its mark, which the owner reviews (T161).

## Scope

This covers how Later marks its items. The roadmap's place and sections are DR-218 (A roadmap says what is now, next and later).

## What reversing it would change

R207 in `project-standards` would change, with its scenarios, and so would design decision 12, task 1.26, the answer of T161 and the roadmap's Later.
