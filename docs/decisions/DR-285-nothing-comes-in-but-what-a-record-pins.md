# DR-285: Nothing comes in from a repository or tool outside this one but what a record of its own names, pins and checks, and tests are built here

- **Type:** scope
- **Boundary:** incoming
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the owner, 2026-10-27 and 2026-11-23
- **Requirements:** R280
- **Threats:** T285, T287, T288
- **Replaces:** none
- **Closed by:** none

## Context

The repository is public and independent, and anyone can copy it (the owner, 2026-11-23). On 2026-10-27 the owner asked that nothing come into it from other repositories or tools, and that its tests be built here instead. Some things do come in from outside, each by a record of its own: the vendored Superpowers (DR-041), OpenSpec (DR-042), the GitHub actions that its workflows run (DR-068), the development tools that CI installs (DR-126), and contributions from other people's forks, under the contributor licence agreement (DR-244). Some of these were not pinned to an exact version when this was decided, as its design-stage review found: CI's newest Python, `3.x`, on purpose (DR-026), Renovate's preset `config:best-practices`, which Renovate expands when it runs (DR-265), the development tools' own dependencies, whose hashes wait for task 1.8 (DR-126), Claude Code's review commands (DR-093, DR-262), the runner image `ubuntu-latest`, which no record named, and, as the review against what was built found, Node, which CI installs by the major version alone that `.node-version` gives, and the patch releases of the oldest Python, `3.11`, neither of which any record named.

## Decision

No code, test, check, skill or text comes into this repository from another repository or tool, except what a record of its own names. Each such thing is pinned to an exact version or commit, or a record says why it is not, and CI checks what it can of it. A check that resembles one kept elsewhere is written here anew, with tests of its own. The page on how the tool works lists each thing that comes in, how it is pinned or that it is not, and the records that decide it (R280). This record names as not pinned the runner image `ubuntu-latest`, which GitHub updates, Node, which `.node-version` gives by its major version alone, and the patch releases of Python `3.11`, which `.python-version` and CI's matrix give by their minor version alone; every workflow that takes them in holds a read-only token (DR-067).

## Alternatives

- Taking checks or tests from another repository as they are: what they rest on would live outside this one, where no reader of this repository can see it, and a copy would drift from its source.
- Naming the owner's other repositories in the rule: the rule holds for anyone who copies this repository, so it names none (the owner, 2026-11-23).

## Consequences

- An addition that would bring in a new tool or repository needs a record of its own, and the tables of what comes in on the page on how the tool works cite it, which a test holds from the records' side, and from the workflows' side for each action, runner image, Python version and file of versions that a workflow names (R280; T285); any other input brought in with no record is left to review, as `CLAUDE.md` asks of agents (T288).
- An input that is not pinned can change what CI checks without a change here (T287).
- The tests of this repository are written in this repository, from its specs.

## Scope

This covers what this repository takes in from elsewhere. What the tool takes in when it runs, such as a session's transcript and GitHub's API, is DR-044 (Everything that crosses into the tool is untrusted) and the records that each of those inputs cites; how vulnerabilities in what comes in are found is DR-287.

## What reversing it would change

How hard it is to reverse: reversible with work. The table of what comes in on the page on how the tool works, R280's scenarios and T285's answer would change. Taking a check or test from elsewhere would then need its own record of where it comes from and how it is kept in step. Nothing that adopters configure or depend on changes, so the change would not be a breaking one for adopters.
