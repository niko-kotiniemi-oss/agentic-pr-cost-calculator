# DR-214: An agent never turns capture on for anyone

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R204
- **Threats:** T150, T158
- **Replaces:** none
- **Closed by:** none

## Context

`CLAUDE.md` sends agents to the README for what the tool does and how to set it up, and the README's short start gives, as its first command, the opt-in, `git config --global pr-cost.capture true`, which writes the global git configuration of the machine where it runs (DR-212). The owner's opt-in for this repository is set only in the setup script of an environment that only this repository's own project uses, never in a global git configuration file on a machine where the owner's sessions can reach this clone beside another's (DR-210), since a session that reaches this clone beside another repository's would otherwise record here what it does from this clone on the other (T2, T32, T128). An agent that set the tool up here by following the README would write the opt-in where DR-210 keeps it out (T150). A record about what agents may do lands in the same pull request as the change to `CLAUDE.md` that steers by it. An agent that sets the tool up in another repository from the README does not load this repository's `CLAUDE.md`, and could go on from the short start's step for a repository to its opt-in, opting in the person who asked it, or to its step for an organization, opting in the organization's members (T158).

## Decision

An agent working here never turns capture on for anyone, the owner included: it never sets `pr-cost.capture` to `true` in a git configuration file, a setup script or an environment's variables, and the owner sets their own opt-in, as DR-210 says. A test that needs the opt-in sets it only in a git configuration of the test's own. `CLAUDE.md`'s section on what an agent never does here says so. The README's sections on the opt-in, on a project's cloud threads and on organizations say the same to an agent that sets the tool up elsewhere: that a person sets their own opt-in, or their organization does once it has told them, and that an agent that sets the tool up turns capture on for no one and leaves the opt-in to whoever asked it (R204).

## Alternatives

- No rule, which leaves an agent that follows the README's short start here to opt the owner in on whatever machine it runs on.
- The rule in `CLAUDE.md` alone, which steers only the agents that work here, so that an adopter's agent that follows the README could opt in the person who asked it.
- A check that fails when a session's global git configuration holds the opt-in, which no test can run, since no test may reach a person's machine or a session's environment (DR-090).

## Consequences

- An agent asked to set the tool up here, or to try the README's steps, leaves the opt-in to the owner (T150).
- `CLAUDE.md` changes in the same pull request, which the owner reviews as a change to what steers agents (A15).
- An agent that sets the tool up elsewhere from the README reads, in its section on the opt-in, which sits inside the section on adopting the tool that the short start's step for a repository links, that it opts no one in (T158).
- Whether an agent keeps to the rule rests on agents following the repository's rules, and what the README says to them (A16).

## Scope

This covers who may turn capture on, here, and what the README tells an agent that sets the tool up elsewhere. Where the owner's own opt-in is set is DR-210 (The owner's opt-in for this repository is set only in the environment of its own project), and whose consent capture needs is DR-202 (Capture needs an opt-in that the person sets, or that the environment they use sets).

## What reversing it would change

`CLAUDE.md`'s section on what an agent never does here would change, and so would R204 in `project-standards`, design decisions 12 and 17, task 4.4, the answers of T150 and T158 and assumption A16.
