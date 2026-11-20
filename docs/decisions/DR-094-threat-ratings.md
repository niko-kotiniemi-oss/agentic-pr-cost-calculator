# DR-094: Threats are rated for impact and likelihood

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the owner, 2026-10-20
- **Requirements:** R31
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

The threat model lists every threat to the tool, boundary by boundary, with what answers it. It was written for the change `add-pr-cost-calculator` before any code, so its answers are requirements and tasks, and every later change revisits it (see the threat model's introduction).

## Decision

Each threat in `docs/threat-model.md` carries an impact and a likelihood, each from 1 to 3, and a risk that is their product, from 1 to 9. A risk matrix shows every threat in the cell of its two ratings.

## Alternatives

- Impact alone, as the first version of the threat model had, which cannot tell a severe threat that needs several unlikely conditions from one that ordinary use meets.
- A scale of 1 to 5, whose finer steps a design with no code cannot support with evidence.

## Consequences

- The threat model's method names what each level means, and `tests/test_threat_model.py` fails on a missing rating, a wrong product or a threat outside its matrix cell (R31; see the design's decision 9).
- A reader sees at a glance where the risk sits, and every threat that a change adds is rated the same way.
- The method rates as unlikely a threat that needs a defect which a test is written to catch, so the matrix relies on those tests being written (DR-084).

## Scope

This covers how each threat is rated. What a likelihood is rated against is DR-112 (Likelihood is rated with the answer in place), and when the threat model is revisited, and by whom, is DR-095 (Threats are modelled twice in every change).

## What reversing it would change

R31 in `project-standards` would change, with its scenarios "A threat without both ratings fails CI" and "A threat outside its matrix cell fails CI". So would the design's decision 9, the threat model's method, every threat's ratings and its risk matrix, `tests/test_threat_model.py`, task 1.10, which rated T1 to T69, `CLAUDE.md`'s section on the threat model, the steps on threats at design and at implementation in `CONTRIBUTING.md`, the pull request template's checklist, the README's entry for the threat model, the proposal's list of what changes and the feature page for `project-standards`. The choice bears on every threat alike, so the record lists none of them among its threats. DR-095, whose reviews rate the likelihoods, and DR-112, which says what a likelihood is rated against, would be revisited.
