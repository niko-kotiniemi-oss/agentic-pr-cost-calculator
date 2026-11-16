# Walking Skeleton Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:test-driven-development for each task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build tasks 1.31 to 1.35 of `add-pr-cost-calculator`: the walking skeleton in `skeleton/`, the checks that hold it, and its tests, as design decision 18 gives it.

**Architecture:** Four standard-library scripts in `skeleton/`, each opening with a comment that says it is the walking skeleton and not the tool: `capture.py`, which the plugin's hooks run; `report.py`, which `workflow.yml` runs in the scratch repository; `build_zip.py`, which builds the plugin's zip from a commit; `shape.py`, which records the value-free shape of the run's transcripts; and the plugin's `plugin.json` and `hooks.json`. The checks live in `tests/test_skeleton_checks.py`, as the other document checks of this repository do, and each is shown to fail on a planted defect. The scripts are driven through the seam that DR-246 names: capture through a hook's input on standard input, transcript files that the test writes and a real git repository in a temporary folder; the report through ledger files in such a repository, checked out into two folders as the workflow does, and recorded responses of GitHub's API.

**Tech Stack:** Python 3.11 standard library; pytest and PyYAML for the tests, which `requirements-dev.txt` pins.

**Spec:** R234 to R243 in `openspec/changes/add-pr-cost-calculator/specs/project-standards/spec.md`, design decision 18, DR-242 to DR-246.

## Global Constraints

- No test uses the network or a real transcript. Every transcript, ledger file and API response is written by the test.
- Planted identifiers in the tests are built by joining strings, so that no tracked file holds one whole and the private-reference check stays meaningful.
- Each test is seen to fail for the expected reason before the code that passes it.

## Tasks

- [x] **1.31 Checks.** `tests/test_skeleton_checks.py` holds `registration_problems` (R234), `shape_problems`, `kept_shapes` and `missing_shape_problems` (R236), `workflow_problems` and `checkout_problems` (R237) and `identity_problems` (R242); `tests/test_repository.py`'s private patterns gain the identifiers of a message, a request and a tool call. Red: with every check made to return no problem, each planted test failed; with the checks in place, only the two tests that read `skeleton/` failed, for want of the folder.
- [x] **1.32 Capture.** `tests/test_skeleton_capture.py`, then `skeleton/capture.py`, and the README's status. Red: every test failed because the script did not exist.
- [x] **1.33 Report and workflow.** `tests/test_skeleton_report.py`, then `skeleton/report.py` and `skeleton/workflow.yml`. Red: the test module could not import `report`. The workflow checks out `before` and `after` into two folders by SHA, so that no step fetches anything else, and skips the checkout of `before` when it is all zeros.
- [x] **1.34 Plugin and zip.** `tests/test_skeleton_plugin.py`, then `skeleton/plugin.json`, `skeleton/hooks.json` and `skeleton/build_zip.py`. Red: the test module could not import `build_zip`.
- [x] **1.35 Shape recorder.** `tests/test_skeleton_shape.py`, then `skeleton/shape.py`. Red: the recorder did not exist, so each test that runs it failed.

## What the build found in the spec

R236's scenario on a name of an identifier's form said "a lower-case prefix, an underscore and a token of 8 or more letters and digits". That form also matches field names such as `stop_sequence` and `is_sidechain`, so a real shape would have failed. The scenario now asks for a token that holds a digit or an upper-case letter, as identifiers do, and the spec changed before the check.

## Checks of the tests themselves

- Planted defects: after each script passed, single changes were planted in it, such as reading the opt-in from any scope, keeping calls made outside the repository, reading a half-written line or never taking a file back, and the tests were run again. Each planted change failed a test except two, which led to two new assertions: that the log never says `staged` for a command in another form, and that the shape recorder never reads a line that has no line break yet.
- Branch coverage was measured once, outside the repository, with `coverage` installed only in the session's virtual environment. Every line of the four scripts ran; after the fixes below, the one branch not taken is the `if __name__ == "__main__"` check of `capture.py`, which is false only when a test imports the script, and the tests only run it as a script. No gate holds this until the build's coverage gate exists.
- Property-based testing: `tests/test_skeleton_shape.py` searches random transcripts from a fixed seed for a value that reaches the shape, in place of Hypothesis, which the build brings (design decision 8).

## Fixes after the threat review at implementation

Seven reviewers, one per trust boundary, read the code at `7869896`; their findings are comments on the pull request. Each fix below was written test-first, the spec changing before the code where it changed a requirement.

- The skeleton has its own opt-in, `pr-cost-skeleton.capture`, so that the tool's opt-in, which an environment may already hold, never turns it on (R235).
- A recognised commit may give `-m` more than once, as for trailer lines, and only in the repository of each `git add` before it (R240).
- The log counts the calls it leaves out and why, and the calls whose lines that give a stop reason differ, and gives the SHA-256 of the capture script that ran; it no longer gives fields that could only be true.
- The shape keeps top-level names only from a list that the recorder and its check share (R236).
- The report follows no link and takes as a count only a whole number from zero to below a bound.
- The workflow's check also refuses other checkout inputs, another folder, another command and the word `secrets` anywhere.
- The zip is built only from a full commit id, printed beside its hash, with its files stored rather than compressed.
- The private-reference check knows a session's and a line's identifier.
- Task 1.36 and design decision 18 now check the files at the pull request's head before the merge, check that log lines appear before reading their absence, and run the privacy checks before the results come here.

## Fixes after the review lanes

The four lanes, `/simplify`, `/security-review`, `/code-review` and `/verify`, read the code at `c23f7d0`; their findings are comments on the pull request. Each fix below was written test-first, and seen to fail before the code changed; the spec changed before the code where a requirement changed.

- The opt-in comes from the person's global files alone, read without the session's git variables or `XDG_CONFIG_HOME`, which a repository's settings can set, and without asking git for a boolean, so that a repository's own value that is not one never turns it off (R235).
- A call made in a repository inside the repository is not kept (R235), and a quoted message that holds `-m` is recognised.
- A folder whose git common directory lies outside it, as a worktree's, gets no log, and a ledger folder that is a link gets no file.
- The report follows no linked ledger folder, counts a folder named like a ledger file as unread, and writes a model name as code.
- The zip is built with `--no-replace-objects`.
- The private-reference check knows a server tool call's identifier and a message's with a platform's infix.
- A test holds the ledger's form equal in capture and the report, and the command recogniser's path step is written once.
- After the command, a staged ledger file is settled by the command as written, not by resolving it again from the folder that the command moved to (A4).
- A word that the shell would expand is not recognised, a message after two blanks is, and a new file is seen whatever the person's `status.showUntrackedFiles` says.
- The private-reference pattern asks for a digit in an identifier's value, so that ordinary names pass, and names the platforms' infixes.
- The workflow's check also refuses a step's `shell`, `defaults`, a `container`, `services` and another runner.
- The shape recorder refuses an output named like a transcript, and the check for a missing shape reads task 1.36 as the other checks do and fails when it cannot find it.
- The tests of the report and the zip use the repository's shared isolated git environment.

## Fixes after the narrow review of those fixes

One `/code-review` read `a773eca` alone; its findings are a comment on the pull request. Each fix was written test-first, and the three points of the fixes that no test held were each undone once to see a new test fail.

- The opt-in is read with git's values separated by NUL, so a repository's value that holds a line break is never read as a global one, and a number other than zero counts as true, as git reads it; a key written with no value is not taken.
- Calls made in a worktree are kept by no repository, which decision 18 now says.
- The workflow's check is an allowlist of the keys that the designed workflow uses, at each level, and a step's `env` may hold the token alone.
- The capture tests shut out the developer's own XDG git configuration.
- The store keeps the SHA-256 of the staged command, not its text; only the hook before a command resolves it; a carriage return is refused.
- The pages say that `XDG_CONFIG_HOME` and `HOME` are guarded against should A5 not hold.

## Left for after the build

- The threat review at implementation, which rates each of T185 to T194 again against the code.
- The four review lanes, before the owner merges.
- Task 1.36, the run, from one commit that those reviews have read.
