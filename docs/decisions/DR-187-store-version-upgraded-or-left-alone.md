# DR-187: The store states its format's version, a later release upgrades an earlier one, and an unknown one is left alone

- **Type:** technical
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-02
- **Requirements:** R55, R107, R109, R145, R148, R150, R153
- **Threats:** T44
- **Replaces:** DR-137
- **Closed by:** none

## Context

Every worktree shares one store (DR-011), while each session runs the hook file from its own working tree, so two releases of the hook can meet one store, and an older one could misread a newer store's notes, among them those that keep a removed file's calls out (T44). DR-137 decided what a run does with a version that it does not know. A later release meets the stores that earlier releases wrote too, whose intervals an earlier release's rules bounded, and the owner asked on 2026-11-02 for a conservative boundary of consent, under which no call is recorded unless capture can show that it was made while consent held, and for the store's lifecycle to be specified. A run with a switch off removes a store that does not parse (DR-170), and a review of the change's later commits, in a context separate from the one that wrote them, found that nothing made every version state its version in the same way, so that an earlier release could take a later release's store for a broken one and remove it, and with it the notes that T44 is about.

## Decision

From the first release on, the store states the version of its format. A run that meets a version it does not know exits with success having done nothing, whatever the switches say: it records, stages, takes back and puts back nothing, and leaves the store untouched, as DR-137 decided. A run that meets a store that an earlier release wrote rewrites it in its own version, keeping its waiting calls, its notes of taken calls and its notes of staged and taken-back ledger files, and begins every session's interval anew. Every version of the store is a JSON object whose `version` field every release reads in the same way, and a store does not parse only when a run cannot read a version from it, or reads one that it knows from a store that is not of that version's form, so that a run always tells a store that a later release wrote from a broken one.

## Alternatives

- Leaving a store of an earlier version alone too, which would stop capture in that clone until the person removed the store, and the notes that take-backs and put-backs need with it.
- Carrying an earlier release's intervals over, which would place calls inside intervals by rules that the later release may no longer hold.
- Removing a store of an earlier version, which would leave a ledger file staged before the upgrade to git, as a removed store does (DR-177).

## Consequences

- A run of a release that does not know the store's version records nothing, so its session's calls are not counted (the design's risk "[Two releases of the hook meet one store, as when sessions start in two worktrees that hold different releases]"; T44).
- At an upgrade, the calls that answer lines written before the run that upgrades the store are left out, and the next ledger file staged for their worktree and branch says that calls were left out for consent (DR-180), so the count is too low across an upgrade.
- A ledger file that an earlier release staged is still taken back and put back, since its note is kept.
- No later version can move or change the `version` field without every earlier release taking its stores for broken ones, so the field stays as the first release writes it.
- An opt-out that only an earlier release's runs see empties a later release's store only at the next run of a release that knows its version, which treats it as an opt-out that no run saw (DR-169, T44).

## Scope

This covers the version that the store states and what a run does with a store of an earlier version or of one that it does not know. How the store is written is DR-036 (The store is replaced whole, under a lock), what the store holds is the design's decision 15, and the ledger formats that a newer report reads are DR-040 (A newer report reads every earlier ledger format).

## What reversing it would change

R55 in `usage-capture` would change, with its scenarios "A store of a format the step does not know is left alone", "A store that an earlier release wrote is upgraded" and "A store that a later release wrote is left alone by a run with a switch off", and so would R153's clause on when a store does not parse, and the clauses of R107, R109 and R145 in `switch-and-opt-in`, and of R148 and R150 in `usage-capture`, that leave a store of a version that a run does not know to R55. The store's format, which carries the version, is part of the public surface, so the change would be a breaking one for adopters (DR-096). The design's decision 1 and the risk named above, T44's answer, the usage-capture feature page and task 2.1, which builds the store, would change too, and DR-011, whose consequences give the version as the answer to two releases meeting one store, would be revisited.
