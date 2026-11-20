# DR-035: Capture never changes what the agent's commit would do

- **Type:** technical
- **Boundary:** inside
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R56, R84, R85
- **Threats:** T10, T12
- **Replaces:** none
- **Closed by:** none

## Context

The ledger file joins the agent's commit (DR-010), staged before the command runs (DR-013). Added to a commit with nothing else to commit, it would turn a commit that ought to fail into one that succeeds with only the ledger file, and an empty commit asked for into one that is not empty. Staged in the ledger folder, it would make a `git rm` of that folder fail, and a `git mv` of the folder would take it where capture does not look (T10). Staging anything beyond its own file would put unrelated work into the commit (T12).

## Decision

Apart from adding its own ledger file, capture leaves the agent's commit as it would be without the tool, and stages only the file it wrote. It stages nothing for a commit that would commit nothing, counting the changes that `-a` adds, when no `git add`, `git rm` or `git mv` comes before it, so that a commit that would fail still fails and an empty commit asked for stays empty, and it stages nothing after a `git rm` or `git mv` that may reach the ledger folder.

## Alternatives

None were recorded when this was decided.

## Consequences

- A `git add` that stages nothing, before a commit that would otherwise commit nothing, lets that commit hold the ledger file alone instead of failing, since what the `git add` will stage is unknown when the file is staged (the design's risk "[A `git add` that stages nothing comes before a commit that would otherwise commit nothing]"; T10).
- The repository's own git hooks see the staged file, so a `pre-commit` hook that refuses it fails a commit that would pass without the tool, which is why the README's adopting section from task 4.4 asks adopters to leave `.pr-cost/` out of their hooks (the design's risk "[A repository's own git hooks see the staged ledger file]"; T10).

## Scope

This covers what capture does to a commit that it stages for. Which commits it stages for is DR-034 (Capture stages only for a commit whose branch and contents it can tell).

## What reversing it would change

R84 and R85 in `usage-capture` and R56 in `ledger` would change, with their scenarios. The design's decision 1 and its risks, the answers and residuals of T10 and T12, the commit flow and the hook's credentials in `docs/how-it-works.md`, the usage-capture and ledger feature pages, and task 2.2 would change too. Nothing on the design's public surface would change. DR-034 would be revisited.
