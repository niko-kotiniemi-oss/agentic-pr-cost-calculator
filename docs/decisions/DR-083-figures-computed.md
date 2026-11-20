# DR-083: Every figure is computed in the same session

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** none
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

The repository's prose states many figures about the repository itself. The threat model opens with how many threats and trust boundaries it holds, and commit messages and pull request text give counts of requirements, scenarios and citations. The prose also states facts about the repository's own code. A figure like these can be written from memory, carried over from an earlier message or read off a diff, rather than taken from what it counts.

## Decision

Numbers, counts, ratios, prices and comparisons are written in prose, commit messages and pull request descriptions only when a computation in the same session produced them, with its output pasted, and never from memory, from an earlier message or from a diff. Where a figure cannot be computed, what was observed is written instead. A statement about the repository's own code, such as how many callers a function has, is settled the same way, by running the query that answers it.

## Alternatives

None were recorded when this was decided.

## Consequences

- Each figure costs a command or a query in the session that writes it.
- No check in the repository holds the rule, so it rests on whoever writes the text.

## Scope

This covers the figures and the statements of fact that people and agents write about the repository and its work. When the correction of such a claim counts as made is DR-146 (A correction counts as made once the claim's other copies are searched for). The numbers in the tool's own reports fall instead under the design's goal that each of them can be reproduced from what the report reads: its ledger, its price table and the job times that GitHub reports (see the design's goals).

## What reversing it would change

The section of `CLAUDE.md` on figures, but for its sentence on corrections (DR-146), would change, and so would the README's summary of the rules for working here, which names this one. No requirement, threat or part of the public surface is involved.
