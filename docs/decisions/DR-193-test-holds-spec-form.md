# DR-193: A test of the repository's own holds the specs' form

- **Type:** process
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-09
- **Requirements:** R173, R174, R175, R177
- **Threats:** T124, T126
- **Replaces:** none
- **Closed by:** none

## Context

OpenSpec reads a spec line by line: a requirement from each `### Requirement:` heading, its text from the lines before the next heading, and a scenario from each level-4 heading under it. Its validation, which `scripts/verify-openspec.sh` runs with `--strict` on every spec and every change, fails a requirement with no scenario or with no SHALL or MUST, and, in the release that `package-lock.json` pins, 1.14.1, one longer than 500 characters that a change adds or that the main specs hold.

On 2026-11-09, each of these defects, planted in a copy of the specs of `add-pr-cost-calculator` and in a copy of the main specs that archiving it writes, passed that validation in both: a scenario with no WHEN line or no THEN line, with its THEN first, with those words not in bold, or with a line of prose after them; a scenario's heading made plain text or bold, at level five, without `Scenario:` or without a name; and a requirement's heading made plain text or at level four. A scenario's heading at level three passed in the change and failed in the main spec, a requirement longer than 500 characters that a change modifies passed, and a level-1 heading among a main spec's requirements hid every requirement after it from OpenSpec, and passed too. OpenSpec's own instructions for writing a spec say that a scenario at another level than four fails silently. The first check of the privacy revision's fixes found the gap for a scenario's THEN, and the revision's `/verify` review found it for a heading made plain text.

The review of this design at Boundary 7 found more. OpenSpec skips every line from one that starts, after any spaces, with three backticks or tildes to the line that closes it, so two such lines, each inside an HTML comment that GitHub hides, took three of the 33 requirements of `project-standards` out of OpenSpec's reading while its validation passed and the spec showed no change. When it splits a spec to archive a change, OpenSpec takes `###Requirement:`, with no space, for a requirement's heading, which GitHub shows as text. It leaves out of a requirement's text a line that starts with a bold label and a colon, when other lines remain. And it reads a `spec.md` at any depth below the specs' folders, where some of this repository's other readers of the specs look one folder down.

The security review of the build found that GitHub shows a heading or a fence written after a list's or a quote's marker inside the list item or the quote, where OpenSpec, which takes headings and fences from the start of a line alone, reads text, and that GitHub shows text before a spec's first section, which OpenSpec does not read. So a requirement and its scenario can show on GitHub where OpenSpec reads no requirement. No spec held either form, and refusing both limits no one who uses the tool, as with the dollar sign and the tilde of DR-195.

## Decision

`tests/test_spec_form.py` reads as specs every `spec.md` that OpenSpec reads, in a folder at any depth below `openspec/specs/` and below the `specs/` folder of each change that is not archived, line by line, as OpenSpec reads it, ending lines at line feeds alone. It fails on a requirement whose text has no SHALL or MUST, is longer than 500 characters, measured as DR-194 says, or holds a line that starts with a bold label and a colon, or that has no scenario; on a scenario other than one `- **WHEN**` line and then one `- **THEN**` line, each followed by any `- **AND**` lines, or with the name of another scenario in its spec; on text other than a title before the first section; on a heading other than that title, a section that OpenSpec reads, spelled as its template spells it, and a requirement's or a scenario's heading with a name, in its place, on a main spec's title that OpenSpec reads as its Requirements section, on any other line that, after any spaces, tabs or list or quote markers, starts with `#` or with three backticks or tildes, and on a line of `=` or `-` signs after any such markers, with which GitHub makes the line above it a heading; on a scenario's line in a requirement's text, and a line before the first requirement of a section that gives their text; on a `spec.md` elsewhere in `openspec/` but the archive, and on a symbolic link, which it never follows; and when it reads no requirement or no scenario. It holds three checks that OpenSpec's validation makes too, a requirement's SHALL or MUST, its length and its scenario, so that these hold whatever a later release of OpenSpec checks, and leaves two others to that validation: a requirement whose name another requirement of its spec, or of its section of a change, already has, and a main spec with no Purpose or an empty one. It reports each problem only in a test's failure message.

## Alternatives

- Relying on OpenSpec's validation, which passes the defects above.
- Adding the checks to `scripts/verify-openspec.sh`, in shell, which would hold them only where the OpenSpec CLI runs, and would make each planted defect harder to test.
- Holding only what OpenSpec's validation passes, which would leave a requirement's SHALL and its length to OpenSpec, whose validator DR-113 recorded as reporting a longer text only as information, and which now fails it.
- Skipping a fence's lines, as OpenSpec does, or reading them as they stand, as the first draft of this record chose: either passes two fence lines that hide requirements from OpenSpec while GitHub shows them, as the design review found. No spec holds a fence, so failing each such line asks no spec to change.
- Allowing a scenario other lines than its WHEN, its THEN and their AND lines, such as GIVEN, which OpenSpec's template does not give and none of the specs uses.
- Reading only the specs one folder below each specs' folder, as some of the repository's other readers of the specs do, which would leave a deeper spec, which OpenSpec validates and archives, unread by every check of form.
- Allowing two scenarios in a spec to have one name, as OpenSpec does, which would let whatever reads scenarios by name, such as the traceability test of task 1.3, take one for the other.
- Holding in the test too the two checks that it leaves to OpenSpec's validation, a requirement's name that another requirement of its spec or section already has and a main spec's Purpose, which would widen what R173 to R175 hold after the owner approved them.

## Consequences

- A spec that OpenSpec would read otherwise than it is written fails CI in the pull request that writes it, not only once its change is archived.
- Each scenario keeps the form that OpenSpec's template gives, with a name of its own in its spec, so that what reads the scenarios by their headings, as the acceptance tests of task 1.4 and the traceability test of task 1.3 will, reads each of them.
- The test is stricter than OpenSpec where a heading is indented by up to three spaces, which GitHub shows as a heading and OpenSpec does not read, where a heading's keyword or a section's name is in another case, which OpenSpec accepts, and where a spec holds a fence, a label line, a line of `=` or `-` signs or another line that starts with `#`. No spec holds any of them, and an example that needs a fenced block goes in the change's design.
- The test models how OpenSpec reads a spec, so a release of OpenSpec that reads specs otherwise could pass what it should fail, which DR-196 answers.
- What a requirement or a scenario says is still for the reviews: the test reads only its form.

## Scope

This covers the form of each requirement and scenario of the specs, and which files are read as specs. The length of a requirement's text is DR-194 (Each requirement is 500 characters or fewer), the plain text that the specs hold is DR-195 (The specs hold only text that GitHub shows as it is), the comparison of the test's reading with OpenSpec's is DR-196 (CI compares the test's reading of the specs with OpenSpec's), that each requirement states one behaviour is DR-105 (Each requirement states one behaviour), and that the register and the feature pages agree with the specs are DR-100 (A register lists every requirement with its kind) and DR-101 (Each feature has a page).

## What reversing it would change

R173, R174, R175 and R177 in `project-standards` would change, with their scenarios, and so would the design's decision 12, task 1.23, `tests/test_spec_form.py`, the `project-standards` feature page, the proposal's lines on `project-standards`, T124, T126 and A32. The defects above would again be left to OpenSpec's validation and to review, and DR-196 would have no reading of the specs to compare with OpenSpec's.
