# DR-054: Names the price table does not list are recorded as `unknown`

- **Type:** security and privacy
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R17, R77, R98
- **Threats:** T1
- **Replaces:** none
- **Closed by:** none

## Context

Of a transcript's text, an entry keeps only the model's name and the values of the price attributes (DR-045). Those can still be private, since a private gateway, a custom model or an alias can carry a name that looks like one of Anthropic's (T1).

## Decision

The hook records a call's model name, and each of its price attribute values, only when the price table that it ships with, the one at its own commit, lists that name or value. It records anything else as `unknown`.

## Alternatives

None were recorded when this was decided.

## Consequences

- No name of a private gateway, custom model or alias is published, and a name that holds characters such as spaces, brackets or Markdown is recorded as `unknown` too (T1, R77).
- A call recorded as `unknown` is counted in tokens and left out of the cost, and the report says that its model is unknown (R17). A ledger line that names any other value that the price table does not list is refused (R98).
- A hook and a report from one commit share one price table. A model that appears after the hook's commit stays `unknown` until the adopter updates the hook, as the design's risk "[Prices go stale, or a new model appears]" says. A hook older than the report also records as `unknown`, and so leaves out of the cost, a model that only the report's newer table lists, as the design's risk "[An adopter updates the hook and the workflow pin at different times]" says.

## Scope

This covers which transcript values an entry may hold as text. That an entry holds counts and no other content is DR-045 (Ledger entries hold counts, never content), where the price table comes from is DR-020 (Prices come from a dated price table in the repository), and tool names, which are read only to choose an activity type, are DR-029 (Activity types come from tool names, which are never recorded).

## What reversing it would change

R77 in `ledger`, with its scenarios, R17 in `pricing` and R98 in `report-comment` would change, and so would the names that task 1.2's ledger format allows, T1's answer, the design's decision 1 and its risks, the `ledger` feature page and task 2.1, which checks names against the price table. The ledger format is part of the public surface, so the change would be a breaking one for adopters (DR-096).
