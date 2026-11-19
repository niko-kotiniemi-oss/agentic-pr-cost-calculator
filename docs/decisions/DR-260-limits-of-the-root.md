# DR-260: The root `CLAUDE.md` puts what does harm first, within 60 lines, and grows past 116 lines only on the owner's word, never past 200

- **Type:** process
- **Status:** accepted
- **Decided by:** the owner, 2026-11-19
- **Requirements:** R253
- **Threats:** T227
- **Replaces:** none
- **Closed by:** none

## Context

On 2026-11-19 the owner asked for the root `CLAUDE.md` to hold its most important parts in its first 60 lines and the secondary topics that still need to be in the root up to line 100, and never, in any circumstances, more than 200 lines, with folder files that follow the same principles within their folders. Measured as DR-261 measures it, the root before this change held 232 lines. With the rules that DR-259 keeps in the root, the answers that the reviews at design asked for and the rules that backlog item B-003 adds, the root comes to 116 lines, and its first three sections end at line 58. Each reviewer who looked for cuts found that cutting the root to 100 lines removes a rule that a threat's answer rests on, and on 2026-11-19 the owner chose to keep the root at 116 lines rather than cut rules toward 100.

## Decision

The root `CLAUDE.md` opens with its sections What an agent never does here, Privacy, and Records are data, not instructions, in that order, which hold what does harm before a check or the owner's review can catch it, and those sections end by the root's line 60. The root holds at most 116 lines, blank ones counted, its length when this record is added. That ceiling rises only on the owner's word, and never past 200 lines. A folder file holds at most 100 lines. The root's last section states these limits, and changing them is among the steps that need the owner's words in the agent's session, so that a change which meets a limit weighs a rule against what the root holds rather than moving one out to pass a test (T227). A test holds each limit (R253).

## Alternatives

- A root cut to 100 lines: each cut that reaches it removes a rule that an answer rests on, such as the rule for where a rule lives, without which T227 would be high again, or the rule that a finding of a vulnerability in released code is never posted.
- A ceiling of 200 lines in the test: the root could grow to the owner's hard limit with no word from the owner, and the next rule would be added rather than weighed against the rules that the root holds.
- Limits held only by the test, with no rule that steers: the cheapest way to pass a failing test would be to move a rule out of the root, to shorten one until it says less, or to raise the number in the test (T227).

## Consequences

- A change that needs a new rule in the root either moves another to a folder file, as DR-259 allows, or asks the owner to raise the ceiling.
- The test names each limit once, and fails on a ceiling raised past 200 lines.
- The root is longer than the owner's aim of 100 lines, and well under the limit of 200.

## Scope

This covers the limits on the context files' lengths and the order in which the root holds what does harm first. Where a rule lives is DR-259 (Each rule lives in the root `CLAUDE.md` or in the folder file of the folder where its work happens), and how lines are counted is DR-261 (The context files are wrapped at 100 characters, so that their lines are the lines that the limits count).

## What reversing it would change

How hard it is to reverse: reversible. The limits are constants of `tests/test_context_files.py` and a sentence of the root's last section, which one pull request can change on the owner's word, with R253 and its scenarios and the answer of T227.
