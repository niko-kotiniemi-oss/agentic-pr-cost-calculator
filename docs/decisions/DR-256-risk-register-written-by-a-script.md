# DR-256: The risk register is written by a script from the threat model

- **Type:** process
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-29
- **Requirements:** R245, R246, R247
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

The owner asked on 2026-10-29 for a risk register: each threat with its raw and adjusted ratings, what answers it and the assumptions that it rests on. The threat model holds 205 threats, and a rating changes whenever a review rates a threat again. DR-250 keeps the register of requirements and the feature pages' lists of requirements written by hand and held by tests, since they are indexes of IDs and titles that a test already compares with the specs.

## Decision

A script in this repository writes `docs/risk-register.md` from the threat model, the specs and the register of requirements alone, and a test fails when the committed page differs from what the script writes (R245). No one edits the page by hand: a change to a threat's ratings, answer or assumptions runs the script and commits its output.

The register differs from the indexes that DR-250 keeps by hand. Each of its rows gives figures that the threat model holds, two ratings, their products and their bands, and what answers the threat, read from its Held by and placed under the requirements that hold its scenarios. A test that compared a page written by hand with the threat model would read all of it back, which is as much code as writing it, while each rating changed would also be changed by hand.

## Alternatives

- The page written by hand and held by a test that reads it back, as DR-250 keeps the register of requirements: as much code, and every rating changed twice.
- No page: the threat model alone, with raw fields beside the others. A reader could not see the threats in order of risk, nor which answers carry the most weight.

## Consequences

- The page opens by saying that the script writes it, from what, and that it is not edited by hand.
- The threat model's own risk matrix stays, held by the checks that R31 gives; the register's matrix of ratings with the answers in place is written from the same ratings, so the two cannot differ while both pass.
- The script and its tests are development tools, Python with the standard library only, and read no network.

## Scope

This covers how the risk register is kept. What it shows is R246 and R247, the raw rating DR-254, the bands DR-253 and the rule on high risks DR-255. How the register of requirements is kept is DR-250, which this record leaves as it is.

## What reversing it would change

How hard it is to reverse: easy. The script and its test would go, and the page would be written by hand and held by a test that reads it back, or removed; no other page rests on how it is written.
