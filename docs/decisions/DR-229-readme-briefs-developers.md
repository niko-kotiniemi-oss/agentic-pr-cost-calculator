# DR-229: The README's section on working here opens with a briefing for developers

- **Type:** process
- **Status:** accepted
- **Decided by:** the owner, 2026-11-13
- **Requirements:** R212
- **Threats:** T161, T166
- **Replaces:** none
- **Closed by:** none

## Context

Most people who come to the repository read only its README. How work flows here, from a proposal to an agreed item, its order and its delivery, is spread over `CONTRIBUTING.md`, the roadmap, the backlog's page and the records, which few will open. A contributor who does not know that an issue is open to anyone and commits no one to anything may read an open issue as a promise, or wait for an approval that an issue does not need. On 2026-11-13 the owner asked that the README's section on working on this repository open with a short briefing for developers, like an executive summary, and that it carry the table of stages from the assessment that the owner agreed to that day.

## Decision

The README's section on working on this repository opens, before its setup, with a briefing for developers. It says that anyone may open an issue to propose, ask or report, with no approval needed, and that what an issue proposes is neither planned nor committed to; that planned work is a backlog item, which changes only through a pull request that the owner merges; and it gives the stages of the work as a table, with the steps An idea or a bug, Agreed work, Order, Delivery and Result, each with where it lives, what it holds and who writes it, linking the page that goes deeper. The README is the table's one home: `CONTRIBUTING.md` and the backlog's page link the section rather than repeat it. The briefing names issues without linking any, as DR-215 has the README do.

## Alternatives

- The briefing in `CONTRIBUTING.md` alone, which GitHub links from its pages for new issues and pull requests: most readers never open it.
- The table repeated in `CONTRIBUTING.md` and the backlog's page: three copies of one table drift apart, with nothing to check them.

## Consequences

- A test fails when the briefing is missing or follows the setup, leaves out what it must say, its table lacks a column or a row or gives them out of order, a row links no page, another Markdown file gives the table, or `CONTRIBUTING.md` or the backlog's page does not link the section (R212).
- A contributor reads, on the page that most people see, that an issue is not a commitment and that an item is agreed only by a merged pull request (T161, T166).
- The README's other rules hold for the briefing: it links no issue and nothing outside this repository but what its test lists (R201), and holds no text that GitHub hides (R203).

## Scope

This covers the briefing for developers and the home of the table of stages. Where planned work is kept is DR-225 (Planned work is kept as backlog items, and the roadmap is their index), and its statuses are DR-226 (Each backlog item has one of five statuses, and only a merged pull request makes it planned).

## What reversing it would change

How hard it is to reverse: reversible. The briefing is text in the README, which one pull request can move. R212 in `project-standards` would change, with its scenarios, and so would design decision 12, task 1.27, the README, `CONTRIBUTING.md`, the backlog's page and the answers of T161 and T166.
