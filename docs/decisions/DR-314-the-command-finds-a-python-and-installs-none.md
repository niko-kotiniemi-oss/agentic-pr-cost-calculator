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

The registered command and the plugin's command try `python3`, `python` and `py -3` in turn, each with `-I` and `PYTHON_MANAGER_AUTOMATIC_INSTALL` set to `false`, first as a probe that exits with a code that only a Python 3.11 or later gives, and start the capture step once, with the first that passes, and no other Python after it, in `sh`, Git Bash, PowerShell 7 and Windows PowerShell 5.1 alike (R307). The design gives the form for each shell.

## Alternatives

- `python3` alone: it records nothing on many Windows machines.
- `py -3` first, or any order alone: Python's documentation says that, with no runtime installed, any launch command of the install manager, its `python3` and `python` among them, tries to install one, so the order does not stop an install, and the setting is given to each candidate.
- Moving on whenever a candidate fails: a step that started and then failed would run again under the next Python.

## Consequences

- The command's form is part of the public surface (R122), and a change to it reaches adopters as a release, so it is run in each shell on the Windows runner before the first release.
- Each hook run starts a Python twice, once for the probe.

## Scope

This covers how the command finds a Python. The floors are R32's.

## What reversing it would change

How hard it is to reverse: reversible with work. R307, the registration's form and the plugin's command would change.
