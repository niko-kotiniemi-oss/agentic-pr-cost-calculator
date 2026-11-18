# DR-224: The roadmap names issues and pull requests by number, with no link

- **Type:** security and privacy
- **Status:** closed
- **Decided by:** the owner, 2026-11-11
- **Requirements:** R209
- **Threats:** T160, T164
- **Replaces:** none
- **Closed by:** DR-228

## Context

Open issues hold the known later changes, and the bug form opens issues for known bugs, so the roadmap names issues. Anyone can open an issue here or comment on one, and GitHub serves that text, and a fork's pull request, under this repository's address, which is why the README links no issue and no pull request (DR-215). The README links the roadmap. A link invites a reader, or an agent that an adopter asks to read the roadmap, to follow it, and the agents of adopters load no `CLAUDE.md` of this repository, whose rule makes issue text data (T158). The design-stage review rated a linked issue a risk of 6 for adopters' agents.

## Decision

The roadmap names an issue or a pull request by its number, as in "issue 15", with its own summary of what the issue holds, and links none, as the owner chose on 2026-11-11.

## Alternatives

- Links to issues, with a line at the top of the roadmap that says that their text is written by anyone: an adopter's agent could still follow a link and act on a stranger's comment.
- No issues on the roadmap, which leaves the known later changes and known bugs that issues hold off it.

## Consequences

- A test fails on any address under this repository on GitHub, an issue's included (R209).
- A reader finds an issue by its number among the repository's issues, and an agent that looks one up reads text that anyone can write, which only agents that work here are told to treat as data (T164).
- The roadmap's summary of an issue is the repository's own text, which the owner reviews (A15).

## Scope

This covers how the roadmap names issues and pull requests. What else it may link is DR-221 (The roadmap describes, and leads only to this repository's own files).

## What reversing it would change

R209 in `project-standards` would change, with its scenarios, and so would design decision 12, task 1.26, the answer of T164 and the roadmap's items that name issues.
