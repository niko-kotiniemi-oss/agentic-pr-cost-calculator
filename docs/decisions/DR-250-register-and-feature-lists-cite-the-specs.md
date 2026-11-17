# DR-250: The register and the feature pages' lists of requirements stay written by hand and held by tests, not generated

- **Type:** process
- **Status:** accepted
- **Decided by:** the owner, 2026-11-17
- **Requirements:** R29, R100
- **Threats:** T173
- **Replaces:** none
- **Closed by:** none

## Context

DR-232 makes the specs the single source of what the tool does and leaves to the pull request that delivers B-022 whether the register and the feature pages' lists of requirements become views generated from the specs, as the review of the design's architecture on 2026-11-12 proposed, or stay pages that cite them. The register gives each requirement's ID, kind, capability and title, and each feature page lists its requirements by ID. Neither states a requirement's behaviour, and `tests/test_documentation.py` already fails when the register misses a requirement or names one that the specs do not hold, and when a requirement is on no feature page or on another spec's page (R100).

The owner chose on 2026-11-17, on the view that the specs are the portable definition of what to build and that tests coupled to the code, outer ones of the outcomes and inner ones of the logic, are the canonical truth of whether the product works as intended, so that an index of IDs and titles needs no generator of its own.

## Decision

The register and each feature page's list of requirements stay written by hand, as an index of the specs, and the tests that compare them with the specs keep holding them. No script generates them.

## Alternatives

- Views generated from the specs by a script, with CI checking that the committed pages match its output: no one edits the lists, but the script is code to maintain and test, and it would hold nothing that the tests do not already hold.

## Consequences

- The sweep of B-022 leaves the register and the lists as they are, apart from what DR-232 asks of every page.
- A requirement added, renamed or moved changes the register and its feature page by hand in the same pull request, and the tests fail until it does (R100).

## Scope

This covers how the register and the feature pages' lists of requirements are kept. That the register is the specs' index is DR-100, and that the specs are the single source is DR-232.

## What reversing it would change

How hard it is to reverse: reversible. A later pull request can add a script that writes the lists and a check that the committed pages match it, and replace the tests of R100 that compare them, with no change to what the pages say.
