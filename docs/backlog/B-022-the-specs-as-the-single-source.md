# B-022: The specs as the single source

- **Status:** Planned
- **Last changed:** 2026-11-14
- **Brief:** The documents that state what the tool does today, such as the threat model, the design's risks, the feature pages and the register, brought to cite the specs instead of stating it again.
- **Rests on:** DR-232, T173
- **Issue:** none
- **Pull requests:** none

## Problem

The same behaviour is stated in the specs and again in other documents, such as a threat's answer, the design's risks, the feature pages and the page on how the tool works, and the tests hold the copies' IDs and tables but not their prose, which drifts apart from the specs.

## What done looks like

Each document other than the specs cites the requirement or scenario that states a behaviour instead of stating it again, and says only what no scenario can, such as why or what remains, while a page that a requirement obliges to tell its readers something tells them and cites that requirement (DR-232). The pull request shows, for each sentence that it removes, the scenario that holds it or the spec that it moved into, so that no clause is lost on the way (T173). A record says which checks of the documentation stay, and when a rule about prose goes to review instead of a new check, so that those checks do not grow faster than what they protect.

## Postponed points

- From the assessment of 2026-11-12, by the review of the design's architecture: whether the register and the feature pages' lists of requirements become views generated from the specs rather than pages that cite them, which DR-232 leaves to this item.
