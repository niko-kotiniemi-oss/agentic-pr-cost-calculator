# DR-146: A correction counts as made once the claim's other copies are searched for

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** none
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

Figures and statements of fact about the repository are written in its prose, commit messages and pull request descriptions, and each is computed, or settled by a query, before it is written (DR-083). One claim can stand in several places: the oldest supported Python, for one, is stated in the CI matrix, the ruff and mypy settings, `.python-version` and the documents, besides `requires-python` in `pyproject.toml`, and will be in the bill of materials and the hook's own guard once they are built (see the design's decision 10). A claim corrected in one place stays wrong in the others.

## Decision

A claim that is found to be wrong counts as corrected only once its other copies have been searched for, and not as soon as the copy that was found is fixed.

## Alternatives

None were recorded when this was decided.

## Consequences

- Each correction costs a search for the claim's other copies.
- A test compares some copies, such as those of the oldest supported Python (R99), but no check holds the rule as a whole, so it rests on whoever makes the correction.

## Scope

This covers when the correction of a claim about the repository counts as made. How such a claim is written in the first place, computed and never recalled, is DR-083 (Every figure is computed in the same session).

## What reversing it would change

The sentence on corrections in the section of `CLAUDE.md` on figures would change. No requirement, threat or part of the public surface is involved.
