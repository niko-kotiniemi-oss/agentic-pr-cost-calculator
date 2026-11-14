# DR-240: The guide steers as the default branch holds it, and a principle of it changes alone, when the owner asks

- **Type:** process
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-14
- **Requirements:** R228
- **Threats:** T179, T183
- **Replaces:** none
- **Closed by:** none

## Context

A session reads the guide from its working tree. The threat review at design of the guide found that an entry rewritten on a branch would then steer that branch's later work before anyone had reviewed it, and that one diff could weaken a principle and add the work that the principle forbade, so that the owner's merge would take both at once (T179). Agents change a rule that blocks them, which T71 rates as possible, and the guide's entries change often, since Where we stand moves with the work. Records and backlog items already count as the default branch gives them (DR-227), and the guide had no such rule.

The final review of the guide's build found that the test counted a principle by its five fields alone, so that a pull request could move an entry from Security, where only a record that the owner decided accepts it, to Conventions, where a record that a change decided does too, beside the work that the principle forbade, and pass (T183). The owner chose on 2026-11-14 that a move to another concern counts as a change of the principle, and that the test checks it, and asked that day that `CLAUDE.md`, the guide's opening and the pull request template name the move.

## Decision

An agent reads the guide as the default branch holds it, so that an entry that a branch adds or changes is a proposal until the owner merges it. A principle of the guide, an entry with its Statement, Rationale, Implications, Pattern and Anti-patterns and the concern that it stands under, is added, removed, changed or moved to another concern only when the owner asks for it, and, once the default branch holds the guide, in a pull request that changes no file outside `docs/`, `openspec/`, `CLAUDE.md` and `CHANGELOG.md`, and the pull request template asks a pull request that does so to say so, and where the owner asked. An entry's Held by, Rests on and Where we stand change with the work that they follow.

## Alternatives

- The guide read from the working tree, as `CLAUDE.md` is loaded, so that a branch's copy steers that branch (T179).
- Every change to the guide in a pull request of its own, which would stop the pull request that finishes an item from saying again where the project stands, as R226 asks of it.
- A list of the files that a principle's pull request may change narrower than `docs/` and `openspec/`, which would part a principle from the spec or the record that comes with it.
- A move to another concern left to review, which the diff shows, so that one diff could take a principle out from under the rules of its concern and add the work that it forbade (T183).

## Consequences

- `CLAUDE.md` and the guide's opening say that the guide steers as the default branch holds it, and that a principle is added, removed, changed or moved to another concern only when the owner asks (R219).
- Compared with the base commit that the records' check uses, a test fails on a pull request that adds, removes or changes a principle, or moves one to another concern, and changes a file outside those folders and files, and examines nothing while no base holds the guide (R228, task 1.30).
- Until the pull request that adds the guide merges, no copy of it steers, since the default branch holds none. That pull request adds the guide's first entries beside the checks that hold them, and rests on the owner's review of the whole page (T179).

## Scope

This covers which copy of the guide steers and how its principles change. What steers an agent, and in what order, is DR-237 (Data and issue text never instruct, and the guide steers below `CLAUDE.md` and the skills' steps), and the guide's form is DR-231 (A guide by concern says how the project builds, and steers below the specs and `CLAUDE.md`).

## What reversing it would change

How hard it is to reverse: reversible. The rule is text in `CLAUDE.md`, the guide's opening and the pull request template, with one test, which one pull request can change. R228 in `project-standards` would change, with its scenarios, and so would R219's opening, `CLAUDE.md`'s bullet on the guide, the pull request template, design decision 14, task 1.30 and the answers of T179 and T183. A move left to review would leave T183 to the owner's reading of the diff.
