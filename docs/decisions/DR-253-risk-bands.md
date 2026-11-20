# DR-253: Risks are banded by OWASP's table of overall risk severity: 1 note, 2 low, 3 and 4 medium, 6 high and 9 critical

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-11-18
- **Requirements:** R247, R249, R251
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

Each threat's risk is the product of its impact and its likelihood, each from 1 to 3 (DR-094), so a risk can only be 1, 2, 3, 4, 6 or 9. The owner asked on 2026-10-29 for a risk register in which every high or critical risk is answered further, which needs a line between the bands, and asked on 2026-11-18 whether an established definition exists. GitHub's advisories, which Renovate reads, give a vulnerability a severity from its CVSS score, which scores the flaw itself rather than an impact and a likelihood. OWASP's Risk Rating Methodology rates impact and likelihood each as low, medium or high, and reads the overall severity from a table of the two, which fits the threat model's scale level for level.

## Decision

Each risk, raw or with its answer in place, takes the band that OWASP's table of overall risk severity gives its impact and its likelihood, read as levels 1 to 3 of low, medium and high. By the threat model's score, that is 1 note, 2 low, 3 and 4 medium, 6 high and 9 critical (R247). The rule on high and critical risks reads these bands (R249, R251). The source is OWASP Foundation, OWASP Risk Rating Methodology, its step on determining the severity of the risk.

## Alternatives

- 1 and 2 low, 3 and 4 medium, 6 high, 9 critical: OWASP's table with its lowest band folded into low, a choice of this project's own with no source to cite.
- 1 and 2 low, 3 medium, 4 and 6 high, 9 critical: a threat of medium impact that is possible would be high, and the risks that need a further answer would grow from 13 to 63 before the build.
- The CVSS bands that GitHub's advisories use: they band a score from 0 to 10 that rates a vulnerability's own traits, which the threat model's ratings do not give.

## Consequences

- The risk register gives each threat's band, raw and with its answer in place, and how many threats each band holds.
- The 13 threats whose risk with the answer in place is 6 each carry a further answer or an acceptance (DR-255).

## Scope

This covers where the lines between the bands fall. The scale and the risk are DR-094, the raw rating DR-254, and what a high or critical risk needs DR-255.

## What reversing it would change

How hard it is to reverse: easy. The script that writes the risk register gives each band from its score, so moving a line changes the script, the requirements that name the bands, R247, R249 and R251, and the register that the script writes again; a threat that a new line makes high or critical then needs a further answer before CI passes.
