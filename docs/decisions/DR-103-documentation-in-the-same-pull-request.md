# DR-103: Documentation changes in the same pull request as what it describes

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-20
- **Requirements:** R73, R100, R101
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

Three documents describe the tool: the register of requirements (DR-100), the page for each feature (DR-101) and `docs/how-it-works.md` (DR-102). The tool is designed before it is built, so each of them first describes what the specs require (see `docs/features/README.md` and `docs/how-it-works.md`).

## Decision

The documentation is meant to name everything the tool does (R29). So three documents are kept with the code, each checked by `tests/test_documentation.py`, and each changed in the same pull request as what it describes.

## Alternatives

- Documentation written once the code exists, which describes what was built rather than what was meant, and falls behind without anything noticing.

## Consequences

- A pull request that adds a requirement to a spec fails CI until the register and the spec's feature page list it (R73, R100), and one that changes a job's permissions, or adds an action or an image to a workflow, fails until `docs/how-it-works.md` says so too (R101).
- The tests check what a machine can. What they do not check, such as a flow that the page leaves out, rests on the rule itself, which `CLAUDE.md` sets for everyone who works on the repository.
- Task 5.3 brings all three up to date with what was built.

## Scope

This covers when the three documents change. What each of them holds is DR-100 (A register lists every requirement with its kind), DR-101 (Each feature has a page) and DR-102 (A page explains how the tool works as a whole), and the changelog's line for a change that adopters would notice is DR-098 (The changelog is kept by hand).

## What reversing it would change

R73, R100 and R101 in `project-standards` would change, since each fails CI when its document falls behind. So would the design's decision 12, `tests/test_documentation.py`, `CLAUDE.md`'s section on documentation, the step on documentation in `CONTRIBUTING.md`, the pull request template's checklist, and the statements in `docs/how-it-works.md` and `docs/features/README.md` that each changes in the same pull request as what it describes. DR-100, DR-101 and DR-102 would be revisited.
