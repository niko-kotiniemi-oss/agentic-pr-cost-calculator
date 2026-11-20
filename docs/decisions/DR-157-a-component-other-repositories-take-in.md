# DR-157: The tool is a component that other repositories take in

- **Type:** scope
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the owner, 2026-10-20
- **Requirements:** R71, R122
- **Threats:** T28
- **Replaces:** none
- **Closed by:** none

## Context

The tool is for teams that build pull requests with AI coding agents (DR-001), and it is developed in a public repository that anyone can read and adopt (DR-114). The proposal says that it is delivered as a session hook script and a GitHub Actions workflow that other repositories can use, and the threat model's boundary 6 is the tool reaching adopters, who run the hook on their own machines and the report in their own CI, called from a workflow they write.

## Decision

The tool is a component that other repositories take into their own work, rather than an application or a service of its own.

## Alternatives

None were recorded when this was decided.

## Consequences

- Adopters copy the hook file from a pinned commit (DR-022) and call the report as a reusable workflow from a workflow of their own (DR-132), so the tool has no deployment, no account and no service of its own to run.
- The hook and the report use Python's standard library only, so the tool fits into other projects without pulling anything in (DR-023; the README's section on compatibility and releases).
- Each version is a release whose number says what an adopter must do (DR-096), and what adopters configure or depend on is the public surface (DR-154).
- The tool's code runs inside other people's work, so a malicious change here, or to something the repository depends on, would reach them through the hook and the workflow (T28).

## Scope

This covers what kind of thing the tool is. Whom it is for is DR-001 (The tool is for teams that build pull requests with AI coding agents), that it is developed in the open is DR-114 (The tool is open source, in a public repository), how the hook reaches adopters is DR-022 (Adopters copy the hook file from a pinned commit), and how the report does is DR-132 (The report is a reusable workflow that adopters call).

## What reversing it would change

R71 and R122 in `releases-and-compatibility`, which say what a version's number tells adopters and what they depend on, would change. The proposal's account of what the change delivers, the README's opening and its statement that the tool fits into other projects, the opening of the feature page for `releases-and-compatibility`, the design's decisions 1, 7 and 11, the threat model's boundary 6 and T28's answer would change too, and so would the record of each part that rests on adopters taking the tool in: DR-022, DR-023, DR-025, DR-096, DR-132, DR-154 and DR-156 would be revisited. The answers to the other threats of boundary 6 rest on other records, which their Held by lines name, so this record lists only T28, the tool's code reaching adopters. Adopters hold the hook file and call the reusable workflow from this repository, so the change would reach every one of them and would be a breaking one.
