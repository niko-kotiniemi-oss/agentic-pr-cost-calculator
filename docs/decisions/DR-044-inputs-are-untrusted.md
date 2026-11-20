# DR-044: Everything that crosses into the tool is untrusted

- **Type:** security and privacy
- **Boundary:** incoming
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R5, R14, R21, R23, R24, R35, R36, R45, R66, R67, R89, R92, R96, R97, R98, R102
- **Threats:** T6, T14, T17, T18, T23, T25, T26, T48, T49, T52
- **Replaces:** none
- **Closed by:** none

## Context

The tool reads data that others control. A session's transcript holds everything that the session saw, in every repository it worked in, possibly secrets. Whoever can push to a pull request's branch writes its ledger and the rest of its diff, the author of a pull request from a fork included, and names such as runner labels and job names come from data that contributors control (T26). The report runs in a workflow whose token can write comments, and its comment and job summary are rendered as Markdown, while GitHub reads workflow commands from its log (T52).

## Decision

The tool treats everything that crosses into it as untrusted data: the transcripts, the ledgers, what GitHub's API returns, and the pull request that it reports on.

## Alternatives

None were recorded when this was decided.

## Consequences

- Values are read strictly: whole counts within a ceiling, no entry dated after the day the report runs, and ledger lines that match the ledger format and name only listed values or `unknown` (R5, R14, R35, R98; T6, T17).
- Reading is bounded: ledger files are read from git as blobs within a size bound, and the configuration only as a regular file within its own (R23, R36, R45, R66, R67, R92; T18, T48, T49).
- A refused value or line is counted, and no line stops the report (R102).
- Nothing from the pull request is run, imported or installed (R24, T23).
- A marker in someone else's comment is input that the report does not trust, so the report updates only a comment that its own identity wrote (R96, T25).
- The comment, the job summary and the log hold only numbers, the report's own words and names that the price table lists, and the hook's standard error only its own words and numbers (R21, R89, R97; T14, T26, T52).
- Holding the ledger to its format does not show that its counts are true, so a ledger edited by hand remains an accepted risk (DR-066).

## Scope

This covers how the tool treats what it reads. What a ledger entry may hold is DR-045 (Ledger entries hold counts, never content), and how the report keeps its own code apart from the pull request it reads is DR-062 (The report runs its own pinned code).

## What reversing it would change

R5, R45 and R89 in `usage-capture`, R14 in `pricing`, in its clause that refuses an entry dated after the day the report runs and its scenario "An entry from the future is refused", R36 and R92 in `switch-and-opt-in`, and R21, R23, R24, R35, R66, R67, R97, R98 and R102 in `report-comment` would change, with their scenarios, and so would R96's clause that the report updates only a comment that its own identity wrote, with the scenario "A planted marker does not redirect the update", which holds T25's answer. So would the design's goals, the threat model's trust boundaries and the answers of the threats above, the list of what the tool never does in `docs/how-it-works.md`, the hostile fixtures of task 1.1 and the tests of tasks 2.1, 4.1 and 4.2, and DR-045, DR-062 and DR-066 would be revisited. The ledger format, which documents the bounds, and `.pr-cost.json` are part of the public surface, so a change to either would be a breaking one for adopters (DR-096).
