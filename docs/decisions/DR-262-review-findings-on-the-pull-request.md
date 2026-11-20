# DR-262: Each review lane's findings and then their resolutions go on the pull request as comments of their own, under one index comment

- **Type:** process
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-27 and 2026-11-04
- **Requirements:** none
- **Threats:** T65, T229
- **Replaces:** none
- **Closed by:** none

## Context

Before the owner merges a change, a context apart from the builder's reviews it in four lanes, `/simplify`, `/security-review`, `/code-review` and `/verify`, and every finding is fixed or answered with the reason (DR-093). On 2026-10-27 the owner asked for a review's findings to go on the pull request, followed by their resolutions and by an index of every open point, since a summary in the pull request's description does not show what each finding was or how it was dealt with, and on 2026-11-04 for this to happen lane by lane, with an issue for each finding that is deferred. Backlog item B-003 asks for a rule that says so, with its record, in a file that agents load. A pull request's comments are public, though, and the review of a later change can find a vulnerability in code that a release already holds, which `SECURITY.md` asks to be reported privately rather than in a public issue, and a finding of a vulnerability in the change's own code, deferred to an issue, would describe it in public while the next release shipped the code (T229). The comments are also more public text that agent sessions write as the owner's account, and no check of a pull request's text reads them (T65).

## Decision

Each review lane posts its findings on the pull request as a comment of its own, and, once they are dealt with, their resolutions as another, saying how each was fixed, answered with its reason or deferred. One index comment lists every point that is still open. A finding that is deferred gets a GitHub issue. A finding of a vulnerability in code that a release holds is never posted: the agent tells the owner, as `SECURITY.md` asks. A finding of a vulnerability is never deferred to an issue either: it is fixed in the change, or the agent tells the owner. The lanes are Claude Code's own commands of those names, not a skill of the same name from another repository, the person, an organization or a plugin. The comments follow the rules that hold for a pull request's text, so that they carry no link to a session, project or thread, or any identifier from one, and no private reference (T65). The root `CLAUDE.md` gives this rule in its section on every change, and the rule on a finding of a vulnerability in its section on what an agent never does here.

## Alternatives

- Findings and resolutions summarised in the pull request's description: the owner asked for more, since a summary leaves out what each finding was and how it was dealt with.
- One comment for all the lanes: a lane's findings could not be read and answered before the next lane runs, and a long comment hides which finding is still open.
- A finding of a vulnerability posted like any other: a public comment or issue would tell everyone of a flaw in a release before its fix ships.
- A finding of a vulnerability in the change's own code deferred like any other: its issue would tell everyone of a flaw that the next release ships.

## Consequences

- Each pull request's review leaves on GitHub what each lane found and how each finding was dealt with, which the owner reads before the merge, and an issue for each point deferred.
- More text that agent sessions write as the owner's account is public, held only by the rules on public text and by the agent reading each post back (T65).
- A vulnerability in released code reaches the owner and no public page, and one in the change's own code is fixed before the merge or reaches the owner, never a public issue.

## Scope

This covers how a review's findings and their resolutions are reported. That every change is reviewed in a context apart from the builder's is DR-093 (Every change is reviewed in a separate context before it merges), and that public text carries no link to a session is DR-070 (Public text carries no link to a Claude session).

## What reversing it would change

How hard it is to reverse: reversible. The rule is a sentence of the root `CLAUDE.md`, and the comments already posted stay on their pull requests. The answers of T65 and T229 would change.
