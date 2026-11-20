# DR-032: A call with no stop reason is read from its last line, as a lower bound

- **Type:** technical
- **Boundary:** incoming
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R42, R95
- **Threats:** T7, T8
- **Replaces:** none
- **Closed by:** none

## Context

A transcript does not always give a call's whole usage. In one shape of subagent transcript almost no call has a line that gives a stop reason, and such a call's lines give the usage of its start, with too few output tokens and server-side tool requests (see the design's context; T7). A hook that succeeds shows its standard error to no one (DR-031), so the ledger and the comment are where such gaps can be told.

## Decision

A call none of whose lines gives a stop reason is read from its last line once a later call follows it or its agent has stopped, and the comment then calls the token cost a lower bound. Capture records such a call as far as that line's usage goes and counts it in the ledger, and the comment gives that count, rather than estimating the usage that the line leaves out.

## Alternatives

- Waiting for a line that gives a stop reason, which never comes for such a call, so that the call would be left out (T7).

## Consequences

- The token cost stays short by what such calls' lines leave out, which T7's residual accepts, as the design's risk "[A call read without a stop reason gives the usage of its start, not of its end]" says.
- A call that is not over waits for a later run, so the last call of a subagent that never finishes is never read if it gives no stop reason (T8).

## Scope

This covers a call none of whose lines gives a stop reason. A call whose usage holds a field that capture does not know is DR-135 (A call with an unknown usage field is counted from the fields capture knows), and a cache write whose lifetime the transcript does not give is DR-155 (A cache write of unknown lifetime is priced as a range). It does not cover calls refused for a malformed value or for final lines that disagree, or model calls that Claude Code makes for its own tools without writing them to the transcript.

## What reversing it would change

R42 in `usage-capture` and R95's clause on calls read without a stop reason in `report-comment` would change, with their scenarios, and so would the ledger format, which holds their count. The ledger format is part of the public surface, so the change would be a breaking one for adopters (DR-096). The design's decision 1 and its risk "[A call read without a stop reason gives the usage of its start, not of its end]", the answers and residuals of T7 and T8, the outputs in `docs/how-it-works.md`, the usage-capture and report-comment feature pages, and tasks 1.2, 2.1 and 4.1 would change too, and DR-040 (A newer report reads every earlier ledger format) would be revisited.
