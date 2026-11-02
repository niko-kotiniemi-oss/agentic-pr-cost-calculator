# DR-181: Each ledger file states its format's version, and each version has a published schema

- **Type:** technical
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-02
- **Requirements:** R156, R158
- **Threats:** T115
- **Replaces:** none
- **Closed by:** none

## Context

The ledger is the published record from which a pull request's cost is recomputed, and a newer report reads every earlier ledger format (DR-040). The owner asked on 2026-11-02 that the ledger format support independent validation and version-aware processing. Without a version in the file, a report has to infer a file's format from what its lines hold, and nobody can check a ledger file without the tool (T115).

## Decision

Each ledger file states, on its first line, the version of the ledger format that it is written in, with the file's counts and its flags (DR-180). The format is published in `docs/ledger-format.md` for every version that a release wrote, with a JSON Schema for each kind of line, and the tests check that each schema refuses each line that the report refuses and accepts each line that it counts. The report reads each file by its version's rules, and counts as refused a file whose first line states no version, or a version that it does not read.

## Alternatives

- Inferring each file's format from its lines, which a line built to look like another version could mislead.
- Publishing the format as prose alone, against which nobody could check a file without writing a reader of their own.
- Checking files against the schema in the tool itself, with a library, which the rule that the tool uses the standard library alone does not allow.

## Consequences

- Anyone can check a ledger file without the tool, against the schema of the version that it states.
- Checking the schema in CI needs a JSON Schema validator as a development dependency, which the tool itself never imports, as the design's open questions say.
- A report older than a ledger file's version says that it could not read the file, rather than misreading it.

## Scope

This covers how the ledger format is versioned and published. Reading earlier formats is DR-040 (A newer report reads every earlier ledger format), and what an entry holds is DR-045 (Ledger entries hold counts, never content).

## What reversing it would change

R156 in `ledger` and R158 in `report-comment` would change, with their scenarios, and so would the design's decision 16, T115, `docs/ledger-format.md`, and tasks 1.2 and 4.2. The ledger format is part of the public surface, so the change would be a breaking one for adopters (DR-096).
