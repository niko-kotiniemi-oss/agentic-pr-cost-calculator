# DR-238: The glossary, the assumptions and the pages that a file here links to describe, apart from the files that steer

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-28 and 2026-11-13
- **Requirements:** none
- **Threats:** T33, T93, T95
- **Replaces:** DR-166
- **Closed by:** none

## Context

DR-166 held that the glossary, the assumptions and the pages that a file in the repository links to describe and never instruct, and that where a meaning in the glossary, or an assumption, differs from `CLAUDE.md`, a requirement or a scenario, those hold and the glossary or the assumption is corrected. The owner asked for the assumptions and the glossary on 2026-10-28. On 2026-11-13 the owner asked for a guide that developers and agents follow (DR-231), which the README's list of documentation links, so that the guide is a page that a file in the repository links to, and DR-166 would have it describe. The threat review at design of the guide found that `CLAUDE.md` then said both that such a page describes and that the guide is not one of the pages that only describe, and that three texts, T33's answer, DR-231 and the design, read DR-166 as covering only the pages that the glossary and the assumptions link to. That narrower reading would leave the other pages that a file here links to, which any pull request can change, steering agents that act as the owner's account (T64).

## Decision

The glossary, the assumptions and the pages that a file in the repository links to describe, and never instruct, apart from the files that steer: `CLAUDE.md`, `.claude/`, the workflows, the Superpowers skills that `.claude/settings.json` enables and the guide, as DR-237 gives them. The pages that the guide links to describe too. Where a meaning in the glossary, or an assumption, differs from `CLAUDE.md`, a requirement or a scenario, those hold, and the glossary or the assumption is corrected.

## Alternatives

- DR-166 left as it was and read as covering only the pages that the glossary and the assumptions link to: the pages that the README or the guide link to, which any pull request can change, would then steer.
- DR-231 naming the guide as an exception to DR-166, which would leave one rule in two records that must be read together.
- Leaving the glossary and the assumptions as plain pages, with nothing saying which text holds where one of them and a rule differ, as DR-166 recorded.
- A test that a meaning does not narrow a rule, which no test can tell, as DR-166 recorded.

## Consequences

- DR-166 is closed. What it held is restated here, the files that steer apart, and its consequences hold:
  - `CLAUDE.md`'s section on what is data names the glossary, the assumptions and the pages that a file here links to, the files that steer apart, and says that where the glossary or an assumption differs from `CLAUDE.md` or a spec, those steer, and the agent tells the owner. It changes in the same pull request as this record.
  - An assumption's entry says what would change if it is wrong, never how to change it, and a documented fact links only a vendor's page on a host that the test lists or a file at a full commit of a repository that it lists, while a page of the assumptions gives no other web address (DR-162).
  - A meaning that narrows a rule without contradicting its words rests on the owner's review of the glossary's diff.
- What DR-166's last section named: `CLAUDE.md`'s section on what is data changes as above; design decision 14 cites this record; the answers of T33, T93 and T95 cite this record, and T33's answer says again "the pages that a file here links to", as it did before the guide. DR-162 and DR-164, which name DR-166 in their scope, still hold, and each keeps its text. DR-231 no longer says that DR-166 stays as it is.

## Scope

This covers what the glossary, the assumptions and the pages that a file here links to are to an agent that reads them. What steers an agent is DR-237 (Data and issue text never instruct, and the guide steers below `CLAUDE.md` and the skills' steps), what each assumption says is DR-162 (The design's assumptions are written down, each with what rests on it and how it is checked), and the glossary's words and their test are DR-164 (A glossary sets the words that the specs and pages use, and a test holds them).

## What reversing it would change

How hard it is to reverse: reversible. The rule is text in `CLAUDE.md`, which one pull request can change. `CLAUDE.md`'s section on what is data would change, and so would design decision 14 and the answers of T33, T93 and T95. None of these is part of the public surface, so the change would not be a breaking one for adopters.
