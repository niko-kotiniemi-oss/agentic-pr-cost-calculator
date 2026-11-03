## Purpose

Keep the tool usable on the Python and git that adopters already have, raise the oldest supported Python and take major updates only on the owner's decision, and release it in versions whose numbers say what an adopter must do, each with a bill of materials.

Scenarios below that run the capture step follow the conventions that `usage-capture` states for its own scenarios.

## ADDED Requirements

### Requirement: The tool runs on the oldest supported Python and on every later release

The hook and the report SHALL run on Python 3.11, the oldest version this change supports, and on every later release, with the standard library only. CI SHALL run the tests on the oldest supported version and on the newest release.

#### Scenario: The tests run on the oldest supported Python

- **WHEN** CI runs on a pull request
- **THEN** the tests run on Python 3.11 and on the newest Python release, and the `ci` check fails if either fails

#### Scenario: Code that needs a newer Python fails on the oldest

- **WHEN** a change uses a feature of the standard library or of the language that Python 3.11 lacks
- **THEN** CI fails on the oldest version's job, or ruff or mypy reports it

#### Scenario: A CI matrix without the newest release fails a test

- **WHEN** the CI matrix lacks the newest Python release
- **THEN** a test fails and names the CI matrix

### Requirement: Every copy of the oldest supported Python agrees with its one source

`requires-python` in `pyproject.toml` SHALL be the one source of the oldest supported version (see "The tool runs on the oldest supported Python and on every later release"): a test SHALL fail when any other copy of it disagrees, among them the versions that ruff and mypy check against, the CI matrix, `.python-version`, the bill of materials, the hook's own guard, and the documents that state it.

#### Scenario: Declared versions that disagree are reported

- **WHEN** a setting or a document names an oldest supported Python other than the one `requires-python` gives, or the CI matrix lacks the oldest version
- **THEN** a test fails and names the copy that differs

### Requirement: The oldest supported Python and major updates change only on the owner's decision

The oldest supported Python SHALL rise only when its version nears its end of life, or when a security fix needs a newer one, and the change SHALL be recorded as a decision with its reason. Dependency updates SHALL be proposed freely for minor and patch versions and for vulnerability fixes, and a major update SHALL wait for the owner's approval on Renovate's dependency dashboard.

#### Scenario: A major update waits for the owner

- **WHEN** Renovate finds a major update of a dependency or a pinned tool
- **THEN** it lists the update on the dependency dashboard and opens no pull request until the owner approves it there

#### Scenario: A minor or patch update is proposed

- **WHEN** Renovate finds a minor or patch update that has been out for the wait the configuration sets
- **THEN** it opens a pull request without waiting for approval

#### Scenario: A vulnerability fix is not held back

- **WHEN** Renovate finds an update that fixes a known vulnerability, whatever its type
- **THEN** it opens a pull request without waiting for approval or for the release age

### Requirement: Releases are made from a tag that matches the version and the changelog

A release SHALL be made only by pushing a tag `vMAJOR.MINOR.PATCH` that names a commit in the default branch's first-parent history, and the release workflow SHALL check the tag's form before any other step, and SHALL refuse a tag whose version differs from the version in `pyproject.toml` or that has no entry in `CHANGELOG.md`. The release's own text SHALL name the tag and the commit in the workflow's fixed words, and SHALL carry the changelog entry after them.

#### Scenario: A tag that matches the version and the changelog is released

- **WHEN** a tag `v1.2.0` is pushed for a commit on the default branch whose `pyproject.toml` says `1.2.0` and whose changelog has an entry for `1.2.0`
- **THEN** a GitHub release `v1.2.0` is published that names the commit and carries the changelog entry

#### Scenario: A tag that does not match the version is refused

- **WHEN** a tag `v1.2.0` is pushed for a commit whose `pyproject.toml` says another version, or whose changelog has no entry for `1.2.0`
- **THEN** no release is published and the workflow says which of the two disagrees

#### Scenario: A tag on a commit outside the default branch's first-parent history is refused

- **WHEN** a release tag names a commit that is not in the default branch's first-parent history, such as a commit from inside a merged pull request or one that only a fork holds
- **THEN** no release is published

#### Scenario: A tag that is not a semantic version stops the workflow first

- **WHEN** a pushed tag is not `v` followed by a semantic version, such as one holding shell characters
- **THEN** the workflow fails before any other step and publishes nothing

### Requirement: Versions are semantic, and their numbers say what an adopter must do

The version SHALL raise its major number for a change that existing adopters must act on, which is any change to the public surface (see "The public surface is kept in a manifest"). It SHALL raise its minor number for a change that adds behaviour without breaking any part of that surface, and its patch number for a fix alone. A changelog entry that lists a breaking change SHALL come with a raised major number and a `### Breaking` section.

#### Scenario: A breaking change raises the major version

- **WHEN** the changelog entry for a release lists a breaking change and the release does not raise the major number over the previous release
- **THEN** no release is published and the workflow says why

### Requirement: The public surface is kept in a manifest

The public surface SHALL be the hook file's registration, by the events and matchers it names and its command's form, not the checksum that the command carries, and the hook file's path, the opt-in key, the ledger path and format, the store's format, the configuration file and the keys and values that its format documents, the reusable workflow's path, inputs and permissions, and the Python and git floors. A manifest of that surface SHALL be kept in the repository.

#### Scenario: The surface manifest names the whole public surface

- **WHEN** the surface manifest in the repository is read
- **THEN** it names each part of the public surface

#### Scenario: The surface manifest names the hook's registration whole

- **WHEN** the surface manifest in the repository is read
- **THEN** it names each hook event and matcher that the hook file's registration names, and its command's form

#### Scenario: The surface manifest names the configuration's keys

- **WHEN** the surface manifest in the repository is read
- **THEN** it names each key that the configuration's format documents, and the values that each takes, and no other key or value of the configuration

### Requirement: The release workflow compares the surface manifest with the previous release's

The release workflow SHALL compare the surface manifest (see "The public surface is kept in a manifest") between the previous release's commit and the tag (see "Releases are made from a tag that matches the version and the changelog"). A release whose surface manifest changed SHALL come with a raised major number and a `### Breaking` section.

#### Scenario: A changed public surface needs a major version

- **WHEN** the surface manifest at the tag differs from the one at the previous release's commit, and the changelog entry has no `### Breaking` section or the major number does not rise
- **THEN** no release is published, and the workflow names what changed

### Requirement: Every release carries a software bill of materials

Each release SHALL carry a CycloneDX JSON software bill of materials, written by a standard-library Python script in this repository from the tagged tree, never a working tree. It SHALL name the tool, its version, the commit it was built from, its licence, the oldest supported Python as `requires-python` gives it, the hook file's SHA-256, each action the reusable workflow uses at its pinned commit, and the vendored and generated parts as development-only components with their source and licence.

#### Scenario: The bill of materials describes the release

- **WHEN** a release is published
- **THEN** a CycloneDX JSON file is attached that names the tool, the release's version and commit, the MIT licence, the oldest supported Python, the hook file's checksum, each action the reusable workflow uses, and the development-only components

### Requirement: A release is not published when its bill of materials is missing or fails a check

A release SHALL NOT be published when its bill of materials cannot be written, when its reusable workflow uses an action that the bill of materials does not list, when the hook checksum in it differs from the hook file's or the README's, or when the private-reference check (see "Pull request text carries no private reference" in `project-standards`) finds a match in it or in the release's text.

#### Scenario: An action missing from the bill of materials stops the release

- **WHEN** the reusable workflow uses an action that the bill of materials does not list, or the hook checksum in it differs from the hook file's or the README's
- **THEN** no release is published

#### Scenario: A release without a bill of materials is not published

- **WHEN** writing the bill of materials fails
- **THEN** no release is published

#### Scenario: A private reference in a release stops it

- **WHEN** the private-reference check finds a match in the bill of materials or in the release's text
- **THEN** no release is published

### Requirement: The capture step does nothing below its floors

The capture step SHALL check, before anything else, that it runs under Python 3.11 or later, and, before its first other git command, that git is 2.43 or later, the oldest git that CI tests. Below either floor it SHALL record nothing, stage nothing, print nothing and exit with success.

#### Scenario: An older Python is refused quietly

- **WHEN** the capture step starts under a Python older than 3.11
- **THEN** it records and stages nothing, prints nothing, and exits with success

#### Scenario: An older git is refused quietly

- **WHEN** the capture step finds a git older than 2.43
- **THEN** it records and stages nothing, prints nothing, and exits with success
