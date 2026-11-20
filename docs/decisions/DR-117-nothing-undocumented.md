# DR-117: The tool does nothing its documentation leaves out

- **Type:** scope
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the owner, 2026-10-20
- **Requirements:** R29, R30, R101
- **Threats:** T57
- **Replaces:** none
- **Closed by:** none

## Context

A developer reading the documentation should be able to say how the tool works, and rightly be suspicious of anything it does that the documentation leaves out. Adopters run the hook on their own machines and the report in their own CI, from a workflow they write (see the threat model's boundary 6).

## Decision

Everything the tool does is in its documentation, so that a reader can rightly be suspicious of anything it does that the documentation leaves out.

## Alternatives

None were recorded when this was decided.

## Consequences

- What the tool does is set out in three documents, the register (DR-100), the feature pages (DR-101) and `docs/how-it-works.md` (DR-102), and each changes in the same pull request as what it describes (DR-103).
- Tests hold the page to the permissions, actions and images that the workflows use (R101), which is T57's answer, and to a diagram for every flow (R29), and the tool connects only where its documentation says (R30).
- Until the code exists, the documentation describes the design. Task 5.3 brings it up to date with what was built, and adds a check that every network call and environment variable that the code reads is named in `docs/how-it-works.md`.
- `CLAUDE.md`'s section on documentation names this as the rule that it serves.
- `docs/how-it-works.md` sets out each flow, input, output, credential, permission and connection (DR-102), and treats anything the tool does that it leaves out as a defect.

## Scope

This covers how much of what the tool does its documentation holds. What each document holds is DR-100 (A register lists every requirement with its kind), DR-101 (Each feature has a page) and DR-102 (A page explains how the tool works as a whole), and when it changes is DR-103 (Documentation changes in the same pull request as what it describes).

## What reversing it would change

R29 and R101 in `project-standards` would change, with their scenarios, and only R30's title would change, not its text or its scenarios, which state fixed connection rules (DR-008, DR-020, DR-060, DR-160). So would the design's decision 12, which names this record, the opening of `docs/how-it-works.md`, which treats anything the tool does that the page leaves out as a defect, `CLAUDE.md`'s section on documentation, T57's answer and task 5.3. DR-100, DR-101, DR-102 and DR-103 would be revisited. The documentation is not part of the public surface, so the change would not be a breaking one for adopters.
