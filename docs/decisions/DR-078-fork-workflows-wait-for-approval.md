# DR-078: Outside contributors' workflows wait for approval

- **Type:** security and privacy
- **Boundary:** incoming
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** none
- **Threats:** T37
- **Replaces:** none
- **Closed by:** none

## Context

CI runs on a pull request from a fork with code that the fork's author chose, which is how a contributor could misuse it (T37). Such runs get a read-only token and no secrets from GitHub, and this repository's CI asks only for read access and keeps no secrets (T37). The repository's Actions settings can also hold an outside contributor's workflows until they are approved, with options for first-time contributors and one for every external contributor.

## Decision

Approval for running fork pull request workflows from contributors, under the repository's Actions settings, is set to *Require approval for all external contributors*, the strictest choice, so that no workflow of an outside contributor's pull request runs before it is approved.

## Alternatives

- The options for first-time contributors only, which GitHub warns a contributor can meet by getting one harmless change merged.

## Consequences

- An outside contributor's pull request has no CI run, and so no `ci` result, until its workflows are approved.
- The approval comes on top of the read-only token and the absence of secrets, which hold for such runs whether or not they wait (T37).
- The setting is the owner's. No file in the repository holds it and no test reads it, so nothing in the repository can check that it is applied.

## Scope

This covers when an outside contributor's workflows run. What a workflow can do once it runs is DR-067 (Workflow tokens are read-only, except for releases and the report's comment), and how such a pull request is reviewed is DR-081 (Outside pull requests are reviewed from `main`).

## What reversing it would change

The threat model's entry among the settings the owner keeps would change, with T37's answer, which names the approval. No requirement and no part of the public surface is involved.
