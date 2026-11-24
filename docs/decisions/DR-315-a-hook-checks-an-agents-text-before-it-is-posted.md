# DR-315: A hook checks an agent's text for GitHub before it is posted

- **Type:** security and privacy
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R298
- **Threats:** T65, T319
- **Replaces:** none
- **Closed by:** none

## Context

CI checks a pull request's title and body against the private patterns, but only after the text is public, and issues and comments are not checked (T65).

## Decision

`.claude/settings.json` registers a hook that runs before each tool call that opens or edits a pull request, an issue, a comment or a review on GitHub, and before each Bash command that runs `gh`, and blocks the call, naming the pattern and quoting none of the text, when its input matches a private pattern or name hash that pull request text is checked against, or holds a link to a Claude session, project or thread. It blocks a call whose input it cannot read (R298).

## Alternatives

- Relying on CI and `CLAUDE.md` alone: CI sees only a pull request's text, after it is public.

## Consequences

- A project's cloud thread runs none of the hooks that the repository's settings register (A61), so there the rule in `CLAUDE.md` and CI hold alone.
- A tool that the hook's matcher does not name is not checked.

## Scope

This covers text that an agent posts from a session here. Text in tracked files is R33's and the repository's own tests'.

## What reversing it would change

How hard it is to reverse: reversible. R298, the hook and its registration would change.
