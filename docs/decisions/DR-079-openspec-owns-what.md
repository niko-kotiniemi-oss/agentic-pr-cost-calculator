# DR-079: OpenSpec owns what the tool must do

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-20
- **Requirements:** R73, R74, R100
- **Threats:** T35
- **Replaces:** none
- **Closed by:** none

## Context

New features and changes of behaviour are agreed before anyone writes code, and people and agent sessions work on the repository under the same rules (`CONTRIBUTING.md`). OpenSpec, one of two tools pinned for that work, holds what the calculator must do (README). Its skills, which its pinned CLI writes, are loaded into the context of the agents that work here (T35).

## Decision

OpenSpec owns what the tool must do: the requirements and their scenarios are kept in OpenSpec's changes and specs under `openspec/`, and the code follows an approved change.

## Alternatives

None were recorded when this was decided.

## Consequences

- When the work shows that a requirement is wrong, the OpenSpec change is corrected before the code, so that intent never changes silently in code.
- What OpenSpec's skills say shapes what agents do, so a changed skill is a threat to the work (T35), which its pin answers (DR-042).
- The documentation's checks rest on OpenSpec's structure: the register matches the specs (R100), each spec has a feature page (R73), and the proposal of each change lists every capability its specs hold and says how each is validated (R74).

## Scope

This covers what OpenSpec owns: what the tool must do, in the changes and specs that hold it. How the tool is built is DR-142 (Superpowers owns how the tool is built), and that the skills of both tools are used as their files write them is DR-143 (Skills are used as written, never from memory). How OpenSpec is pinned and its skills checked is DR-042 (OpenSpec is pinned and its skills are regenerated in CI), and its usage reporting is DR-071 (Development tools report nothing about how they are used).

## What reversing it would change

The bullet on OpenSpec in the section "Who owns what" of `CLAUDE.md`, the README's account of OpenSpec, the steps of `CONTRIBUTING.md` and the pull request template's section on the OpenSpec change would change. R73, R74 and R100 in `project-standards` would change with their scenarios, and so would `tests/test_documentation.py`, the files that install and check OpenSpec (`.claude/hooks/session-start.sh` and `scripts/verify-openspec.sh`) and T35's answer. DR-042, DR-071, DR-104, DR-142, DR-143 and DR-150 would be revisited.
