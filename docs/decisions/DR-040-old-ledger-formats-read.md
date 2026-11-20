# DR-040: A newer report reads every earlier ledger format

- **Type:** technical
- **Boundary:** incoming
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** none
- **Threats:** T53
- **Replaces:** none
- **Closed by:** none

## Context

An adopter copies the hook file into their repository and pins the report's workflow to a commit. Update bots can propose a new commit for that pin but cannot change the copied file, so the two drift apart (T54). The ledger format is part of the public surface (DR-154), and a newer report that could not read an older hook's ledger would fail in the common case of a pin updated before the hook (T53).

## Decision

A newer report reads every ledger format that an earlier release's hook wrote, since adopters update the workflow pin more readily than the copied hook, and its tests keep one fixture per released format.

## Alternatives

None were recorded when this was decided.

## Consequences

- Each released format stays among those that every later report reads, and its fixture stays in the report's tests (task 6.4), so the set only grows.
- A change to the format is still a change to the public surface, released as a new major version (DR-096).

## Scope

This covers a newer report reading the ledger lines of an older hook. That the comment says when the merged commit's hook file differs from the one at the report's own commit is DR-139 (The report names a hook that is not the report's own), and the version of the store's own format, which only the hook reads, is DR-137 (The store states its format's version).

## What reversing it would change

No requirement states this, so the specs would not change, but T53's answer would, and so would the design's decision 11, task 6.4, and the ledger's feature page and the proposal's row for `ledger`, which name one fixture per released format. A report that stopped reading a released format would break adopters whose hook still writes it, so the change would be a breaking one, released as a new major version (DR-096).
