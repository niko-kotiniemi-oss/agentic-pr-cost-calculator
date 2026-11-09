# DR-195: The specs hold only text that GitHub shows as it is

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-09
- **Requirements:** R176
- **Threats:** T125
- **Replaces:** none
- **Closed by:** none

## Context

Agents build to the specs, and the owner and the reviews read them as GitHub shows them. GitHub hides an HTML comment, a link reference definition, a link's target and the cells of a table's row beyond its header's, and shows a character reference or an escaped character as something other than its text, while OpenSpec and an agent read the raw text, so a spec could hold a requirement, or words of one, that its reviewers never see (T125). The decision records are held to plain text for the same reason (DR-152), and the specs were not.

On 2026-11-09, the specs of `add-pr-cost-calculator`, as the default branch held them, held only printable ASCII characters and line feeds. A less-than sign stood on 9 of their lines and an ampersand on 14, all inside inline code, and an at sign on 4, 2 of them outside inline code, where it names a mention. They held no backslash and no tab, every run of backticks was closed on its own line, and outside inline code they held no vertical bar, no closing square bracket followed at once by an opening parenthesis or by a colon, no web address and no HTML comment.

## Decision

A spec that `tests/test_spec_form.py` reads holds printable ASCII characters and line breaks, which are line feeds alone, and nothing else. Each of its runs of backticks is closed on its own line by a run as long. Outside inline code, it holds no less-than sign, with which Markdown starts HTML, an HTML comment among it; no ampersand, with which it starts a character reference; no backslash, with which it escapes a character; no vertical bar, with which it makes a table; and no closing square bracket followed at once by an opening parenthesis, with which a link hides its target, or by a colon, with which a link's target is defined out of sight. The test names the spec, the line and what the line holds.

## Alternatives

- Holding the specs to the whole of DR-152's rule, which also fails an ampersand, a backslash and an at sign inside inline code, where the specs name them, and a web address, which GitHub shows as its text.
- Failing only a less-than sign, which leaves a table's hidden cells, a link's target and a definition out of sight.
- Leaving hidden text to the reviews, which read the specs as GitHub shows them and so cannot see it.

## Consequences

- What GitHub shows of a spec is all that OpenSpec and an agent read in it, so the owner and the reviews approve the specs that agents build to (T125).
- The specs already hold no such text, so the rule refuses nothing that is written in them.
- A spec's line ends only at a line feed, so a carriage return or a line separator, which another reader may take for the end of a line, fails as a character that is not printable ASCII, and a spec that is not UTF-8 fails naming the spec.
- Inline code that runs onto the next line fails, though GitHub shows it as code, so that the test never takes for code what GitHub shows as text, nor the other way round.
- An at sign and a web address stay allowed outside inline code, since GitHub shows each with its text. A note or an example that needs another mark goes in the change's proposal or design.

## Scope

This covers the characters and marks that a spec may hold. The form of each requirement, scenario and heading, and which files are read as specs, is DR-193 (A test of the repository's own holds the specs' form), and the plain text that the records and their index hold is DR-152 (A record is plain text and links only to other records).

## What reversing it would change

R176 in `project-standards` would change, with its scenarios, and so would task 1.23, `tests/test_spec_form.py`, the `project-standards` feature page, the design's decision 12, T125 and A9. A spec could again hold text that GitHub hides from its reviewers.
