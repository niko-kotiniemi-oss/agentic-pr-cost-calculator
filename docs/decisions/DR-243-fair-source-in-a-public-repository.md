# DR-243: The tool is fair source, in a public repository

- **Type:** scope
- **Status:** accepted
- **Decided by:** the owner, 2026-11-16
- **Requirements:** none
- **Threats:** T32, T61, T65
- **Replaces:** DR-114
- **Closed by:** none

## Context

DR-114 made the tool open source, developed in a public repository that anyone can read and adopt. Adopters copy its hook file from a pinned commit (DR-022) and call its reusable workflow from a workflow of their own, and they run the hook on their own machines and the report in their own CI (see the threat model's boundary 6), where the hook reads their sessions' transcripts. DR-242 puts the repository's work under the Fair Core License, version 1.0, with MIT as its future licence, which restricts a Competing Use and so is not an open source licence by the Open Source Initiative's definition. Fair.io lists it among the fair source licences. On 2026-11-16 the owner chose to keep all of the tool's code public, in one repository, the features of a later paid version among it.

## Decision

The tool is fair source: all of its source, any paid feature's included, is public in a public repository that anyone can read and adopt, under the licence that DR-242 gives, and the tool is not called open source while that licence holds.

## Alternatives

- Open source, as DR-114 had it: it needs a licence that the Open Source Initiative approves, which DR-242 does not choose.
- Open core, with the paid features in a closed add-on beside a public tool: the users of the paid version could not read what it runs.
- A private repository whose source only customers see: no one else could check what the hook does with the transcripts that it reads before adopting it.

## Consequences

- Anyone can read every line that the hook and the report run, so an adopter can check what capture records before turning it on.
- The README's opening and the opening sentence of `CLAUDE.md` call the tool fair source, and neither calls it open source.
- Anyone can open a pull request here, and agents working here read what others wrote (see the threat model's boundary 7; DR-244).
- Anything that reaches the repository is published, so it holds no session transcript or identifier, no cost figure from private work, no internal name and no secret. A test checks tracked files and their path names for the private references it knows, and a reference it does not know rests on whoever writes it (DR-069; T32).
- Pull request text is public as soon as it is posted. The CI job that task 1.14 adds checks a pull request's title and body for private references only after that, and issues and comments are not checked (T65).
- Vulnerabilities are reported privately, through the repository's Security tab, never in a public issue (`SECURITY.md`; DR-077).
- What DR-114's last section named was read again. `LICENSE`, the README's opening and its section on the licence, `CONTRIBUTING.md` and the opening sentence of `CLAUDE.md` change with DR-242 and this record. `SECURITY.md` and the section on privacy of `CLAUDE.md` still hold as they are, since the repository is still public. The threat model's boundary 7 and the risks of T32, T61 and T65 rest on everything here being public, which still holds, so their ratings stay, and the threats and assumptions that cited DR-114 for that cite this record. DR-069 (The public repository holds no private data) and DR-077 (Private vulnerability reporting is on) still hold. DR-099 is closed by DR-242, and DR-115 by DR-244, as those records say, and DR-116 still holds, as DR-242 says. DR-118 (The tool is named `agentic-pr-cost-calculator`) and DR-157 (The tool is a component that other repositories take in), which name DR-114 for the repository being public, still hold, since it still is. DR-189 (An organization mode, in which capture cannot be turned off, is left to a later change), which calls the tool an open-source product that people opt in to, and DR-218 (A roadmap says what is now, next and later), which calls it an open-source project that others help to prioritise, still hold for what they decide, since both rest on the source being public and open to feedback, which this record keeps.

## Scope

This covers that the tool and its repository are open for everyone to read, and what the tool is called. The licence is DR-242 (The licence is the Fair Core License, with MIT as its future licence), contributions from outside are DR-244 (Outside contributions are welcome, and one merges only once its author has agreed to a contributor licence agreement), the files the repository carries are DR-116 (The repository carries the usual open-source files), and what the repository may hold is DR-069 (The public repository holds no private data).

## What reversing it would change

How hard it is to reverse: reversible with work. Making the tool open source again needs an open source licence, which would close DR-242, and the README's opening, the opening sentence of `CLAUDE.md` and `CONTRIBUTING.md` would change. Making the repository private instead would change `SECURITY.md`, the section on privacy of `CLAUDE.md`, the threat model's boundary 7 and the risks of T32, T61 and T65, and would reach every adopter, who takes the hook file and the reusable workflow from this repository; DR-069, DR-077, DR-116 and DR-244 would be revisited. No requirement's text would have to change.
