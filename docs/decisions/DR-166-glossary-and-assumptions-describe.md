# DR-166: The glossary, the assumptions and the pages they link to describe, and never steer

- **Type:** security and privacy
- **Status:** closed
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-28
- **Requirements:** none
- **Threats:** T33, T93, T95
- **Replaces:** none
- **Closed by:** DR-238

## Context

The owner asked on 2026-10-28 for a list of the design's assumptions and a light glossary, partly so that agents read fewer words. Both are pages that anyone can change through a pull request, and agents are meant to read them and rely on them. The threat reviews at design found that a meaning in the glossary can narrow a word that a rule in `CLAUDE.md` or a requirement rests on, with no change to either, and that a page that an assumption links to is fetched into the context of each agent that checks the fact. `CLAUDE.md` named data files, decision records, issues and pull request text as text that describes, and none of these.

## Decision

The glossary, the assumptions and the pages that a file in the repository links to describe, and never instruct. Where a meaning in the glossary, or an assumption, differs from `CLAUDE.md`, a requirement or a scenario, those hold, and the glossary or the assumption is corrected.

## Alternatives

- Leaving the glossary and the assumptions as plain pages, with nothing saying which text holds where one of them and a rule differ.
- A test that a meaning does not narrow a rule, which no test can tell.

## Consequences

- `CLAUDE.md`'s section on what is data names the glossary, the assumptions and the pages that a file here links to, and says that where the glossary or an assumption differs from `CLAUDE.md` or a spec, those steer, and the agent tells the owner. This record lands in the same pull request as that change.
- An assumption's entry says what would change if it is wrong, never how to change it, and a documented fact links only a vendor's page on a host that the test lists or a file at a full commit of a repository that it lists, while a page of the assumptions gives no other web address (DR-162).
- A meaning that narrows a rule without contradicting its words rests on the owner's review of the glossary's diff.

## Scope

This covers what the glossary, the assumptions and the pages they link to are to an agent that reads them. What each assumption says is DR-162 (The design's assumptions are written down, each with what rests on it and how it is checked), and the glossary's words and their test are DR-164 (A glossary sets the words that the specs and pages use, and a test holds them).

## What reversing it would change

`CLAUDE.md`'s section on what is data would change, and so would the design's decision 14 and the threat model's answers to T33, T93 and T95. None of these is part of the public surface, so the change would not be a breaking one for adopters.
