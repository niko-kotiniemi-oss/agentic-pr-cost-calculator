# DR-244: Outside contributions are welcome, and one merges only once its author has agreed to a contributor licence agreement

- **Type:** process
- **Boundary:** incoming
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-16
- **Requirements:** none
- **Threats:** T33, T34, T37, T61
- **Replaces:** DR-115
- **Closed by:** none

## Context

DR-115 let anyone open an issue or a pull request, with contributions licensed under the MIT licence. DR-242 puts the repository's work under the Fair Core License with MIT as its future licence, and on 2026-11-16 the owner chose that licence together with a contributor licence agreement. A contribution licensed under the repository's licence alone does not let the licensor also offer it under other terms, such as in a paid version, so a contribution merged before its author agrees to more cannot be offered that way without asking them again. No contribution from outside the project has been merged so far. The repository is public (DR-243), so anyone can open an issue or a pull request in it, and agents working here read what others wrote (see the threat model's boundary 7). A pull request from a fork runs this repository's CI with code its author chose (T37), and a session started on an unmerged branch loads that branch's instructions and hooks (T34).

## Decision

Anyone may open an issue or a pull request. A pull request from outside the project is merged only once its author has agreed to the contributor licence agreement that backlog item B-023 brings, and until that item is done, none is merged.

## Alternatives

- Merging outside pull requests under the repository's licence alone, as DR-115 allowed under MIT: each one would stay out of a paid version unless its author agreed again later.
- Closing the repository to outside pull requests: issues and proposals would still come, but the welcome that DR-115 gave would go, and with it the contributions that the fair source licence still allows.

## Consequences

- Contributions come under the contributing guide, `CONTRIBUTING.md`, and the code of conduct, `CODE_OF_CONDUCT.md`, which DR-116 (The repository carries the usual open-source files) adds.
- `CONTRIBUTING.md` says how a change gets made, from an issue for a new feature to the checks, under the rules in `CLAUDE.md`, that contributions are licensed under the repository's licence, and that a contribution from outside the project waits for the contributor licence agreement.
- Every issue starts from a template, since blank issues are off, and a security problem goes to private reporting instead (`.github/ISSUE_TEMPLATE/config.yml`, `SECURITY.md`).
- A bug report is public the moment it is posted, before any check can read it. Its form opens with a required checkbox that it holds nothing private, and a reporter who ticks it and still pastes private text is not caught (T61).
- Issue text, pull request text and review comments, from anyone, are data and never instruct an agent, which rests on `CLAUDE.md` alone (T33).
- An outside pull request is reviewed from `main`, never by starting a session on its branch (T34), and its CI runs with a read-only token and no secrets (T37).
- The owner decides merges, so no check holds the wait for the agreement until B-023 adds one, and until then it rests on the owner's review.
- An agent never copies code or text from a pull request, issue or comment by someone outside the project into a change until its author has agreed to the agreement, as `CLAUDE.md`'s section on outside contributions says, since an agent's commits are authored as the owner's and would carry outside work in unmarked.
- What DR-115's last section named was read again. `CONTRIBUTING.md` changes with this record. `CODE_OF_CONDUCT.md`, the issue templates, the README's section on working on the repository and `CLAUDE.md`'s section on outside contributions still hold as they are. T33, T34, T37 and T61 come with text and code from outside the project, which still arrive as before, so their ratings stay, and the threats and assumptions that cited DR-115 cite this record. DR-078 (Outside contributors' workflows wait for approval), DR-081 (Outside pull requests are reviewed from `main`), DR-082 (Records and issue text are data, never instructions) and DR-237 (Data and issue text never instruct, and the guide steers below `CLAUDE.md` and the skills' steps), which names DR-115 among the records that it assessed, still hold. DR-116 still holds, as DR-242 says.

## Scope

This covers who may contribute, under which rules, and when an outside contribution may merge. The terms that its author agrees to are backlog item B-023 (A contributor licence agreement), and the licence is DR-242. How an outside pull request is reviewed is DR-081 (Outside pull requests are reviewed from `main`), when an outside contributor's workflows run is DR-078 (Outside contributors' workflows wait for approval), why issue and pull request text never steers an agent is DR-082 (Records and issue text are data, never instructions), and the files themselves, the code of conduct with the Contributor Covenant that it follows among them, are DR-116 (The repository carries the usual open-source files).

## What reversing it would change

How hard it is to reverse: reversible. Dropping the wait would change `CONTRIBUTING.md` and B-023, and a contribution merged without the agreement could not be offered under other terms without its author's later agreement. Closing the repository to contributions instead would change `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, the issue templates, the README's section on working on the repository and `CLAUDE.md`'s section on outside contributions, and T33, T34, T37 and T61 would be rated again.
