# DR-170: A run that finds a switch off creates no store

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-02
- **Requirements:** R118, R145
- **Threats:** T38, T46, T113
- **Replaces:** none
- **Closed by:** none

## Context

DR-047 had every run note in the store whether it found both switches on, so a run that found a switch off created the store in the repository's git common directory, even for someone who had never opted in, and started git to find it (T38, T46). The owner asked on 2026-11-02 that no session-identifying information be kept for someone who never opted in, unless it is needed to clean up state that already exists. Intervals now begin only at a run that finds both switches on (DR-168), so a run that finds a switch off has nothing to note of its own session but the end of an interval that is open.

## Decision

A run that finds either switch off creates no store and adds no note of its session to one. It removes a store that does not parse, and in one of a version that it knows (DR-187) only ends its own session's interval, does what an opt-out (DR-171) and the take-backs and put-backs that the store notes call for, drops what the retention window ends (DR-175), and removes the store when it then holds nothing, since those only remove. It reads both switches before it starts any program: when its own reading finds either off, it starts git only to find the store, and when its own reading finds both on and git's reading of the opt-in then finds capture off (DR-183), it starts git only for that reading and to find the store.

## Alternatives

- Noting every run that finds a switch off, as DR-047 did, which keeps a note of a session for someone who never opted in.
- Starting no program at all in a run that finds a switch off, which would leave in place a ledger file staged before an opt-out, with T10's disturbances, since the step asks git where the store is.

## Consequences

- Someone who has never opted in leaves nothing in the git common directory, and no note of their sessions.
- A run that finds a switch off still starts git, at its absolute path, to find the store, so T46's answer still holds for it (DR-188).
- A repository that turns the tool off while a person's store holds notes still drops them at the end of the retention window, and a store that does not parse goes at the next run that finds a switch off.
- An open interval ends at its session's next run that finds a switch off, or at any run that finds the person's capture off (DR-171).

## Scope

This covers what a run that finds a switch off writes. Which calls the switches let through is DR-168, what an opt-out removes is DR-171, take-backs and put-backs are DR-014 (A ledger file that no commit took is taken back) and DR-130 (A taken-back ledger file is put back once, when its commit holds it), and how the step starts git is DR-188 (The hook starts only git, by absolute path, from a safe folder, without the session's git variables).

## What reversing it would change

R145 in `switch-and-opt-in` and R118 in `usage-capture` would change, with their scenarios, and so would the design's decisions 1 and 6, T38's answer, T46's residual, T113, and tasks 2.1 and 2.4. A store would then exist for people who never opted in, as it did under DR-047. The store's format would not change, so the change would not be a breaking one for adopters.
