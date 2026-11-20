# DR-060: The hook opens no network connection

- **Type:** security and privacy
- **Boundary:** incoming
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R30, R45, R111
- **Threats:** T45
- **Replaces:** none
- **Closed by:** none

## Context

The hook runs on the machine of the person whose session it records, and reads that session's transcripts there. Git, in a partial clone, goes to the remote for an object that a command needs and the clone lacks, a ledger blob included (see the design's context), and such a fetch could wait on a credential helper or a slow remote until the hook's time budget is spent (T45). A network guard inside the Python process would not see a connection that a git subprocess makes (T45).

## Decision

The hook opens no network connection, neither itself nor through the git commands that it starts.

## Alternatives

None were recorded when this was decided.

## Consequences

- Each git command that the hook starts runs with `GIT_NO_LAZY_FETCH=1` and `GIT_TERMINAL_PROMPT=0`, so that none of them fetches what the clone lacks or asks for credentials (R111). In a partial clone, capture then skips a ledger file whose blob is missing, as it skips one above the size bound (R45, T45).
- Nothing leaves the person's machine through the hook. The ledger leaves it only in the person's own commits, when they push, as `docs/how-it-works.md` says.
- A network guard in the tests holds the hook to this (R30, task 1.13), and task 2.1 runs the tests against a partial clone and checks that no git command started a fetch.

## Scope

This covers every connection that the hook could open, its git commands' included. That capture as a whole uses no service outside GitHub and the repository is DR-008 (Capture uses no service outside GitHub and the repository), and that no test uses the network is DR-090 (No test uses the network). The report's connections, to GitHub's API and by git, are outside it.

## What reversing it would change

R30 in `project-standards` would change, with its scenario "The hook opens no connection", and so would R111 and R45 in `usage-capture`, with their scenarios "Capture fetches no ledger file that its clone lacks" and "Capture skips a ledger file whose blob its clone lacks", the design's decision 1, T45's answer, the table of connections and the list of environment variables in `docs/how-it-works.md`, the `usage-capture` and `project-standards` feature pages, and tasks 1.13 and 2.1.
