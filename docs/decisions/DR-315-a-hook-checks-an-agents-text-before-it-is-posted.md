# DR-315: A hook checks an agent's text for GitHub before it is posted

- **Type:** security and privacy
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-24
- **Requirements:** R298, R316, R322
- **Threats:** T65, T319
- **Replaces:** none
- **Closed by:** none

## Context

CI checks a pull request's title and body against the private patterns, but only after the text is public, and issues and comments are not checked (T65). A project's cloud thread, and a cloud session with several repositories, runs none of the hooks that the repository's settings register (A61), and the owner chose on 2026-11-24 that the hook also ships as a plugin, so that those sessions are guarded too.

## Decision

`.claude/settings.json` registers, with `onFailure` set to `block`, a hook that runs before each Bash command and each `mcp__*` tool call, and blocks the call, naming the pattern and quoting none of the text, when any string of its input, at any depth, matches a private pattern or name hash that pull request text is checked against, or holds a link to, or an identifier of, a Claude session, project or thread. It blocks a call whose input it cannot read, or on any error of its own (R298). It also checks the files that a command names for what it posts, the messages of commits and tags and of the commits that a push sends, and blocks a `gh` command whose text comes from an expansion that it cannot resolve (R316).

The hook also ships as a plugin of its own, from a folder of this repository that the marketplace loading Superpowers into its sessions lists and `.claude/settings.json` enables, built by a script as a zip that `CONTRIBUTING.md` says to add to a project's settings; a test holds its script, patterns, matcher and `onFailure` to the repository hook's (R322).

## Alternatives

- Relying on CI and `CLAUDE.md` alone: CI sees only a pull request's text, after it is public.
- The repository's hook alone, with the owner accepting that a project's cloud threads go unguarded: most sessions that work here are such threads.

## Consequences

- A cloud session with several repositories runs the plugin through `enabledPlugins`, and a project's cloud thread runs it once the owner adds its zip in the project's settings (A61, A69); a thread that started before, or a zip older than the patterns, leaves the rule in `CLAUDE.md` and CI to hold alone.
- A browser tool that types into a page is not read, and every Bash command and `mcp__*` call meets the hook, which the build keeps quick.
- The hook uses the private patterns that task 1.14 moves into one shared module, so task 1.62 builds it after task 1.14.

## Scope

This covers text that an agent posts from a session here. Text in tracked files is R33's and the repository's own tests'.

## What reversing it would change

How hard it is to reverse: reversible. R298, R322, the hook, the plugin and their registrations would change.
