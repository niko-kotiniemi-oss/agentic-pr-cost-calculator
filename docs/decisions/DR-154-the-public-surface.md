# DR-154: The public surface is what adopters configure or depend on

- **Type:** technical
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R71, R122
- **Threats:** T44, T53, T56
- **Replaces:** none
- **Closed by:** none

## Context

Adopters configure the tool in their own repositories and build their own settings around parts of it, and their update bots let a minor or patch release through as safe (T53). The major number rises for a change that existing adopters must act on (DR-096), so which parts those are has to be named.

## Decision

The public surface, whose breaking change raises the major number, is what adopters configure or depend on: the hook file's registered command, by its form and not the checksum it carries, which changes with every change to the hook, and the hook file's path, the opt-in key `pr-cost.capture`, the `.pr-cost/` path that adopters set their git hooks, sparse checkouts and attributes around, the ledger format, the store's format, `.pr-cost.json`, the reusable workflow's path, inputs and permissions, and the Python and git floors.

## Alternatives

None were recorded when this was decided.

## Consequences

- A part on the list cannot change without a new major release, which is why the registered command counts by its form and not by the hook file's checksum that it carries, a value that changes whenever the file does (`docs/features/releases-and-compatibility.md`).
- The store's format and the Python and git floors are on the list, so a store that an older hook could misread (T44) and a raised floor (T56) reach adopters only in a major release.
- A part that the list leaves out could change in a minor or patch release, which neither the manifest nor the release check can make up for, since both read the list (T53, DR-123).

## Scope

This covers which parts make up the public surface. How a change to it moves the version number is DR-096 (Versions are semantic), how the release check holds such a change to a raised major number is DR-123 (The release check compares a manifest of the public surface), and the earlier ledger formats that a newer report goes on reading are DR-040 (A newer report reads every earlier ledger format).

## What reversing it would change

R122 in `releases-and-compatibility` would change in its list of the surface, with its scenario "The surface manifest names the whole public surface", and so would R71's clause that makes any change to that surface one the major number follows. The design's decisions 10 and 11, the answers of T44, T53 and T56, the surface manifest and the release check that task 6.1 builds, and the feature page's list of the surface would change too, and DR-040, DR-096 and DR-123 would be revisited. A surface that named fewer parts would let a change to a part it dropped reach adopters as a minor or patch release; one that named more would make a change to any part it added a breaking one.
