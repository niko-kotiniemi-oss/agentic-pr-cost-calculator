# DR-196: CI compares the test's reading of the specs with OpenSpec's

- **Type:** process
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-09
- **Requirements:** R178
- **Threats:** T124, T127
- **Replaces:** none
- **Closed by:** none

## Context

`tests/test_spec_form.py` reads each spec as the release of OpenSpec that `package-lock.json` pins reads it (DR-193), so it holds the specs' form only while the two read a spec alike. The pull request that moved the pin from 1.14.0 to 1.14.1, merged on 2026-11-02, changed `package.json`, `package-lock.json` and the seven skills that the new release writes, so its diff showed nothing of how the new release reads a spec. That reading has changed: the code of 1.14.1 says that it reads specs in nested folders to close a loss of specs on archiving, issue 1353 of OpenSpec's repository, and that it fails a longer requirement that a change adds, so that the change's validation catches it before archiving, issue 1976. DR-113, written on 2026-10-27 while the pin was 1.14.0, said that OpenSpec reported a longer requirement only as information, which does not hold of 1.14.1. A defect in the test's own reader would pass unseen in the same way, since the defects that the test plants show only that it fails what it reads as a defect.

## Decision

`scripts/verify-openspec.sh`, which CI's `openspec` job runs, compares the test's reading of the specs with the pinned OpenSpec CLI's: the specs and the changes that each reads, and, for each requirement, in order, its operation in a change, its name, its text and its scenarios' names and lines, as the CLI lists and shows them. It fails naming the spec and the first difference, on a call of the CLI that fails or prints JSON in another form than the comparison reads, naming the call and what the CLI said, and when it compares no requirement. The comparison is written in Python and tested in pytest on the CLI's recorded output, since the job that runs pytest installs no Node.

## Alternatives

- Recording as a fact of A32 that the pinned release reads specs as the test does, checked once on the planted specs, which a later release could make false with nothing to say so.
- Reading the release notes of each new release in the pull request that moves the pin, which rests on notes that may leave a change in reading out.
- Reading every spec through the CLI's JSON alone, which gives no reading of a line that OpenSpec leaves out, such as one that a fence hides, and so cannot fail on it.

## Consequences

- A release of OpenSpec that reads a spec otherwise than the test, or a defect in the test's reader, fails CI in the pull request that brings it, so the pin's own pull request shows it (T124).
- The comparison runs only in the `openspec` job, where the CLI is installed, and its own tests run in the `python` job on recorded output, so that each difference that it fails on is planted and shown to fail without the CLI. A test fails when the recording is of another release than the one that `package-lock.json` pins, so the pull request that moves the pin records the CLI's output again, and the recording leaves out the folder that the CLI ran in and the times at which it found each change last changed. The comparison asks the CLI to list the changes by name, which it otherwise lists by those times, so that the recording made again is the same (T127).
- What the CLI shows of a requirement is the text that OpenSpec reads, so the comparison holds DR-194's measure too.
- A change that the CLI does not show fails the comparison, such as one whose folder holds no `proposal.md`, which `show` refuses though the validation reads its specs, so a change's proposal comes before its specs, as `/openspec-propose` writes them. So does a folder in `openspec/changes/` whose name starts with a dot, which the CLI lists as a change, though its validation skips it and the test does not read it as one, and so does a change's spec from which the test reads no requirement, since the CLI shows a change's specs only by their requirements.

## Scope

This covers the comparison of the test's reading of the specs with the pinned CLI's. The test and the form that it holds is DR-193 (A test of the repository's own holds the specs' form), the plain text of the specs is DR-195 (The specs hold only text that GitHub shows as it is), and the pin and the regeneration of OpenSpec's skills is DR-042 (OpenSpec is pinned and its skills are regenerated in CI).

## What reversing it would change

R178 in `project-standards` would change, with its scenarios, and so would task 1.24, `scripts/verify-openspec.sh`, the design's decision 12, T124, T127 and A32. A release of OpenSpec that read specs otherwise than the test would again pass CI unseen.
