# DR-304: Each acceptance test names an expected error of its own

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R291
- **Threats:** T309
- **Replaces:** none
- **Closed by:** none

## Context

Acceptance tests are written before their code and marked as expected failures (DR-084). A test marked that way passes CI whatever error it raises, so one that fails for another test's reason, or for an error in its own comparison, hides that its own scenario is unbuilt or wrong. The guide names this as a gap that B-007 closes. The golden tests already name such an error (design decision 14).

## Decision

Each capability's acceptance test drives its capability's own entry point in the tool's package, which raises the capability's own error class until its code is built, and is held back only by a strict expected-failure marker naming that class: never `AssertionError`, a built-in error, one raised from under `tests/`, or another capability's error or a base or subclass of it. The golden set's tests, which run the capture step and the report end to end, name the error of a missing capture step or report. A test that reads the collected tests after every hook has run fails otherwise, and on an acceptance test skipped or marked to fail by any other means (R291). The seam that they drive is the one that the walking skeleton built (DR-249).

## Alternatives

- Expected failures with no named error: any error would pass, including one in the test itself.

## Consequences

- Each capability's code raises an error of its own while it is unbuilt, which the build removes with the code that replaces it.
- A test of `pricing` that went through the report would fail first on the report's unbuilt reading of ledger files, which is why each capability's tests drive its own entry point, and the end-to-end paths are the golden set's.
- The rule is per capability, not per scenario, since a test can compare error classes across capabilities but cannot tell which scenario's missing code raised an error; two scenarios of one capability can share its error, and their own assertions tell them apart once the code is built.

## Scope

This covers how an acceptance test marks its expected failure. Writing acceptance tests first is DR-084.

## What reversing it would change

How hard it is to reverse: reversible. R291 and its scenarios, and the test that holds them, would change. Nothing that adopters configure changes.
