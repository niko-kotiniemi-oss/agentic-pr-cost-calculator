# The report comment

When a pull request merges with the tool on before its merge or after it, a workflow posts one short comment on it with what it cost.

**Status:** designed, not built yet.

**Spec:** `report-comment`

**Requirements:** R20, R94, R95, R157, R96, R65, R21, R97, R98, R23, R66, R67, R168, R24, R68, R69, R70, R35, R158, R102

## Expected behaviour

- **What it shows.** The total cost; the cost by model, by token type and by activity type; the CI minutes and their cost; the price table's date; the tool's version; how many ledger entries were counted, and how many were not, for each reason; how many calls capture refused; how many it read without a stop reason, with a note that the token cost is then a lower bound, and how many carried a usage field that capture does not know, with a note that the token cost may be low, counting those marks only on the entries that it counts. It also says when the hook file at the merged commit differs from the one at the report's own commit.
- **Calls left out.** When the pull request's ledger files say that calls were left out, for consent, for their age or because their repository could not be told, the comment says so for each reason, as what those files say, with no count, and says that the token cost, each of its parts and the total are then lower bounds. For consent, it says that capture could not show that some calls were made while it was on, and nothing of capture being off. It always says that calls that no ledger file holds are neither counted nor flagged. A restored ledger file, or one that holds at least one entry, each of which the default branch already held, adds no counts and no flags.
- **What it says about itself.** That the figure is an API-equivalent estimate, not a bill, and that it counts the usage that the pull request's commits carry and the CI runs on those commits. Calls that Claude Code's own tools make to a model, such as a web fetch's summary, are counted only where the transcript holds them.
- **Only its own words.** The comment, the job summary and the log hold numbers, the report's fixed text, and names that the price table lists. It never quotes ledger lines, file names, branch names, job names or any other text from the pull request.
- **One comment.** When the report runs again, it updates its own comment and no one else's.
- **Within bounds.** The report reads ledger files from git as data. It counts as a refused file any path that the merge adds in the ledger folder and that is not a regular file, and skips such a path among the ledger files that the default branch already held. When a pull request's ledger files are together above the documented size bound, it counts none of their entries and says they are too large to read, while still reporting the CI cost. Each ledger line that the merge adds is held to the ledger format: a line with a count that is not a whole number within the ceiling, a field given twice or unknown, nesting too deep or a day that is not a date is refused and counted, and the report completes.
- **Read by its version.** The report reads each ledger file that the merge adds by the version of the ledger format that its first line states, matched exactly as a whole number, choosing no code by its value. A file whose first line states no version or one that the report does not read, or breaks its version's rules, is counted as a refused file, and none of its entries, counts or flags is used, so that a report older than the hook says what it could not read rather than misreading it. A line shaped as a first line anywhere else is a refused line. The default branch's earlier ledger files are read by the versions that they state too, and the job summary says how many the report skipped for a version that it does not read.
- **When there is no comment.** A push that merges no pull request, or more than one, or that has more commits than the report's call budget allows, gets no comment, and the report says why in its job summary. So does a merge that finds the tool off both before it and after it: its job summary says why the configuration after the merge leaves the tool off.
- **A budget that runs short.** A pull request whose runs and jobs take more calls to read than the budget leaves still gets its comment, with its CI cost marked incomplete, as the CI minutes page says.

## How it is validated

This feature is validated first by its spec's scenarios: each gets an acceptance test before its code, seen to fail for the expected reason (task 1.4). Then come the checks that DR-084 to DR-093 and DR-109 apply to all the tool's code. Beyond those, this feature has its own:

- A property test that no planted string reaches the comment, the job summary or the log (task 4.1), and unit tests at every boundary of the ledger format, with each file read by the version that its first line states (task 4.2).
- Tests that the report refuses every event but the push that a merge makes, and that the token is in none of its outputs (task 4.3).
- End to end: this repository's own merge posts a report whose figures can be recomputed from its ledger, the price table and the jobs API (task 7.1).

## See also

- `report-comment` in `openspec/`, and design decisions 7 and 16 of `add-pr-cost-calculator`.
