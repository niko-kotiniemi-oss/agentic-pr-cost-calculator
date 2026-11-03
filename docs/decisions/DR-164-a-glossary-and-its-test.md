# DR-164: A glossary sets the words that the specs and pages use, and a test holds them

- **Type:** process
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-28
- **Requirements:** R137, R138
- **Threats:** T90, T94
- **Replaces:** none
- **Closed by:** none

## Context

The owner asked on 2026-10-28 for a light glossary, so that the documents say one thing one way and agents read fewer words. A review found one word used for two things, such as "report" for the component and for the comment it posts, and two words for one thing, such as "capture hook" and "capture step". The threat reviews at design found that a word to avoid can also be a name that adopters type, such as the configuration key `enabled`; that rules tell apart concepts whose words a hunt for synonyms would merge, such as the directories a hook sees and the reasons the comment gives for what it did not count; that a rewording reaches `CLAUDE.md` and the threat model's answers, not only the requirements; and that accepted records quote titles that a rewording could change.

## Decision

`docs/glossary.md` gives each term's meaning and the words to avoid for it, and a test fails when a Markdown file that the repository tracks uses a word to avoid in its prose, outside inline code and code blocks, except where the words are kept as written: the records, the archived changes, the changelog's released entries, the vendored and generated files, and the titles that an accepted record quotes (R137, R138). A word is listed to avoid only if it is wrong wherever it appears in prose; a word with several right senses is defined instead, and each concept that a rule tells apart from another has a term of its own.

## Alternatives

- A glossary with no test, which would fall behind the documents as they change.
- A controlled vocabulary for every word, heavier than the owner asked for.
- Rewording the records too, which an accepted record does not allow (DR-121).
- Matching words inside code as well, which would push a name that adopters type to change with the prose around it.
- Leaving `CLAUDE.md` out of the test, which would keep in the file that steers agents the words that the other pages avoid.

## Consequences

- The specs, the change's proposal, design and tasks, and the other pages, `CLAUDE.md` among them, are reworded to the glossary in task 1.20. A title that changes, changes with the register and with the citations that quote it, and a title that an accepted record quotes keeps its words.
- A script, run once in each pull request that rewords, shows that each changed line differs only by words to avoid replaced with their terms, and lists every other change, those to `CLAUDE.md` first, for the owner and the review in a separate context, which reads before and after the requirements, `CLAUDE.md`, the threat model's answers and residuals, the README's statements of what opting in records and publishes, and the pages that adopters act on.
- The records keep their words, so the words to avoid also tell a reader what an older record means.
- A word added to the list to avoid comes with the rewording of its every use in prose, in the same pull request.
- A word with several senses is held by the reviews, not by the test.
- The changelog's released entries are the sections under a version's heading.
- The threat model's test resolves a cited scenario only in `openspec/specs/` and the active changes, so that a title that a rewording changed cannot pass on an archived copy.

## Scope

This covers the words that the documents use. What the glossary is to an agent that reads it is DR-166 (The glossary, the assumptions and the pages they link to describe, and never steer), what a record holds is DR-108 (Each decision has a record of its own, in an index), and how a record changes is DR-121 (A record is never edited once accepted, only closed by a record that replaces it).

## What reversing it would change

R137 and R138 in `project-standards` would change, with their scenarios, and so would the design's decision 14, task 1.20, `docs/glossary.md` and its test, the threat model's test of cited scenarios, and the feature page for `project-standards`. The documents would keep the words that task 1.20 gave them. The glossary is not part of the public surface, so the change would not be a breaking one for adopters.
