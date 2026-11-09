# DR-193: A test of the repository's own holds the specs' form

- **Type:** process
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-09
- **Requirements:** R173, R174
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

OpenSpec reads a spec line by line: a requirement from each `### Requirement:` heading, its text from the lines before the next heading, and a scenario from each level-4 heading under it. Its validation, which `scripts/verify-openspec.sh` runs with `--strict` on every spec and every change, fails a requirement with no scenario or with no SHALL or MUST, and, in the release that `package-lock.json` pins, 1.14.1, one longer than 500 characters that a change adds or that the main specs hold.

On 2026-11-09, each of these defects, planted in a copy of the specs of `add-pr-cost-calculator` and in a copy of the main specs that archiving it writes, passed that validation in both: a scenario with no WHEN line or no THEN line, with its THEN first, with those words not in bold, or with a line of prose after them; a scenario's heading made plain text or bold, at level five, without `Scenario:` or without a name; and a requirement's heading made plain text or at level four. A scenario's heading at level three passed in the change and failed in the main spec, a requirement longer than 500 characters that a change modifies passed, and a level-1 heading among a main spec's requirements hid every requirement after it from OpenSpec, and passed too. OpenSpec's own instructions for writing a spec say that a scenario at another level than four fails silently. The first check of the privacy revision's fixes found the gap for a scenario's THEN, and the revision's `/verify` review found it for a heading made plain text.

## Decision

`tests/test_spec_form.py` reads every spec in `openspec/specs/` and in each change that is not archived, line by line, as OpenSpec reads it. It fails on a requirement whose text has no SHALL or MUST or is longer than 500 characters, measured as DR-194 says, or that has no scenario; on a scenario other than one `- **WHEN**` line and then one `- **THEN**` line, each followed by any `- **AND**` lines; on a heading other than a title before the first section, a section that OpenSpec reads, and a requirement's or a scenario's heading with a name, in its place; on a scenario's line in a requirement's text, and a line before the first requirement of a section that gives their text; and when it reads no requirement or no scenario. It holds what OpenSpec's validation already fails too, so that the form holds whatever a later release of OpenSpec checks.

## Alternatives

- Relying on OpenSpec's validation, which passes the defects above.
- Adding the checks to `scripts/verify-openspec.sh`, in shell, which would hold them only where the OpenSpec CLI runs, and would make each planted defect harder to test.
- Holding only what OpenSpec's validation passes, which would leave a requirement's SHALL and its length to OpenSpec, whose validator DR-113 recorded as reporting a longer text only as information, and which now fails it.
- Skipping the lines of a fenced code block, as OpenSpec does, which no spec needs, since none holds one: the test reads such a line as it stands, so that it counts toward a requirement's length and fails inside a scenario.
- Allowing a scenario other lines than its WHEN, its THEN and their AND lines, such as GIVEN, which OpenSpec's template does not give and none of the specs uses.

## Consequences

- A spec that OpenSpec would read otherwise than it is written fails CI in the pull request that writes it, not only once its change is archived.
- Each scenario keeps the form that OpenSpec's template gives, so that what reads the scenarios by their headings, as the acceptance tests of task 1.4 and the traceability test of task 1.3 will, reads each of them.
- The test is stricter than OpenSpec where a spec holds a fenced code block, which none does, and where a heading is indented by up to three spaces, which GitHub shows as a heading and OpenSpec does not read.
- What a requirement or a scenario says is still for the reviews: the test reads only its form.

## Scope

This covers the form of each requirement and scenario of the specs. The length of a requirement's text is DR-194 (Each requirement is 500 characters or fewer), that each requirement states one behaviour is DR-105 (Each requirement states one behaviour), and that the register and the feature pages agree with the specs are DR-100 (A register lists every requirement with its kind) and DR-101 (Each feature has a page).

## What reversing it would change

R173 and R174 in `project-standards` would change, with their scenarios, and so would the design's decision 12, task 1.23, `tests/test_spec_form.py`, the `project-standards` feature page, the proposal's lines on `project-standards` and A32. The defects above would again be left to OpenSpec's validation and to review.
