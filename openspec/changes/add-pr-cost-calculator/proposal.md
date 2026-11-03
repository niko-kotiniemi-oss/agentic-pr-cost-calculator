# Proposal

## Why

Teams that build pull requests with AI coding agents can see what a pull request changed, but not what it cost. The tokens a session spent and the CI minutes its pushes used are recorded in different places, in raw form, and nobody adds them up per pull request. A trial on real Claude Code sessions confirmed that the data exists: each session's transcript records per-message token usage by model, and GitHub's jobs API gives each CI job's start and end times. What's missing is a tool that collects it while the work happens and reports it when the pull request merges.

## What Changes

- A capture step for Claude Code, run by session hooks. It records each model call's token counts, model, price attributes, UTC day and activity type, and adds them to the agent's own commits as small usage ledger files. It records only calls made while the session's working directory is in the repository, and only for people who have turned it on for themselves. It records counts only, never prompts, code, tool names or transcript text.
- A dated price table in this repository, for model tokens by type and for GitHub Actions minutes by runner. A cost uses the price that applied on the day the usage happened.
- A cost step that turns the ledger and the CI jobs that ran on the pull request's own commits into a cost per model, per token type, per activity type and in total, applying the price modifiers the price table lists.
- A report at merge: one short comment on the pull request, posted by a workflow that runs on the push a merge makes to the default branch. The usage ledger stays in the repository as the pull request's record, and the report writes nothing else.
- A switch in one configuration file that turns the tool on or off for a repository. The report reads it from before the merge as well as after, so a pull request cannot turn off its own report.
- Code is Python, standard library only, supporting Python 3.11 and every later release, with synthetic test fixtures. It is delivered as a session hook script and a GitHub Actions workflow other repositories can use.
- A threat model, `docs/threat-model.md`, which every later change revisits. Each threat's answer is a scenario in these specs wherever it can be one, so an acceptance test holds it.
- Each threat rated for impact and likelihood, from 1 to 3, with a risk matrix, and the threat model revisited by an independent review at design and again at implementation (design decision 9).
- Releases by semantic version from a tag, each with a CycloneDX bill of materials, and dependency updates that keep the oldest supported Python unless it nears its end of life or a security fix needs a newer one (design decisions 10 and 11).
- Documentation that names everything the tool does: a register of the requirements, a page per feature that names its spec's requirements and says how the feature is validated, and a page explaining the tool as a whole, with its flows, credentials, permissions and connections, each checked against the specs and the workflows (design decision 12).
- A record of each decision in `docs/decisions/`, with an index: one choice per record, typed, with who decided it and the requirements and threats it shapes, so that each decision can be reversed or replaced on its own. Once the default branch holds a record, it is never edited, only closed by the record that replaces it, after which lines of its text may become `[removed]` (design decision 13).
- The assumptions that the design rests on, in `docs/assumptions/`, listed with the most at stake first, each with its impact beside its risk, what rests on it and what changes if it is wrong, and each of its facts with how it is checked, in a form that a reader can follow; and a glossary, `docs/glossary.md`, that gives the words the specs and pages use, with a test that fails on a word it says to avoid. Both describe, and never steer (design decision 14).
- A golden set of synthetic sessions, whose ledger entries and figures are worked out by hand from the specs, which every version must reproduce before it is released, and whose figures change only with the spec that gives them (design decision 14).
- Verification that tests everything that can be tested: acceptance tests first, property-based tests, full branch coverage, mutation testing, every check shown to fail, and a review in a separate context before merge (design decision 8).

## Capabilities

The tool is one product made of nine capabilities, each one spec. Seven are the features that turn a pull request's work into its cost, one is what the tool runs on and how it is released, and one holds the standards for the whole product. Each has a page in `docs/features/` that names its requirements and says how it is validated, and `docs/how-it-works.md` shows how they fit together.

### New Capabilities

- `switch-and-opt-in`: the file that turns the tool on or off for a repository, and each person's own opt-in to having their sessions recorded.
- `usage-capture`: recording what an agent session spent, model call by model call, onto the branch it worked on.
- `activity-types`: labelling each recorded call with the kind of work it was part of.
- `ledger`: the files that carry the counts to the pull request and stay in the repository as its record.
- `pricing`: the dated price table, and how token usage becomes a cost.
- `ci-minutes`: the cost of the GitHub Actions minutes that the pull request's own commits used.
- `report-comment`: the one comment a merged pull request gets, and the trusted code that computes it.
- `releases-and-compatibility`: the Python and git versions the tool supports, how its dependencies move, and its releases with their bill of materials.
- `project-standards`: what holds for the whole product: documentation that names everything the tool does, the tool's connections, rated threats, pull request text without private references, pinned actions, a record of each decision, the assumptions that the design rests on, the words its documents use, and a golden set of its figures.

### Modified Capabilities

None. This repository has no specs yet.

## How the outcome is validated

Every capability is validated first by its scenarios. Task 1.3 traces each scenario to a test. Task 1.4 writes an acceptance test for each scenario whose code is still to be written, before that code, each seen to fail for its expected reason, and names in its test each scenario that a check already in place holds. The checks of design decision 8 then hold all the tool's code: full branch coverage and mutation testing (task 1.5), the network guard (task 1.6), property-based tests for its invariants, and end-to-end tests of the whole flow (task 4.5). Beyond those, each capability has its own:

| Capability | Validated beyond its scenarios by |
|---|---|
| `switch-and-opt-in` | tests of each way a repository could opt a person in (task 2.4), and of the switch read from before and after the merge (task 4.1) |
| `usage-capture` | fixtures in each shape Claude Code writes (task 1.1), property tests (task 2.1), tests against real git (task 2.2), the hook run in each shell its registered command meets (task 2.3), and what the README's section on adopting the tool says about git, tested with the runner's git and with git 2.43 (task 4.4) |
| `activity-types` | fixtures with each kind of tool call and with tools of several types (task 1.1), and the tests of the classification itself (task 2.5) |
| `ledger` | the format written down first, with a secret scanner's check (task 1.2), boundary tests on the report's side (task 4.2), and one fixture per released format (task 6.4) |
| `pricing` | checks on every price row (task 3.1), and property tests that a cost is never negative and adds up (task 3.2) |
| `ci-minutes` | recorded API responses for each way a pull request can merge (task 3.3) |
| `report-comment` | a property test that no planted string reaches its outputs (task 4.1), tests that it refuses every other event and never shows its token (task 4.3), and the end-to-end run on this repository's own merge (task 7.1) |
| `releases-and-compatibility` | the version checks already in place (task 1.11), the capture step's floors (task 6.5), a CI job with git 2.43, the oldest git that CI tests (task 4.4), and the release check and bill of materials (tasks 6.1 to 6.3) |
| `project-standards` | the documentation, threat model, workflow and decision record tests already in place (tasks 1.10, 1.12 and 1.16 to 1.18), the checks of connections, pull request text and pins (tasks 1.13 to 1.15), the checks of the assumptions and of the glossary's words (tasks 1.19 and 1.20), the golden set (task 1.21), the release's test job (task 6.3), and the check of what the code reads (task 5.3) |

The change as a whole succeeds when:

- the threat model has been reviewed independently at design (task 1.10) and again against what was built (task 5.2);
- every finding of a review in a context separate from the builder's is fixed or answered (task 5.1);
- the documentation says what was built, and names every network call and environment variable the code reads (task 5.3);
- this repository's own merge posts a report whose figures can be recomputed from its ledger, the price table and GitHub's jobs API (task 7.1);
- and the owner has reviewed and merged it, since nothing merges because an AI reported success.

## Impact

- New: the standard files of an open-source project (a README, a licence, a security policy, a contributing guide, a code of conduct, a changelog, issue and pull request templates, code owners and an editor configuration), a release workflow, the requirements register, the feature pages, the page explaining the tool, the decision records with their index, the assumptions and the glossary.
- New: a hook file for Claude Code, a single file that an adopter copies from the commit that their workflow pins, a reusable GitHub Actions workflow, a price table, the threat model, the golden set, and their tests.
- Development tools added with the first code: coverage.py, Hypothesis, mutmut, and detect-secrets, which checks that a ledger file does not look like a secret to a common scanner, pinned like the others.
- A repository that adopts the tool gains a configuration file, the ledger files that each pull request's commits add, which stay after merge as the record, and a workflow of its own that runs on pushes to the default branch and calls the tool's reusable workflow, granting it only `pull-requests: write` to comment, `actions: read` to read job times and `contents: read` to read the ledger.
- Each person whose sessions should be recorded turns capture on in their own global git configuration. A call made while the session's working directory is in the repository is recorded there even when it works on another repository, so work on other repositories belongs in sessions of its own.
- Agents other than Claude Code are out of scope for this change. The ledger format is documented, so other agents can write it later.
- Shell commands sent through Claude Code's PowerShell tool, as on Windows, are out of scope too: the hooks are registered for Bash, so a commit or a change of branch made through that tool is not seen. The hooks that run when a turn or a session ends still run there, and the registered command is written to exit with success in PowerShell too.
- The cost of AI review on the pull request by an app or a job in CI is out of scope for this change too, as the owner decided on 2026-10-18 and 2026-10-27. A later change can add it once it is known where that usage can be read. A review that the agent runs in its own session is recorded like its other calls.
- Repository and CI services other than GitHub, such as GitLab or Gitea, are out of scope for this change too, as the owner decided on 2026-10-27.
