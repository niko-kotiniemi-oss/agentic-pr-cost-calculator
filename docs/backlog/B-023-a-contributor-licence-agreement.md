# B-023: A contributor licence agreement

- **Status:** Open to feedback and contributions
- **Last changed:** 2026-11-16
- **Brief:** Terms that each outside contributor agrees to, which let the licensor also offer their contribution under other licences, such as in a paid version, while the contributor keeps their copyright.
- **Rests on:** DR-242, DR-244
- **Issue:** none
- **Pull requests:** none

## Problem

The repository's work is under the Fair Core License with MIT as its future licence (DR-242), and a contribution comes in under that licence alone, as `CONTRIBUTING.md` says. That does not let the licensor offer a contribution in a paid version under other terms, or move later versions to another licence, without asking each contributor again. No contribution from outside the project has been merged so far.

## What done looks like

Before the first contribution from outside the project is merged, its author has agreed to terms that let the licensor also offer it under other licences while the author keeps their copyright, the terms were read by a lawyer, `CONTRIBUTING.md` says what they are, and a check on each pull request shows whether its author has agreed, and covers work copied in from outside, not only a pull request's author. The check adds its threats to `docs/threat-model.md`, keeps CI's token read-only with no secrets (T37), and keeps no personal data of contributors, such as a list of who signed, in the repository.

## Postponed points

None.
