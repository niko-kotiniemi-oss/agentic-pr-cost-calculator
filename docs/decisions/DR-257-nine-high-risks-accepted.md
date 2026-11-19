# DR-257: The owner accepts nine high risks that no further answer can lower

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the owner, 2026-11-19
- **Requirements:** R249
- **Threats:** T2, T7, T16, T32, T33, T34, T61, T62, T128
- **Replaces:** none
- **Closed by:** none

## Context

Thirteen threats carry a high risk with their answers in place. Under DR-255 each needs a further answer, or, if nothing can lower it, the owner's acceptance. The reviewers of each threat's trust boundary proposed one for each. For T8, T65, T132 and T137 they found a further answer that the specs can hold, which B-007 builds. For the nine threats that this record lists, they found none: each rests on a person, on a setting that only the owner keeps, on what Claude Code writes, or on a choice that the owner already made. The owner chose on 2026-11-19 to accept all nine.

## Decision

The owner accepts these nine high risks, each for its reason:

- T2, calls made from a session in this repository while it works on another are published here: the owner chose to tell a call's repository by its working directory alone (DR-199), and only the person working can avoid it.
- T7, a call counted from a partial line: in one shape of subagent transcript Claude Code writes no usage at a call's end, and the comment says that the cost is a lower bound.
- T16, a ledger file edited by hand: the ledger is self-reported and nothing that the report trusts signs it, so only a reviewer of the diff sees an edited count; the figure is an estimate, not a bill.
- T32, private data in this public repository: a private name that no pattern knows is seen only by its author or by the owner reading the diff.
- T33, text in the repository steering an agent: no check tells text that instructs from text that describes, so it rests on agents following `CLAUDE.md` and on the owner's merge.
- T34, a session on a contributor's branch: that branch controls the hooks and `CLAUDE.md` that a session on it loads, so it rests on no session ever starting on an outside contributor's branch.
- T61, a bug report that carries private data: an issue is public once it is posted, so it rests on the reporter heeding the form's warning.
- T62, a code-owner rule that invites a bypass: it rests on two settings that only the owner keeps, code-owner review off and no bypass actor on the default branch's ruleset.
- T128, calls made from a folder that holds the repository left out: the owner chose to leave such calls out and flag them with no count (DR-199, DR-200).

Each of the nine cites this record in its Acceptance and its Held by.

## Alternatives

- Accept some and look further for the rest: the reviewers found nothing that a spec or a test could hold for any of them.
- Accept none: the check of R249 would fail on all nine until a further answer exists, which none can have.

## Consequences

- Each of the nine threats carries an acceptance that cites this record, and the check of R249 passes them.
- The changelog entry of each release names each of the nine while it stands (R251).
- A further answer found later for one of them replaces its acceptance, and a record that closes this one restates the acceptances that still hold.

## Scope

This covers the nine high risks of 2026-11-19 that no further answer can lower. What a high or critical risk needs is DR-255.

## What reversing it would change

How hard it is to reverse: easy. A record that closes this one would take back the acceptances, and the check of R249 would fail on each threat until it had a further answer.
