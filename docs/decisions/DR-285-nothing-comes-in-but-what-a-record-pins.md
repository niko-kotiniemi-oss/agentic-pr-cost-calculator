# DR-285: Nothing comes in from a repository or tool outside this one but what a record of its own names, pins and checks, and tests are built here

- **Type:** scope
- **Boundary:** incoming
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the owner, 2026-10-27 and 2026-11-23
- **Requirements:** R280
- **Threats:** T284
- **Replaces:** none
- **Closed by:** none

## Context

The repository is public and independent, and anyone can copy it (the owner, 2026-11-23). On 2026-10-27 the owner asked that nothing come into it from other repositories or tools, and that its tests be built here instead. Some things do come in from outside, each by a record of its own: the vendored Superpowers (DR-041), OpenSpec (DR-042), the GitHub actions that its workflows run (DR-068) and the development tools that CI installs (DR-126).

## Decision

No code, test, check, skill or text comes into this repository from another repository or tool, except what a record of its own names, pins to an exact version or commit, and has CI check. A check that resembles one kept elsewhere is written here anew, with tests of its own. The page on how the tool works lists each thing that comes in, with the records that decide it (R280).

## Alternatives

- Taking checks or tests from another repository as they are: what they rest on would live outside this one, where no reader of this repository can see it, and a copy would drift from its source.
- Naming the owner's other repositories in the rule: the rule holds for anyone who copies this repository, so it names none (the owner, 2026-11-23).

## Consequences

- An addition that would bring in a new tool or repository needs a record of its own, and the table of what comes in on the page on how the tool works cites it, which a test holds (R280; T284).
- The tests of this repository are written in this repository, from its specs.

## Scope

This covers what this repository takes in from elsewhere. What the tool takes in when it runs, such as a session's transcript and GitHub's API, is DR-044 (Everything that crosses into the tool is untrusted) and the records that each of those inputs cites; how vulnerabilities in what comes in are found is DR-287.

## What reversing it would change

How hard it is to reverse: reversible with work. The table of what comes in on the page on how the tool works, R280's scenarios and T284's answer would change. Taking a check or test from elsewhere would then need its own record of where it comes from and how it is kept in step. Nothing that adopters configure or depend on changes, so the change would not be a breaking one for adopters.
