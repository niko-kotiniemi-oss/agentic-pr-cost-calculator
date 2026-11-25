# DR-319: A refused tag's version is marked in the default branch's changelog, and a failed run spends none

- **Type:** process
- **Boundary:** outgoing
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-24
- **Requirements:** R319
- **Threats:** T67, T153, T222
- **Replaces:** none
- **Closed by:** none

## Context

The owner deletes a refused release's tag and its draft, and never tags its version again (DR-209), so neither git nor the releases keep a record that a version was refused, and nothing that the release workflow can read says so. Reading the workflow's own run history would need a permission that its job does not hold, and would read a run that failed for an outage as a refusal.

## Decision

The changelog on the default branch keeps, for each version whose tag the release workflow refused, a heading that gives that version and `[REFUSED]`, which the owner adds when the tag is deleted, and the release workflow publishes no release of a version that the default branch's changelog marks so. The workflow says whether it refused a tag, and a run that fails without refusing one spends no version (R319).

## Alternatives

- The workflow's run history: it needs `actions: read`, and cannot tell a refusal from an outage.
- A file of its own: one more file to keep, where the changelog already holds each version.

## Consequences

- A refused version stays marked in a tracked file that the default branch keeps, which the release workflow reads at the default branch's tip.
- Marking a version is the owner's step, beside deleting its tag.

## Scope

This covers how a refused version is kept from release. Why a refused tag is deleted is DR-209.

## What reversing it would change

How hard it is to reverse: reversible. R319, the release workflow's check and the changelog's marks would change, and DR-209's rule would rest on the owner alone again.
