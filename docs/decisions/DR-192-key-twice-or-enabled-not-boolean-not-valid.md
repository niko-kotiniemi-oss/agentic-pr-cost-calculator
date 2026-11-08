# DR-192: A configuration file that gives a key twice, or no `enabled` of `true` or `false`, is not valid

- **Type:** technical
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R92, R171
- **Threats:** T49
- **Replaces:** none
- **Closed by:** none

## Context

`.pr-cost.json` turns the tool on in a repository while it enables the tool, and a file that is not valid leaves the tool off without stopping the report (DR-021, DR-051). The owner chose on 2026-11-03 that a file that holds a key that its format does not document is not valid (DR-190). A check of that choice's commit, in a context separate from the one that wrote it, found two cases that the format left open. Python's JSON reader takes the last of a key's values when a file gives the key twice, so a file that gives `enabled` first as false and then as true turns the tool on while a reviewer of its diff sees false. And `{}`, or a file whose `enabled` is neither `true` nor `false`, holds no key that the format does not document, and says nothing that the format defines. The change settled both, and later checks found that no record held what it chose.

## Decision

A configuration file is not valid when it gives a key more than once, whatever its values, or when it is not a JSON object whose `enabled` is `true` or `false`, as `{}` is not, whatever else it holds. Such a file leaves the tool off at its commit, as every file that is not valid does.

## Alternatives

- Reading a key given twice as its last value, as Python's JSON reader does, which lets a file that a reviewer reads as disabling the tool turn it on.
- Taking `{}` to disable the tool, as a file whose `enabled` is false does, which would read a file that says nothing as a choice, and give the report's job summary a reason that the file does not state.
- Taking a value that some reader counts as true, such as `1` or `"yes"`, to enable the tool, which would make the switch depend on how one reader turns values into true and false.

## Consequences

- A file that gives `enabled` twice, or gives no `enabled` of `true` or `false`, leaves the tool off: capture records nothing, and where the file before the merge turned the tool on, the report posts the comment of the pull request that made the file so, flagged, saying that the file after the merge cannot be read as a valid configuration (DR-191).
- The configuration's format documents `enabled` as `true` or `false`, and lists a key given twice among what no schema can hold (task 1.2).
- The rules read strictly what crosses into the tool, as the report does when it refuses a ledger line that gives a field twice (DR-044).

## Scope

This covers which `.pr-cost.json` files are not valid beyond those that DR-190 names. A key that the format does not document is DR-190 (A configuration file with a key that the tool does not know is not valid), what the report says when a file leaves the tool off is DR-191 (The report says when a merge leaves the tool off), and when the report runs is DR-051 (A pull request cannot turn off its own report).

## What reversing it would change

R171 in `switch-and-opt-in` would keep only its clause on a key that the format does not document, its scenarios "A configuration file that gives a key twice is not valid" and "A configuration file without an `enabled` of `true` or `false` is not valid" would be removed, and R171's row in `docs/requirements.md` would change with its title. Task 1.2 would document the file's validity anew, tasks 2.4 and 4.1 would test other files, and the design's decision 6, the switch and opt-in feature page, `docs/how-it-works.md`, T49's answer and the changelog's line would change.
