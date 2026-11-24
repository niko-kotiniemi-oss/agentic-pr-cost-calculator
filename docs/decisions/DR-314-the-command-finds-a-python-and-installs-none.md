# DR-314: The registered command tries `python3`, `python`, then `py -3`, and installs no Python

- **Type:** technical
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-21 and 2026-11-22
- **Requirements:** R307
- **Threats:** T317
- **Replaces:** none
- **Closed by:** none

## Context

A Windows machine may give Python only as `python` or through the `py` launcher, and `python3` there can be Windows' stub that opens the Microsoft Store, so a command that starts only `python3` would record nothing. Python's documentation says that the install manager's launch commands install a Python when none is installed. The owner asked on 2026-11-21 and 2026-11-22 that every known Windows problem be covered in the design.

## Decision

The registered command and the plugin's command start the capture step with the first of `python3`, `python` and `py -3` that starts a Python, trying each only where the one before it is missing or starts no Python, and start nothing that installs Python. The step's own check refuses a Python older than 3.11 (R307).

## Alternatives

- `python3` alone: it records nothing on many Windows machines.
- `py -3` first: on a machine with no Python the install manager's launcher would install one.

## Consequences

- The command's form is part of the public surface (R122), and a change to it reaches adopters as a release.

## Scope

This covers how the command finds a Python. The floors are R32's.

## What reversing it would change

How hard it is to reverse: reversible with work. R307, the registration's form and the plugin's command would change.
