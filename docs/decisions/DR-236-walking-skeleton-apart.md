# DR-236: The walking skeleton runs apart from this repository and records only with the switch and the opt-in

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R223, R229
- **Threats:** T32, T172, T174, T178
- **Replaces:** none
- **Closed by:** none

## Context

On 2026-11-12 the owner decided that a walking skeleton, the thinnest path from a session's calls through capture and a ledger file in a commit to the report's figure, run once in a real Claude Code session, comes right after the pull request that adds the guide, and that its design is approved before it is built (DR-233). Its run comes before task 7.1, which turns the tool on in this repository only from a project that holds this repository alone, with the owner's opt-in only in that project's environment (DR-207, DR-210), while this repository's work is done from a project that also holds a private repository of the owner's (DR-207). Each of the three reviews of 2026-11-12 put the skeleton's run in a repository apart, a scratch or a throwaway one, and one of them with no capture turned on and synthetic ledger files only. The design-stage review of 2026-11-12 found two ways in which the run could record what it should not: a thinnest path that checks neither switch, reached from this repository by someone who clones it (T172), and a run in this clone, from that project, whose capture stages ledger files into this repository's commits, with counts of work on the private repository among them (T174). The threat review at design of the guide found a third: the skeleton's reusable workflow, merged here before task 4.3 makes it refuse every event but a push to the default branch, which another repository could then call from an event that gives it a write token, so that a pull request's code could run with that token (T178).

## Decision

The walking skeleton records nothing unless the repository's configuration turns the tool on and the person's own opt-in is on, as `switch-and-opt-in` gives them. Its real run happens in a repository made for it, from a project that holds no other repository, on throwaway work, and nothing reaches the skeleton through this repository's settings, its marketplace, a release or a workflow here that another repository calls, until task 4.3 gives the reusable workflow its guard on events (R229). This repository tracks no switch and no ledger file until task 7.1 turns the tool on here (R223), and keeps from the run only what the skeleton's pull request asks the owner to keep.

## Alternatives

- The run in this clone, from the project that holds this repository, which would publish here what T174 describes.
- No real run, with synthetic transcripts only, which would not meet the assumptions about Claude Code's transcripts and hooks that DR-233 brings the skeleton forward to meet.
- The bounds left wholly to the skeleton's own pull request, which would leave this record, once merged, deciding when the run comes and saying nothing of where.

## Consequences

- A test fails while this repository tracks `.pr-cost.json` or a file under `.pr-cost/` at its root before task 7.1 is ticked (R223, task 1.29).
- A test fails while a tracked workflow here declares `workflow_call` before task 4.3, which adds the reusable workflow with its guard that refuses every event but a push to the default branch, is ticked, so that a thinnest path merged here cannot be called from another repository, the skeleton's own among them, before that guard exists (R229, task 1.29, T178).
- The skeleton's pull request says where its run happened and what of it the repository keeps, and the owner approves that with its design, before it is built (DR-233).
- The opt-in for that run is set by the owner, in that project's environment, since an agent never turns capture on for anyone (DR-214).

## Scope

This covers where the walking skeleton runs and what it records. When it comes is DR-233 (A walking skeleton comes before the remaining pull requests that prepare the build), and how this repository turns the tool on at task 7.1 is DR-207 (This repository turns the tool on only from a project that holds this repository alone) and DR-210 (The owner's opt-in for this repository is set only in the environment of its own project).

## What reversing it would change

How hard it is to reverse: reversible, until the skeleton's run. The bounds are a record and a check, which one pull request can change, but a run made outside them could publish what T174 describes, which no later change takes back. R223 and R229 in `project-standards` would change, with their scenarios, and so would design decision 12, task 1.29, B-021, DR-233's bounds, and the answers of T32, T172, T174 and T178.
