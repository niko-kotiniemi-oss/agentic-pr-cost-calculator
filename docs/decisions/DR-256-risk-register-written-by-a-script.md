# DR-256: The risk register is written by a script from the threat model

- **Type:** process
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-29
- **Requirements:** R245, R246, R247, R248
- **Threats:** T206
- **Replaces:** none
- **Closed by:** none

## Context

The owner asked on 2026-10-29 for a risk register: each threat with its raw and adjusted ratings, what answers it and the assumptions that it rests on. The threat model holds 215 threats, and a rating changes whenever a review rates a threat again. DR-250 keeps the register of requirements and the feature pages' lists of requirements written by hand and held by tests, since they are indexes of IDs and titles that a test already compares with the specs.

## Decision

A script in this repository writes `docs/risk-register.md` from the threat model, the specs and the register of requirements alone, and a test fails when the committed page differs from what the script writes (R245). No one edits the page by hand: a change to a threat's ratings, answer or assumptions runs the script and commits its output.

The register differs from the indexes that DR-250 keeps by hand. Each of its rows gives figures that the threat model holds, two ratings, their products and their bands, and what answers the threat, read from its Held by and placed under the requirements that hold its scenarios. A test that compared a page written by hand with the threat model would read all of it back, which is as much code as writing it, while each rating changed would also be changed by hand.

## Alternatives

- The page written by hand and held by a test that reads it back, as DR-250 keeps the register of requirements: as much code, and every rating changed twice.
- No page: the threat model alone, with raw fields beside the others. A reader could not see the threats in order of risk, nor which answers carry the most weight.

## Consequences

- The page opens by saying that the script writes it, from what, that it is not edited by hand, and that each rating with the answer in place takes the answer as built as specified (T206).
- The threat model's own risk matrix stays, held by the checks that R31 gives. The register's matrices are written by the script and held by tests of their own that plant a threat in the wrong cell, since the comparison with the script's output alone would pass a defect of the script.
- The script also writes, for the reviewers of the raw ratings, a copy of a boundary's threats without their ratings (DR-254), which nothing commits.
- The script and its tests are development tools, Python with the standard library only, and read no network.

## Scope

This covers how the risk register is kept. What it shows is R246 to R248, the raw rating DR-254, the bands DR-253 and the rule on high risks DR-255. How the register of requirements is kept is DR-250, which this record leaves as it is.

## What reversing it would change

How hard it is to reverse: easy. The script and its test would go, and the page would be written by hand and held by a test that reads it back, or removed; no other page rests on how it is written.
