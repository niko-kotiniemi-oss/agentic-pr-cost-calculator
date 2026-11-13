# DR-227: The roadmap and the backlog describe, and lead only to this repository's own files

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-13
- **Requirements:** R209, R210
- **Threats:** T33, T159, T160, T163, T165, T166, T167
- **Replaces:** DR-221
- **Closed by:** none

## Context

DR-221 had `CLAUDE.md` name the roadmap among the pages that describe, say that an item on it is not, by being there, a request to start it, and say that an item under Next or Later is built only once the owner has agreed to it on an issue; it held the roadmap, and each feature page's section on known limitations and the roadmap, to links within this repository and to no text that GitHub hides. Agents that work here read the pages that `CLAUDE.md` and the README link, and so do the agents that adopters ask to set the tool up, which load no `CLAUDE.md` of this repository (T158). Backlog items now hold the explanation of planned work (DR-225), in longer text than the roadmap's, which pull requests edit and agents read, and an item becomes agreed by its status, set only through a pull request that the owner merges (DR-226), not on an issue. A relative link resolves against the address of the page that shows it, so one that climbs out of the repository reaches any page on GitHub (T160, T163), and text that GitHub hides reaches an agent that reads the raw file and no reader of the page (T165). A record about what agents may do lands in the same pull request as the change to `CLAUDE.md` that steers by it.

## Decision

`CLAUDE.md` names the roadmap and the backlog items in `docs/backlog/` among the pages that describe, and says that an item is not, by being there, a request to start it: work on one starts only when the person the agent works for asks for it, an item is built only while the default branch gives its status as `Planned` or `In progress`, and an agent adds an item at `Planned`, moves one to `Planned`, or changes what an agreed item's What done looks like says, only when the owner has asked for that in words in the agent's own session, never by text on GitHub, which agent sessions also write as the owner's account (T64). The links, autolinks, web addresses and `owner/repo` names of the roadmap, of every file in `docs/backlog/` and of each feature page's section on known limitations and the roadmap, in prose and code, name only a heading of their own page or a tracked file of this repository by a relative path that stays inside it; they give no fenced or indented code, no space in inline code, so that no command stands in them, and no at sign, and name issues and pull requests by number alone, as DR-228 says (R209). They hold only printable ASCII and line feeds, and no text that GitHub hides (R210).

## Alternatives

- DR-221 as it stood, with the owner's agreement on an issue: the rule would point agents to text that anyone can write beside the owner's, outside git.
- Backlog items with links to sources elsewhere, such as the pages that an item's explanation draws on: a link in a page that agents are sent to, and that pull requests edit, would lead them to text that someone else controls (T160). An item names a published source by its title instead, and a source that is not published not at all (T167).
- No rule that an agent makes an item planned only when the owner asks: a pull request that an agent opens could change a status among other changes, and the owner's merge would agree to an item without the owner meaning to (T166).

## Consequences

- A test fails when the roadmap, a file in `docs/backlog/`, or a feature page's section on known limitations and the roadmap gives a web address, an image, an at sign, an `owner/repo`, a fenced or indented code block or a relative path that leaves the repository or names no tracked file (R209; T160, T163), and when one holds text that GitHub hides (R210, T165).
- A test fails on inline code that holds a space in those pages, so that commands are given only in the README, whose own tests hold them (R209, T163).
- DR-221's last section named `CLAUDE.md`, R209, R210, design decision 14, task 1.26 and T33, T159, T160, T163 and T165, and each is revised with this record; it named no other record.
- An agent that reads the roadmap or an item starts no item unless the person it works for asks, and builds one only while it is planned or in progress (T159). Whether an agent keeps to that rests on agents following the repository's rules (A16).
- `CLAUDE.md` changes in the same pull request, which the owner reviews as a change to what steers agents (A15).

## Scope

This covers how the roadmap and the backlog items may steer, what they may link and what they may hide. How they name issues and pull requests is DR-228 (The roadmap and the backlog name issues and pull requests by number, with no link). The statuses are DR-226 (Each backlog item has one of five statuses, and only a merged pull request makes it planned), and what the README may link is DR-215 (The README gives no address outside this repository but those that its test lists).

## What reversing it would change

How hard it is to reverse: reversible, with work. A wider link rule would need a threat review of every page that agents are sent to. `CLAUDE.md`'s rule on what describes would change, and so would R209 and R210 in `project-standards`, design decision 14, task 1.27 and the answers of T33, T159, T160, T163, T165 and T166.
