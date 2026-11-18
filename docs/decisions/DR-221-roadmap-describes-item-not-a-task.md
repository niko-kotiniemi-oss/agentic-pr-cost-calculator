# DR-221: The roadmap describes, and leads only to this repository's own files

- **Type:** security and privacy
- **Status:** closed
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R209, R210
- **Threats:** T33, T159, T160, T163, T165
- **Replaces:** none
- **Closed by:** DR-227

## Context

Agents that work here read the pages that `CLAUDE.md` and the README link, and so do the agents that adopters ask to set the tool up, which load no `CLAUDE.md` of this repository (T158). The roadmap lists work that is wanted but not asked for, in sentences such as "a command that exports each pull request's cost", which an agent can read as a request to start it. `CLAUDE.md` already says that the glossary, the assumptions and any page that a file here links to describe and never tell an agent what to do (T33). The README links nothing under this repository's address but its releases and the files at their tags, since GitHub also serves under that address what others write, such as an issue, a pull request and a comparison with a fork's branch (DR-215). A relative link resolves against the address of the page that shows it, so one that climbs out of the repository reaches any page on GitHub (T160, T163). Text that GitHub hides, such as an HTML comment, reaches an agent that reads the raw file and no reader of the page (T165). A record about what agents may do lands in the same pull request as the change to `CLAUDE.md` that steers by it.

## Decision

`CLAUDE.md` names the roadmap among the pages that describe, and says that an item on it is not, by being there, a request to start it: work on one starts only when the person the agent works for asks for it, and an item under Next or Later is built only once the owner has agreed to it on an issue. The roadmap's links, autolinks, web addresses and `owner/repo` names, in prose and code, name only its own headings and tracked files of this repository by relative paths that stay inside it; it gives no fenced code, and names issues and pull requests by number alone, as DR-224 says (R209). The roadmap, and each feature page's section on known limitations and the roadmap, hold only printable ASCII and line breaks, and no text that GitHub hides (R210).

## Alternatives

- The README's own rule, which also allows addresses on a list and this repository's releases: the roadmap needs neither, and a shorter rule leaves less to check.
- No rule in `CLAUDE.md`, which leaves an agent that reads the roadmap to start an item.
- No check of hidden text, which leaves the roadmap, a page that agents are sent to and that pull requests edit, as the one page of its kind that such text can reach unseen (T165).

## Consequences

- A test fails when the roadmap, or a feature page's section on known limitations and the roadmap, gives a web address, an image, an at sign, an `owner/repo`, a fenced or indented code block or a relative path that leaves the repository or names no tracked file (R209; T160, T163), and when the roadmap or a feature page's section on it holds text that GitHub hides (R210, T165).
- An agent that reads the roadmap starts no item unless the person it works for asks, and a contributor reads that an item starts with an issue on which the owner agrees (T159). Whether an agent keeps to that rests on agents following the repository's rules (A16).
- `CLAUDE.md` changes in the same pull request, which the owner reviews as a change to what steers agents (A15).

## Scope

This covers how the roadmap may steer, what it may link and what it may hide. How it names issues and pull requests is DR-224 (The roadmap names issues and pull requests by number, with no link). The roadmap's place and sections are DR-218 (A roadmap says what is now, next and later), and what the README may link is DR-215 (The README gives no address outside this repository but those that its test lists).

## What reversing it would change

`CLAUDE.md`'s rule on what describes would change, and so would R209 and R210 in `project-standards`, design decision 14, task 1.26 and the answers of T33, T159, T160, T163 and T165.
