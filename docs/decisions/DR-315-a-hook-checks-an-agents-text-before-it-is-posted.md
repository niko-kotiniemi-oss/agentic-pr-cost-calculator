# DR-315: A hook checks an agent's text for GitHub before it is posted

- **Type:** security and privacy
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R298, R316
- **Threats:** T65, T319
- **Replaces:** none
- **Closed by:** none

## Context

CI checks a pull request's title and body against the private patterns, but only after the text is public, and issues and comments are not checked (T65).

## Decision

`.claude/settings.json` registers, with `onFailure` set to `block`, a hook that runs before each Bash command and each `mcp__*` tool call, and blocks the call, naming the pattern and quoting none of the text, when any string of its input, at any depth, matches a private pattern or name hash that pull request text is checked against, or holds a link to, or an identifier of, a Claude session, project or thread. It blocks a call whose input it cannot read, or on any error of its own (R298). It also checks the files that a command names for what it posts, the messages of commits and tags and of the commits that a push sends, and blocks a `gh` command whose text comes from an expansion that it cannot resolve (R316).

## Alternatives

- Relying on CI and `CLAUDE.md` alone: CI sees only a pull request's text, after it is public.

## Consequences

- A project's cloud thread, and a cloud session with several repositories, runs none of the hooks that the repository's settings register (A61), so there the rule in `CLAUDE.md` and CI hold alone.
- A browser tool that types into a page is not read, and every Bash command and `mcp__*` call meets the hook, which the build keeps quick.
- The hook uses the private patterns that task 1.14 moves into one shared module, so task 1.62 builds it after task 1.14.

## Scope

This covers text that an agent posts from a session here. Text in tracked files is R33's and the repository's own tests'.

## What reversing it would change

How hard it is to reverse: reversible. R298, the hook and its registration would change.
