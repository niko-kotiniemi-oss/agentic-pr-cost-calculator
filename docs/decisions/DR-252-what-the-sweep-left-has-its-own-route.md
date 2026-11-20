# DR-252: Each kind of sentence that the sweep of B-022 left reaches the specs' rule by its own route

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-11-17 and 2026-11-18
- **Requirements:** none
- **Threats:** T173
- **Replaces:** none
- **Closed by:** none

## Context

DR-232 makes the specs the single source of what the tool does, and leaves to the pull request that delivers B-022 the bringing of the documents that state behaviour to that rule, with other pull requests leaving those statements as they are until it merges (T173). `CLAUDE.md` said that a page is brought to the rule only through B-022, which leaves no route once B-022 is done. The sweep leaves two kinds of sentence as they are: a clause that no scenario holds, or that a scenario contradicts, which its mapping lists for B-007 so that whether it becomes an obligation is decided there, and a sentence in a document that design decision 19 leaves as it is, such as the glossary, the assumptions or the change's proposal. The review of that pull request found the route closed once B-022 is done, and the review of its fixes found that the sentence that replaced it left the second kind with no fence, so that an agent touching such a document in a pull request about something else could replace a sentence that no scenario holds with a citation that does not state it, and that B-007's own text named neither the mapping nor its list. The owner chose on 2026-11-17 to reword the sentence in that pull request, and on 2026-11-18 to fence the second kind and to give B-007 a postponed point that names the list.

## Decision

`CLAUDE.md` says that B-022 brought the pages that it swept to the rule, that a clause that its mapping lists for B-007 is brought to the rule only through B-007, and that a sentence that states what the tool does in a document that the sweep left as it is is brought to it only by a change of its own that the owner asks for. B-007 has a postponed point that names the list as the pull request that delivers B-022 merges it, so that what it takes on shows in its own text, and a later change to the mapping does not widen it (DR-239).

## Alternatives

- `CLAUDE.md` naming B-022 alone: no route once B-022 is done, and the listed clauses stay on their pages with nothing to bring them to the rule.
- B-007 named alone: an agent could rewrite a sentence of a document that the sweep left as it is in passing, which is what T173 describes.
- Both gaps tracked as issues: `CLAUDE.md` steers as before until a later pull request.

## Consequences

- T173's answer says the same, and design decision 19 names both routes.
- Whether each listed clause becomes an obligation is decided in B-007, which corrects the requirements before the build.
- A document that the sweep left as it is keeps its sentences until a change that the owner asks for brings them to the rule, with its own evidence, as T202's answer has a later sweep do.

## Scope

This covers the route by which what the sweep of B-022 left reaches the rule that DR-232 sets. That the specs are the single source is DR-232, which checks of the documentation stay is DR-251, and how an agreed item gains a postponed point is DR-239.

## What reversing it would change

How hard it is to reverse: reversible. A later record could let agents bring such a document to the rule in passing, with `CLAUDE.md`'s sentence and T173's answer changed to match, and B-007's postponed point removed once its clauses are settled otherwise.
