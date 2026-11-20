# DR-076: Actions' default workflow permissions are read-only

- **Type:** security and privacy
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** none
- **Threats:** T68
- **Replaces:** none
- **Closed by:** none

## Context

A workflow that declares no permissions gets the token that the repository's Actions settings give by default. The workflows here declare their own: CI declares `contents: read`, a test fails on any workflow whose top-level permissions are anything but `contents: read`, and only the release job, once it exists, holds `contents: write` (DR-067). T68 is the threat that a job holding a write token runs someone else's code.

## Decision

The repository's Actions settings give workflows a read-only token by default, as a backstop for a workflow that declares no permissions of its own.

## Alternatives

None were recorded when this was decided.

## Consequences

- The workflows' own declarations, which `tests/test_repository.py` holds, stay the control, and the default only backs them up (T68).
- The setting is the owner's. No file in the repository holds it and no test reads it, so nothing in the repository can check that it is applied.

## Scope

This covers the token a workflow gets when it declares none. What each workflow and job declares, and which of them may write, is DR-067 (Workflow tokens are read-only, except for releases and the report's comment).

## What reversing it would change

The threat model's entry among the settings the owner keeps and T68's answer would change, and the workflows' own declarations (DR-067) would be left without the backstop. No requirement and no part of the public surface is involved.
