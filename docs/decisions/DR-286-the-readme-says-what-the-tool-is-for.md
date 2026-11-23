# DR-286: The README says what the tool is for and which uses to avoid

- **Type:** scope
- **Boundary:** outgoing
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-10-27 and 2026-11-23
- **Requirements:** R279
- **Threats:** T285
- **Replaces:** none
- **Closed by:** none

## Context

On 2026-10-27 the owner asked that the README say what the tool is for and which uses to avoid. On 2026-11-23 the owner agreed the list of uses to avoid, and said that more may be added later by an ordinary pull request. Each use rests on a decision that already holds: the figure is an estimate at list prices (DR-002), the tool is opt-in and not built to catch anyone who avoids it (DR-189), what is pushed stays published (DR-182), and a call counts in the repository that it is made from (R3).

## Decision

The README holds, after its section on what the tool will do and before its list of documents, a section that says what the tool is for, estimating what a pull request cost in model tokens and CI minutes, and lists the uses to avoid, each with a link to the record or requirement that gives its reason: as a bill or an invoice; to watch, rank or judge people; in a public repository, by anyone who does not want their usage published; in a session that also works on private repositories; and as a security or compliance control (R279).

## Alternatives

- Leaving the uses to avoid to the pages on each feature: an adopter reads the README before adopting the tool, and may never reach those pages.

## Consequences

- A test fails on a README without the section, with the section out of its place, or with a use that links no accepted record or requirement (R279; T285).
- A use to avoid is added or removed by an ordinary pull request that the owner merges.

## Scope

This covers what the README says about the tool's purpose. How the README opens, with a short start, is DR-212 (The README opens with a short start).

## What reversing it would change

How hard it is to reverse: reversible. R279 and its scenarios, the README's section and T285's answer would change. Nothing that adopters configure or depend on changes, so the change would not be a breaking one for adopters.
