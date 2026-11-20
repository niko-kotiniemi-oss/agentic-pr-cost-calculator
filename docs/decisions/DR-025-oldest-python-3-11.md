# DR-025: The oldest supported Python is 3.11

- **Type:** technical
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the owner, 2026-10-20
- **Requirements:** R25, R32
- **Threats:** T56
- **Replaces:** none
- **Closed by:** none

## Context

The tool runs inside other people's work: the hook on whatever machine a session uses, with that machine's `python3`, and the report on a runner the adopter's workflow chooses. A tool that needs the newest Python would leave out every adopter who cannot follow it.

## Decision

The oldest supported Python is 3.11, the oldest release that keeps upstream security support once 3.10 reaches its end of life, which the 3.10 release schedule (PEP 619) sets for October 2026, as the 3.11 schedule (PEP 664) sets October 2027 for 3.11.

## Alternatives

- Following the newest Python, which keeps the tool's own code simplest and leaves adopters behind.
- Supporting a version past its end of life, which no longer gets security fixes.

## Consequences

- Code that uses anything of the language or the standard library that Python 3.11 lacks fails CI on that version's job, or ruff or mypy reports it, and CI also runs the tests on the newest release (R25).
- On a machine whose `python3` is older than 3.11, the hook records and stages nothing and exits with success, so that machine's calls go unrecorded, but it is never blocked from committing (DR-027, T56).

## Scope

This covers which Python the tool supports. The development tools themselves may need newer versions than the tool does, since adopters never run them, but they run on the oldest supported Python too, so that one CI job shows the tool works there. Which file states the version is DR-026 (`requires-python` is the one source of the oldest supported Python), the hook's check of its floors, the git floor among them, is DR-027 (The hook checks its Python and git versions first), and when the oldest supported Python rises is DR-134 (The oldest supported Python rises only near its end of life or for a security fix).

## What reversing it would change

R25 and R32 in `releases-and-compatibility` would change, with their scenarios, and so would every copy of the version that R99 holds to `requires-python`. The Python floor is part of the public surface, so changing it would be a breaking change, released as a new major version (DR-096). The design's decision 10, T56's answer, tasks 1.11 and 6.5, the proposal, the feature page, the README, `SECURITY.md`, `CONTRIBUTING.md` and `CLAUDE.md` would change too, and DR-023, DR-026 and DR-027 would be revisited.
