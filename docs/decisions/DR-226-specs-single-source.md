# DR-226: The specs are the single source of what the tool does

- **Type:** process
- **Status:** accepted
- **Decided by:** the owner, 2026-11-12
- **Requirements:** none
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

The specs give each requirement with its scenarios, and the register is their index (DR-100). The same behaviour is also stated elsewhere: a threat's answer and residual, the design's risks, the feature pages and the page on how the tool works restate what scenarios say, and the tests hold the copies' IDs and tables, not their prose. The review of the design's architecture on 2026-11-12 names this the duplication of knowledge that Hunt and Thomas warn against in The Pragmatic Programmer (1999). The owner said on 2026-11-12 that the specs are the one point of truth of what to build, to which every other document leads, that they are updated with what the other documents find, and that they are the canon, kept and portable, so that they could be taken out and used to build a similar product in another form.

## Decision

The specs, each requirement with its scenarios, are the single source of what the tool does. Every other document, among them the threat model, the design's risks, the feature pages, the register, the page on how the tool works and the tests, cites a requirement or a scenario rather than stating its behaviour again, and says only what no scenario can, such as why, or what remains. What another document finds that the tool must do, such as a threat's answer or a review's finding, is written into a spec first. The specs say what the tool does and the design says how it is built, so that the specs, taken out alone, say what a similar product would need to do. `CLAUDE.md` steers by this. The documents that state behaviour today are brought to it by a pull request of their own, as the owner asked on 2026-10-29 that a sweep of earlier content come in a pull request of its own.

## Alternatives

- The copies kept and held by tests, as before, which hold IDs and tables but not prose that drifts.
- Views generated from the specs, which the review proposed for the register and the feature pages' lists of requirements. Whether a view is generated or cites is left to the pull request that brings the documents to this rule.
- Each document the source of what it covers, which leaves no one place that says what to build.

## Consequences

- `CLAUDE.md` says so, in the same pull request, so that every page written from then on cites the specs.
- A pull request of its own brings the documents that state behaviour today to this rule, and the roadmap lists it under Now.
- The register stays the specs' index (DR-100).
- A spec that cannot be read alone, because another document holds what it needs, is to be corrected in the spec.

## Scope

This covers which document states what the tool does. The register is DR-100 (A register lists every requirement with its kind), and the patterns page, which lists this duplication among the anti-patterns to fix, is DR-225 (A page says which recognised patterns the design follows and which anti-patterns it meets).

## What reversing it would change

`CLAUDE.md`'s section on who owns what would change, and so would design decision 12, the roadmap's item for the pull request that brings the documents to this rule, the anti-pattern on the patterns page that rests on this record, and what that pull request changes.
