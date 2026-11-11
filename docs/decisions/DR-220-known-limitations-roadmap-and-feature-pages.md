# DR-220: The roadmap lists a short list of known limitations, and each feature page lists the rest of its own

- **Type:** process
- **Status:** accepted
- **Decided by:** the owner, 2026-11-11
- **Requirements:** R208
- **Threats:** T162
- **Replaces:** none
- **Closed by:** none

## Context

The design's risks and trade-offs list where the tool, as designed, falls short, such as the calls that reach no commit and the model calls that Claude Code makes for its own tools without writing them to the transcript. They are long and many, too many for a short page, and a reader who adopts the tool meets only some of them. A risk that no page lists is one that a reader cannot find outside the design.

## Decision

The roadmap's Known limitations lists the limitations that an adopter notices, and each feature page has a section on known limitations and the roadmap that lists the rest of the risks that concern its feature and links the roadmap. Each risk is listed by its title as the design gives it, and every risk is listed on the roadmap or on at least one feature page.

## Alternatives

- A short list on the roadmap with a link to the design for the rest, with no check that every risk is listed.
- Every risk on the roadmap, which makes it long.

## Consequences

- A test fails when a risk of the design is listed nowhere, when a page lists as a risk a title that the design does not give, and when a feature page has no such section or it does not link the roadmap (R208), so that a risk added to the design, or one whose title changes, fails CI until a page lists it (T162).
- Which risks an adopter notices, and which feature a risk concerns, rest on review.

## Scope

This covers where the design's risks are listed. The roadmap's place and sections are DR-218 (A roadmap says what is now, next and later).

## What reversing it would change

R208 in `project-standards` would change, with its scenarios, and so would design decision 12, task 1.26, the answer of T162, the feature pages and the roadmap's Known limitations.
