# Walking Skeleton Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:test-driven-development for each task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build tasks 1.31 to 1.35 of `add-pr-cost-calculator`: the walking skeleton in `skeleton/`, the checks that hold it, and its tests, as design decision 18 gives it.

**Architecture:** Five standard-library scripts in `skeleton/`, each opening with a comment that says it is the walking skeleton and not the tool: `capture.py`, which the plugin's hooks run; `report.py`, which `workflow.yml` runs in the scratch repository; `build_zip.py`, which builds the plugin's zip from a commit; `shape.py`, which records the value-free shape of the run's transcripts; and the plugin's `plugin.json` and `hooks.json`. The checks live in `tests/test_skeleton_checks.py`, as the other document checks of this repository do, and each is shown to fail on a planted defect. The scripts are driven through the seam that DR-246 names: capture through a hook's input on standard input, transcript files that the test writes and a real git repository in a temporary folder; the report through ledger files in such a repository, checked out into two folders as the workflow does, and recorded responses of GitHub's API.

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
- Branch coverage was measured once, outside the repository, with `coverage` installed only in the session's virtual environment. Every line of the four scripts ran; the two branches not taken are the `if __name__ == "__main__"` checks of `capture.py` and `shape.py`, which are false only when a test imports the script, and the tests run both as scripts. No gate holds this until the build's coverage gate exists.
- Property-based testing: `tests/test_skeleton_shape.py` searches random transcripts from a fixed seed for a value that reaches the shape, in place of Hypothesis, which the build brings (design decision 8).

## Left for after the build

- The threat review at implementation, which rates each of T185 to T194 again against the code.
- The four review lanes, before the owner merges.
- Task 1.36, the run, from one commit that those reviews have read.
