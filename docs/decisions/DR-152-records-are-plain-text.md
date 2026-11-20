# DR-152: A record is plain text and links only to other records

- **Type:** security and privacy
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R128
- **Threats:** T73, T75, T79
- **Replaces:** none
- **Closed by:** none

## Context

Agents build to accepted records, and a record that the default branch holds can never be corrected, only closed (DR-121). GitHub hides an HTML comment when it shows a file, and characters that a reader cannot see can make one text read two ways, so a reviewer and an agent could read different records (T73). The first check refused hidden characters by their Unicode category, and a review of the records found text that a reader can neither see nor follow that it let through (T79).

## Decision

A record and the index hold printable ASCII characters and line breaks, and nothing else. They hold no ampersand, no backslash and no at sign; no fenced block; no less-than sign outside a code span, with which Markdown starts HTML or a link; no web address, which is a colon followed by two slashes, or a host name that begins with three w's and a full stop; no closing square bracket followed at once by a colon, with which a link's target is defined out of sight, and, outside a code span, none followed at once by an opening one, with which Markdown links by reference; and no link but from a record's ID to that record's file. A record also holds no vertical bar outside a code span, with which Markdown makes a table, and no line but its headings that starts with a number sign.

## Alternatives

- Refusing only the characters to which Unicode gives a category for text that does not show, which let through a variation selector, a filler and a blank braille pattern among such characters, and, beyond characters, a target defined out of sight, an HTML comment between escaped backticks, a link that carries its target by a label, an address that begins with three w's and a full stop, without the part that names its protocol, and a character written as an entity.

## Consequences

- `tests/test_decisions.py` reads every record and the index and fails naming the file and what it holds (R128; task 1.18).
- The records and the index already keep to printable ASCII, so the rule refuses nothing that is written in them, and it answers the whole class at once rather than naming each way of hiding text (T73).
- A record cannot link to a page outside the repository, so what it rests on is named rather than linked (DR-158; T75).
- A link whose text is a record's ID and whose target is another record's file is refused, so a reader who follows an ID reaches the record it names (T79).

## Scope

This covers the characters and the links that a record and the index may hold. How a record names what it rests on is DR-158 (A record names other things by ID, number or path, and its change by name), and what a record's fields and sections hold is DR-108 (Each decision has a record of its own, in an index).

## What reversing it would change

R128 in `project-standards` would change, with its scenario "A record that hides text or links elsewhere fails CI", and so would the plain-text check in `tests/test_decisions.py`, task 1.18, the design's decision 13 and the answers of T73, T75 and T79. DR-158 would be revisited. Records are not part of the public surface, so the change would not be a breaking one for adopters.
