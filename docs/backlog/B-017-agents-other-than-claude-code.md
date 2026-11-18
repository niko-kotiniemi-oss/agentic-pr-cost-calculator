# B-017: Agents other than Claude Code

- **Status:** Planned
- **Last changed:** 2026-11-14
- **Brief:** Agents other than Claude Code, such as GitHub Copilot, Codex or Gemini, each in a change of its own after the first version.
- **Rests on:** DR-003, DR-234, DR-235, A68, T175
- **Issue:** none
- **Pull requests:** none

## Problem

The first version captures only Claude Code's calls (DR-003), so work done with another coding agent is not counted.

## What done looks like

Capture records the calls of other coding agents, such as GitHub Copilot, Codex or Gemini, and the report prices them as it prices Claude Code's. Each agent comes in a change of its own, by a record that replaces DR-003, which first checks that the agent gives what capture needs, such as each call's token counts, and that the answers that hold for Claude Code hold for it, and the one opt-in then records it for everyone who has opted in (DR-234, DR-235).

## Postponed points

None.
