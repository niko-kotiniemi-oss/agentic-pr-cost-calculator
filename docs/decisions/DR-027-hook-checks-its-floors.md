# DR-027: The hook checks its Python and git versions first

- **Type:** technical
- **Boundary:** outgoing
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R32, R99, R110
- **Threats:** T56
- **Replaces:** none
- **Closed by:** none

## Context

Adopters copy the hook rather than install it (DR-022), so no installer holds it to `requires-python`: it runs with whatever `python3` and `git` the machine has, and its registered command hides a failure (DR-031). The design also relies closely on how git behaves, and an older git that behaves otherwise could misrecord calls or leave the index changed (T56).

## Decision

The hook's first statement checks that Python is 3.11 or later, and its first git command checks that git is 2.43 or later, the oldest git that CI tests. When either is older, the run stops there, having recorded, staged and printed nothing, and exits with success.

## Alternatives

None were recorded when this was decided.

## Consequences

- An old machine is never kept from committing, but its usage goes unrecorded and the hook shows nothing. The comment of a pull request whose capture never ran then says that no agent usage was recorded (R20), as the design's risk "[Capture fails without anyone seeing it, since a hook that succeeds shows nothing]" says.
- Taking back and putting back ledger files, which R110 asks of every run whatever the switches say, is left to the runs that the floors let go on.
- The guard is one more copy of the oldest supported Python, which a test holds to `requires-python` (R99, DR-026, T55).
- Since the git floor is the oldest git that CI tests, a CI job keeps running the tests that use git with git 2.43 (task 4.4), and task 6.5 tests the check under an older Python and an older git.

## Scope

This covers the hook's check of the Python and git it runs with. The report is outside it. Which Python is the oldest supported is DR-025 (The oldest supported Python is 3.11), and where that version is declared is DR-026 (`requires-python` is the one source of the oldest supported Python).

## What reversing it would change

R32 in `releases-and-compatibility` would change, with its scenarios "An older Python is refused quietly" and "An older git is refused quietly", and so would R99, whose list of copies names the hook's guard, R110 in `switch-and-opt-in`, which names the floors, the design's decision 10, T56's answer, the `releases-and-compatibility` feature page and task 6.5. Both floors are part of the public surface, so removing or changing either would be a breaking change for adopters (DR-096).
