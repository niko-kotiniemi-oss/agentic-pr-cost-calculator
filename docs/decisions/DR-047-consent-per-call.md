# DR-047: Consent holds for each recorded call

- **Type:** security and privacy
- **Status:** closed
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R40, R107, R108, R109, R118
- **Threats:** T38, T46
- **Replaces:** none
- **Closed by:** DR-168

## Context

A person's usage is published only with their consent (DR-046), which the design's goals ask to hold for each call. Each run reads a transcript on from where the last stopped, and one that finds a switch off records nothing, so calls made while capture was off would be read by the next run that finds both on. Recorded calls can also still wait for a commit when the person turns capture off (T38).

## Decision

Consent holds for each call, not only for the run that records it. Capture records only the calls made inside one of their session's intervals when both switches were on, each of which begins at the session's start or at a run and ends at a run. A run that finds the person's capture off ends every session's interval and withholds the calls made before it.

## Alternatives

None were recorded when this was decided.

## Consequences

- Every run notes what it found, so a run with a switch off still writes the store, creating it where there is none, even for someone who never opted in, and starts git to do so; nothing in it leaves the git directory (the residuals of T38 and T46).
- Runs, not the moments a setting changed, bound the intervals, so the design's risk "[A person turns capture on during a session, before the step's first run in it]" accepts that such a person's calls from before the opt-in are recorded too.
- An opt-out withholds only what no commit has taken yet.

## Scope

This covers which calls the switches let through. The switches are DR-021 (One file, `.pr-cost.json`, turns the tool on or off) and DR-046 (Each person turns on capture of their own sessions), and take-backs, which run whatever the switches say (R110), are DR-014 (A ledger file that no commit took is taken back).

## What reversing it would change

R40, R107, R108 and R109 in `switch-and-opt-in` would change, with their scenarios, and so would R118 in `usage-capture` where a run with a switch off starts git. So would the design's decision 6 and its risk on opting in during a session, T38's answer and residual, T46's residual, the `switch-and-opt-in` feature page, the capture flow and the list of what the tool never does in `docs/how-it-works.md`, and tasks 1.1 and 2.4. The notes are in the store, whose format is part of the public surface, so the change would be a breaking one for adopters (DR-096).
