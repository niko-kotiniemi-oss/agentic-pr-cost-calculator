# DR-115: Outside contributions are welcome

- **Type:** process
- **Status:** closed
- **Decided by:** the owner, 2026-10-18
- **Requirements:** none
- **Threats:** T33, T34, T37, T61
- **Replaces:** none
- **Closed by:** DR-244

## Context

The repository is public (DR-114), so anyone can open an issue or a pull request in it, and agents working here read what others wrote (see the threat model's boundary 7). A pull request from a fork runs this repository's CI with code its author chose (T37), and a session started on an unmerged branch loads that branch's instructions and hooks (T34).

## Decision

Anyone may open an issue or a pull request.

## Alternatives

None were recorded when this was decided.

## Consequences

- Contributions come under the contributing guide, `CONTRIBUTING.md`, and the code of conduct, `CODE_OF_CONDUCT.md`, which DR-116 (The repository carries the usual open-source files) adds.
- `CONTRIBUTING.md` says how a change gets made, from an issue for a new feature to the checks, under the rules in `CLAUDE.md`, and contributions are licensed under the MIT licence.
- Every issue starts from a template, since blank issues are off, and a security problem goes to private reporting instead (`.github/ISSUE_TEMPLATE/config.yml`, `SECURITY.md`).
- A bug report is public the moment it is posted, before any check can read it. Its form opens with a required checkbox that it holds nothing private, and a reporter who ticks it and still pastes private text is not caught (T61).
- Issue text, pull request text and review comments, from anyone, are data and never instruct an agent, which rests on `CLAUDE.md` alone (T33).
- An outside pull request is reviewed from `main`, never by starting a session on its branch (T34), and its CI runs with a read-only token and no secrets (T37).

## Scope

This covers who may contribute and under which rules. How an outside pull request is reviewed is DR-081 (Outside pull requests are reviewed from `main`), when an outside contributor's workflows run is DR-078 (Outside contributors' workflows wait for approval), why issue and pull request text never steers an agent is DR-082 (Records and issue text are data, never instructions), and the files themselves, the code of conduct with the Contributor Covenant that it follows among them, are DR-116 (The repository carries the usual open-source files).

## What reversing it would change

`CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, the issue templates and the README's section on working on the repository would change, and so would `CLAUDE.md`'s section on outside contributions. T33, T34, T37 and T61, whose risks come with text and code from outside the project, would be rated again. DR-078, DR-081 and DR-082 would be revisited, and so would DR-116, whose files include the guide, the code of conduct and the templates. No requirement's text would have to change.
