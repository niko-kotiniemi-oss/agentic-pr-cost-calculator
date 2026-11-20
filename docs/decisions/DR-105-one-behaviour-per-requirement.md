# DR-105: Each requirement states one behaviour

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

OpenSpec's guide for writing specs asks that each new requirement state one behaviour, with its examples and edge cases in scenarios, and that a requirement covering several behaviours be split into requirements of their own. When the specs were first split one per feature (DR-104), some of their requirements stated several behaviours.

## Decision

Each requirement in the specs states one behaviour, with its examples and edge cases in its scenarios. A requirement that states more than one is split into requirements of its own, without changing what it requires.

## Alternatives

None were recorded when this was decided.

## Consequences

- A requirement that was split kept its ID, and the parts split from it took the next free IDs, R75 to R123, each with its original's kind (DR-106).
- A part split off can refer to its original by name, as R100, split from R29, does, and scenarios that tested two requirements at once were split so that each sits under the requirement it tests.
- No test or script in the repository checks that a requirement states one behaviour.

## Scope

This covers how many behaviours each requirement states. The length of its text is DR-113 (Each requirement is 500 characters or fewer), how IDs are kept is DR-106 (Requirement IDs are stable and never reused), one spec per feature is DR-104 (Each feature is one spec), and the register of every requirement is DR-100 (A register lists every requirement with its kind).

## What reversing it would change

No requirement's text would have to change, since nothing in the repository checks that a requirement states one behaviour: requirements could again hold several behaviours, and OpenSpec's guide would still ask for one each. Requirements merged back together would change the register and the feature pages with them (DR-100, DR-101), and DR-113 would be revisited.
