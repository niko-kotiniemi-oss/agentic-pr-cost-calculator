# DR-137: The store states its format's version

- **Type:** technical
- **Status:** closed
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R55
- **Threats:** T44
- **Replaces:** none
- **Closed by:** DR-187

## Context

Every worktree shares one store (DR-011), while each session runs the hook file from its own working tree, so two releases of the hook can meet one store, and an older one could misread a newer store's notes, among them those that keep a removed file's calls out (T44).

## Decision

From the first release on, the store states the version of its format, and a run that meets a version it does not know exits with success having done nothing: it records, stages, takes back and puts back nothing, and leaves the store untouched.

## Alternatives

None were recorded when this was decided.

## Consequences

- A run of a release that does not know the store's version records nothing, so its session's calls are not counted (the design's risk "[Two releases of the hook meet one store, as when sessions start in two worktrees that hold different releases]"; T44).

## Scope

This covers the version that the store states and what a run does with a version it does not know. How the store is written is DR-036 (The store is replaced whole, under a lock), and the ledger formats that a newer report reads are DR-040 (A newer report reads every earlier ledger format).

## What reversing it would change

R55 in `usage-capture` would change, with its scenario "A store of a format the step does not know is left alone". The store's format, which carries the version, is part of the public surface, so the change would be a breaking one for adopters (DR-096). The design's decision 1 and the risk named above, T44's answer, the usage-capture feature page and task 2.1, which builds the store, would change too, and DR-011, whose consequences give the version as the answer to two releases meeting one store, would be revisited.
