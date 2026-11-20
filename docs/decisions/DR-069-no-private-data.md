# DR-069: The public repository holds no private data

- **Type:** security and privacy
- **Boundary:** outgoing
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-17 and 2026-10-18
- **Requirements:** R33, R72
- **Threats:** T32, T61, T65, T69, T77
- **Replaces:** none
- **Closed by:** none

## Context

The repository is public: anyone can open a pull request, and anyone can read an issue as soon as it is posted (T61). The tool works close to private data: a transcript holds everything its session saw, possibly secrets (the threat model's first trust boundary), and the fixtures copy the shapes that Claude Code writes (task 1.1). Usage records, transcripts, identifiers or private names could end up in a tracked file, in a fixture, in a commit message or in the history (T32), and tooling that opens pull requests can add identifiers to their public text (T65).

## Decision

The repository holds no transcripts of sessions or their identifiers, no internal names, no secrets and no cost figures measured on someone's private work. Its only real usage records are its own ledger files, once task 7.1 turns the tool on here with the owner's opt-in, and its tests use synthetic fixtures. A test checks every tracked file for the private references that the repository knows, and the same check is extended to the messages and files of each commit that a pull request adds (task 1.9), to each pull request's title and body (R33), and to each release's bill of materials and text (R72, T69).

## Alternatives

None were recorded when this was decided.

## Consequences

- The check finds only the references it knows. One it does not know gets through, and so does one in a file that is not UTF-8, which the check skips; the author answers for those (T32's residual).
- The check holds the private names as SHA-256 hashes, so that its list publishes none of them, and catches a two-word name however it is separated.
- Issues and comments are not checked, and a pull request's text is checked only once it is public (T65's residual). The bug report form has the reporter confirm that the issue holds no private data, which nothing can check before it is posted (T61).

## Scope

This covers what the repository, its pull requests, its issues and its releases hold. What the tool publishes in an adopting repository is DR-045 (Ledger entries hold counts, never content), and session links in public text are DR-070 (Public text carries no link to a Claude session). The bill of materials that the private-reference check reads on each release is DR-097 (Each release carries a bill of materials).

## What reversing it would change

R33 in `project-standards` would change with its scenarios, and so would R72 in `releases-and-compatibility`, in its clause on the private-reference check and its scenario "A private reference in a release stops it". So would what `CLAUDE.md`, `CONTRIBUTING.md`, `SECURITY.md`, the pull request template's last checkbox and the bug report form say of private data, the private-reference checks and the form's test in `tests/test_repository.py`, tasks 1.1, 1.9, 1.14 and 6.3, and the answers of T32, T61, T65, T69 and T77. DR-070 would be revisited.
