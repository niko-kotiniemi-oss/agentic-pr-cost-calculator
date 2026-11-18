# DR-253: A risk of 1 or 2 is low, 3 or 4 medium, 6 high and 9 critical

- **Type:** process
- **Status:** accepted
- **Decided by:** the owner, 2026-11-18
- **Requirements:** R246, R248
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

Each threat's risk is the product of its impact and its likelihood, each from 1 to 3 (DR-094), so a risk can only be 1, 2, 3, 4, 6 or 9. The owner asked on 2026-10-29 for a risk register in which every high or critical risk is answered further, which needs a line between the bands. With the answers in place, the threat model of 2026-11-18 holds no risk of 9 and 13 of 6.

## Decision

A risk of 1 or 2 is low, 3 or 4 medium, 6 high and 9 critical, both for a raw rating and for a rating with the answer in place. The risk register gives each risk its band (R246), and the rule on high and critical risks reads them (R248).

## Alternatives

- 1 and 2 low, 3 medium, 4 and 6 high, 9 critical: a threat of medium impact that is possible would be high, and the risks that need a further answer would grow from 13 to 63 before the build.
- 1 to 3 low, 4 medium, 6 high, 9 critical: the same high and critical risks, with a threat of high impact that is unlikely counted as low beside the slightest inconveniences.

## Consequences

- The risk register gives each threat's band, raw and with its answer in place, and how many threats each band holds.
- The 13 threats whose risk with the answer in place is 6 each carry a further answer (DR-255).

## Scope

This covers where the lines between the bands fall. The scale and the risk are DR-094, the raw rating DR-254, and what a high or critical risk needs DR-255.

## What reversing it would change

How hard it is to reverse: easy. The script that writes the risk register gives the bands from one table, so moving a line changes that table, the requirements that name the bands, R246 and R248, and the register that the script writes again; a threat that a new line makes high or critical then needs a further answer before CI passes.
