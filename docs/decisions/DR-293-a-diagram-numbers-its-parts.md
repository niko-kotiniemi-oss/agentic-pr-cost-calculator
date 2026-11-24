# DR-293: A diagram's parts have short names and numbers, explained below it

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-10-27
- **Requirements:** R281
- **Threats:** T283, T286, T289
- **Replaces:** none
- **Closed by:** none

## Context

The owner gave five rules for diagrams on 2026-10-27, to be kept as one record each so that each can be replaced on its own (the owner, 2026-11-23). Until this change the page on how the tool works held nine diagrams and the threat model one, and the README and the feature pages held none. How a diagram is written, in Mermaid in the Markdown that shows it, is DR-276.

## Decision

A diagram's parts have short names and numbers, each in a label in double quotes that opens with its number and `)`, such as `A["1) Capture step"]`, and a list right after the diagram explains each number once, citing the requirement that states what the part does where one does. Each node and participant has an identifier of at most three letters or digits, so that nearly all of a diagram's text is text that GitHub shows.

## Alternatives

None were recorded when this was decided.

## Consequences

- A test fails on a number that a diagram carries and the list does not explain, on one explained and not drawn, on a diagram that numbers nothing, on a number outside a quoted label and on a longer identifier (R281; T283, T286, T289).
- Whether GitHub draws each diagram is checked by looking at it on GitHub at the build (T286).
- Each part cites its requirement, so that review can compare what a diagram draws with what the specs hold (DR-232).

## Scope

This covers where and how a diagram is drawn. That a diagram is Mermaid is DR-276 (A diagram is Mermaid in the Markdown that shows it, and an image, a PDF or a video needs a record of its own), and what a Mermaid block may hold is DR-279 (No page that this repository writes holds text that GitHub hides).

## What reversing it would change

How hard it is to reverse: reversible. R281 and its scenarios, and the diagrams that follow this rule, would change. Nothing that adopters configure or depend on changes, so the change would not be a breaking one for adopters.
