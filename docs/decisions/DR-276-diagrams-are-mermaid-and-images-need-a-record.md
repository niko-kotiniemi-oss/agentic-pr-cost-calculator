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

The owner asked on 2026-10-27 that diagrams be kept as code: a diagram is Mermaid, in the Markdown that shows it, and an image, a PDF or a video comes in only with an exception record of its own, which a test holds. A diagram kept as an image cannot be reviewed in a diff, and an image, a PDF or a video can carry what no check of text reads, such as words that instruct an agent that opens it (T254). GitHub draws a Mermaid block in Markdown as a diagram (A9). On 2026-11-21 the repository tracked no image, PDF or video, and its diagrams were Mermaid: nine in the page on how the tool works and one in the threat model. The design-stage review of this change found that an exception that gives a path alone holds for whatever bytes that path holds later, so that an accepted image could be replaced with no new record, and that an exception for any file whose bytes are not UTF-8, or for an SVG, which is text, would take a page of text out of the test of characters.

## Decision

A diagram is written in Mermaid, in the Markdown page that shows it. A file whose extension is that of an image, a PDF or a video, in any case, is tracked only where the list of exceptions in `tests/test_conventions.py` gives its path and its git object id together with an accepted record whose text names that path in a code span, and the list gives no other file. Such a file needs a record of its own, and each new version of it a changed entry. The test of characters still reads a listed file whose bytes are UTF-8, such as an SVG, and any other file whose bytes are not UTF-8 is not tracked.

## Alternatives

- Diagrams as images, drawn with another tool: a change to one cannot be read in a diff, and its source lives elsewhere.
- Another notation that is text, such as PlantUML or Graphviz: the project's diagrams are Mermaid already, and GitHub draws Mermaid without another tool.
- An exception that gives the path alone: a later pull request could replace an accepted image at that path with one that carries other words, with no new record and nothing in the test's diff (T254).
- An exception for any file whose bytes are not UTF-8: a script or a page written in another encoding could be listed, and leave the test of characters (T253).

## Consequences

- `tests/test_conventions.py` fails on such a file that the list does not give with its object id and its record, on a listed file whose object id is not the one that its entry gives, and on an exception for a path that git does not track, for a file that is not an image, a PDF or a video by its extension, without an object id, or with a record that is missing, closed or silent on the path, so that the list cannot take a page out of the test of characters (R270; T253, T254; task 1.49).
- Whether a diagram kept as text is Mermaid rather than another notation is for review, as a rule about prose is (DR-251).
- The owner reads a record that lets such a file in together with the file itself, and each new version of it with its changed entry, since an image can still carry words that instruct and a PDF text that its pages do not show (T254).

## Scope

This covers which files that are not text the repository tracks, and how its diagrams are kept. What the files of text hold is DR-274 (Everything that this repository writes holds printable ASCII) and DR-275 (The files that others write hold only the visible characters that a test lists), and what a Mermaid block may hold is DR-279 (No page that this repository writes holds text that GitHub hides). Where a diagram is drawn, and what it shows, is backlog item B-006's.

## What reversing it would change

How hard it is to reverse: reversible. The list and its check are part of one test. R270 in `project-standards` would change, with its scenarios, and so would the answers of T253 and T254, design decision 23 and task 1.49. Nothing that adopters configure or depend on changes, so the change would not be a breaking one for adopters.
