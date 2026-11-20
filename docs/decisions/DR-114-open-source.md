# DR-114: The tool is open source, in a public repository

- **Type:** scope
- **Boundary:** outgoing
- **Reversibility:** one-way door
- **Status:** closed
- **Decided by:** the owner, 2026-10-17
- **Requirements:** none
- **Threats:** T32, T61, T65
- **Replaces:** none
- **Closed by:** DR-243

## Context

The tool is for teams that build pull requests with AI coding agents (DR-001). They adopt it by copying its hook file from a pinned commit (DR-022) and calling its reusable workflow from a workflow of their own (see the design's decision 7), and they run the hook on their own machines and the report in their own CI (see the threat model's boundary 6).

## Decision

The tool is open source, and it is developed in a public repository that anyone can read and adopt.

## Alternatives

None were recorded when this was decided.

## Consequences

- The tool is released under the MIT licence, and every contribution comes under it (DR-099; `CONTRIBUTING.md`).
- Anyone can open a pull request here, and agents working here read what others wrote (see the threat model's boundary 7).
- Anything that reaches the repository is published, so it holds no session transcript or identifier, no cost figure from private work, no internal name and no secret. A test checks tracked files and their path names for the private references it knows, and a reference it does not know rests on whoever writes it (DR-069; T32).
- Pull request text is public as soon as it is posted. The CI job that task 1.14 adds checks a pull request's title and body for private references only after that, and issues and comments are not checked (T65).
- Vulnerabilities are reported privately, through the repository's Security tab, never in a public issue (`SECURITY.md`; DR-077).

## Scope

This covers that the tool and its repository are open to everyone. The licence is DR-099 (The licence is MIT), contributions from outside are DR-115 (Outside contributions are welcome), the files an open-source project carries are DR-116 (The repository carries the usual open-source files), and what the repository may hold is DR-069 (The public repository holds no private data).

## What reversing it would change

`LICENSE`, the README's opening and its section on the licence, `CONTRIBUTING.md`, `SECURITY.md`, and the opening and the section on privacy of `CLAUDE.md` would change. So would the threat model's boundary 7 and the risks of T32, T61 and T65, which rest on everything here being public. Adopters take the hook file and the reusable workflow from this repository, so the change would reach every adopter. DR-069, DR-077, DR-099, DR-115 and DR-116 would be revisited. No requirement's text would have to change.
