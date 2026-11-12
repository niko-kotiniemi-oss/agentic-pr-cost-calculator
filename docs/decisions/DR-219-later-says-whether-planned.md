# DR-219: Each item under Next and Later says whether it is planned

- **Type:** process
- **Status:** accepted
- **Decided by:** the owner, 2026-11-11
- **Requirements:** R207
- **Threats:** T159, T161
- **Replaces:** none
- **Closed by:** none

## Context

What the first version leaves out is of two kinds. Some is planned for a later change, such as the cost of AI review by an app or a job in CI (DR-004). Some is left to the future for feedback and contributions to call for, such as a mode in which an organization turns its members' capture on and they cannot turn it off (DR-189), other agents than Claude Code (DR-003) and services other than GitHub (DR-006, DR-160). A public list headed Later can read as a promise of all of them, and a list headed Next reads as one even more. Some of these items, such as the organization mode, are left to a change with its own spec, its own threat review and the owner's decision (DR-189), so an invitation to contribute that says nothing of that would lead a contributor to build what cannot be merged.

## Decision

The roadmap keeps one list under Later, as the owner chose on 2026-11-11, and each item under Next and Later opens with **Planned.** or **Open to feedback and contributions.** Later opens by saying that work on an item starts with an issue on which the owner agrees, and that some items need a spec, a threat review and the owner's decision first. Each record that the README's list of what the first version does not support links is named by an item under Later, so that what the README leaves out has its place on the roadmap.

## Alternatives

- Later holding only what is planned, with a fourth list for what is open to contributions.
- Every item that the first version leaves out under Later, with no mark, which reads as a promise of each.
- The mark under Later alone, which leaves Next, the list nearest to a promise, unmarked.

## Consequences

- A test fails when an item under Next or Later opens with neither mark, when Later does not open with its sentence on how work on an item starts, and when a record that the README's list links is named by no item under Later (R207).
- An item moves from open to planned only by a pull request that changes its mark, which the owner reviews (T161).
- A contributor reads, before building an item, that it starts with an issue and may need the owner's decision first (T159).

## Scope

This covers how Next and Later mark their items and how Later says work on one starts. The roadmap's place and sections are DR-218 (A roadmap says what is now, next and later).

## What reversing it would change

R207 in `project-standards` would change, with its scenarios, and so would design decision 12, task 1.26, the answers of T159 and T161 and the roadmap's Next and Later.
