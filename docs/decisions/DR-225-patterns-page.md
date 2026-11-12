# DR-225: A page says which recognised patterns the design follows and which anti-patterns it meets

- **Type:** process
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-29
- **Requirements:** R211, R212, R213
- **Threats:** T33, T159, T160, T163, T165, T166
- **Replaces:** none
- **Closed by:** none

## Context

The owner asked on 2026-10-29 whether the design follows recognised patterns or falls into recognised anti-patterns, written down so that agents get it as context, and asked that each anti-pattern be fixed before the build. On 2026-11-12 three reviewers, each in a context of its own, assessed the design: one its architecture, one its CI and security, one its testing. They found patterns that records chose, anti-patterns that records accept with their reasons, and anti-patterns that no record accepts, among them a long design before any code runs, behaviour stated again in several documents, acceptance tests written before the entry points that they call are defined, and two security rules that the design does not state. The plan of the pull requests that prepare the build moved four named practices to this page from the one on conventions: Clean Code, PEP 8, OWASP's secure coding practices and OpenSSF's Scorecard. Agents read the pages that `CLAUDE.md` and the README link (T33), and a list of what to fix reads as a list of tasks (T159).

## Decision

The repository keeps a patterns page, `docs/patterns.md`, linked from the README's list of documentation, with the sections Patterns followed, Anti-patterns and Named practices. Each item gives the pattern or anti-pattern by its recognised name, its source by author or body and work, where it applies, and the requirements, records, threats or tasks that it rests on (R211). Each item under Anti-patterns opens with **Avoided.**, **Knowingly accepted.** or **To fix before the build.**: one knowingly accepted names the record that gives the reason, and one to fix gives in bold the opening words of the item under the roadmap's Now that fixes it (R212). Named practices says where each of the four applies and where the design falls short of it. The page holds to the roadmap's rules on links and hidden text, and names each source with no web address (R213). `CLAUDE.md` names it among the pages that describe: an item on it is not a task.

## Alternatives

- The assessment kept only in the pull request's comments, which no agent reads as context once the pull request merges.
- The patterns written into the design, which an agent reads as part of the change that it builds, so that an anti-pattern to fix reads as part of the work.
- Each source linked by its address, which leads a reader or an agent to pages that others write and change (T160).

## Consequences

- Tests fail as R211, R212 and R213 say.
- An anti-pattern to fix stays on the page, with the roadmap's item that fixes it, until the pull request that fixes it changes it to **Avoided.**, and a test fails when that item leaves Now first.
- Whether a verdict is right, and whether a source says what an item says it does, rest on review (T166).
- `CLAUDE.md` changes in the same pull request, which the owner reviews as a change to what steers agents.

## Scope

This covers the patterns page: its sections, what each item gives and what it may link. Which document states what the tool does is DR-226 (The specs are the single source of what the tool does), and how the roadmap may steer and link is DR-221 (The roadmap describes, and leads only to this repository's own files).

## What reversing it would change

R211 to R213 in `project-standards` would change, with their scenarios, and so would design decisions 12 and 14, task 1.27, `CLAUDE.md`'s list of the pages that describe, the README's list of documentation, the project standards' feature page and the answers of T33, T159, T160, T163, T165 and T166.
