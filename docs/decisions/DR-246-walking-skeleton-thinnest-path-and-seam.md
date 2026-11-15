# DR-246: The walking skeleton builds only the thinnest path, and its tests drive it through the seam that the build keeps

- **Type:** architecture
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R235
- **Threats:** T189
- **Replaces:** none
- **Closed by:** none

## Context

The design asks capture to handle many forms of git command, worktrees, several repositories, a store with a version, checksums, time budgets and a long list of edge cases (design decisions 1, 6, 15 to 17). The skeleton exists to run the path from a session's calls to the report's figure once, end to end, before the build (DR-233), and the guide's entry on acceptance tests asks that a test seam be named and built before the build's acceptance tests are written (B-007, B-021).

## Decision

The skeleton's capture reads a session's transcript and its subagents' transcripts, keeps each call's model, token counts and UTC day under a hash of its message id, and stages one ledger file only for a command that is `git commit` alone, with at most `git add` before it joined by two ampersands, taking the file back when the commit does not hold it. Design decision 18 lists what it leaves out. Its tests drive capture through the hook's input on standard input, transcript files and a real git repository in a temporary folder, and the report through ledger files and recorded GitHub responses, and the build keeps that seam.

## Alternatives

- The skeleton built to the full design: that is the build, and it would leave the design's assumptions unmet until the build was done.
- No named seam: the build's acceptance tests would bind to an interface that nobody has built, which the guide names as an anti-pattern.

## Consequences

- Every gap between the skeleton and the full design is listed in design decision 18, so that nothing is narrowed silently.
- The coverage and mutation gates do not exist yet, so the skeleton's tests cover each branch without a gate to hold it, and the build's gates then hold the code that grows from it.
- A commit in the scratch repository that the skeleton does not recognise gets no ledger file, and its calls wait (T189).

## Scope

This covers what the skeleton builds and how its tests drive it. Where its code lives is DR-242.

## What reversing it would change

How hard it is to reverse: reversible. The skeleton's scope is a list in the design and a set of tasks, which one pull request can change. R235 in `project-standards` would change, with its scenarios, and so would design decision 18, tasks 1.32 and 1.33 and the answer of T189.
