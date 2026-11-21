# DR-276: A diagram is Mermaid in the Markdown that shows it, and an image, a PDF or a video needs a record of its own

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-10-27
- **Requirements:** R270
- **Threats:** T253, T254
- **Replaces:** none
- **Closed by:** none

## Context

The owner asked on 2026-10-27 that diagrams be kept as code: a diagram is Mermaid, in the Markdown that shows it, and an image, a PDF or a video comes in only with an exception record of its own, which a test holds. A diagram kept as an image cannot be reviewed in a diff, and an image, a PDF or a video can carry what no check of text reads, such as words that instruct an agent that opens it (T254). GitHub draws a Mermaid block in Markdown as a diagram (A9). On 2026-11-21 the repository tracked no image, PDF or video, and its diagrams were Mermaid: nine in the page on how the tool works and one in the threat model.

## Decision

A diagram is written in Mermaid, in the Markdown page that shows it. A file whose extension is that of an image, a PDF or a video, in any case, and any file whose bytes are not UTF-8, is tracked only where the list of exceptions in `tests/test_conventions.py` gives its path together with an accepted record whose text names that path in a code span, and the list gives no other file. Such a file needs a record of its own.

## Alternatives

- Diagrams as images, drawn with another tool: a change to one cannot be read in a diff, and its source lives elsewhere.
- Another notation that is text, such as PlantUML or Graphviz: the project's diagrams are Mermaid already, and GitHub draws Mermaid without another tool.

## Consequences

- `tests/test_conventions.py` fails on such a file that the list does not give with its record, and on an exception for a path that git does not track, for a file of text, or with a record that is missing, closed or silent on the path, so that the list cannot take a page out of the test of characters (R270; T253, T254; task 1.49).
- Whether a diagram kept as text is Mermaid rather than another notation is for review, as a rule about prose is (DR-251).
- The owner reads a record that lets such a file in together with the file itself, since an image can still carry words that instruct (T254).

## Scope

This covers which files that are not text the repository tracks, and how its diagrams are kept. What the files of text hold is DR-274 (Everything that this repository writes holds printable ASCII) and DR-275 (The files that others write hold only the visible characters that a test lists). Where a diagram is drawn, and what it shows, is backlog item B-006's.

## What reversing it would change

How hard it is to reverse: reversible. The list and its check are part of one test. R270 in `project-standards` would change, with its scenarios, and so would the answers of T253 and T254, design decision 23 and task 1.49. Nothing that adopters configure or depend on changes, so the change would not be a breaking one for adopters.
