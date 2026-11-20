# DR-010: Usage travels inside the agent's own commits

- **Type:** architecture
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R7
- **Threats:** T8, T10, T16
- **Replaces:** none
- **Closed by:** none

## Context

Capture reads usage on the session's machine (DR-009), which a cloud session throws away, while the report reads usage from git in CI after the merge (DR-017, DR-018). The counts need a way from that machine into the repository without a service outside GitHub and the repository (DR-008), and the agent's commits already make that journey when they are pushed.

## Decision

Usage reaches the pull request inside the agent's own commits. When capture stages for a commit, it writes the waiting calls into a ledger file in the repository, and the commit carries it. No usage travels on a side branch, a separate ref or a service.

## Alternatives

- Pushing a separate ref from the hook, which makes every turn a network write that can fail.
- Keeping the ledger on a side branch that is never merged, which needs a push from the hook on every turn.
- Posting the usage to a separate service from the hook, for the reason that DR-008 (Capture uses no service outside GitHub and the repository) gives.

## Consequences

- The hook makes no network write: the ledger leaves the machine only when the person's commits are pushed (DR-060).
- Calls made after the agent's last commit on a branch, such as pushing and opening the pull request, reach no pull request (the design's risk "[Some calls reach no commit]"; T8).
- Staging a file in the person's index brings capture into their git work (T10), which DR-011, DR-013, DR-014, DR-034, DR-035, DR-128, DR-129 and DR-130 answer.
- The ledger is in the pull request's diff, where a reviewer sees it and anyone who can push to the branch can edit it (the design's risk "[A ledger edited by hand changes the reported cost]"; T16).

## Scope

This covers the route that usage takes to the pull request. The shape of the files it travels in is DR-127 (Each commit's usage goes in a new file, written once), where calls wait is DR-011 (Recorded calls wait in the git directory), which commit takes them is DR-012 (A call goes only to a commit in its worktree, on its branch), when a file is staged is DR-013 (A ledger file is staged just before a commit that capture can follow), and the ledger staying on the default branch is DR-015 (The ledger stays in the repository as the record).

## What reversing it would change

R7 in `usage-capture` would change, with its scenarios. The `.pr-cost/` path and the ledger format are part of the public surface, so the change would be a breaking one for adopters (DR-096). The design's decisions 1 and 3, the proposal's "What Changes" and "Impact", the flow in the threat model's "How data moves", the answers of T8, T10 and T16, the README's summary, the parts table, the commit flow and what the tool never does in `docs/how-it-works.md`, the usage-capture and ledger feature pages, and tasks 1.2 and 2.2 would change too. DR-011, DR-012, DR-013, DR-014, DR-015, DR-017, DR-034, DR-035, DR-066, DR-127, DR-128, DR-129, DR-130 and DR-131 would be revisited.
