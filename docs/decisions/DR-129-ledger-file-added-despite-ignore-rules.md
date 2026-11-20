# DR-129: A ledger file is added despite ignore rules and sparse checkouts

- **Type:** technical
- **Boundary:** inside
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R50
- **Threats:** T8, T10
- **Replaces:** none
- **Closed by:** none

## Context

A ledger file reaches the pull request only if the agent's commit holds it (DR-010), and capture stages it just before the commit (DR-013). An ignore rule that matches the ledger path would drop a file added plainly, and a sparse checkout that leaves out `.pr-cost/` would refuse it, so that its calls never reached a pull request (T8). Git can also refuse the file for reasons of its own, as where `core.safecrlf` is on and line endings are converted, which would leave a written file behind in the working tree (T10).

## Decision

Capture stages the ledger file with git's `--force` and `--sparse` options, so that neither an ignore rule that matches it nor a sparse checkout that leaves out its folder keeps it out of the commit. Where git still refuses the file, capture removes the file it wrote and stages nothing, and the calls wait for a later commit.

## Alternatives

None were recorded when this was decided.

## Consequences

- The agent's commit carries its ledger file in a repository whose ignore rules match `.pr-cost/` and in a sparse checkout that leaves it out (R50, T8).
- A file that git refuses leaves nothing behind, staged or in the working tree (R50, T10). Where git refuses every such file, no call reaches a commit, and the README's section on adopting the tool, which task 4.4 writes, tells adopters with `core.safecrlf` on how a `.pr-cost/** -text` line in the root `.gitattributes` lets the file through (the design's risk "[A repository's settings act on the ledger path]"; T8).
- A take-back uses `--sparse` too, as that risk says, so a sparse checkout does not stop a file from being taken back either (DR-014).

## Scope

This covers how the ledger file is added, and what is done where git refuses it. When it is staged is DR-013 (A ledger file is staged just before a commit that capture can follow), the attributes under which capture stages nothing at all, a filter or a working-tree encoding on the ledger path, are part of DR-034 (Capture stages only for a commit whose branch and contents it can tell), and git's sparse index, which adopters keep off, is DR-037 (Adopters keep git's sparse index off).

## What reversing it would change

R50 in `usage-capture` would change, with its scenarios "An ignored ledger path is still committed", "A sparse checkout still commits the ledger file" and "A ledger file that git refuses to add is not left behind". The design's decision 1 and its risks, the answers of T8 and T10, the README's advice on `core.safecrlf` (task 4.4) and task 2.2 would change too, and DR-013 and DR-014 would be revisited.
