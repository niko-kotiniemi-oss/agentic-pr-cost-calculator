# DR-255: Every high or critical risk has a further answer, a high one may be accepted by the owner, and a critical one holds back a release

- **Type:** process
- **Status:** accepted
- **Decided by:** the owner, 2026-10-29 and 2026-11-18
- **Requirements:** R248
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

The owner asked on 2026-10-29 that every high or critical risk be mitigated. Every threat already has an answer, so the rule asks for more than one: a threat whose risk stays high or critical with its answer in place needs a further answer. A further answer may still leave a risk high, such as one that rests on a person's own mistake, so the rule also says what then follows. The owner chose on 2026-11-18.

## Decision

Every threat whose risk with its answer in place is high or critical carries a further answer, which cites what holds it, as Held by does, or the backlog item that is to build it (R248). The further answers to the high risks of 2026-11-18 are built by backlog item B-007, which corrects the change's requirements before the build, after which each threat is rated again with its further answer in place.

A high risk that no answer brings lower may instead carry an acceptance, which cites a decision record in which the owner accepts it and gives the reason. A critical risk cannot be accepted: it holds back every release while it stands.

## Alternatives

- The owner may accept any risk, critical ones among them, in a record with its reason: nothing would hold a release back, and a critical risk could ship with only a record against it.
- No release while any high or critical risk stands, with no acceptance: a high risk that no answer can lower, such as one that rests on a person's own mistake, would stop every release for good.

## Consequences

- A test fails on a high or critical threat with neither a further answer nor an acceptance, on one whose further answer or acceptance cites nothing that holds, and on an accepted critical threat.
- The release workflow refuses a tag whose threat model holds a critical risk (task 6.3).
- The risk register lists each high and critical risk with its further answer or its acceptance (R246).

## Scope

This covers what a high or critical risk needs. The bands are DR-253, the raw rating DR-254, and the register DR-256.

## What reversing it would change

How hard it is to reverse: easy. R248 and its checks would change, and the release workflow's refusal of a critical risk with them; the further answers that B-007 builds would stay, as answers of their own.
