# DR-171: An opt-out empties the store

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-02
- **Requirements:** R109, R146, R161
- **Threats:** T38, T114
- **Replaces:** none
- **Closed by:** none

## Context

A run that finds the person's capture off ends every session's interval and withholds the calls made before it (DR-168). Under DR-047 the store still kept every session's notes and the calls waiting to be staged, which no later run would stage but which stayed on the person's machine. The owner asked on 2026-11-02 that the store's behaviour at an opt-out be specified, with as few identifiers and as short a retention as capture can work with.

## Decision

A run that finds the person's own capture off, in their global configuration, in the repository's or as git reads it there (DR-183), removes from a store of a version that it knows (DR-187) every call waiting to be staged, every flag due, every note of a taken call and every session's notes, keeping only the notes that a take-back or a put-back still needs, whose calls and flags a take-back after it returns to nothing that waits, and the store removes itself once those are done (DR-175). An opt-out removes or changes no ledger file that a commit holds. A run holds the store's lock from when it reads the store until it has written it, reads both switches again under that lock before it writes a call to the store or stages a ledger file, and acts only on a store whose file is still the one that its lock holds, so that a run that began before an opt-out writes nothing after it.

## Alternatives

- Keeping the notes, as DR-047 did, which keeps on the person's machine what no run will use.
- Removing the whole store at once, which would leave a ledger file staged before the opt-out in place, with T10's disturbances.
- Removing committed ledger files too, which would change the person's branch and still leave the files in git's history, clones and forks.
- Reading the switches only when a run starts, which would let a run that began before an opt-out write the calls it read, or stage them, after it.

## Consequences

- If capture is turned on again, every transcript is read afresh, since the store no longer notes how far each was read, and intervals that begin only at later runs keep the earlier calls out (DR-168).
- Without the notes of taken calls, the calls of a committed ledger file could be staged again only if they answered a line written inside a later interval, which they cannot, so DR-055 still holds.
- An opt-out that no run sees, because no session runs again in the repository, leaves the store as it was until a run comes or the person removes it, which the README says how to do (T114), and one that only an earlier release's runs see waits for a run of a release that knows the store's version (DR-187).
- A ledger file that was pushed stays published (DR-182).
- A run that waited for the lock while an opt-out emptied and removed the store writes nothing into it, and a run that notes another fingerprint does what an opt-out does (DR-169).

## Scope

This covers what an opt-out removes. Which calls the switches let through is DR-168, what a run with a switch off writes is DR-170, how long the store keeps anything is DR-175, and what stays published is DR-182.

## What reversing it would change

R109, R146 and R161 in `switch-and-opt-in` would change, with their scenarios, and so would the design's decisions 6 and 15, T38's answer, T114, the README's section on turning capture off that task 4.4 writes, and task 2.4. The store's format would not change, so the change would not be a breaking one for adopters.
