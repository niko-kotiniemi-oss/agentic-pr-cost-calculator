# DR-178: Capture keeps no transcript, and reprocessing transcripts is a change of its own

- **Type:** scope
- **Status:** accepted
- **Decided by:** the owner, 2026-11-02
- **Requirements:** R154
- **Threats:** T107
- **Replaces:** none
- **Closed by:** none

## Context

A pull request's cost is recomputed from its ledger files, the price table and GitHub's jobs API (see the design's decision 3), so a historical estimate can be reproduced from what the repository and GitHub hold, as the golden set checks (see the design's decision 14). A transcript holds everything the session saw: prompts, code, tool output, web pages and possibly secrets (T1, T107).

## Decision

The owner decided on 2026-11-02 that recomputing a pull request's cost from its ledger is kept apart from reprocessing the sessions' transcripts, that this change needs only the former, and that the tool keeps no copy of a transcript. A capability that keeps transcripts as evidence, or reprocesses them, would need a change of its own, with its own specification, its own threat review and the owner's explicit authorization.

## Alternatives

- Keeping each session's transcript, or the lines of its calls, so that a figure could be recomputed from them later, which would keep on the person's machine, or publish, everything the session saw.

## Consequences

- A figure is reproduced only from what the ledger files hold, so a call that capture left out, or counted wrongly, cannot be recovered later from its transcript.
- The capture step writes no line of a transcript, and no value from one beyond what an entry or the store's notes name, to any file or to standard error (R154).

## Scope

This covers whether the tool keeps or reprocesses transcripts. What the store keeps is DR-173, and what a ledger entry holds is DR-045 (Ledger entries hold counts, never content).

## What reversing it would change

R154 in `usage-capture` would change, with its scenario, and so would the design's non-goals and decision 15, T107 and task 2.1, and a change of its own would add the specification and the threat review that keeping transcripts needs. The ledger's and the store's formats would not change, so the change would not be a breaking one for adopters.
