# The ledger

The ledger is a set of small files under `.pr-cost/ledger/` that the agent's commits add. It carries the counts to the pull request, and after the merge it stays on the default branch as the pull request's record, so that every reported cost can be recomputed.

**Status:** designed, not built yet.

**Spec:** `ledger`

**Requirements:** R4, R156, R163, R77, R10, R56, R57, R22, R58, R59, R119, R60

## Expected behaviour

- **One file per commit,** named `.pr-cost/ledger/<YYYY-MM>/<random>.jsonl`, one line per call. Each file is written once and never changed by the tool.
- **Counts, never content.** A line holds no prompt, response, code, file contents, tool name, path, branch name, user name, session identifier or time of day. The model's name and the price attributes are the only text taken from a transcript, and each is recorded only when the price table lists it, or else as `unknown`.
- **The record.** The ledger stays in the repository after the merge, and the report writes nothing to the repository.
- **Counted once.** The report counts only the ledger files that the merge adds, and each call at most once: identical entries for one call count once, and entries for one call that differ are all refused. A ledger file that the pull request removes or changes is flagged in the comment and not counted, and a ledger file that a revert brings back is counted as restored, not again.
- **Visible in review.** A pull request's ledger files are in its diff like any other file. Removing a ledger file before the merge removes its calls from the cost.

## How it is validated

This feature is validated first by its spec's scenarios: each gets an acceptance test before its code, seen to fail for the expected reason (task 1.4). Then come the checks that DR-084 to DR-093 and DR-109 apply to all the tool's code. Beyond those, this feature has its own:

- The format is written down first, and the tests read its values from that document (task 1.2).
- Property tests that no planted string reaches a ledger file's contents or its path (task 2.1), and a check that a ledger file raises no finding from a common secret scanner (task 1.2).
- Unit tests at every boundary of the format on the report's side (task 4.2), and one fixture for each released format (task 6.4).

## See also

- `ledger` in `openspec/`, and design decision 3 of `add-pr-cost-calculator`.
- `docs/ledger-format.md`, which task 1.2 writes, for the exact format.
