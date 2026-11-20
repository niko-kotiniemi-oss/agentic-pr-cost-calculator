# DR-138: An entry records whether the main agent or a subagent made its call

- **Type:** technical
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R2, R75
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

Claude Code writes a subagent's calls to a transcript of the subagent's own, in a `subagents/` folder under the session's, and capture reads them there as well as in the session's own transcript (R75; see the design's context and its decision 1). Capture therefore knows, for each call that it records, which of the two kinds of transcript the call came from. An entry holds counts, never content (DR-045), and no session value (DR-053). When this was decided, no reason for noting which agent made a call was recorded.

## Decision

Each ledger entry records whether the main agent or a subagent made its call. A call that capture reads from a subagent's own transcript is marked as a subagent's.

## Alternatives

None were recorded when this was decided.

## Consequences

- Every entry carries the field, so the ledger format that task 1.2 documents includes it, and `SECURITY.md`, `docs/how-it-works.md` and the `usage-capture` feature page list it among what the tool records.
- The field says only which of the two made the call, as R2 words it, and takes no text from the transcript, which R4 allows only for the model's name and the price attributes' values.
- The comment gives the cost by model, by token type and by activity type (R20), not by agent, so no figure in it depends on the field.

## Scope

This covers whether an entry says which agent made its call. That an entry holds no session value is DR-053 (An entry records no session value), and the rest of what it holds is DR-045 (Ledger entries hold counts, never content). The activity type named subagent, which a call gets when its first tool call starts a subagent, is DR-029 (Activity types come from tool names, which are never recorded).

## What reversing it would change

R2 in `usage-capture` would change where it lists the field, with its scenario "An entry records that the main agent made its call", and so would R75's scenario "Subagent calls are included", which has a subagent's calls marked as a subagent's. So would the ledger format that task 1.2 documents, the design's decision 1 where it lists what an entry records, `docs/how-it-works.md`, the `usage-capture` feature page and `SECURITY.md`. The ledger format is part of the public surface (DR-154), so the change would be a breaking one for adopters (DR-096), and a newer report would go on reading the earlier format (DR-040).
