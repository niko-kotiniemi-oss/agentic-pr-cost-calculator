# DR-142: Superpowers owns how the tool is built

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-18 and 2026-10-20
- **Requirements:** none
- **Threats:** T35
- **Replaces:** none
- **Closed by:** none

## Context

What the tool must do is kept in OpenSpec's changes and specs, and the code follows an approved change (DR-079). That leaves how the code is built: how the work is planned inside the change, how its tests are written, how faults are found and how the result is reviewed. Superpowers, the other tool pinned for the work, is a library of skills for Claude Code (`.claude-plugin/marketplace.json`), vendored under `vendor/superpowers/` at the commit that `UPSTREAM.lock` names (README). `.claude/settings.json` enables it in every session here, so its skills are loaded into the context of the agents that work on the repository (T35).

## Decision

Superpowers owns how the tool is built: its skills drive planning inside an approved change, test-driven development, debugging and review.

## Alternatives

None were recorded when this was decided.

## Consequences

- Planning starts from a change that is already approved, so Superpowers settles how a requirement is met, while what must hold stays with OpenSpec (DR-079).
- What the skills say shapes what agents do, so a changed skill is a threat to the work (T35), which the vendored copy's pin and CI's comparison with upstream answer (DR-041).
- Every session here loads Superpowers from the vendored copy, and a session-start hook loads its introduction whenever a session starts, is cleared or is compacted (`.claude/settings.json`).

## Scope

This covers how the tool is built. What it must do is DR-079 (OpenSpec owns what the tool must do), and that the skills of both tools are used as their files write them is DR-143 (Skills are used as written, never from memory). How Superpowers is vendored and pinned is DR-041 (Superpowers is vendored and compared with upstream in CI), and its usage reporting is DR-071 (Development tools report nothing about how they are used). The tests and the review that every change gets have records of their own, such as DR-084 (Acceptance tests come first) and DR-093 (Every change is reviewed in a separate context before it merges).

## What reversing it would change

The bullet on Superpowers in the section "Who owns what" of `CLAUDE.md` and the README's account of Superpowers would change, and so would the design's decision 8, which names this record, and T35's description and answer, which name Superpowers' skills. DR-041, which vendors Superpowers for this work, and DR-143, which names its skills, would be revisited. Superpowers is a development-only part, outside the public surface, so the change would not be a breaking one for adopters.
