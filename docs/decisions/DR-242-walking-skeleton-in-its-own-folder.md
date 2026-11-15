# DR-242: The walking skeleton's code lives in its own folder here, under tests, and the build grows from it

- **Type:** architecture
- **Status:** accepted
- **Decided by:** the owner, 2026-11-14
- **Requirements:** R234, R238
- **Threats:** T188
- **Replaces:** none
- **Closed by:** none

## Context

The owner approved on 2026-11-14 a plan for the walking skeleton (B-021) whose first choice was where its code lives: in this repository's pull request, under tests, so that the build grows from it, or only in the scratch repository where it runs, as code to throw away. DR-236 bounds where the skeleton runs and what reaches it from here, and leaves what it builds to its own pull request (DR-233). No code of the tool exists yet, and the guide's entries on acceptance tests and fixtures name the skeleton as the change that builds the test seam (B-007, B-021).

## Decision

The walking skeleton's code, its capture script, its report script, its plugin's files, its workflow for a scratch repository and its shape recorder, lives in `skeleton/` of this repository, with tests written before it under `tests/`. Nothing here registers it (R234), and the build grows the tool from it and removes the folder before the first release, which the release workflow refuses while a tag's tree holds it (R238).

## Alternatives

- Code only in the scratch repository, thrown away after the run: faster, but the test seam would be built again by the build, and what the run showed would rest on code that no review here read.
- The skeleton's code at the paths that the tool's own files will take: it would then read as the tool to anyone who clones the repository before the build.

## Consequences

- Tasks 1.31 to 1.35 of `add-pr-cost-calculator` build `skeleton/` test-first, and its tests run in this repository's CI.
- Anyone who clones the repository sees code that is not the tool, so its files open by saying that they are the walking skeleton and not a release (T188).
- Task 6.1's release check refuses a tag whose tree holds `skeleton/` (R238).

## Scope

This covers where the skeleton's code lives and when it goes. Where it runs is DR-236 (The walking skeleton runs apart from this repository and records only with the switch and the opt-in) and DR-245 (The walking skeleton runs as a plugin of its own, in a project that holds only its scratch repository).

## What reversing it would change

How hard it is to reverse: reversible, until the build starts. One pull request can move or remove the folder. R234 and R238 in `project-standards` would change, with their scenarios, and so would design decision 18, tasks 1.31 to 1.35 and 6.1, and the answer of T188.
