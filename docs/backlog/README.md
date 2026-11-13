# Backlog

Planned work, one item to a file. The [roadmap](../roadmap.md) is their index, in the order of the work, and the README's [briefing on how work flows](../../README.md#working-on-this-repository) says where an item stands among the stages of the work.

An item describes: it is neither a promise nor a date, and it is not a request to start the work. Work on an item starts only when someone asks for it, and an item is built only while the default branch gives its status as Planned or In progress.

## An item's form

An item is a file named B-NNN-words.md, numbered from B-001 with no gap. It opens with a heading that gives its ID and its title, and then these fields, in this order:

- **Status:** one of the five statuses below.
- **Last changed:** the day, in UTC and as YYYY-MM-DD, on which the item last changed. It is never a deadline.
- **Brief:** one to three sentences on what the item is.
- **Rests on:** the requirements, decision records, threats, assumptions, other items and tasks that it rests on, by their IDs, or none.
- **Issue:** the number of the issue that it came from, or none.
- **Pull requests:** the numbers of the pull requests that deliver it, or none.

Its sections follow, in this order:

- **Problem**: why it matters.
- **What done looks like**: the outcome, not a solution.
- **Postponed points**: each point that a review postponed to the item, with the review that postponed it, or None.
- **Why it was dropped**: for a dropped item, and for no other.

## What each status means

- **Open to feedback and contributions**: the owner has not agreed to it. Work on it starts with an issue, where it is discussed.
- **Planned**: the owner has agreed to it, by merging the pull request that made it planned.
- **In progress**: some of the work that delivers it has merged to the default branch, and more remains.
- **Done**: its pull requests have merged to the default branch, and `CHANGELOG.md` names the release that holds it.
- **Dropped**: it will not be built, and its section says why.

An item becomes planned only through a pull request that the owner merges. An issue on which the owner agrees is where a proposal is discussed, not where it is agreed. Issues and pull requests are named by their numbers and never linked, since anyone can write text on GitHub.

An item keeps its file once the default branch holds it, done or dropped, so that every link to it still leads to it, and its date moves whenever its text changes. The tests in tests/test_backlog.py hold all of this.
