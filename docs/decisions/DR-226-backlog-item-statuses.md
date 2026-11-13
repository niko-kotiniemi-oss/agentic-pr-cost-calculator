# DR-226: Each backlog item has one of five statuses, and only a merged pull request makes it planned

- **Type:** process
- **Status:** accepted
- **Decided by:** the owner, 2026-11-11 and 2026-11-13
- **Requirements:** R207, R214, R218
- **Threats:** T159, T161, T166
- **Replaces:** DR-219
- **Closed by:** none

## Context

DR-219 had each item under the roadmap's Next and Later open with one of two marks, planned or open to feedback and contributions, as the owner chose on 2026-11-11, so that a public list would not read as a promise of everything on it, and so that a contributor would not build an item, such as the organization mode that DR-189 leaves to a change with its own spec, threat review and owner's decision, that could not be merged. It had Later open by saying that work on an item starts with an issue on which the owner agrees. With planned work kept as backlog items (DR-225), each item needs to say how far it is from being built, and the owner's agreement, which DR-219 placed on an issue, is text that anyone can write beside and that lives outside git. On 2026-11-13 the owner agreed to five statuses, building on the two marks, Open to feedback and contributions, Planned, In progress, Done and Dropped, and to an item becoming planned only through a pull request that the owner merges, in place of the rule that the owner agrees on an issue.

## Decision

Each backlog item gives one of five statuses: `Open to feedback and contributions`, for an item that the owner has not agreed to; `Planned`, for one that the owner has agreed to; `In progress`, once some of the work that delivers it has merged and more remains, so that the default branch can show it; `Done`; and `Dropped`, with a section that says why. An item that is `In progress` or `Done` names at least one pull request, and an item that one pull request delivers whole goes from `Planned` to `Done` in that pull request. An item counts as the default branch gives it. An item becomes `Planned` only through a pull request that the owner merges, and, compared with the base commit, an item is added only as open or planned and never moves from open or dropped straight to in progress or done, so that its agreement is a change to its status line that the diff shows, so that the owner's agreement is kept in the repository's history; an issue on which the owner agrees is where a proposal is discussed, not where it is agreed. Later opens by saying that work on an item that is open to feedback and contributions starts with an issue, that an item is built only once it is `Planned`, which only a pull request that the owner merges makes it, and that some items need a spec, a threat review and the owner's decision first. Each record that the README's list of what the first version does not support links is named in the field Rests on of an item listed under Later, so that what the README leaves out has its place on the roadmap.

## Alternatives

- The two marks of DR-219, with the owner's agreement on an issue: the agreement is outside git, beside text that anyone writes, and the roadmap cannot say which items are under way or when they last changed.
- Statuses with no In progress, leaving open pull requests to say what is under way: a reader of the roadmap would not see it.
- A status set by a label on the item's issue: labels are the owner's to set on GitHub, change without review, and no test can read them.

## Consequences

- A test fails when an item gives no status or another one, when an item in progress or done names no pull request, when a dropped item does not say why, and when Later does not open with its sentence or a record that the README's list links is named by no item under Later (R207, R214).
- A test fails on an item added as in progress, done or dropped, and on one moved from open or dropped to in progress or done, compared with the base commit (R218, T159, T166).
- A pull request that makes an item planned is a change that the owner reads before merging, and the pull request template asks a pull request that does so, or that changes what an agreed item's What done looks like says, to say it, and where the owner asked for it (T166). Whether the owner meant to agree rests on that review (A15).
- DR-219's last section named no other record to revisit, and its requirement, R207, and threats, T159 and T161, change in this change.
- A contributor reads, before building an item, whether it is agreed and that an item open to feedback starts with an issue (T159), and a reader of the roadmap sees which items are agreed, under way, or only open (T161).

## Scope

This covers an item's statuses, how an item becomes planned, and how Later says work on one starts. Where items are kept and the roadmap's index are DR-225 (Planned work is kept as backlog items, and the roadmap is their index). What an agent may start is DR-227 (The roadmap and the backlog describe, and lead only to this repository's own files).

## What reversing it would change

How hard it is to reverse: reversible. The statuses are text in each item, which one pull request can change. R207, R214 and R218 in `project-standards` would change, with its scenarios, and so would design decision 12, task 1.27, `CLAUDE.md`'s rule on what describes, the README's briefing, `CONTRIBUTING.md`, the pull request template, the answers of T159, T161 and T166, and every item's status. DR-227 would be assessed again, since what an agent may build rests on the status.
