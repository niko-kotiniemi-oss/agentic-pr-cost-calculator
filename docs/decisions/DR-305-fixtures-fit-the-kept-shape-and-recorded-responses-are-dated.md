# DR-305: Transcript fixtures fit the kept shape, and recorded responses are dated

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R292
- **Threats:** T310, T311
- **Replaces:** none
- **Closed by:** none

## Context

The tests meet Claude Code's transcripts and GitHub's API only through fixtures and recorded responses (DR-090). The walking skeleton's run kept the shape of a real transcript, with no values (DR-247). The guide names as a gap that B-007 closes that fixtures are not checked against that shape and that a recorded response does not say when it was recorded.

## Decision

Each transcript fixture holds only the fields, paths and types that the kept transcript shape gives for any line, which is one flat list with no kind of line, and under `message.usage` only the fields that `usage-capture` names, but for the paths that it names, each with an existing scenario that it departs for. Each recorded response has a file beside it giving the UTC day on which it was recorded or written, which of the two, and its page, on a host that the test lists, so that the response stays as the service sent it (R292).

## Alternatives

- Fixtures written by hand with no check: a fixture could test a shape that Claude Code never writes.

## Consequences

- A change to the kept shape shows which fixtures no longer fit it.
- A recorded response's day tells a reader how old the behaviour that it holds is.
- The Renovate check's recorded responses get their file in the same change, so the check does not fail on them.
- A day earlier than the true one is not caught, as a fact's is not (T101).

## Scope

This covers the check of fixtures and responses. The kept shape is DR-247 (This repository keeps from the skeleton's run only a transcript's shape with no values, and what was observed).

## What reversing it would change

How hard it is to reverse: reversible. R292 and its scenarios, and the test that holds them, would change. Nothing that adopters configure changes.
