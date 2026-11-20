# DR-008: Capture uses no service outside GitHub and the repository

- **Type:** architecture
- **Boundary:** incoming
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R30
- **Threats:** T24
- **Replaces:** none
- **Closed by:** none

## Context

Usage is read on the machine that runs the agent's session, which in a cloud session is gone once the session ends (see the design's context). The report runs in GitHub Actions, on the push that a merge makes to the default branch (DR-018). The counts have to get from the one to the other.

## Decision

Capture depends on no service but GitHub and the repository itself: the counts that it records reach the report only through the repository.

## Alternatives

- A separate service the hook posts to, which the repository would have to run and trust.

## Consequences

- The hook uses no token, key or account, and the report uses only the workflow's own `GITHUB_TOKEN` (see `docs/how-it-works.md`).
- The hook opens no network connection (R30), and every connection that the report makes goes to GitHub (T24).
- The counts leave the session's machine only in the person's own commits, when they push (DR-010).

## Scope

This covers which services the tool depends on to carry the counts. That the hook opens no network connection at all is DR-060 (The hook opens no network connection), how the counts travel to the pull request is DR-010 (Usage travels inside the agent's own commits), and where prices come from is DR-020 (Prices come from a dated price table in the repository).

## What reversing it would change

R30 in `project-standards` would change, with its scenarios "The hook opens no connection" and "The report connects only to GitHub", and so would the design's goals and decision 1, the threat model's data flow and trust boundaries, T24's answer, the credentials and connections that `docs/how-it-works.md` lists, with its list of what the tool never does, and tasks 1.13 and 5.3, which check the tool's connections. DR-010 and DR-060 would be revisited. A change to the ledger format, the `.pr-cost/` path, or the reusable workflow's inputs or permissions, which are part of the public surface, would be a breaking one for adopters (DR-096).
