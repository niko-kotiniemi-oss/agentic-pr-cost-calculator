# DR-316: Usage travels inside the agent's own commits, and in a commit of its own before a push

- **Type:** architecture
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the owner, 2026-11-24
- **Requirements:** R7, R305, R311, R312, R313, R320
- **Threats:** T8, T10, T16, T314
- **Replaces:** DR-010
- **Closed by:** none

## Context

Capture reads usage on the session's machine (DR-009), which a cloud session throws away, while the report reads usage from git in CI after the merge (DR-017, DR-018). The counts need a way from that machine into the repository without a service outside GitHub and the repository (DR-008), and the agent's commits already make that journey when they are pushed. DR-010 sent usage only inside those commits, so the calls made after the agent's last commit on a branch reached no pull request (T8). B-007 asked for a record that weighs git notes, and a commit that holds only the ledger file, as other ways for usage to reach a commit. The owner chose on 2026-11-24 the commit that holds only the ledger file, and that it signs with the person's own signer and is on unless a repository turns it off.

## Decision

Usage reaches the pull request inside the agent's own commits: when capture stages for a commit, it writes the waiting calls into a ledger file in the repository, and the commit carries it (R7). Before a top-level `git push` in the foreground, the only git command of its input, that sends the checked-out branch to a branch of its own name, a run that finds calls recorded on that branch that no commit carries, with the index free, nothing staged and no rebase, merge, cherry-pick or bisect in progress, writes them into a ledger file and commits only that file, with a message saying so (R305, R311). That commit runs no hook, starts no program that git's configuration names but the person's own signer, and takes no identity that git would guess (R312); where git asks for signed commits, it signs with the format, key and program of the person's global or system configuration, and commits nothing where the repository's own configuration or a worktree's names any of them; it is on unless the configuration file turns it off (R320). The next run takes the commit back where the push did not run and the branch's tip is still that commit, and a commit or a take-back that fails leaves HEAD, the index and the working tree as they were (R313). No usage travels on a side branch, a separate ref, a note or a service.

## Alternatives

- Git notes: notes travel on a ref of their own, which a plain `git push` does not send, a pull request does not show and a squash or a rebase leaves behind on the old commits.
- Keeping DR-010 as it stands: the calls after the agent's last commit, such as those that push and open the pull request, stay uncounted.
- Pushing a separate ref from the hook, which makes every turn a network write that can fail.
- Keeping the ledger on a side branch that is never merged, which needs a push from the hook on every turn.
- Posting the usage to a separate service from the hook, for the reason that DR-008 (Capture uses no service outside GitHub and the repository) gives.

## Consequences

- The hook makes no network write: the ledger leaves the machine only when the person's commits are pushed (DR-060).
- The calls made before a push that sends the checked-out branch reach the pull request; calls after the last push, such as opening the pull request, still reach none, as the README says (T8).
- The person's history holds small commits that they did not type, one before a push that finds calls waiting; a repository whose rules ask for a sign-off line or a message form may turn them off with `commit_before_push` in its configuration file, as the README says (R320, T314).
- Staging a file in the person's index brings capture into their git work (T10), which DR-011, DR-013, DR-014, DR-034, DR-035, DR-128, DR-129 and DR-130 answer; the commit before a push touches neither the index nor the working tree where it cannot finish (R313).
- The ledger is in the pull request's diff, where a reviewer sees it and anyone who can push to the branch can edit it (the design's risk "[A ledger edited by hand changes the reported cost]"; T16).
- DR-010 is closed, and this record holds what it decided. R7, T8, T10 and T16, which rested on it, rest on this record, and the threat model, the assumptions, the design and `docs/how-it-works.md` cite it in DR-010's place; records that name DR-010 keep their text.

## Scope

This covers the route that usage takes to the pull request. The shape of the files it travels in is DR-127 (Each commit's usage goes in a new file, written once), where calls wait is DR-011 (Recorded calls wait in the git directory), which commit takes them is DR-012 (A call goes only to a commit in its worktree, on its branch), when a file is staged is DR-013 (A ledger file is staged just before a commit that capture can follow), and the ledger staying on the default branch is DR-015 (The ledger stays in the repository as the record).

## What reversing it would change

How hard it is to reverse: reversible with work. R7, R305, R311, R312, R313 and R320 in `usage-capture` would change, with their scenarios. The `.pr-cost/` path and the ledger format are part of the public surface, so the change would be a breaking one for adopters (DR-096). The design's decisions 1, 3 and 26, the proposal's "What Changes" and "Impact", the flow in the threat model's "How data moves", the answers of T8, T10, T16 and T314, the README's summary, the parts table, the commit flow and what the tool never does in `docs/how-it-works.md`, the usage-capture and ledger feature pages, and tasks 1.2 and 2.2 would change too. DR-011, DR-012, DR-013, DR-014, DR-015, DR-017, DR-034, DR-035, DR-066, DR-127, DR-128, DR-129, DR-130 and DR-131 would be revisited.
