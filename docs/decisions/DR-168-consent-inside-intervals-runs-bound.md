# DR-168: Consent holds for each call, inside intervals that runs begin and end

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-02
- **Requirements:** R40, R108, R109, R144, R165, R166
- **Threats:** T38, T104
- **Replaces:** DR-047
- **Closed by:** none

## Context

A person's usage is published only with their consent (DR-046), which the design's goals ask to hold for each call. Each run reads a transcript on from where the last one stopped, and a run that finds a switch off records nothing, so the calls made while capture was off would be read by the next run that finds both switches on (T38). DR-047 held consent for each call, but let a session's interval begin at the session's start when its first run found both switches on, so a person who opted in during a session, before its first run, had the session's earlier calls recorded.

The owner asked on 2026-11-02 that no call made before an opt-in be recorded, that the boundary of consent be a conservative one, that `SessionStart` be considered for it without being depended on, and that a call be left out, with the gap reported, whenever capture cannot establish that it was made while consent held. In the transcripts examined for the design, the line that a call's first line names as its parent was sometimes written after that first line, while the first line up that chain of parents that gives a prompt or a tool result was always in the same transcript and written before it (see the design's context).

## Decision

Consent holds for each call, not only for the run that records it, as DR-047 decided. Capture records only the calls made inside one of their session's intervals when both switches were on, and an interval begins and ends at a run: it begins only at a run that finds both switches on while the session has no open interval, never at the session's start, and it ends at its last run before one that finds either switch off or a change to the files that hold the person's opt-in (DR-169). A call counts as made inside an interval only when, by each line's own time, the line it answers, the nearest up its first line's chain of parents in the same transcript that gives the person's prompt, a tool's result or a compaction's summary, was written at or after the run that began the interval and no later than the call's first line, and that first line no later than the interval's last run. A run reads again, from the earliest line that a call not yet recorded may answer, the lines that earlier runs read, so that a call is placed by the line it answers whichever run read that line, and a run whose clock reads earlier than its session's last run, or than the time that a line it has read gives, ends each of that session's intervals and places no call inside any of them. Every other call is left out. A run that finds the person's capture off ends every session's interval and withholds the calls made before it, as DR-047 decided.

## Alternatives

- Keeping DR-047's interval from the session's start, which records the earlier calls of a person who opts in during a session, before its first run.
- Taking the line that a call's first line names as its parent, which can be a line that Claude Code writes after the call's first line, so that a call already being made when its interval began would count as inside it.
- Taking the order of the lines in the file, which can lag behind the conversation.
- Placing a call only by a line that the same run read, which would leave out a call whose answered line an earlier run read, as when a run stops between a tool's result and the call that answers it.
- Trusting each line's time whatever the clock did, which would let a clock set back between two runs place a call made while capture was off inside an earlier interval.
- Registering `UserPromptSubmit` as well, which would add a run to every prompt that the person sends, for a gain only to sessions that get no start run (DR-172).

## Consequences

- A session's first turn is recorded only when a run, such as its start run (DR-172), began the interval before the turn's prompt was written. Where the person opts in during a session, or a session gets no start run, the calls before its first run that finds both switches on are left out, so the count is too low, and its next ledger file says so (DR-180).
- The rule rests on Claude Code writing the line that a call answers before the call's first line, in the same transcript, and on each line's time coming from the clock that the runs read, which no test may check, since no test may reach Claude Code. A clock set back between two runs costs the calls made between them, and one set back and forward again between two runs, which no run sees, can still place a call inside an earlier interval (T104).
- Each run reads again the lines that a call not yet recorded may answer, which its time budget counts, so a line too long for what a run has left after them is skipped as one refused call (R90, R165).
- An opt-out withholds only what no commit has taken yet, and a ledger file that was pushed stays published (DR-182).

## Scope

This covers which calls the switches let through. The switches are DR-021 (One file, `.pr-cost.json`, turns the tool on or off) and DR-046 (Each person turns on capture of their own sessions). What ends an interval between runs is DR-169, what a run that finds a switch off writes is DR-170, what an opt-out removes from the store is DR-171, and take-backs, which run whatever the switches say (R110), are DR-014 (A ledger file that no commit took is taken back).

## What reversing it would change

R40, R108, R109, R144 and R166 in `switch-and-opt-in` and R165 in `usage-capture` would change, with their scenarios, and so would the design's decision 6 and its risks on opting in during a session and on the clock, T38's answer and residual, T104, the `switch-and-opt-in` feature page, the capture flow in `docs/how-it-works.md`, and tasks 1.1 and 2.4. The intervals are in the store, whose format is part of the public surface, so the change would be a breaking one for adopters (DR-096).
