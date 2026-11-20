# DR-116: The repository carries the usual open-source files

- **Type:** process
- **Boundary:** outgoing
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-20
- **Requirements:** none
- **Threats:** T61, T62
- **Replaces:** none
- **Closed by:** none

## Context

The repository is public, and anyone may contribute to it (DR-114, DR-115). The README, the licence and the security policy came with the proposal, in the first commit of `add-pr-cost-calculator`, and the proposal counts the standard files of an open-source project among what the change adds (see the proposal's "Impact").

## Decision

The repository carries the files an open-source project is expected to have: a README, a licence, a contributing guide, a code of conduct, a security policy, a changelog, issue and pull request templates, code owners and an editor configuration. Its code of conduct follows the Contributor Covenant, version 2.1.

## Alternatives

None were recorded when this was decided.

## Consequences

- `tests/test_repository.py` lists every one of these files among those it requires, fails when one is missing, and checks that `LICENSE` is the MIT licence (task 1.12).
- The bug report form opens with a required checkbox that the issue holds no transcript, session identifier, token, private name or usage figure from private work, and a test holds that the box is required (T61).
- The feature request template suggests a scenario in WHEN and THEN form, which helps a request become a requirement, and the pull request template carries a checklist.
- `.github/CODEOWNERS` describes the owner's review of every change while code-owner review stays off, so the file states a rule and is not a control (T62).
- No test reads which code of conduct `CODE_OF_CONDUCT.md` follows, so that rests on review.
- `.editorconfig` keeps editors writing files the way the checks expect, and `CHANGELOG.md` follows the form that Keep a Changelog describes (DR-149).

## Scope

This covers which of these files the repository carries. The licence chosen is DR-099 (The licence is MIT), how the changelog is written is DR-098 (The changelog is kept by hand), its form and the version that `pyproject.toml` holds are DR-149 (`pyproject.toml` holds the version, and the changelog has one entry per release), private vulnerability reporting is DR-077 (Private vulnerability reporting is on), and code-owner review is DR-075 (Code-owner review is off).

## What reversing it would change

The files themselves would change, the Contributor Covenant that the code of conduct follows among them, and so would `REQUIRED_FILES` and the tests of the bug form in `tests/test_repository.py`, task 1.12, the proposal's "Impact", the README's links to the guide, the code of conduct, the security policy and the changelog, and the steps in `CONTRIBUTING.md` that use the templates. T61's answer, which the bug form holds, and T62's, which cites the code-owners file, would change too, and DR-075, DR-077, DR-098, DR-099, DR-115 and DR-149 would be revisited. None of these files is part of the public surface, so the change would not be a breaking one for adopters.
