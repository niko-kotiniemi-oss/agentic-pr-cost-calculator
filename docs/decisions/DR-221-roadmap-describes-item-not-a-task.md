# DR-221: The roadmap describes, and an item on it is not a task

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R209
- **Threats:** T33, T159, T160
- **Replaces:** none
- **Closed by:** none

## Context

Agents that work here read the pages that `CLAUDE.md` and the README link. The roadmap lists work that is wanted but not asked for, in sentences such as "a command that exports each pull request's cost", which an agent can read as a task to start. `CLAUDE.md` already says that the glossary, the assumptions and any page that a file here links to describe and never tell an agent what to do (T33). The roadmap also links issues, whose text anyone can write, and a link to another site would lead an agent that follows it to text that its author controls (T95). The README links nothing under this repository's address but its releases and the files at their tags, since GitHub also serves under that address what others write (DR-215). A record about what agents may do lands in the same pull request as the change to `CLAUDE.md` that steers by it.

## Decision

`CLAUDE.md` names the roadmap among the pages that describe, and says that an item on it is not a task: work on an item starts only from the owner. The roadmap links only files of this repository, its own headings, and the issues and pull requests of this repository on GitHub (R209), and issue text stays data, as `CLAUDE.md` already says.

## Alternatives

- Naming issues by their number without a link, which the README's rule would allow, but which leaves a reader to search for each one, while an agent can still look the issue up by its number.
- No issues on the roadmap, which leaves the known later changes that issues hold off it.
- No rule in `CLAUDE.md`, which leaves an agent that reads the roadmap to start an item.

## Consequences

- A test fails when the roadmap links anything but a file of this repository, one of its headings, or an issue or a pull request of this repository (R209, T160).
- An agent that follows an issue's link reads text that anyone can write, which it treats as data (T33, T160).
- An agent that reads the roadmap starts no item unless the owner asks for it (T159). Whether it keeps to that rests on agents following the repository's rules (A16).
- `CLAUDE.md` changes in the same pull request, which the owner reviews as a change to what steers agents (A15).

## Scope

This covers how the roadmap may steer and what it may link. The roadmap's place and sections are DR-218 (A roadmap says what is now, next and later), and what the README may link is DR-215 (The README gives no address outside this repository but those that its test lists).

## What reversing it would change

`CLAUDE.md`'s rule on what describes would change, and so would R209 in `project-standards`, design decision 14, task 1.26 and the answers of T33, T159 and T160.
