# DR-218: A roadmap says what is now, next and later

- **Type:** process
- **Status:** closed
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-29
- **Requirements:** R206
- **Threats:** T161
- **Replaces:** none
- **Closed by:** DR-225

## Context

The tool is an open-source project that others are to help prioritise. What it will do is in the specs, what the first version leaves out is in the README and in records such as DR-003, DR-004, DR-006, DR-007, DR-160 and DR-189, what comes after the first build is in records and open issues, and what can go wrong is in the design's risks and the threat model. No page brings these together, so a reader cannot see in one place what is being built, what comes next, and what is left for later. On 2026-10-29 the owner asked for a roadmap of now, next and later.

## Decision

The repository keeps a roadmap, `docs/roadmap.md`, which the README's list of documentation links, with the sections Now, Next, Later, Known limitations and Known bugs, in that order. Each item is a few sentences. Each item under Next and Later names the requirements, records, threats or tasks that it rests on, a task by its change and number, and an item that names a closed record, or tasks that are all finished, is stale. Now holds the work under way: the pull requests before the build, in their order, and the build itself, by its tasks. Next holds what follows the first build, such as the command that writes each pull request's cost as a small file (DR-222) and a report that shows a pull request as still in progress (DR-223), and the open issues that hold later changes, each named by its number. Later holds what the first version leaves out. Known bugs is empty until there is code, and then names the issues that the bug form opens by their numbers. A pull request that finishes, adds or moves an item changes the roadmap in the same pull request, as `CLAUDE.md`'s rule on documentation and the pull request template say.

## Alternatives

- Issues labelled now, next or later, with no page: the order would be spread over issues, labels are the owner's to set, and an item that rests on records and requirements could not name them where a test reads them.
- A roadmap in the README, which would make the README longer and mix what the tool does with what it may do.
- No roadmap, which leaves contributors to piece the order together from records and issues.

## Consequences

- Tests hold the page's sections, the README's link, every requirement, record, threat and task that an item names, in active and archived changes alike, and fail on an item whose tasks are all ticked or whose record is closed (R206).
- No test reads the issues, which no test may reach, so whether an issue that an item names is still open, whether an item under Now is still under way, and whether the roadmap moved with the pull request that finished or moved an item, rest on review (T161).
- Items can later become issues labelled now, next or later, with the page linking them, once the owner sets those labels.

## Scope

This covers the roadmap's place, its sections and keeping it current. How Next and Later mark their items is DR-219 (Each item under Next and Later says whether it is planned), which of the design's risks it lists is DR-220 (The roadmap lists a short list of known limitations, and each feature page lists the rest of its own), and how it may steer, link and hide is DR-221 (The roadmap describes, and leads only to this repository's own files).

## What reversing it would change

R206 in `project-standards` would change, with its scenarios, and so would design decision 12, task 1.26, the README's list of documentation, `CLAUDE.md`'s rule on documentation, the pull request template, the answer of T161, the glossary's roadmap and the feature page for `project-standards`. DR-219, DR-220 and DR-221 would be revisited.
