# DR-283: No job or step of CI can be skipped, or fail, while the job `ci` passes

- **Type:** technical
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R276, R278
- **Threats:** T269, T279
- **Replaces:** none
- **Closed by:** none

## Context

The job `ci` is the one check that the ruleset on `main` requires, and it needs every other job of `.github/workflows/ci.yml` and passes only where each of them succeeded (DR-043, DR-072). A key of a job or of a step can still let a check pass around it: the threat review of this change against what was built found that a condition could skip the job of Windows line endings, or its step that saves the files, and that `continue-on-error` could let a step fail, while the job `ci` passed (T269). GitHub skips a job whose needed job failed, and reports it as passing, unless its `if` uses a status function, so the job `ci` runs with `if: always()`, and its last step reads what each job gave. The second review of this change, by `/code-review` and `/verify`, found that no test held either of those, so that a change to one could let a merge pass where a job failed. It found too that every step's exit status, and so every job's result and the gate's own, had become that of the filter through which every command of CI writes what it prints (DR-274), so that a change that made the filter lose a command's status would turn every job green, the gate and the filter's own tests among them (T279).

## Decision

A test holds the job `ci` to need every other job of `.github/workflows/ci.yml`, to run with `if: always()`, and to end in a step that reads the result of each job that it needs and fails unless every one is a success, which the test shows by running that step, under the shell that the workflow gives it, with a success beside each result that a job can give: a success, a failure, a cancel and a skip. No job there but `ci` sets `if`, no job sets `continue-on-error`, and no step sets either, and the test names each that does. One step of the job `ci` runs under GitHub's own shell for bash, outside the filter, and fails unless the filter exits with 3 for a command that exits with 3 and with 143 for one that SIGTERM stops. It is the one step that the filter's rule leaves out, and its test gives it word for word and shows that it fails a filter changed to lose either status.

## Alternatives

- Leaving the gate to DR-043's last step and the ruleset, as before this change: a key that skips a job or a step, or lets a step fail, passes the gate, and a change to the job `ci`'s own `if` or last step meets no test.
- Running only the job `ci`'s last step outside the filter: it would read each job's result rightly, but each other job's result would still be the filter's, so a filter that lost the status would make every job a success that the gate then passes.
- Running every step outside the filter: a check that quotes a path as it is would carry its hidden characters into the log that a session reads (T264).
- A check of the filter that the ruleset requires apart from `ci`: the ruleset would need a change that only the owner makes, and the check's own step would still run under the filter or outside it, as this one does.

## Consequences

- `tests/test_conventions.py` fails, naming the job, where the job `ci` does not need a job of `.github/workflows/ci.yml`, and, naming the job, the step and the key, where a job other than `ci` sets `if`, or a job or a step sets `continue-on-error`, or a step sets `if`, and it fails where the job `ci` sets no `if: always()` or where its last step passes with a failure, a cancel or a skip beside a success, or fails with two successes (R276; T269; task 1.54).
- `tests/test_printable_log.py` fails where the job `ci` holds no step that runs the filter, as the test gives it, under GitHub's own shell for bash, and where that step changes or another step gives a shell of its own, and shows that the step fails a filter that drops a command's exit status or the signal that stopped it (R278; T279; task 1.56).
- A change that makes the filter lose a command's exit status fails the job `ci`, for which a merge waits, though every other step passes.
- The step that checks the filter sends what the filter prints nowhere, and writes to the log only its two lines, which name the statuses that the filter gave.

## Scope

This covers what lets the job `ci` pass only where every job of CI ran and succeeded, and the step that checks the filter from outside it. That CI ends in one aggregate job is DR-043 (CI ends in one aggregate `ci` job), what the ruleset on `main` requires is DR-072 (The ruleset on `main` requires a pull request and the `ci` check), and the filter through which every other step writes what it prints is DR-274 (Everything that this repository writes holds printable ASCII). The job that saves the repository's files with Windows line endings is DR-281 (A checkout writes line feeds whatever `core.autocrlf` says, and the checks read Windows line endings as git stages them).

## What reversing it would change

How hard it is to reverse: reversible. The checks are part of two tests and of one step of the job `ci`. R276's scenarios on a job that the job `ci` does not need and on a job or a step that CI may skip or let fail would change, and so would R278's scenario on a filter that loses a command's exit status and the exception in its scenario on a step whose output does not go through the filter, the answers of T269 and T279, design decision 23 and tasks 1.54 and 1.56. A key that skips a check, or a filter that loses a status, would then let a merge pass again. CI is not part of the public surface, so the change would not be a breaking one for adopters.
