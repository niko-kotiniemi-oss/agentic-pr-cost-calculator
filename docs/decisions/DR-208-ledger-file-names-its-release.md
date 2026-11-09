# DR-208: Each ledger file names the release that wrote it, and the comment says when it is later than the report's

- **Type:** technical
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R156, R193, R195
- **Threats:** T136
- **Replaces:** none
- **Closed by:** none

## Context

A repository pins the report's release in its calling workflow and copies the hook file of the same release, so that the hook and the report share a price table and a ledger format, and the report says when the hook file in the merged commit differs from its own (DR-139). The plugin follows the person's account instead (DR-203), so in a project's cloud thread, where only the plugin runs, every ledger file comes from a release that the repository did not pin. The pinned report refuses a line that names a model that only a later price table lists, and every file of a later ledger format (DR-040), and the comment's only explanation, a hook file from another commit, does not apply there. A ledger file's first line states its format's version (DR-181), not the release that wrote it.

## Decision

Each ledger file's first line states, beside the ledger format's version, the release of the capture step that wrote it. When a ledger file that a merge adds names a later release than the report's own, the comment says that some ledger files come from a later release than the report, so that lines or files that the report cannot read may be refused, and quotes nothing from them. The README says that the plugin's release, not the repository's pinned report, writes the ledger files of the sessions that run it, and that a repository keeps its pin current and a person keeps their plugin current.

## Alternatives

- Counting a well-formed model name that the report's table does not list as `unknown`, in tokens and not in cost, which would let a later plugin's calls count where the report cannot price them, but would also count a name that a hand-edited ledger file makes up; it can come in a later change.
- Saying nothing, which would leave a reader with refused lines and no reason that applies.
- Refusing ledger files of a later release, which would refuse the work of everyone whose plugin moved first.

## Consequences

- The release that wrote a ledger file is published with it, which tells no more about the person than their commit does.
- A pull request whose ledger files come from a later plugin gets a comment that says why some lines may be refused, without quoting them (T136).
- The release is part of the ledger format from its first version, which no release has written yet, so its schema and the report's reader hold the first line's field from the start.

## Scope

This covers what a ledger file says about the release that wrote it, and what the comment says of it. How the ledger states its format's version is DR-181, how the report reads each version is DR-040, and how an earlier copy leaves a session to a later one is DR-206 (Two copies of the capture step in one session share the store).

## What reversing it would change

R156 in `ledger` and R193 in `report-comment` would change, with their scenarios, and so would R195 in `project-standards`, the ledger format and its schemas, the design's decisions 7 and 16, T136, and the README's section on installing the plugin.
