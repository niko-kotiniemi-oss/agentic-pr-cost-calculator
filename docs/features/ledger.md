# The ledger

The ledger is a set of small files under `.pr-cost/ledger/` that the agent's commits add. It carries the counts to the pull request, and after the merge it stays on the default branch as the pull request's record, so that every reported cost can be recomputed.

**Status:** designed, not built yet.

**Spec:** `ledger`

**Requirements:** R4, R156, R163, R77, R10, R56, R57, R22, R58, R59, R119, R60

## Expected behaviour

- **One file per commit,** named `.pr-cost/ledger/<YYYY-MM>/<random>.jsonl`, one line per call after a first line that states the file's format. Each file is written once and never changed by the tool.
- **The first line.** It states the version of the ledger format that the file is written in, the number of calls that capture refused, and three flags, one for each reason that capture left calls out: for consent, for their age, or because their repository could not be told. A flag says only that calls were left out, with no count, time or other fact about them. Each entry after it marks whether its call was read without a stop reason, or held a usage field that capture does not know, so that the report counts those marks only on the entries that it counts.
- **Counts, never content.** A line holds no prompt, response, code, file contents, tool name, tool input or output, path, working directory, branch name, user name, session identifier, transcript path, `tool_use_id` or time of day, nor a hash of any of them. The model's name and the price attributes are the only text taken from a transcript, and each is recorded only when the price table lists it, or else as `unknown`.
- **A published format.** Each version of the format is published in `docs/ledger-format.md` with a JSON Schema for each kind of line, so that anyone can check a ledger file without the tool, and what no schema can hold, such as a field given twice, is listed beside it, where the report's rules decide. A ledger file holds nothing that its version's schema does not allow, and a released version's schema never changes. Every version names a call by the same id, the SHA-256 hash of its message id, so that a call is counted once whichever versions its entries are in.
- **The record.** The ledger stays in the repository after the merge, and the report writes nothing to the repository.
- **Counted once.** The report counts only the ledger files that the merge adds, and each call at most once: identical entries for one call count once, and entries for one call that differ are all refused. A ledger file that the pull request removes or changes is flagged in the comment and not counted, and a ledger file that a revert brings back is counted as restored, not again.
- **Visible in review.** A pull request's ledger files are in its diff like any other file. Removing a ledger file before the merge removes its calls from the cost.
- **What stays published.** A ledger file that was pushed stays in its branch's history, in every clone and fork that holds it, and in the report comments already posted, whatever its author does later: an opt-out, a removed ledger file or a removed store changes none of them. A ledger file in a commit not yet pushed is published by that commit's push, opt-out or not, and a force-push that drops a commit does not remove what GitHub keeps for the pull requests that referenced it.
- **What a hash does not hide.** An entry names its call by a hash of the call's message id, and that does not hide whose record it is: the commit that adds the ledger file names its author, and whoever holds the transcript can match each hash to its call.

## How it is validated

This feature is validated first by its spec's scenarios: each gets an acceptance test before its code, seen to fail for the expected reason (task 1.4). Then come the checks that DR-084 to DR-093 and DR-109 apply to all the tool's code. Beyond those, this feature has its own:

- The format is written down first, and the tests read its values from that document (task 1.2).
- Each version's schema checked with a standard JSON Schema validator and its default options, refusing each line that the report refuses, but for what no schema can hold, and accepting each line that it counts, with a property-based test that finds no line that the schema and the report's reader judge apart (task 1.2), and the surface manifest holding each released version's schema by its hash, so that a change to one fails the checks (task 6.1).
- Property tests that no planted string reaches a ledger file's contents or its path (task 2.1), and a check that a ledger file raises no finding from a common secret scanner (task 1.2).
- Unit tests at every boundary of the format on the report's side (task 4.2), and one fixture for each released format (task 6.4).

## See also

- `ledger` in `openspec/`, and design decisions 3 and 16 of `add-pr-cost-calculator`.
- `docs/ledger-format.md`, which task 1.2 writes, for the exact format.
