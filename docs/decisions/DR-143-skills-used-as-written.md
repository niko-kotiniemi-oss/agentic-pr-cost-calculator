# DR-143: Skills are used as written, never from memory

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-25
- **Requirements:** none
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

The work on this repository goes through the skills of two pinned tools: OpenSpec's, which its pinned CLI writes under `.claude/skills/`, for what the tool must do, and Superpowers', vendored under `vendor/superpowers/skills/`, for how it is built (DR-079, DR-142). CI holds both sets of files to the pinned versions (DR-041, DR-042). The skills reach agents loaded into their context, and a session that started outside this repository does not have them loaded.

## Decision

OpenSpec's and Superpowers' skills are used as their files write them, never from a memory of them. Where a skill is not loaded, its `SKILL.md` under `.claude/skills/` or `vendor/superpowers/skills/` is read and followed, and the session says that it did.

## Alternatives

None were recorded when this was decided.

## Consequences

- The steps an agent takes are those of the skills at the versions that the repository pins and CI checks, not those of a version that it remembers.
- A session that started outside this repository can still follow a skill, by reading its file, and its account of the work says so.
- No test holds the rule; it rests on `CLAUDE.md`.

## Scope

This covers how the two tools' skills are used. What OpenSpec owns is DR-079 (OpenSpec owns what the tool must do), and what Superpowers owns is DR-142 (Superpowers owns how the tool is built). That the skill files themselves match the pinned versions is DR-041 (Superpowers is vendored and compared with upstream in CI) and DR-042 (OpenSpec is pinned and its skills are regenerated in CI).

## What reversing it would change

The bullet of `CLAUDE.md` on using the skills themselves, not a memory of them, in its section "Who owns what", would change. No requirement, threat or part of the public surface is involved.
