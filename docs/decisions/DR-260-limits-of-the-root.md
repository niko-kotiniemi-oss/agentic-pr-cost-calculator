# DR-260: The root `CLAUDE.md` puts what does harm first, within 60 lines, and holds at most 200 lines

- **Type:** process
- **Status:** accepted
- **Decided by:** the owner, 2026-11-19 and 2026-11-20
- **Requirements:** R253
- **Threats:** T227
- **Replaces:** none
- **Closed by:** none

## Context

On 2026-11-19 the owner asked for the root `CLAUDE.md` to hold its most important parts in its first 60 lines and the secondary topics that still need to be in the root up to line 100, and never, in any circumstances, more than 200 lines, with folder files that follow the same principles within their folders. Measured as DR-261 measures it, the root before this change held 232 lines. With the rules that DR-259 keeps in the root, the answers that the reviews at design asked for and the rules that backlog item B-003 adds, the root comes to 116 lines, and its first three sections end at line 58. Each reviewer who looked for cuts found that cutting the root to 100 lines removes a rule that a threat's answer rests on, and on 2026-11-19 the owner chose to keep the root at 116 lines rather than cut rules toward 100, under a ceiling that would rise only on the owner's word. On 2026-11-20, asked whether the root's last section should go on stating that ceiling and no longer the aim of 100 lines, the owner chose to set the ceiling at the limit of 200 lines, and said that as the root grows, the owner will have it reviewed adversarially again in a later pull request. Shown on 2026-11-20 that a rule moved out of the root's first three sections, to make room in them, passes every test and needs no word from the owner, the owner chose to list that move among the steps that need the owner's words.

## Decision

The root `CLAUDE.md` opens with its sections What an agent never does here, Privacy, and Records are data, not instructions, in that order, which hold what does harm before a check or the owner's review can catch it, and those sections end by the root's line 60. The root holds at most 200 lines, blank ones counted, the limit that the owner set, and a folder file at most 100 lines. The root's last section states these limits, and changing them, or moving a rule out of the root's first three sections, is among the steps that need the owner's words in the agent's session, so that a change which meets a limit weighs a rule against what the root holds rather than moving one out, or down, to pass a test (T227). A test holds each limit (R253).

## Alternatives

- A root cut to 100 lines: each cut that reaches it removes a rule that an answer rests on, such as the rule for where a rule lives, without which T227 would be high again, or the rule that a finding of a vulnerability in released code is never posted.
- A ceiling of 116 lines, the root's length when the limits were set, that rises only on the owner's word: the owner chose it on 2026-11-19, and on 2026-11-20 set the ceiling at the limit instead, so that the root takes a rule without the owner's word for each line it gains, and is reviewed again as it grows.
- A rule moved out of the first three sections left to the owner's review of the diff: the move passes every test while those sections still end by line 60, so only that review would catch it.
- Limits held only by the test, with no rule that steers: the cheapest way to pass a failing test would be to move a rule out of the root, to shorten one until it says less, or to raise the number in the test (T227).

## Consequences

- A change that needs a new rule in the root adds it while the root stays within 200 lines, or moves another rule to a folder file, as DR-259 allows. One that needs a new rule in the first three sections, which end by line 60, moves another rule out of them only on the owner's words in its session.
- The root can grow to 200 lines with no word from the owner, so a new rule need not be weighed against the rules that the root holds; the owner's review of each change, the limit of line 60 for what does harm, and the adversarial review that the owner plans as the root grows weigh it instead.
- The test fails on a root of more than 200 lines, and on a ceiling raised past 200 lines.
- The root holds more than the owner's aim of 100 lines, which its last section no longer states.

## Scope

This covers the limits on the context files' lengths and the order in which the root holds what does harm first. Where a rule lives is DR-259 (Each rule lives in the root `CLAUDE.md` or in the folder file of the folder where its work happens), and how lines are counted is DR-261 (The context files are wrapped at 100 characters, so that their lines are the lines that the limits count).

## What reversing it would change

How hard it is to reverse: reversible. The limits are constants of `tests/test_context_files.py` and a sentence of the root's last section, which one pull request can change on the owner's word, with R253 and its scenarios and the answer of T227.
