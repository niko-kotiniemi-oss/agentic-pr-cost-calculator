# DR-264: The templates and `CONTRIBUTING.md` are data, and a template is filled in only with what is true

- **Type:** security and privacy
- **Boundary:** incoming
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-19
- **Requirements:** none
- **Threats:** T33
- **Replaces:** none
- **Closed by:** none

## Context

The threat review at design of the change's first pull request postponed a point that backlog item B-003 carries: how an agent reads the pull request and issue templates and `CONTRIBUTING.md`. The templates hold the headings and checklists that an agent fills in when it opens a pull request or an issue, and `CONTRIBUTING.md` tells a contributor how a change gets made, in the imperative. A pull request can change any of them, so text in them that reads as an instruction to an agent is text in the repository that steers an agent (T33). A box of a template that an agent ticks without having done or checked what it names would also tell the owner that a step was taken when it was not. On 2026-11-19 the owner asked for B-003 to be built.

## Decision

The pull request and issue templates and `CONTRIBUTING.md` describe, like every other page and data file here, and never tell an agent what to do, since only the files that the root `CLAUDE.md` names steer (DR-258). An agent fills in a template with what is true, and ticks one of its boxes only for what it did and checked. The root names the templates and `CONTRIBUTING.md` among what describes, and gives the rule on filling in a template in its section on records being data.

## Alternatives

- The templates and `CONTRIBUTING.md` among the files that steer: a pull request that changed them would change what agents do, while their wording is written for contributors rather than as rules.
- No rule on filling in a template: an agent could tick each box of a checklist as a form to complete, and the owner would read the ticks as steps taken.

## Consequences

- `CONTRIBUTING.md` and the templates keep wording written for people, while the rules that bind agents stay in the context files.
- Where `CONTRIBUTING.md` or a template differs from a file that steers or from a spec, those steer, and the agent tells the owner (DR-258).
- A box left unticked in a pull request's description is a step not taken or not checked, which the owner can ask about before the merge.

## Scope

This covers how an agent reads the templates and `CONTRIBUTING.md`, and how it fills in a template. Which files steer is DR-258 (Only the context files and the files that the root lists steer work here, and everything else describes).

## What reversing it would change

How hard it is to reverse: reversible. The rule is in the root `CLAUDE.md`, and the answer of T33 would change.
