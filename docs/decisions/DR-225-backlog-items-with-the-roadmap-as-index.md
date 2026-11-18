# DR-225: Planned work is kept as backlog items, and the roadmap is their index

- **Type:** process
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-13
- **Requirements:** R206, R211, R213, R215, R216, R217
- **Threats:** T161, T167
- **Replaces:** DR-218
- **Closed by:** none

## Context

DR-218 gave the repository a roadmap of what is now, next and later, as the owner asked on 2026-10-29, with each item a few sentences on the page itself. The full explanation of the items under Now, the pull requests that come before the build, was kept only in the owner's planning notes outside the repository, so neither a contributor nor an agent reading a clone could read what an item is for. Reviews homed each point they postponed in one of those future pull requests by name, and when an item is delivered by two pull requests, or two items by one, every such home is wrong, with nothing to check that it still leads anywhere. No item said how far it was from being built or when it last changed. On 2026-11-13 the owner agreed that planned work is kept in backlog items, as Markdown files in the repository, each with its status, the date it last changed and a brief of one to three sentences, that the roadmap is their index, and that issues stay for proposals from anyone, discussion and bugs. The change chose the rest of the form.

## Decision

Each piece of planned work is a backlog item, one Markdown file in `docs/backlog/`, named `B-NNN-words.md`, numbered from B-001 in the order that items are added, beside a `README.md` that gives the form, links the roadmap, and says that an item describes, is neither a promise nor a date and is not a request to start work, what each status means, and that `Done` means merged, with `CHANGELOG.md` naming the release that holds it. The roadmap opens by saying the same of its items. An item opens with its ID and title and six fields: its status, the date it last changed, a brief of one to three sentences, the requirements, records, threats, assumptions and tasks it rests on, the issue it came from, by number, and the pull requests that deliver it. Its sections follow: the problem and why it matters, what done looks like as an outcome, the points that reviews postponed to it, each naming its review, and for a dropped item why it was dropped. An item names a published source outside the repository by its title, and a source that is not published not at all. An item changes only through a pull request, and is never removed or renamed, so that every link to it still leads to it once it is done or dropped.

The roadmap, `docs/roadmap.md`, keeps the sections that DR-218 gave it, Now, Next, Later, Known limitations and Known bugs, in that order, and the README's list of documentation links it. Now, Next and Later become the index of the items that are still open: one line for each, in the order of the work, linking the item's file and giving its ID, title, status, date and brief as the item gives them. The roadmap is the one home of the order, and the item of everything else. Now lists only items that are agreed, and ends with one line on the build that links the change's proposal and tasks, which are the build's home. Each item listed under Next or Later rests on at least one ID. An item that is done or dropped leaves the roadmap and stays in the folder, and the changelog says what shipped. A pull request that finishes, adds or moves an item changes the item and the roadmap with it. A review's postponed point goes into a backlog item, and the review's index names the item as its home.

## Alternatives

- The roadmap as DR-218 had it, with each item's text on the page and the explanation of the items under Now outside the repository: contributors and agents cannot read what an item is for, and postponed points are homed in pull requests that may never exist under that name.
- Issues as the backlog, with labels for status and a project board: issue text is written by anyone and changes without review, the roadmap may not link it (DR-228), and it lives outside git, apart from the specs and records it rests on, where no test can check it and an agent reading a clone does not see it.
- Backlog items with the order kept in each item: the order would be spread over many files, and moving one item would change several.

## Consequences

- Tests fail when a line under Now, Next or Later differs from its item, when an open item is missing or listed twice, when a done or dropped item is listed, when an item under Now is not agreed, and when an item listed under Next or Later rests on nothing (R206, R213).
- Tests fail when an item is out of form (R211), names an ID that does not exist or a closed record, as R127 asks of every page outside the history, or is open and names tasks that are all ticked (R215), and when it is changed without a later date than the base commit gives it, or is removed or renamed (R216, T161).
- The items under Now are written for public readers from the owner's planning notes, which keep only what is private and point to the items for the rest, so that the items hold no private text (T167).
- Tests fail when the roadmap or the backlog's page does not say that an item describes and is neither a promise nor a date, and when the page does not say what each status means (R206, R217, T161).
- DR-218's last section named DR-219, DR-220 and DR-221 to be revisited: DR-219 and DR-221 are closed by DR-226 and DR-227, and DR-220 still holds as it stands, since which risks the roadmap lists does not change.
- No test reads the issues, so whether an issue that an item names is still open, and whether an item's text still says what holds, rest on review (T161).

## Scope

This covers where planned work is kept, the form of an item, and the roadmap as their index. The statuses and how an item becomes agreed are DR-226 (Each backlog item has one of five statuses, and only a merged pull request makes it planned). How the roadmap and the items may steer and link is DR-227 (The roadmap and the backlog describe, and lead only to this repository's own files), and how they name issues and pull requests is DR-228 (The roadmap and the backlog name issues and pull requests by number, with no link). Which risks the roadmap lists is DR-220 (The roadmap lists a short list of known limitations, and each feature page lists the rest of its own).

## What reversing it would change

How hard it is to reverse: reversible, with work. The items would move back into the roadmap's text or into another home, and the links that reviews give to items would need new homes. R206, R211, R213, R215 and R216 in `project-standards` would change, with their scenarios, and so would design decision 12, task 1.27, the README's briefing, `CLAUDE.md`'s rules on documentation and on what describes, the pull request template, the answers of T161 and T167, the glossary's roadmap and backlog item, and the feature page for `project-standards`. DR-226, DR-227, DR-228 and DR-229 would be assessed again.
