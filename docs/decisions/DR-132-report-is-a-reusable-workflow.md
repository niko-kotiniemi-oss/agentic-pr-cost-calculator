# DR-132: The report is a reusable workflow that adopters call

- **Type:** architecture
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R122
- **Threats:** T24, T29
- **Replaces:** none
- **Closed by:** none

## Context

The tool is a component that other repositories take in (DR-157), and its report runs in each adopter's CI once a pull request has merged (DR-005). The proposal delivers it as a GitHub Actions workflow that other repositories can use, beside a hook file that adopters copy (DR-022). GitHub hands a reusable workflow its caller's `github` context, the triggering event among it, while the `job` context names the reusable workflow's own repository and commit (see the design's context).

## Decision

The report is a reusable workflow that this repository provides. An adopting repository runs it by calling it from a workflow of its own, and the README gives that calling workflow.

## Alternatives

None were recorded when this was decided.

## Consequences

- The report can run its own code at the commit that the caller pins, which the `job` context gives it, and read the caller's repository only as data (DR-062).
- A reusable workflow runs with its caller's event and token, so an adopter could call the report from a `pull_request_target` workflow, grant it every permission or pass it every secret with `secrets: inherit` (T29). The report therefore checks the event itself (DR-061), and the README's calling workflow grants only what the report needs and passes no secret (DR-063).
- The reusable workflow declares the permissions that the report needs, which a caller can narrow but not widen (T24).
- Its path, inputs and permissions are part of the public surface (R122, DR-154), so changing any of them is a breaking change, released as a new major version (DR-096).

## Scope

This covers how adopters run the report. The push that the calling workflow is triggered by is DR-018 (The report runs on the push that a merge makes to the default branch), the report's own check of the event is DR-061 (The report runs only for a push to the default branch), the code it runs is DR-062 (The report runs its own pinned code), what the calling workflow grants is DR-063 (The calling workflow grants only what the report needs), and how the hook reaches adopters is DR-022 (Adopters copy the hook file from a pinned commit).

## What reversing it would change

R122 in `releases-and-compatibility` would change where it names the reusable workflow's path, inputs and permissions, and so would the surface manifest that task 6.1 writes. So would the design's decisions 7 and 11 where they name the reusable workflow, the proposal's What Changes and Impact, the answers of T24 and T29, tasks 4.3 and 4.4, the README's calling workflow, and the report's part and permissions in `docs/how-it-works.md`. Adopters would have to change how they run the report, so the change would be a breaking one (DR-096), and DR-018, DR-061, DR-062, DR-063 and DR-154 would be revisited.
