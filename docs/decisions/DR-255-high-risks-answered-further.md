# DR-255: Every high or critical risk has a further answer, a high one may be accepted by the owner, and a critical one holds back a release

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-10-29 and 2026-11-18
- **Requirements:** R249, R250, R251
- **Threats:** T207, T208, T209, T210, T211, T212, T213, T214, T215, T216, T220, T221, T222
- **Replaces:** none
- **Closed by:** none

## Context

The owner asked on 2026-10-29 that every high or critical risk be mitigated. Every threat already has an answer, so the rule asks for more than one: a threat whose risk stays high or critical with its answer in place needs a further answer. A further answer may still leave a risk high, such as one that rests on a person's own mistake or on a setting that only the owner keeps, so the rule also says what then follows. The owner chose on 2026-11-18.

## Decision

Every threat whose risk with its answer in place is high or critical carries a further answer, which cites what holds it beyond what its Held by cites, or a backlog item, `Planned` or `In progress`, whose What done looks like names the threat (R249). A further answer that cites a backlog item is a plan, whatever else it names: it does not count toward the rating with the answer in place until it cites what holds it alone, and only then is the threat rated again. Since the item is agreed to what its further answers say, such a further answer changes only with the item. A plan, or a further answer removed, is no reason to lower a high or critical rating (R250). The further answers to the high risks of 2026-11-18 that the specs can hold are written into them by backlog item B-007, which corrects the change's requirements before the build.

A high risk that no answer brings lower may instead carry an acceptance, which cites an open record in which the owner accepts it, gives the reason and lists the threat. A critical risk cannot be accepted: the release check refuses every tag while one stands (R251).

A threat that the base of a pull request rates high or critical is rated lower only with a change to what it says or what answers it, in the same diff (R250).

## Alternatives

- The owner may accept any risk, critical ones among them, in a record with its reason: nothing would hold a release back, and a critical risk could ship with only a record against it.
- No release while any high or critical risk stands, with no acceptance: a high risk that no answer can lower would stop every release for good.

## Consequences

- A test fails on a high or critical threat with neither a further answer nor an acceptance, on a further answer that adds nothing to its Held by or cites an item whose text does not name it, on an acceptance that no open record of the owner's gives for it, on an accepted critical threat, and on hidden text in either line.
- The release check refuses a tag while the tag or the default branch holds a critical risk, and a tag whose changelog entry leaves out a high risk that is accepted or answered further only by a plan (task 6.1).
- While a critical risk stands, no release goes out, not even one that fixes something else (T214); the owner chose that.
- `CLAUDE.md` says that an agent writes an acceptance, or a record that accepts a risk, only when the owner has asked for it in words in its own session.
- The risk register lists each high and critical risk with its further answer or its acceptance (R247).

## Scope

This covers what a high or critical risk needs. The bands are DR-253, the raw rating DR-254, and the register DR-256.

## What reversing it would change

How hard it is to reverse: easy. R249 to R251 and their checks would change, with the line of `CLAUDE.md` on acceptances; the further answers that B-007 builds would stay, as answers of their own.
