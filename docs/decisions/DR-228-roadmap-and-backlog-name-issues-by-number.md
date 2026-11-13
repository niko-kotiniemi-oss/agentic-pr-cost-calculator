# DR-228: The roadmap and the backlog name issues and pull requests by number, with no link

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the owner, 2026-11-11 and 2026-11-13
- **Requirements:** R209
- **Threats:** T160, T164
- **Replaces:** DR-224
- **Closed by:** none

## Context

DR-224 had the roadmap name an issue or a pull request by its number, with its own summary of what the issue holds, and link none, as the owner chose on 2026-11-11. Anyone can open an issue here or comment on one, and GitHub serves that text, and a fork's pull request, under this repository's address, which is why the README links no issue and no pull request (DR-215). Backlog items now name the issue that an item came from and the pull requests that deliver it (DR-225), and the assessment that the owner agreed to on 2026-11-13 had them name issues by number, as the roadmap does, while the roadmap links the items, which are this repository's own files.

## Decision

The roadmap and every file in `docs/backlog/` name an issue or a pull request by its number, as in "issue 15" or in an item's fields Issue and Pull requests, with their own summary of what it holds, and link none.

## Alternatives

- Links to issues and pull requests from the items, with a line that says their text is written by anyone: an adopter's agent could still follow a link and act on a stranger's comment.
- No issue numbers in the items: where a proposal came from, and which pull requests delivered an item, could not be found from the item.

## Consequences

- A test fails on any address under this repository on GitHub, in the roadmap and in the items (R209).
- A reader finds an issue or a pull request by its number among the repository's, and an agent that looks one up reads text that anyone can write, which only agents that work here are told to treat as data (T164).
- The roadmap's and the items' summaries are the repository's own text, which the owner reviews (A15).

## Scope

This covers how the roadmap and the backlog items name issues and pull requests. What else they may link is DR-227 (The roadmap and the backlog describe, and lead only to this repository's own files).

## What reversing it would change

How hard it is to reverse: reversible. Links could be added to the pages in one pull request, after a threat review of what they lead adopters' agents to. R209 in `project-standards` would change, with its scenarios, and so would design decision 12, task 1.27, the answer of T164 and every item that names an issue or a pull request.
