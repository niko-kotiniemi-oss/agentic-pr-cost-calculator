# DR-049: The opt-in is read strictly

- **Type:** security and privacy
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R106
- **Threats:** T3
- **Replaces:** none
- **Closed by:** none

## Context

Capture reads the person's `pr-cost.capture` itself, from their global configuration files (DR-048) and by git's rules for those files (R38), so it has to say which values turn capture on. Git's spellings of true include `yes`, `on` and `1`, and a key given with no value. Git reads other numbers, such as `2`, as true too, but an opt-in is better read too strictly than too loosely.

## Decision

Of the values, only `true`, `yes`, `on` and `1`, in any case, and the key alone turn capture on. Every other value leaves capture off, whether git would read it as true, as it reads `2`, or could not read it as true or false, as with `maybe`.

## Alternatives

- Reading the value as git does, which also takes other numbers as true, and so reads the opt-in more loosely.

## Consequences

- A person who sets a value that git reads as true and the step does not, such as `2`, is not recorded.
- The `switch-and-opt-in` feature page names the values that opt a person in, and task 2.4 tests each of git's spellings that the spec names, as well as `2` and `maybe`.

## Scope

This covers which values of the opt-in turn capture on. Where it is read is DR-048 (The opt-in is read only from the person's global git configuration), and how a configuration file is parsed, with names in any case, quotes and comments dropped and the last value deciding, is R38.

## What reversing it would change

R106 in `switch-and-opt-in` would change, with its scenarios "Git's spellings of the setting opt a person in" and "A number other than `1`, or a value that git cannot read, does not opt a person in". So would T3's answer and the `switch-and-opt-in` feature page, which both list the values, task 1.2, which documents the opt-in setting in `docs/ledger-format.md`, and task 2.4's tests. Reading the opt-in as git does would add values, such as `2`, that turn capture on, so people who set one of them, and are not recorded now, would be. The opt-in key is part of the public surface (DR-154), and R71 and the design's decision 11 have a change to that surface raise the major number, as one that existing adopters have to act on, so the change would be a breaking one for adopters (DR-096).
