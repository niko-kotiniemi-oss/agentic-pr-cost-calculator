# DR-233: A walking skeleton comes before the remaining pull requests that prepare the build

- **Type:** process
- **Status:** accepted
- **Decided by:** the owner, 2026-11-12
- **Requirements:** none
- **Threats:** T172, T174
- **Replaces:** none
- **Closed by:** none

## Context

On 2026-11-12 the change's specs on the default branch hold 210 requirements and 584 scenarios, and the assumptions hold 430 facts, of which 363 are not yet checked, 3 are observed and none is tested, while no fact about Claude Code is observed. No code of the tool exists, and the roadmap's Now lists six more pull requests before the build after the one that adds the patterns page, which became the guide (DR-231). The reviews of the design's architecture, CI and security, and testing on that day each name this a long design before any code runs, the big design up front that Beck argues against in Extreme Programming Explained (1999), and each names a walking skeleton as its remedy, as Cockburn gives it in Crystal Clear (2004) and Freeman and Pryce in Growing Object-Oriented Software, Guided by Tests (2009): the thinnest build that runs end to end, which meets the riskiest assumptions, those about Claude Code's transcripts and hooks, before the specs grow further.

## Decision

The pull request after the one that adds the guide builds a walking skeleton, the backlog item B-021: the thinnest path from a session's calls through capture and a ledger file in a commit to the report's figure, run once in a real Claude Code session. It comes before the risk register and the other pull requests that prepare the build, and what it finds goes into the specs and the assumptions first (DR-232). It is a pull request of its own, whose design the owner approves before it is built, as for every other.

## Alternatives

- The skeleton as the first task of the build, after the requirements are corrected, which leaves the corrections to be made without what it would show.
- No skeleton, with the long design before any code knowingly accepted.

## Consequences

- The roadmap's Now lists B-021 first once the guide's item, B-001, is done, before the other items that prepare the build.
- Facts about Claude Code's transcripts and hooks can be observed before the requirements are corrected, and the specs and the assumptions take what it shows.
- What the skeleton builds, how it is tested, and what of it the build keeps, are for its own pull request to propose, within the bounds that DR-236 sets on where its real run happens and what it records (T172, T174).
- The README's status, which says that none of the tool's code exists yet and that code starts once the design is approved, changes with the skeleton's pull request.

## Scope

This covers when a walking skeleton comes. What it builds is for its own pull request, where it runs and what it records is DR-236 (The walking skeleton runs apart from this repository and records only with the switch and the opt-in), and which document states what the tool does is DR-232 (The specs are the single source of what the tool does).

## What reversing it would change

How hard it is to reverse: reversible, until the skeleton is built. The order is the order of the items under the roadmap's Now, which one pull request can change. The roadmap's Now would change, with the order of the items that prepare the build, and so would B-021, the guide's entry that rests on this record, the README's status once the skeleton's pull request has changed it, and the answers of T172 and T174.
