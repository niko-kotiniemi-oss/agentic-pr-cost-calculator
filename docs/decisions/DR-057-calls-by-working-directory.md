# DR-057: Calls are kept by the session's working directory

- **Type:** security and privacy
- **Boundary:** incoming
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R3
- **Threats:** T2
- **Replaces:** none
- **Closed by:** none

## Context

A transcript belongs to a session, not to a repository, and one session can work in several, such as a public one and a private one (T2). A line's working directory is Claude's current directory, not where a call worked (see the design's context). So a session whose current directory is in this repository, and that also works on another one, such as a private one, through paths or with a `cd` inside a command, records those calls here. No rule over a transcript's working directories can tell them apart, and telling them apart by reading what each call did would mean reading commands, which can do anything.

## Decision

Capture keeps a call for this repository when the working directory that its transcript line names is in this repository, meaning that its git common directory is this repository's: a worktree counts, and a separate repository nested inside the folder does not. It keeps such a call even when the call worked on another repository.

## Alternatives

- Telling the calls that work on another repository apart by reading what each call did, which was not chosen for the reason that the context gives.

## Consequences

- Such calls reach this repository's ledger and comment, with their counts and models, as the design's risk "[A session whose current directory is in the repository also works on another one, through paths or with a `cd` inside a command]" says. This is a residual (the threat model's T2), and the README says that work on other repositories, private ones above all, belongs in sessions of its own.
- A session that works from a folder that contains the repository records nothing, so its figure is too low, as the design's risk "[A session works from a folder that contains the repository]" says.
- A person who finds such calls in a ledger file can remove the file (DR-055), though a pushed file stays in git history (T2).

## Scope

This covers which calls capture keeps by what their transcript lines name, not which repository is this one, the one that holds the project directory (R76). Which worktree and branch a kept call goes to is DR-012 (A call goes only to a commit in its worktree, on its branch), and whose sessions are recorded at all is DR-046 (Each person turns on capture of their own sessions).

## What reversing it would change

R3 in `usage-capture` would change, with its scenarios, and so would the design's decision 1 and its risks, T2's answer and residual, the README's warning, `SECURITY.md`, which states the rule, the proposal's impact, the `usage-capture` feature page, and tasks 1.1, 2.1 and 4.4, whose fixtures, filter and README text carry it.
