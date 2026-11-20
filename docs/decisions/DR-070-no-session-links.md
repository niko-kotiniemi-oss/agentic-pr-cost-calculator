# DR-070: Public text carries no link to a Claude session

- **Type:** security and privacy
- **Boundary:** outgoing
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-20
- **Requirements:** R33
- **Threats:** T32, T65
- **Replaces:** none
- **Closed by:** none

## Context

Tooling that opens pull requests can put into their public title or body a link to the session, project or thread it ran in, with its identifiers, and anyone can read such text as soon as it is posted (T65). Commit messages stay in the repository's history, where a private reference is part of T32.

## Decision

No commit, pull request text, issue or comment in this repository links to a Claude session, project or thread, and none carries an identifier taken from one. Where a tool adds such a link anyway, the tool is overridden: the text is read back after it is posted, and the link is taken out.

## Alternatives

None were recorded when this was decided.

## Consequences

- The private patterns that `tests/test_repository.py` checks tracked files against include a session's link, a commit trailer that names a session, the identifiers of threads and projects, and the path of a project's files. Under R33, CI runs the same patterns over each pull request's title and body (task 1.14), and task 1.9 runs them over the message of each commit that a pull request adds (T32).
- Issues and comments are not checked, and a pull request's text is checked only after it is public (T65's residual).
- A link taken out after posting stays in the text's edit history (T65).

## Scope

This covers links to, and identifiers from, Claude sessions, projects and threads in the repository's public text. Other private data, in tracked files, history and releases as well, is DR-069 (The public repository holds no private data).

## What reversing it would change

The line on such links in the section "What an agent never does here" of `CLAUDE.md` would change, and so would R33 in `project-standards`, which checks pull request text against the same patterns as tracked files, the session patterns in `tests/test_repository.py`, tasks 1.9 and 1.14, and the answers of T32 and T65. DR-069 would be revisited.
