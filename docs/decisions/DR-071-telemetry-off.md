# DR-071: Development tools report nothing about how they are used

- **Type:** security and privacy
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** none
- **Threats:** T36
- **Replaces:** none
- **Closed by:** none

## Context

OpenSpec collects anonymous usage statistics unless it is told not to, and Superpowers has a switch of its own (T36). OpenSpec runs in the sessions that work on this repository, whose start-up hook installs it in a cloud session, and in `scripts/verify-openspec.sh`, which CI and a person at a terminal both run to check the generated skills and validate the specs. Superpowers runs in those sessions as the plugin that `.claude/settings.json` enables from its vendored copy, while CI only compares that copy with upstream (DR-041).

## Decision

The usage reporting of OpenSpec and of Superpowers is off wherever this repository runs them: in every session here, and for OpenSpec in CI as well. `.claude/settings.json` gives every session here `DO_NOT_TRACK=1`, which OpenSpec honours, and `SUPERPOWERS_DISABLE_TELEMETRY=1`, which Superpowers reads. `scripts/verify-openspec.sh` sets `DO_NOT_TRACK=1` and `OPENSPEC_TELEMETRY=0` for its own run.

## Alternatives

None were recorded when this was decided.

## Consequences

- `tests/test_repository.py` fails when the session settings leave either switch on, and a second test shows that the check names a switch left on.
- No test holds the switches that the script sets, and a development tool added later might honour neither switch (T36's residual).
- The session settings reach every process that Claude Code starts in a session here, hooks included (see the design's context), and the script's switches reach its own run.

## Scope

This covers the usage reporting of OpenSpec and of Superpowers. The script also exports `OPENSPEC_NO_UPDATE_CHECK=1` beside its usage-reporting switches, which is not part of this record. How OpenSpec is pinned and checked is DR-042 (OpenSpec is pinned and its skills are regenerated in CI), and how Superpowers is vendored is DR-041 (Superpowers is vendored and compared with upstream in CI).

## What reversing it would change

The `env` block of `.claude/settings.json`, the switches that `scripts/verify-openspec.sh` exports, the telemetry tests in `tests/test_repository.py`, and T36's answer and residual would change. No requirement and no part of the public surface is involved.
