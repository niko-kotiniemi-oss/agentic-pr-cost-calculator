# DR-288: An adopter never needs to clone the whole repository

- **Type:** architecture
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-27
- **Requirements:** R280
- **Threats:** T285
- **Replaces:** none
- **Closed by:** none

## Context

The owner asked on 2026-10-27 for a record that adopters never clone the whole repository. An adopter copies the hook file from a pinned commit (DR-022), calls the report as a reusable workflow at a release's commit (DR-132, DR-156), and adds the plugin from a release's zip or from this repository as a marketplace (DR-203).

## Decision

An adopter can take the tool in wholly through what a release names: the hook file, the reusable workflow at the release's commit and the plugin's zip, none of which needs a clone of this repository, its history or its development files. The other route, adding this repository as a plugin marketplace, has Claude Code clone the repository with the person's own git (A72, T143); the zip is the route that fetches nothing more. The table of what goes out on the page on how the tool works lists each route, with its records (R280).

## Alternatives

None were recorded when this was decided.

## Consequences

- A person who adds the marketplace holds a clone of the repository, which the table of what goes out says (T143).
- A new way to adopt the tool that needs a clone would need a record that closes this one.

## Scope

This covers what an adopter takes from this repository. Which commit an adopter pins is DR-156 (Adopters pin the commit that a release names).

## What reversing it would change

How hard it is to reverse: reversible with work. The README's section on adopting the tool and the table of what goes out on the page on how the tool works would change, and adopters who copy single files would have to follow a new way, so the change would be a breaking one for adopters.
