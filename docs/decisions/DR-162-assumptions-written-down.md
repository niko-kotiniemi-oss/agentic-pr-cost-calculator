# DR-162: The design's assumptions are written down, each with what rests on it and how it is checked

- **Type:** process
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-28
- **Requirements:** R135, R140, R143
- **Threats:** T32, T82, T86, T88, T95, T96, T97, T100, T101
- **Replaces:** none
- **Closed by:** none

## Context

The design rests on facts about Claude Code, GitHub, git, Python, the development tools, prices, adopters and people. The specs, the design, the threat model and the records each state the ones they need, where they need them, and most were written before anything could check them. The threat model's section on assumptions lists only those that its answers rest on, and two of its ten name a threat. The owner asked on 2026-10-28 for a list of the design's assumptions, so as to see them and adjust them. The threat reviews at design found that a check named for a fact can claim more than it checks: a test cannot reach Claude Code or GitHub, an observation without its build holds only for the build it was made on, and a link can lead anywhere.

## Decision

The assumptions are written down in one place, each with what rests on it, by requirement, threat or record, and what changes if it is wrong, and each of its facts with where it is relied on and how it is checked: by a test, an observation, documentation, or not yet, with the task that will check it or why none will; a threat that rests on an assumption and the assumption name each other (R135). A fact whose subject no test may reach is never checked by a test alone, an observation names the file that reproduces what was seen, its date and the program, version and build it was seen on, and documentation is linked by its address, on a host that the test lists or at a full commit of a repository that it lists, with the date it was read (R140); no page of the assumptions gives another web address (R143).

## Alternatives

- Leaving each assumption where a document states it, which keeps no list to read or adjust, and lets two documents state one fact differently.
- Extending the threat model's section on assumptions, which would leave out the assumptions that no threat's answer rests on.
- Counting the threats listed by the records that an assumption names, in place of naming threats and assumptions both ways, which fixes the assumption's place in the list but lets a correction of it miss a threat that rests on it.

## Consequences

- `tests/test_assumptions.py` checks that each assumption and each fact says all of this, that every requirement, threat, record and task it names exists, that every test it names is collected, that threats and assumptions name each other, and the form of each check (task 1.19).
- The threat model's section on assumptions moves to `docs/assumptions/` and keeps its heading, with a pointer, since accepted records point to it. A sentence of it that states what the tool does, rather than what it assumes, moves to the spec that holds that behaviour, and each setting that the owner keeps is listed as a fact that points to the threat model, not yet checked, since no test may read a setting on GitHub.
- An assumption found wrong changes in the change that finds it, with the requirements, threats and records that rest on it. Its entry says what would change if it is wrong, never how to change it.
- An observation never says whose work it was seen in, and gives no figure measured on someone's private work, since this repository is public; a test fails on a path under a home folder or a session identifier in the assumptions or in a file named for an observation.
- A check holds for the day and the build that it names, so a fact that changes later, as a setting on GitHub can with no commit, is found by the reviews, not by the check.

## Scope

This covers what is written down about each assumption and how each of its facts is checked. How the assumptions are grouped and ordered is DR-163 (The assumptions are grouped, and listed with the most at stake first), the words they use are DR-164 (A glossary sets the words that the specs and pages use, and a test holds them), and what they are to an agent that reads them is DR-166 (The glossary, the assumptions and the pages they link to describe, and never steer).

## What reversing it would change

R135, R140 and R143 in `project-standards` would change, with their scenarios, and so would R136, the design's decision 14, task 1.19, `docs/assumptions/` and `tests/test_assumptions.py`, the threat model's section on assumptions and the field in which its threats name them, and the feature page for `project-standards`. DR-163 would be revisited. The assumptions are not part of the public surface, so the change would not be a breaking one for adopters.
