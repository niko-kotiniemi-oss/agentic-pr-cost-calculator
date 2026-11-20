# DR-123: The release check compares a manifest of the public surface

- **Type:** technical
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R71, R122, R123
- **Threats:** T53
- **Replaces:** none
- **Closed by:** none

## Context

The major number rises for any change to the public surface (DR-096), which is what adopters configure or depend on (DR-154). Adopters' update bots treat minor and patch releases as safe, so a breaking change released under a minor or patch number would reach them as if it were safe (T53).

## Decision

The repository keeps a manifest of the public surface in a form that a program reads, and the release check compares the manifest at the tag with the one at the previous release's commit (see the design's decision 11). When the two differ, the release goes ahead only with a raised major number and a `### Breaking` section in its changelog entry.

## Alternatives

- Trusting the changelog's own label to tell whether a release breaks anything, which would let a breaking change through as a minor or patch release (T53).

## Consequences

- The check is only as complete as the manifest, which is one more account of the surface beside DR-154 and R122: a part that it left out could change in a minor or patch release (T53). R122's scenario holds the manifest to naming every part.
- The check reads the changelog entry's `### Breaking` section, so it rests on the changelog's form (DR-149).

## Scope

This covers how the release check holds the version number to the public surface. Which parts make up that surface is DR-154 (The public surface is what adopters configure or depend on), how version numbers are chosen is DR-096 (Versions are semantic), and the changelog's form, with the section that lists a breaking change, is DR-149 (`pyproject.toml` holds the version, and the changelog has one entry per release). The other half of T53's answer, reading the ledger formats of earlier releases, is DR-040 (A newer report reads every earlier ledger format).

## What reversing it would change

R122's sentence on the manifest, with its scenario "The surface manifest names the whole public surface", and R123, with its scenario "A changed public surface needs a major version", would change in `releases-and-compatibility`, and so would R71's pointer to R122 by its title. So would T53's answer, task 6.1, the release flow in `docs/how-it-works.md`, the feature page's account of versions and the design's decision 11. DR-096, DR-149 and DR-154 would be revisited. The manifest and the check are not part of the public surface, so the change would not be a breaking one for adopters.
