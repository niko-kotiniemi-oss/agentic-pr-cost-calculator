# DR-180: A ledger file flags calls left out, with no count

- **Type:** technical
- **Status:** accepted
- **Decided by:** the owner, 2026-11-02
- **Requirements:** R155, R157
- **Threats:** T16, T27, T106
- **Replaces:** none
- **Closed by:** none

## Context

Capture now leaves out a call that it cannot show was made inside an interval when both switches were on (DR-168), or from this repository (DR-179), and the owner asked on 2026-11-02 that the incompleteness that follows be reported where appropriate. The same day the owner picked flags with no count over a count of the calls left out. A count of the calls left out, or their times, would say how much the person worked while capture was off, or on another repository, which is what leaving them out protects (T106).

## Decision

When a run leaves out a call made in this repository because it fell outside every interval, or drops a waiting call for its age (DR-175), the store keeps a flag for that reason with the call's worktree and branch and the day a run last raised it, as it keeps a waiting call, until the retention window drops it (DR-175), and the next ledger file staged for that worktree and branch says so, and no other does. When a run leaves out a call whose line gives no working directory, or whose repository could not be told from a directory inside this repository's folder (DR-179), the session's next ledger file here says so. Each is one of three flags, for consent, for age or for the repository, with no count, time or other fact about the calls left out, and a staged file's note keeps its flags, so that a take-back returns them with its calls. Calls left out because they were made in another repository raise no flag here. The report's comment says, for each flag that a pull request's ledger files raise, that those files say calls were left out, never that capture was off, and that the token cost, each of its parts and the total are then lower bounds, and it always says that calls that no ledger file holds are neither counted nor flagged.

## Alternatives

- Counting the calls left out, which would show how much is missing, and how much the person did outside consent or outside the repository.
- Saying nothing, which would present a figure that is too low as if it were whole.
- Flagging the session's next ledger file on any branch, which would put the flag on a pull request that holds none of the work left out.

## Consequences

- A reader learns that a figure is too low, not by how much.
- A flag waits for a commit in its worktree, on its branch, so one that no commit there takes is never shown, and the comment's standing sentence covers calls that no ledger file holds.
- A flag is what a pull request's ledger files say, which their author can change, as for every figure in them (T16).
- A flag says that, in some session, calls were left out for consent, for their age or because their repository could not be told, which is the least that reporting the gap can say (T106).

## Scope

This covers how the gap that left-out calls make is reported. Which calls are left out is DR-168, DR-175 and DR-179, and the ledger format that carries the flags is DR-181.

## What reversing it would change

R155 in `usage-capture` and R157 in `report-comment` would change, with their scenarios, and so would the design's decisions 1, 6, 15 and 16, T106, and tasks 1.2, 2.4 and 4.2. The flags are part of the ledger format, which is part of the public surface, so the change would be a breaking one for adopters (DR-096).
