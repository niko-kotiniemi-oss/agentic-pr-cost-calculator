# DR-125: The hook runs in Python's isolated mode

- **Type:** security and privacy
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R12
- **Threats:** T15, T28
- **Replaces:** none
- **Closed by:** none

## Context

Python puts a script's own folder first on its import path, so a file planted beside the hook under a standard module's name, such as `json.py`, would be imported in place of that module (T15). The hook file sits in the adopter's working tree, which any pull request to that repository can change, and the registered command runs it around every git command and at every stop (T59).

## Decision

The command that an adopter registers for the hook starts Python in isolated mode, as `python3 -I`, so that neither the hook file's folder, nor the current directory, nor Python's environment variables decide what the hook imports (T15).

## Alternatives

None were recorded when this was decided.

## Consequences

- The hook's code is run by the checksum check that the command carries, in that same Python, so it runs in isolated mode too (DR-058).
- Isolated mode keeps the hook's folder off the import path, so the hook can import nothing that sits beside it and is kept to a single file that needs only the standard library (R12; DR-022, DR-023).
- Task 2.3's tests hold the isolated mode in the registration and run the hook from a folder that holds nothing else but a planted `json.py`, which it does not import.

## Scope

This covers how the registered command starts Python. How the command ends, in `; exit 0`, is DR-031 (The registered command ends in `; exit 0`), its checksum check is DR-058 (The hook file runs only when its checksum matches), and the report's own `python3 -I` is part of DR-062 (The report runs its own pinned code). The release job also runs only `python3 -I` (see the design's decision 11), which this record does not cover.

## What reversing it would change

R12 in `usage-capture` would change, with its scenario "The capture step runs alone in isolated mode", and so would the registered command in the design's decision 1 and the registration that task 2.3 documents in the README, task 2.3's tests, T15's answer, and the citations of that scenario in T15 and T28. The command's form is part of the public surface, so the change would be a breaking one for adopters, released as a new major version (DR-096). DR-022 and DR-023, which keep the hook to one standard-library file that runs in isolated mode, would be revisited.
