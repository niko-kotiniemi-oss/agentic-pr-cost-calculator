# DR-209: A release is published only once its files are attached and checked

- **Type:** technical
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R72, R189
- **Threats:** T69, T139
- **Replaces:** none
- **Closed by:** none

## Context

Each release carries the bill of materials (DR-097) and the plugin's zip, whose SHA-256 the README gives (DR-203). GitHub publishes a release when it is created, unless it is created as a draft, and its files are attached by separate calls after that. Releases here are immutable (DR-074), so a published release cannot take a file later, and a job that fails between creating a release and attaching its files leaves a published release without them, whose tag is locked, and whose version people cannot install from a zip.

## Decision

The release workflow creates each release as a draft, attaches its plugin's zip and its bill of materials, downloads each attached file again and checks its size and SHA-256 against the file that it built, and only then publishes the release. When an attachment fails or differs, the release stays a draft, the workflow fails and names the file, and nothing is published.

## Alternatives

- Creating the release and then attaching its files, the order that GitHub's API offers by default, which leaves a published release without its files whenever an attachment fails.
- Attaching the files without checking them again, which would trust the upload to have stored what the workflow built.

## Consequences

- A published release always carries the zip whose checksum its README gives and the bill of materials that names it (T69, T139).
- A failed release leaves a draft, which the owner deletes before the next attempt, with its tag, since a refused tag's version is not used again (DR-204).
- The tests hold the order of the workflow's calls against recorded responses, since no test may reach GitHub.

## Scope

This covers when a release is published. How a release is made is DR-148 (Each release is made from a tag), what its bill of materials names is DR-097, and why a published release cannot change is DR-074 (Releases are immutable).

## What reversing it would change

R189 in `releases-and-compatibility` would be removed, with its scenarios, and R72 would change, and so would the design's decision 11, T69, T139, the release workflow and task 6.3.
