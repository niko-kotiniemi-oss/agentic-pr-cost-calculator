# DR-289: A diagram goes wherever it speeds up understanding and no diagram covers it yet

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-10-27
- **Requirements:** R281
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

The owner gave five rules for diagrams on 2026-10-27, to be kept as one record each so that each can be replaced on its own (the owner, 2026-11-23). Until this change the page on how the tool works held nine diagrams and the threat model one, and the README and the feature pages held none. How a diagram is written, in Mermaid in the Markdown that shows it, is DR-276.

## Decision

A diagram is added wherever it speeds up understanding and no diagram on the same page or another covers it yet, so that each page draws what it alone explains and links to what another page draws.

## Alternatives

None were recorded when this was decided.

## Consequences

- Each feature page draws what no other diagram draws, mostly its decision points, and the README links to the overview on the page on how the tool works rather than holding a diagram of its own (the owner, 2026-11-23).
- Whether a diagram speeds up understanding is left to review, as a rule about prose is (DR-251).

## Scope

This covers where and how a diagram is drawn. That a diagram is Mermaid is DR-276 (A diagram is Mermaid in the Markdown that shows it, and an image, a PDF or a video needs a record of its own), and what a Mermaid block may hold is DR-279 (No page that this repository writes holds text that GitHub hides).

## What reversing it would change

How hard it is to reverse: reversible. R281 and its scenarios, and the diagrams that follow this rule, would change. Nothing that adopters configure or depend on changes, so the change would not be a breaking one for adopters.
