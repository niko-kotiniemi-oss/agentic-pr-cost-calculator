# DR-266: The owner accepts the high risk that another repository's context files steer work here

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the owner, 2026-11-19
- **Requirements:** R249
- **Threats:** T232
- **Replaces:** none
- **Closed by:** none

## Context

The threat review of trust boundary 9, run against what was built for B-003, rated T232's impact at 3: in a project's cloud thread, another repository's rules or skills, applied to work on this repository, can put here a step that the root forbids, such as a session's link in a commit, and a command that the root names can run another skill of that name, since Claude cannot start Claude Code's own `/verify` itself (A5). At impact 3 its risk with the answer in place is 6, which is high, so DR-255 asks for a further answer or the owner's acceptance. The further answer that the review proposed is a project that holds this repository alone, which task 7.1 needs anyway (DR-207). Three options were put to the owner: accept it as a high risk, give this repository a project of its own as a further answer, or keep it at medium. The owner chose on 2026-11-19 to accept it.

## Decision

The owner accepts T232's high risk. It rests on a choice that the owner made: to keep this repository's threads, until task 7.1, in a project that holds another repository too. Until then, the owner's sessions here start with another repository's context files and skills beside these, and the risk rests on agents following the root, which names what steers work here and says that another repository's files and skills describe (DR-258, A16).

T232 cites this record in its Acceptance and its Held by.

## Alternatives

- A project that holds this repository alone, now: the further answer that the review proposed, which would lower the likelihood. The owner did not choose it.
- Keep T232 at medium: the review rated its impact from T232's own case, a step that the root forbids reaching a commit or a comment here, so a rating at impact 2 would understate it.

## Consequences

- T232 is rated at impact 3, likelihood 2 and risk 6, raw 3, 3 and 9, and carries an acceptance that cites this record, so the check of R249 passes it.
- The changelog entry of each release names T232 while this acceptance stands (R251).
- A project that holds this repository alone, which task 7.1 needs, is the further answer that a record closing this one could give T232.

## Scope

This covers T232 alone. The nine high risks of DR-257 stay as that record gives them, and what a high or critical risk needs is DR-255.

## What reversing it would change

How hard it is to reverse: easy. A record that closes this one would take back the acceptance, and the check of R249 would fail on T232 until it had a further answer.
