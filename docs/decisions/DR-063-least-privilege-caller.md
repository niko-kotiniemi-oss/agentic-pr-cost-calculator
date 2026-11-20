# DR-063: The calling workflow grants only what the report needs

- **Type:** security and privacy
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R24
- **Threats:** T24, T29
- **Replaces:** none
- **Closed by:** none

## Context

A reusable workflow runs with the token and the secrets that its caller gives it, and an adopter could grant the report every permission or pass it every secret with `secrets: inherit` (T29). A token with wider permissions than the report needs turns any bug into a bigger one (T24). The report needs three things of GitHub: to read the ledger files, `.pr-cost.json` and the pull request's commits from git, to list the workflow runs and job attempts on those commits, and to post and update its one comment (see `docs/how-it-works.md`).

## Decision

The calling workflow that the README gives grants `contents: read`, `actions: read` and `pull-requests: write`, one for each of those needs, and passes no secrets. The reusable workflow declares the same three permissions and asks for no secret, so the report runs with the workflow's own `GITHUB_TOKEN` alone.

## Alternatives

None were recorded when this was decided.

## Consequences

- A repository that has added no secret for the tool still gets its report (R24).
- A caller can narrow the permissions that the reusable workflow declares but not widen them, which rests on GitHub enforcing them as its documentation says (T24, and see the threat model's Assumptions).
- A test holds the README's calling workflow to these three permissions and to passing no secrets (task 4.4, T29).
- This repository's workflow tests keep every workflow but the report's and the release's from granting a write, and task 4.3 has them allow the report's workflow exactly these three (DR-067).

## Scope

This covers the permissions and the secrets that the report runs with. It also covers the permissions that the reusable workflow itself declares, which DR-132 (The report is a reusable workflow that adopters call) gives among its consequences. That it writes nothing to the repository is DR-016 (The report writes nothing to the repository), the events it accepts are DR-061 (The report runs only for a push to the default branch), and the permissions of this repository's own workflows are DR-067 (Workflow tokens are read-only, except for releases and the report's comment).

## What reversing it would change

R24 in `report-comment` would change, with its scenario "No secret is configured", and so would the answers of T24 and T29. The design's decision 7, the calling workflow in the README and the test that holds it (task 4.4), task 4.3 and the allowance it adds to `tests/test_repository.py`, the section on credentials and permissions in `docs/how-it-works.md`, `SECURITY.md`, which promises no secret beyond the `GITHUB_TOKEN` and the narrowest permissions that work, and the proposal's Impact would change too. The reusable workflow's permissions are part of the public surface, so a change to them would be released as a new major version (DR-096), and a new write permission would revisit DR-016.
