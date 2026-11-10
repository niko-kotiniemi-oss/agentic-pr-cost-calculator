# DR-214: An agent never turns capture on for anyone

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** none
- **Threats:** T150
- **Replaces:** none
- **Closed by:** none

## Context

`CLAUDE.md` sends agents to the README for what the tool does and how to set it up, and the README's short start gives, as its first command, the opt-in, `git config --global pr-cost.capture true`, which writes the global git configuration of the machine where it runs (DR-212). The owner's opt-in for this repository is set only in the setup script of an environment that only this repository's own project uses, never in a global git configuration file on a machine where the owner's sessions can reach this clone beside another's (DR-210), since a session that reaches this clone beside another repository's would otherwise record here what it does from this clone on the other (T2, T32, T128). An agent that set the tool up here by following the README would write the opt-in where DR-210 keeps it out (T150). A record about what agents may do lands in the same pull request as the change to `CLAUDE.md` that steers by it.

## Decision

An agent working here never turns capture on for anyone, the owner included: it never sets `pr-cost.capture` to `true` in a git configuration file, a setup script or an environment's variables, and the owner sets their own opt-in, as DR-210 says. A test that needs the opt-in sets it only in a git configuration of the test's own. `CLAUDE.md`'s section on what an agent never does here says so.

## Alternatives

- No rule, which leaves an agent that follows the README's short start here to opt the owner in on whatever machine it runs on.
- A check that fails when a session's global git configuration holds the opt-in, which no test can run, since no test may reach a person's machine or a session's environment (DR-090).

## Consequences

- An agent asked to set the tool up here, or to try the README's steps, leaves the opt-in to the owner (T150).
- `CLAUDE.md` changes in the same pull request, which the owner reviews as a change to what steers agents (A15).
- Whether an agent keeps to the rule rests on agents following the repository's rules (A16).

## Scope

This covers who may turn capture on, here. Where the owner's own opt-in is set is DR-210 (The owner's opt-in for this repository is set only in the environment of its own project), and whose consent capture needs is DR-202 (Capture needs an opt-in that the person sets, or that the environment they use sets).

## What reversing it would change

`CLAUDE.md`'s section on what an agent never does here would change, and so would design decision 17, the answer of T150 and assumption A16.
