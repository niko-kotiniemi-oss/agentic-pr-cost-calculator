# DR-215: The README gives no address outside this repository but those that its test lists

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R134, R201
- **Threats:** T81, T147
- **Replaces:** none
- **Closed by:** none

## Context

The README is what most people who set the tool up follow, and the addresses in it decide where they take the tool from: the repository that a calling workflow's `uses:` names, the release whose zip they upload, the README against which they check its checksum, and the repository that they add as a marketplace, whose updates then reach their sessions with nothing to accept (T132). A pull request that changed one of these, in the short start, in the folded detail or inside a command, would send people to a plugin or a workflow that is not the tool's, and a reviewer reading a large diff could miss it (T147). GitHub serves a commit that only a fork holds under this repository's address (A26), and git fetches a pull request's head, a fork's too, as `refs/pull/<number>/head` (A48), so an address on this repository that names a commit by its ID, or a pull request's ref, can name a fork's code. A line in `.gitattributes` can hide a file's diff from the review (T81).

## Decision

Every link, autolink and web address in the README, in its opening, its short start and its folded detail, prose and code alike, and every repository that it names as `owner/repo`, names a heading of the README, a file of this repository by a relative path, this repository on GitHub, or an address on a list that its test keeps, and none names a commit of this repository by its ID or a pull request's ref. The list changes only in a pull request that the owner reviews. No attribute that the repository sets hides the README's diff.

## Alternatives

- A test of the short start's links alone, as the first draft had it, which leaves the addresses in the detail and inside commands, from which people take the tool, to the review alone.
- No test, with every address left to the owner's review of each diff.

## Consequences

- A pull request that sends people elsewhere fails CI, or changes the test's list, which the owner reads as such (T147, A15).
- The README's calling workflow names no commit, and leaves its pin for the adopter to fill with the commit that a published release names (R203).
- The README's diff shows in full, as a record's does (T81).
- A copy of the README elsewhere holds whatever its owner writes, which no test here reaches (T148).

## Scope

This covers the addresses that the README gives. What the short start says is DR-212 (The README opens with a short start), and where the detail lives and how it shows is DR-213 (The README keeps its detail, folded below its short start).

## What reversing it would change

R201 in `project-standards` would change, with its scenarios, and so would R134's scenario for the README, design decision 12, task 4.4, and the answers of T81 and T147.
