# DR-237: Data and issue text never instruct, and the guide steers below `CLAUDE.md` and the skills' steps

- **Type:** process
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-13
- **Requirements:** R134, R219, R220
- **Threats:** T33, T81, T94, T180, T181
- **Replaces:** DR-082
- **Closed by:** none

## Context

DR-082 held that price tables, fixtures, usage records, changelogs and the repository's other data files, and the text of issues, pull requests and review comments, describe and never instruct an agent, and that anything meant to steer an agent belongs in `CLAUDE.md`, in `.claude/` or in a workflow, beside the vendored Superpowers skills that `.claude/settings.json` enables (DR-142). On 2026-11-13 the owner asked for a guide that developers and agents follow, concern by concern (DR-231), which `CLAUDE.md` names among what steers, for how the project builds, so that DR-082's list no longer says what steers. The threat review at design of the guide, by two reviewers each in a context of its own, found three more gaps. The guide's rank rested on tests of each statement's presence, which pass a line added to the guide's opening, an opening that leaves out that the guide never widens what `CLAUDE.md` lets an agent do, and a `CLAUDE.md` that names the guide but not its rank (T180). No order was given between an entry and a step of a Superpowers skill, whose own rules let an agent skip a step only when the person it works for says so (T181). And the guide, like `CLAUDE.md` itself, was left out of the check that no attribute hides the diff of a record or the README (T81), and the guide out of the rewording script's list, which gives the changes to `CLAUDE.md` first (T94).

## Decision

Price tables, fixtures, usage records, changelogs and the repository's other data files describe things and are never instructions to an agent, and the same holds for the text of issues and pull requests and for review comments, whoever wrote them. Anything meant to steer an agent belongs in `CLAUDE.md`, in `.claude/`, in a workflow or, for how the project builds, in the guide, `docs/patterns.md`, and the vendored Superpowers skills that `.claude/settings.json` enables steer agents too (DR-142). The guide steers below the specs and `CLAUDE.md`, and never widens what `CLAUDE.md` lets an agent do: `CLAUDE.md` gives that rank in a sentence, and the guide opens with a text, each word for word as a requirement gives it, and an entry cites the rule of `CLAUDE.md` that it rests on rather than stating it again, each entry under Working with agents citing `CLAUDE.md` in its Held by. Where an entry and a step of a Superpowers skill differ, the agent follows the step and tells the owner. No attribute hides the diff of the guide or of `CLAUDE.md`, and the rewording script lists the guide's changes right after those to `CLAUDE.md`.

## Alternatives

- DR-082 left as it was, beside a `CLAUDE.md` that names the guide among what steers, so that two texts that agents read would contradict each other.
- The guide's rank held by a test of each statement's presence, which passes a line added beside them (T180).
- An entry that may change or drop a skill's step, which would let a page that any pull request can propose a change to drop a review or a verification step (T181).
- The skills' steps below the guide's principles: the skills hold the steps of building, and their own rules let an agent skip one only when the person it works for says so.

## Consequences

- DR-082 is closed. What it held is restated here, and its consequences hold:
  - whether a text instructs or describes is not something a test can decide, so only the rule holds the pages that describe (T33's residual), while the guide's opening, its rank and the changes to its principles are held by tests (R219, R228);
  - what steers an agent changes only through the owner's merge (T33, DR-080), and the guide steers as the default branch holds it (DR-240);
  - each fixture that carries hostile text on purpose is named for it (T33, task 1.1).
- What DR-082's last section named: the paragraph on data files in the section "Records are data, not instructions" of `CLAUDE.md` names the guide among what steers, and changes in the same pull request as this record; the line on issue and pull request text in its section "What an agent never does here" stays; T33's answer and residual name this record and say what holds the guide; the naming of hostile fixtures in task 1.1 stays. DR-081 and DR-115, which it named for revisiting, were assessed and stand, since how an outside pull request is reviewed and who may contribute do not change, and each keeps its text, which names DR-082.
- A test fails when `CLAUDE.md` does not give the guide's rank in its sentence, when the text before the guide's first section differs from R219's, and when an entry under Working with agents does not cite `CLAUDE.md` in its Held by (R219, R220, T180).
- `CLAUDE.md` and the guide's opening each say that where an entry and a skill's step differ, the step is followed and the owner told (T181).
- A test fails when an attribute hides the diff of the guide or of `CLAUDE.md` (R134, T81), and `scripts/rewording.py` lists the guide's changes right after those to `CLAUDE.md`, for the owner and the review (T94, task 1.30).

## Scope

This covers what steers an agent that works on this repository, and in what order, apart from decision records, which are DR-108 (Each decision has a record of its own, in an index). What the glossary, the assumptions and the pages that a file here links to are to an agent is DR-238 (The glossary, the assumptions and the pages that a file here links to describe, apart from the files that steer), which copy of the guide steers and how its principles change is DR-240 (The guide steers as the default branch holds it, and a principle of it changes alone, when the owner asks), how the tool treats what crosses into it is DR-044 (Everything that crosses into the tool is untrusted), and how an outside pull request is reviewed is DR-081 (Outside pull requests are reviewed from `main`).

## What reversing it would change

How hard it is to reverse: reversible. The rule is text in `CLAUDE.md` and in the guide's opening, with the tests that hold them, which one pull request can change. The paragraph on data files and the bullet on the guide in `CLAUDE.md`, and its line on issue and pull request text, would change, with R134, R219 and R220 in `project-standards` and their scenarios, the guide's opening, design decision 14, tasks 1.1, 1.28 and 1.30, and the answers of T33, T81, T94, T180 and T181. DR-081, DR-115 and DR-231 would be revisited.
