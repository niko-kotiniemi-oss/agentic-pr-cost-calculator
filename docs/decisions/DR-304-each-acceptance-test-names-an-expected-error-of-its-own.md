# DR-304: Each acceptance test names an expected error of its own

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R291
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

Acceptance tests are written before their code and marked as expected failures (DR-084). A test marked that way passes CI whatever error it raises, so one that fails for another test's reason, or for an error in its own comparison, hides that its own scenario is unbuilt or wrong. The guide names this as a gap that B-007 closes. The golden tests already name such an error (design decision 14).

## Decision

Each acceptance test that is marked as an expected failure names as its expected error one that only the missing code of its own scenario raises, never an assertion of its comparison and never one that another capability's missing code raises, and a test fails otherwise (R291). The seam that they drive is the one that the walking skeleton built (DR-249).

## Alternatives

- Expected failures with no named error: any error would pass, including one in the test itself.

## Consequences

- Each capability's code raises an error of its own while it is unbuilt, which the build removes with the code that replaces it.

## Scope

This covers how an acceptance test marks its expected failure. Writing acceptance tests first is DR-084.

## What reversing it would change

How hard it is to reverse: reversible. R291 and its scenarios, and the test that holds them, would change. Nothing that adopters configure changes.
