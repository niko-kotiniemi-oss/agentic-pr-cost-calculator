# DR-181: Each ledger file states its format's version, and each version has a published schema

- **Type:** technical
- **Status:** accepted
- **Decided by:** the owner, 2026-11-02
- **Requirements:** R156, R158, R163, R167, R168
- **Threats:** T16, T115, T118
- **Replaces:** none
- **Closed by:** none

## Context

The ledger is the published record from which a pull request's cost is recomputed, and a newer report reads every earlier ledger format (DR-040). The owner asked on 2026-11-02 that the ledger format support independent validation and version-aware processing. Without a version in the file, a report has to infer a file's format from what its lines hold, and nobody can check a ledger file without the tool (T115).

## Decision

Each ledger file states, on its first line, the version of the ledger format that it is written in, with the file's count of refused calls and its flags (DR-180), and each entry marks whether its call was read without a stop reason or held a usage field that capture does not know. Every version names a call by the same id, the SHA-256 hash of its message id. The format is published in `docs/ledger-format.md` for every version that a release wrote, with a JSON Schema for each kind of line, written with ASCII patterns rather than `format`, and with the rules that no schema can hold listed there: a field given twice, the first line's place, the names that the price table lists and a day that the calendar does not have. The tests check, with a standard validator and its default options, that each schema refuses each line that the report refuses, but for those, and accepts each line that it counts, a property-based test compares each schema with the reader, and the surface manifest holds each released version's schema by its hash. The report reads each file by its version's rules, matching the version exactly as a whole number and choosing no code by its value, and counts as refused a file whose first line states no version, or one that it does not read, or that breaks its version's rules. It reads the default branch's earlier ledger files by the versions that they state too, and capture reads the branch's ledger files the same way, each skipping a file of a version that it does not read.

## Alternatives

- Inferring each file's format from its lines, which a line built to look like another version could mislead.
- Publishing the format as prose alone, against which nobody could check a file without writing a reader of their own.
- Checking files against the schema in the tool itself, with a library, which the rule that the tool uses the standard library alone does not allow.
- Keeping the counts of calls read without a stop reason or with an unknown field on the first line alone, which a restored or copied file would report again.

## Consequences

- Anyone can check a ledger file without the tool, against the schema of the version that it states.
- Checking the schema in CI needs a JSON Schema validator and the packages that it brings, compiled code among them, as development dependencies, added only once task 1.8 locks them by their hashes, which the tool itself never imports, as the design's decision 2 says. The owner chose on 2026-11-02 to check the schema in CI, over a validator of the project's own or no machine check.
- A schema and the report can still disagree on a line that no test holds, and then the report's rules decide (T118).
- A restored ledger file, or one that holds at least one entry, each of which the default branch already held, adds no counts and no flags.
- A report older than a ledger file's version says that it could not read the file, rather than misreading it.

## Scope

This covers how the ledger format is versioned and published. Reading earlier formats is DR-040 (A newer report reads every earlier ledger format), and what an entry holds is DR-045 (Ledger entries hold counts, never content).

## What reversing it would change

R156 and R163 in `ledger`, R158 and R168 in `report-comment` and R167 in `usage-capture` would change, with their scenarios, and so would the design's decisions 2 and 16, T115, T118, `docs/ledger-format.md`, the surface manifest, and tasks 1.2 and 4.2. The ledger format is part of the public surface, so the change would be a breaking one for adopters (DR-096).
