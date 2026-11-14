# DR-239: An agreed item gains a postponed point or a gap of the guide only on the owner's words

- **Type:** process
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R231
- **Threats:** T166
- **Replaces:** none
- **Closed by:** none

## Context

An agent adds a backlog item at `Planned`, moves one to `Planned`, or changes what an agreed item's What done looks like says, only when the owner has asked for that in words in the agent's own session (DR-227), and the pull request template asks a pull request that does any of these to say so (DR-226). The threat review at design of the guide found two other ways in which a merged pull request gives an agreed item work that the owner never agreed to, while the item's own text shows nothing: a gap of the guide that names the item as the one that closes it, and a postponed point that a review adds to it. The builder of an agreed item takes as agreed what its gaps and its postponed points give it. This change had done the first: the record on other agents (DR-234) gave the corrected requirements (B-007) a gap, a ledger format and a price table shaped for one provider, that B-007's What done looks like does not name. The final review of the guide's build found the same of the guide's first gaps, which arrive with the guide, so that no base holds it for the test to compare with: several give B-007 and B-021 work that their What done looks like does not name.

## Decision

An agent gives an agreed item, one that the default branch gives as `Planned` or `In progress`, a postponed point, or names it as the item that closes a gap of the guide, only when the owner has asked for that in words in the agent's own session, as for a change to the item's What done looks like, and never on text on GitHub. The pull request template asks a pull request that does either to say so, and where the owner asked. Compared with the base commit, a pull request that makes an entry of the guide name as a gap an item that the base gives as agreed changes that item's What done looks like, so that what the item takes on shows in its own text.

## Alternatives

- Gaps and postponed points left out of the rule, as before, so that a merged pull request could widen an agreed item with nothing in the item's own diff (T166).
- A test that a postponed point widens its item, which no test can tell: the rule and the template hold postponed points, and a test holds gaps too.
- A gap allowed to name only an item that is open to feedback and contributions, which would leave the gaps that adopters rely on with no agreed item (R226).

## Consequences

- `CLAUDE.md`'s rule on what an agent agrees to only on the owner's words, and the pull request template, name a postponed point and a gap of the guide given to an agreed item.
- A test fails on a gap given to an agreed item whose What done looks like is unchanged, compared with the base, and examines nothing while no base holds the guide (R231, task 1.30).
- The gap of a ledger format and a price table shaped for one provider names B-007, which the owner chose on 2026-11-14, and B-007's What done looks like takes it (DR-234). B-007's and B-021's What done looks like take the work that each of the guide's first gaps gives them, as the owner chose on 2026-11-14, among it the points of the owner's answers of 2026-11-12 that the guide calls before the build. The postponed points that the two items gain in this change are the rest of those answers.

## Scope

This covers what an agent may give an agreed item beside its status and its What done looks like. How an item becomes agreed is DR-226 (Each backlog item has one of five statuses, and only a merged pull request makes it planned), and what an agent may start is DR-227 (The roadmap and the backlog describe, and lead only to this repository's own files).

## What reversing it would change

How hard it is to reverse: reversible. The rule is text in `CLAUDE.md` and the pull request template, with one test, which one pull request can change. R231 in `project-standards` would change, with its scenarios, and so would `CLAUDE.md`'s rule on what describes, the pull request template, design decisions 12 and 14, task 1.30 and the answer of T166.
