# DR-230: Each record says how hard it is to reverse, and replacing one starts an assessment of what rests on it

- **Type:** process
- **Status:** accepted
- **Decided by:** the owner, 2026-11-13
- **Requirements:** none
- **Threats:** T74, T168
- **Replaces:** none
- **Closed by:** none

## Context

Each record holds one choice (DR-108), and a record that the default branch holds changes only by being closed, as a whole, by a record that replaces it and restates whatever still holds (DR-121). A record that held two topics could not be changed for one of them without closing all of it and restating the other, which splits one topic between a closed record and an active one. Each record's last section says what reversing it would change, but none says how hard reversing it would be, so a reader cannot tell how much care a decision needed or what changing it would cost. On 2026-11-13 the owner asked that each record cover one topic only, so that changes are whole and made by superseding, and that each say whether it is a one-way door, expensive to change, or a reversible decision, whose replacement starts an assessment of the decisions that rest on it. The terms follow the one-way and two-way doors of Jeff Bezos's letters to Amazon's shareholders for 2015 and 2016.

## Decision

Each record says how hard it is to reverse, as reversible, reversible with work, or a one-way door, irreversible or nearly so, with the reason. A one-way door has its alternatives weighed and the owner's decision before it is accepted. A record that replaces another starts an assessment of what rests on the one it closes: each requirement, record and threat that the closed record's last section names, and each page that names it, is read again, and each record that no longer holds is closed in the same change; a backlog item, which names the record in Rests on, is kept for a record whose standing the assessment cannot settle. Until records gain a field for it, which backlog item B-004 (Two new fields on every record) brings, with a column in the index and its check, a record says how hard it is to reverse in the first sentence of its section on what reversing it would change, as the records from DR-225 on do.

## Alternatives

- The field and its check in this change: it would change the form of every record, which DR-121 allows only by closing each, and the backlog item that adds two fields to every record already plans the narrow rule that lets one change do it.
- No statement of how hard a record is to reverse: a reader cannot tell a choice that is cheap to change from one that is not.
- An assessment only when a test flags a page that names the closed record: the records that rest on it by their reasons, not by naming it, would be missed.

## Consequences

- A record that closes another names, in its consequences, the records it assessed and what became of each, and the review checks that the assessment was done (T168). Whether a record holds one topic rests on review, as DR-108 has it.
- `tests/test_decisions.py` already fails when a page other than the history still names a closed record, which flags the pages that the assessment reads (R127; T74).
- No test holds the statement of how hard a record is to reverse until the field arrives; until then it rests on review (A15).

## Scope

This covers how a record is reversed: what it says about reversing it, and what replacing it starts. That each record covers one topic is DR-108's rule that a record holds one choice, which this record cites and does not decide again. A record's form is DR-108 (Each decision has a record of its own, in an index), and how a record is closed is DR-121 (A record is never edited once accepted, only closed by a record that replaces it).

## What reversing it would change

How hard it is to reverse: reversible. The statement is a sentence in each record, and a later record could drop the rule, leaving those sentences as history. Design decision 13 would change, and so would the answers of T74 and T168, B-004, and the guide's entry on decisions once it exists.
