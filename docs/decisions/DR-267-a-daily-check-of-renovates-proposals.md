# DR-267: A daily check fails when an update is overdue or Renovate has been quiet for five days

- **Type:** technical
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-20
- **Requirements:** R263
- **Threats:** T238, T239, T240, T241, T242, T243, T244, T245
- **Replaces:** none
- **Closed by:** none

## Context

Renovate opened no pull request in this repository from 2026-11-09 until the owner turned it on again on 2026-11-20, while updates that had passed its wait of 14 days were left unproposed, and nothing told the owner: the dependency dashboard simply stopped changing. Backlog item B-024 asks for a check that warns the owner when Renovate seems to have stopped. The owner's first example was a warning after five days with no updates. Such quiet is normal when nothing new is released, or when releases are still inside the wait, and the dashboard changes only when its content does, so an update that Renovate should already have proposed and has not is a signal that only a stop gives. On 2026-11-20 the owner chose both signals, and confirmed 3 days of grace after the wait and a failed run, with a read-only token, as the way the check reports.

## Decision

A workflow runs every day and on demand and fails, naming each finding, when a minor or patch release of a tool that `requirements-dev.txt` or `package.json` pins is newer than its pin, was published more than 17 days before, and no pull request of Renovate's proposes it or a later version in its major line, or when Renovate itself, by the pull requests that it opened and the commits that it authored, has done nothing for more than 5 days, and when it cannot read what it needs (R263). Only Renovate's own acts count: a design-stage review found that the time at which a pull request or an issue last changed moves for anyone's merge, comment or ticked box, so that the owner's merge of a pull request of Renovate's on 2026-11-18 would have hidden the stop. Its token reads only. A failed scheduled run is what reaches the owner, and its summary lists the findings and says which signal each comes from.

## Alternatives

- Five quiet days alone, the owner's first example: it warns in normal quiet weeks, and cannot tell a stop from a week with nothing to propose.
- The overdue update alone, with a long backstop of 30 days for the tools that the registries do not cover: proposed in the design, and the owner chose the five days in its place.
- An issue opened or updated by the check: more visible than a failed run, but it needs `issues: write`, a write permission that CI here does not hold (DR-067).
- Running Renovate itself in CI and comparing what it would propose: it needs a token for GitHub's lookups and runs a large program with the workflow's token, for a question that the registries answer directly.

## Consequences

- A warning reaches the owner only as GitHub reports a failed scheduled run, to the user who last changed the workflow's schedule by GitHub's documentation, and by the owner's notification settings, so the build includes a run started by hand that fails on purpose, and the owner confirms once that the notice of a failed scheduled run reaches them.
- Runs fail while Renovate works too: when its limit on pull requests an hour holds an update past the grace, as it held an update of pytest on 2026-11-20, in a week with nothing to propose, and when a registry or GitHub is briefly out. The summary names the signal of each finding so that the owner can tell them apart (T242).
- The GitHub Actions that the workflows pin and the vendored Superpowers are covered by the five quiet days alone.
- The check's 14 days are held to the wait that `renovate.json` sets by a test, so that a change to one fails CI until the other follows.
- GitHub turns off a scheduled workflow in a public repository after 60 days without activity, which the check cannot report on itself.

## Scope

This covers how the repository learns that Renovate has stopped. What Renovate proposes and merges is DR-265 (Renovate proposes no newer development Python, merges nothing on its own, and notes how an update of OpenSpec or Superpowers is refreshed), and how long it waits is the owner's configuration that DR-111 and DR-028 rest on.

## What reversing it would change

How hard it is to reverse: reversible. The check is one workflow and one script, held by R263 and its tests, and removing them takes away the answers of T238 to T241 with them.
