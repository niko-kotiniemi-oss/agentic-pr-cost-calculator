# DR-135: A call with an unknown usage field is counted from the fields capture knows

- **Type:** technical
- **Boundary:** incoming
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R43, R95
- **Threats:** T39
- **Replaces:** none
- **Closed by:** none

## Context

Claude Code can add a field to a call's usage, at its top level or in a block nested in it, before capture knows the field, and the new field may carry a charge, such as a new server tool's request count or a new cache tier (T39). Adopters copy the hook file, so the copy they run can meet a field that no fixture of its release held (DR-022). A hook that succeeds shows no one its standard error (DR-031), so only the ledger and the comment can show that such a field was met.

## Decision

Capture records a call whose usage holds a field that it does not know from the fields that it knows, as far as they go, and counts the call in the ledger without naming the new field. The comment gives that count and, when there are any such calls, says that the token cost may be low, rather than estimating what the new field would add.

## Alternatives

- Refusing a call whose usage holds a field that the script does not know, which would refuse every call once Claude Code adds a field (T39).
- Keeping only the fields that the script knows without counting the call, which would drop a field that carries a charge without saying so (T39).

## Consequences

- While capture does not know a field, a charge that the field carries is left out of the cost, though the fields that capture knows still price the call, as the design's risk "[Claude Code changes its transcript format]" says.
- Neither the field's name nor its value reaches the ledger, which holds counts and never content (DR-045).

## Scope

This covers a call whose usage holds a field that capture does not know. A call none of whose lines gives a stop reason is DR-032 (A call with no stop reason is read from its last line, as a lower bound), and a cache write whose lifetime the transcript does not give is DR-155 (A cache write of unknown lifetime is priced as a range). Calls refused for a malformed value, or for final lines that disagree, are outside it.

## What reversing it would change

R43 in `usage-capture` and R95's clause on such calls in `report-comment` would change, with their scenarios, and so would the ledger format, which holds their count. The ledger format is part of the public surface, so the change would be a breaking one for adopters (DR-096). The design's decision 1 and its risk "[Claude Code changes its transcript format]", T39's answer, the outputs in `docs/how-it-works.md`, the usage-capture and report-comment feature pages, and tasks 1.1, 1.2, 2.1 and 4.1 would change too, and DR-040 (A newer report reads every earlier ledger format) would be revisited.
