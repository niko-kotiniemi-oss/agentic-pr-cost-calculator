# DR-279: No page that this repository writes holds text that GitHub hides

- **Type:** security and privacy
- **Boundary:** outgoing
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R273
- **Threats:** T257
- **Replaces:** none
- **Closed by:** none

## Context

The threat review at implementation of pull request 29 found that a link from the roadmap or a backlog item can lead to any tracked file, which no check of hidden text read, so that a linked page could hold text that GitHub hides, and backlog item B-005 took that point. Seven requirements held single pages to the text that GitHub shows as it is (R128, R176, R200, R210, R221, R246, R255). The design-stage review of this change found that characters alone do not answer the point: an HTML comment, a character reference, a link or footnote definition, an image or a mathematical expression is written in printable ASCII, and GitHub hides it or shows something else in its place, so that a check that matches a page's source, such as the changelog's or the table of permissions', can pass text that the page's readers never see, while an agent that reads the raw file reads it (T257). GitHub hides an HTML comment, and draws a Mermaid block and a mathematical expression (A9). On 2026-11-21 only the two templates under `.github/` held such text: HTML comments, on three lines, which guide whoever fills the template in.

## Decision

Every Markdown file that this repository writes holds, outside inline code and fenced blocks, no HTML comment or other raw HTML, no character reference, no link or footnote definition, no image, no dollar sign and no table row with more cells than its header, and holds no fenced block that GitHub draws but Mermaid, whose blocks hold no entity code and no comment. A template under `.github/` may hold HTML comments, and the README the `<details>` and `<summary>` elements with which it folds its sections of detail, as R200 gives them, since a reader opens each to read its text. The seven checks of single pages keep their stricter rules.

## Alternatives

- Holding only the pages that adopters read, by name, as the review proposed: a new page, or one that a link leads to, would be left out, while on 2026-11-21 the rule cost nothing on any page.
- Characters alone, as B-005's postponed point first proposed: an HTML comment and a character reference are printable ASCII (T257).
- Refusing every mark that the checks of single pages refuse, the backslash, the vertical bar and the tilde among them: those show as written, strike text through or draw a table, and hide no text, while many pages use them.

## Consequences

- `tests/test_conventions.py` fails on such text, naming the file, the line and what it holds, and reads code as `scripts/wording.py` reads it (R273; T257; task 1.50).
- A section that a page other than the README would fold, or a price written with a dollar sign, is written in code or left out, a trade-off that the design's risks give.
- A Mermaid drawing keeps its labels in plain text.

## Scope

This covers the text that GitHub hides or redraws in a page that this repository writes. Its characters are DR-274 (Everything that this repository writes holds printable ASCII), and how a diagram is kept is DR-276 (A diagram is Mermaid in the Markdown that shows it, and an image, a PDF or a video needs a record of its own). What a record holds is DR-152 (A record is plain text and links only to other records), and how the README folds its detail is DR-213 (The README keeps its detail, folded below its short start).

## What reversing it would change

How hard it is to reverse: reversible. The check is part of one test. R273 in `project-standards` would change, with its scenarios, and so would the answer of T257, design decision 23, task 1.50, `docs/conventions.md` and the `project-standards` feature page. Nothing that adopters configure or depend on changes, so the change would not be a breaking one for adopters.
