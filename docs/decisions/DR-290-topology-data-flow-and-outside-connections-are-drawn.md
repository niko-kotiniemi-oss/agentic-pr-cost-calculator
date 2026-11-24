# DR-290: Topology, data flow, outside access and each connection to an outside system are drawn

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

Topology, data flow and access from outside are always drawn, and so is each connection to an outside system, with what authenticates and authorizes it: directories, logging and network connections among them.

## Alternatives

None were recorded when this was decided.

## Consequences

- The page on how the tool works draws each connection to an outside system with its credential and what it is allowed, and says that the tool has no directory and no logging service of its own.
- The threat model's diagram of how data moves draws the report's git fetches.

## Scope

This covers where and how a diagram is drawn. That a diagram is Mermaid is DR-276 (A diagram is Mermaid in the Markdown that shows it, and an image, a PDF or a video needs a record of its own), and what a Mermaid block may hold is DR-279 (No page that this repository writes holds text that GitHub hides).

## What reversing it would change

How hard it is to reverse: reversible. R281 and its scenarios, and the diagrams that follow this rule, would change. Nothing that adopters configure or depend on changes, so the change would not be a breaking one for adopters.
