# The report comment

When a pull request merges with the tool on before its merge or after it, a workflow posts one short comment on it with what it cost.

**Status:** designed, not built yet.

**Spec:** `report-comment`

**Requirements:** R20, R94, R95, R157, R96, R65, R202, R193, R21, R97, R98, R23, R66, R67, R168, R24, R68, R69, R70, R35, R158, R102

## Expected behaviour

- **What it shows.** What R20, R94 and R95 give, and, as R65 and R202 give it, when the repository's hook file or its registration does not run the report's own hook file, as when it was copied from the README of another release.
- **Calls left out.** R157 gives what the comment says when the pull request's ledger files flag calls left out, and R95 that a restored or copied ledger file adds no counts and no flags.
- **What it says about itself.** R94 gives what the comment says of its figure. Calls that Claude Code's own tools make to a model, such as a web fetch's summary, are counted only where the transcript holds them.
- **Only its own words.** The comment, the job summary and the log hold numbers, the report's fixed text, and names that the price table lists. It never quotes ledger lines, file names, branch names, job names or any other text from the pull request (R21, R97).
- **One comment.** When the report runs again, it updates its own comment and no one else's (R96).
- **Within bounds.** R23 and R67 give how the report reads ledger files from git as data, R66 what it does when they are too large to read, and R35 and R102 how it holds each line to the ledger format and completes.
- **Read by its version.** R158 gives how the report reads each ledger file that the merge adds by the version that its first line states, so that a report older than the hook says what it could not read rather than misreading it. R193 gives what the comment says when a ledger file comes from a later release of the capture step than the report's own, as a person's plugin can while the repository pins an earlier release (DR-208), and R168 how the default branch's earlier ledger files are read.
- **When there is no comment.** R69 and R70 give the pushes that get no comment, and R172 what the job summary says of a merge that finds the tool off both before it and after it.
- **A budget that runs short.** A pull request whose runs and jobs take more calls to read than the budget leaves still gets its comment, as R64 gives it.

## How it is validated

This feature is validated first by its spec's scenarios: each gets an acceptance test before its code, seen to fail for the expected reason (task 1.4). Then come the checks that DR-084 to DR-093 and DR-109 apply to all the tool's code. Beyond those, this feature has its own:

- A property test that no planted string reaches the comment, the job summary or the log (task 4.1), and unit tests at every boundary of the ledger format, with each file read by the version that its first line states (task 4.2).
- Tests that the report refuses every event but the push that a merge makes, and that the token is in none of its outputs (task 4.3).
- End to end: this repository's own merge posts a report whose figures can be recomputed from its ledger, the price table and the jobs API (task 7.1).

## Known limitations and the roadmap

The design's risks that concern this feature and are not on the roadmap, each with what it means:

- **A workflow runs a script or a local action that a pull request changes**: the comment flags changes to workflow and settings files, but not to the scripts that workflows run, which stay for review in the diff.

The [roadmap](../roadmap.md) gives what is planned next and later, and the limitations that an adopter notices.

## See also

- `report-comment` in `openspec/`, and design decisions 7 and 16 of `add-pr-cost-calculator`.
