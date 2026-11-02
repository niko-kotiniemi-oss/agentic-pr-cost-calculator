# DR-171: An opt-out empties the store

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-02
- **Requirements:** R109, R146
- **Threats:** T38, T114
- **Replaces:** none
- **Closed by:** none

## Context

A run that finds the person's capture off ends every session's interval and withholds the calls made before it (DR-168). Under DR-047 the store still kept every session's notes and the calls waiting to be staged, which no later run would stage but which stayed on the person's machine. The owner asked on 2026-11-02 that the store's behaviour at an opt-out be specified, with as few identifiers and as short a retention as capture can work with.

## Decision

A run that finds the person's own capture off, in their global configuration or in the repository's, removes from the store every call waiting to be staged, every note of a taken call and every session's notes, keeping only the notes that a take-back or a put-back still needs, and the store removes itself once those are done (DR-175). An opt-out removes or changes no ledger file that a commit holds.

## Alternatives

- Keeping the notes, as DR-047 did, which keeps on the person's machine what no run will use.
- Removing the whole store at once, which would leave a ledger file staged before the opt-out in place, with T10's disturbances.
- Removing committed ledger files too, which would change the person's branch and still leave the files in git's history, clones and forks.

## Consequences

- If capture is turned on again, every transcript is read afresh, since the store no longer notes how far each was read, and intervals that begin only at later runs keep the earlier calls out (DR-168).
- Without the notes of taken calls, the calls of a committed ledger file could be staged again only if they answered a line written inside a later interval, which they cannot, so DR-055 still holds.
- An opt-out that no run sees, because no session runs again in the repository, leaves the store as it was until a run comes or the person removes it, which the README says how to do (T114).
- A ledger file that was pushed stays published (DR-182).

## Scope

This covers what an opt-out removes. Which calls the switches let through is DR-168, what a run with a switch off writes is DR-170, how long the store keeps anything is DR-175, and what stays published is DR-182.

## What reversing it would change

R109 and R146 in `switch-and-opt-in` would change, with their scenarios, and so would the design's decisions 6 and 15, T38's answer, T114, the README's section on turning capture off that task 4.4 writes, and task 2.4. The store's format would not change, so the change would not be a breaking one for adopters.
