# DR-286: The README says what the tool is for and which uses to avoid

- **Type:** scope
- **Boundary:** outgoing
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-10-27 and 2026-11-23
- **Requirements:** R279
- **Threats:** T284
- **Replaces:** none
- **Closed by:** none

## Context

On 2026-10-27 the owner asked that the README say what the tool is for and which uses to avoid. On 2026-11-23 the owner agreed the list of uses to avoid, and said that more may be added later by an ordinary pull request. Each use rests on a decision that already holds: the figure is an estimate at list prices (DR-002), the tool is opt-in and not built to catch anyone who avoids it (DR-189), what is pushed stays published (R146, DR-182), a call counts in the repository that it is made from (R3), and a ledger file edited by hand is an accepted risk (DR-066), so the figure cannot serve as a control.

## Decision

The README holds, after its section on what the tool will do and before its list of documents, a section that says what the tool is for, estimating what a pull request cost in model tokens and CI minutes, and lists the uses to avoid, each citing the requirement that states the behaviour behind it, or for a choice the record that makes it: as a bill or an invoice (R94, DR-002); to watch, rank or judge people (DR-189); in a public repository, by anyone who does not want their usage published (R146); in a session that also works on private repositories (R3); and as a security or compliance control (DR-066, DR-189). A short start links the section before its first step (R279).

## Alternatives

None were recorded when this was decided.

## Consequences

- A test fails on a README without the section, with the section out of its place, with a use that cites no requirement or accepted record, or only this record, R279 or the README, and on a short start that links the section only after a step or not at all (R279; T284).
- Whether a cited record or requirement gives the use's reason is left to review (T284).
- A use to avoid is added or removed by an ordinary pull request that the owner merges.

## Scope

This covers what the README says about the tool's purpose. How the README opens, with a short start, is DR-212 (The README opens with a short start).

## What reversing it would change

How hard it is to reverse: reversible. R279 and its scenarios, the README's section and T285's answer would change. Nothing that adopters configure or depend on changes, so the change would not be a breaking one for adopters.
