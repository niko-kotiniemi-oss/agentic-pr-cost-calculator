# DR-050: A repository's git configuration can turn capture off, never on

- **Type:** security and privacy
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R1, R39, R109
- **Threats:** T3
- **Replaces:** none
- **Closed by:** none

## Context

A person opts in once, in their global git configuration, which is not part of any repository, and capture reads the opt-in only from there (DR-048). Each repository also has a git configuration of its own, where the same key, `pr-cost.capture`, can be set too.

## Decision

One opt-in covers every repository that uses the tool, so `pr-cost.capture` set to `false` in a repository's own git configuration turns capture off there. Set to `true` there, it opts no one in. Capture reads the repository's own configuration only to see whether it turns capture off.

## Alternatives

None were recorded when this was decided.

## Consequences

- A person can stay opted in for every other repository and still keep one repository's sessions unrecorded, and the README's section on adopting the tool says how (task 4.4).
- A repository cannot opt in, through its own git configuration, anyone who has not opted in themselves (T3).
- A run that finds capture off in the repository's own configuration counts as an opt-out there: it ends every session's interval in that repository's store, and withholds the calls not yet committed (R109, DR-047).

## Scope

This covers what a repository's own git configuration can do to capture. The person's opt-in is DR-046 (Each person turns on capture of their own sessions), where it is read is DR-048 (The opt-in is read only from the person's global git configuration), and which of its values turn capture on is DR-049 (The opt-in is read strictly). The repository's own switch, `.pr-cost.json`, is DR-021 (One file, `.pr-cost.json`, turns the tool on or off).

## What reversing it would change

R39 in `switch-and-opt-in` would change, with its scenario "A person can turn capture off in one repository", and so would R1's scenario "A repository's own git configuration cannot opt a person in" and R109, which takes a repository's own setting as an opt-out. So would the design's decision 6, T3's answer and residual, the `switch-and-opt-in` feature page, the section of `docs/how-it-works.md` on credentials and permissions, the README's section on adopting the tool, and task 2.4 with its tests. A change that took away a repository's way to turn capture off would be a breaking one for adopters who rely on it (DR-096), since the opt-in key is part of the public surface (DR-154).
