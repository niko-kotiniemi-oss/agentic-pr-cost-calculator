# DR-029: Activity types come from tool names, which are never recorded

- **Type:** technical
- **Boundary:** inside
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-17
- **Requirements:** R4, R6
- **Threats:** T1
- **Replaces:** none
- **Closed by:** none

## Context

The report splits a pull request's token cost by activity type, beside the split by model and by token type (R20), so each recorded call needs one label for its kind of work. The transcript names the tools that each call invoked, but those names cannot reach the ledger, which holds counts and never content (DR-045), and they include the names of MCP servers, which can name a private service (T1). One rule can choose the label from those names alone. The rule is simple enough to test fully and to explain in one line of the report.

## Decision

Each call's activity type comes from the names of the tools it invoked, by a fixed list of types: code generation, file reading, tooling, MCP, subagent, other for a tool the classification does not know, and conversation for a call with no tool call (R6). A call whose tools are of several types takes its first tool call's type. A tool's name is read only to choose the type, and is never recorded.

## Alternatives

None were recorded when this was decided.

## Consequences

- A review cannot be told apart from other work by tool names alone, so review is not a type in `add-pr-cost-calculator`.
- A call that runs a shell command and then edits a file is tooling, so none of its cost counts as code generation.
- The ledger and the report hold only the type, so neither can show which tool, or which MCP server, a call used (T1).

## Scope

This covers how a call's activity type is chosen, and what becomes of the tool names read for it. The cost of AI review by an app or a job in CI is DR-004 (The cost of AI review by an app or a job in CI is left to a later change), and the rest of what an entry may hold is DR-045 (Ledger entries hold counts, never content).

## What reversing it would change

R6 in `activity-types` would change, with its scenarios, and so would the ban on tool names in R4 in `ledger`. So would the design's decision 5, T1's answer, the `activity-types` feature page, the README's list of activities, the statements in the proposal, `SECURITY.md`, `docs/how-it-works.md` and the `ledger` feature page that no tool name is recorded, and tasks 1.1 and 2.5. A change that recorded tool names would change the ledger format, which is part of the public surface, so it would be a breaking one for adopters (DR-096). DR-004, which leaves AI review by an app or a job in CI to a later change, and DR-045 would be revisited.
