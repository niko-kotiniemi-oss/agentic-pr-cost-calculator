# DR-312: A pull request that changes the vendored copy or the marketplace is also checked by its base commit's scripts

- **Type:** security and privacy
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-12
- **Requirements:** R299
- **Threats:** T132, T137, T320
- **Replaces:** none
- **Closed by:** none

## Context

A pull request that changes the vendor check or a marketplace check together with what it checks passes its own CI, so only the owner's review stops it (T132, T137). The owner chose on 2026-11-12 that the vendor check runs the base commit's script, as the marketplace check already takes its build script from a trusted commit.

## Decision

When a pull request changes `vendor/` or the marketplace's root file or plugin folder, CI also runs the base commit's own vendor check and marketplace checks over the pull request's tree, from a checkout of the base commit that reads that tree only as data, runs none of its code, and holds no secret and no token that can write, and fails when either check fails (R299).

## Alternatives

- `pull_request_target`, which runs the base's workflow with a token that can write: it is the event through which a pull request's code most often reaches a write token, so it is not used.

## Consequences

- A pull request that changes a check reaches the default branch only through the owner's review, and checks only the pull requests after it.
- The job reads the pull request's tree through git, which the design threat-models (T320).

## Scope

This covers which commit's checks hold the vendored copy and the marketplace. The checks themselves are R184, R190 and the vendored copy's own requirement.

## What reversing it would change

How hard it is to reverse: reversible. R299 and the job that runs it would change, and the answers of T132 and T137 would rest on the owner's review alone.
