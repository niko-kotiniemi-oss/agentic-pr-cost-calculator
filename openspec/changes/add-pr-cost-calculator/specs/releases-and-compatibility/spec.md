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

A release SHALL be made only by pushing a tag `vMAJOR.MINOR.PATCH` that names a commit in the default branch's first-parent history, and the release workflow SHALL check the tag's form before any other step, and SHALL refuse a tag whose version differs from that in `pyproject.toml` or in the plugin that the tag builds, or that has no entry in `CHANGELOG.md`. The release's own text SHALL name the tag and the commit in the workflow's fixed words, and SHALL carry the changelog entry after them.

#### Scenario: A tag that matches the version and the changelog is released

- **WHEN** a tag `v1.2.0` is pushed for a commit on the default branch whose `pyproject.toml` says `1.2.0` and whose changelog has an entry for `1.2.0`
- **THEN** a GitHub release `v1.2.0` is published that names the commit and carries the changelog entry

#### Scenario: A tag that does not match the version is refused

- **WHEN** a tag `v1.2.0` is pushed for a commit whose `pyproject.toml`, or the plugin that it builds, gives another version, or whose changelog has no entry for `1.2.0`
- **THEN** no release is published and the workflow says which of them disagrees

#### Scenario: A tag on a commit outside the default branch's first-parent history is refused

- **WHEN** a release tag names a commit that is not in the default branch's first-parent history, such as a commit from inside a merged pull request or one that only a fork holds
- **THEN** no release is published

#### Scenario: A tag that is not a semantic version stops the workflow first

- **WHEN** a pushed tag is not `v` followed by a semantic version, such as one holding shell characters
- **THEN** the workflow fails before any other step and publishes nothing

### Requirement: A release's guide was read for it, and its text names the gaps that adopters rely on

The release workflow SHALL refuse a tag whose guide, `docs/patterns.md`, does not say that its entries were last read for that tag's version, or gives a gap under Security, Privacy, Identity and credentials, or Supply chain and releases whose backlog item the tag's entry in `CHANGELOG.md` does not name, so that each release's guide was read for it and its text, which carries that entry, tells adopters of each such gap.

#### Scenario: A release whose guide was read for it, and whose changelog names its gaps, goes on

- **WHEN** a tag `v1.2.0` is pushed whose guide says that its entries were last read for release 1.2.0, and whose changelog entry for `1.2.0` names the backlog item of each gap that the guide gives under those concerns
- **THEN** the check of the guide passes, and the release goes on to its other checks

#### Scenario: A release whose guide was not read for it is refused

- **WHEN** a tag `v1.2.0` is pushed whose guide says that its entries were last read for another release, or for an assessment
- **THEN** no release is published, and the workflow says that the guide was not read for that release

#### Scenario: A release whose changelog leaves out a gap that adopters rely on is refused

- **WHEN** a tag's guide gives, under Security, Privacy, Identity and credentials, or Supply chain and releases, a gap whose backlog item the tag's changelog entry does not name
- **THEN** no release is published, and the workflow names the entry and the item

### Requirement: Versions are semantic, and their numbers say what an adopter must do

The version SHALL raise its major number for a change that existing adopters must act on, which is any change to the public surface (see "The public surface is kept in a manifest"). It SHALL raise its minor number for a change that adds behaviour without breaking any part of that surface, and its patch number for a fix alone. A changelog entry that lists a breaking change SHALL come with a raised major number and a `### Breaking` section.

#### Scenario: A breaking change raises the major version

- **WHEN** the changelog entry for a release lists a breaking change and the release does not raise the major number over the previous release
- **THEN** no release is published and the workflow says why

### Requirement: The public surface is kept in a manifest

The public surface SHALL be the hook file's path and registration and the plugin's name and hooks, each by its events, matchers and command's form, not the checksum it carries; the marketplace's name, the opt-in key and the agents it records, the ledger path and format, the store's format and fingerprint, the configuration file and the keys and values its format documents, the reusable workflow's path, inputs and permissions, and the Python and git floors. The repository SHALL keep its manifest.

#### Scenario: The surface manifest names the whole public surface

- **WHEN** the surface manifest in the repository is read
- **THEN** it names each part of the public surface

#### Scenario: The surface manifest names the hook's registration whole

- **WHEN** the surface manifest in the repository is read
- **THEN** it names each hook event and matcher that the hook file's registration names, and its command's form

#### Scenario: The surface manifest names the plugin whole

- **WHEN** the surface manifest in the repository is read
- **THEN** it names the plugin's name, each hook event and matcher that the plugin's hooks name, and their command's form, and the marketplace's name

#### Scenario: The surface manifest names the configuration's keys

- **WHEN** the surface manifest in the repository is read
- **THEN** it names each key that the configuration's format documents, and the values that each takes, and no other key or value of the configuration

#### Scenario: The surface manifest names each agent that the opt-in records

- **WHEN** the surface manifest in the repository is read
- **THEN** it names each agent whose calls the release records under the opt-in, so that a release that adds one changes the public surface

### Requirement: The release workflow compares the surface manifest with the previous release's

The release workflow SHALL compare the surface manifest (see "The public surface is kept in a manifest") between the previous release's commit and the tag (see "Releases are made from a tag that matches the version and the changelog"). A release whose surface manifest changed SHALL come with a raised major number and a `### Breaking` section.

#### Scenario: A changed public surface needs a major version

- **WHEN** the surface manifest at the tag differs from the one at the previous release's commit, and the changelog entry has no `### Breaking` section or the major number does not rise
- **THEN** no release is published, and the workflow names what changed

### Requirement: Every release carries a software bill of materials

Each release SHALL carry a CycloneDX JSON software bill of materials, written by a standard-library Python script in this repository from the tagged tree, never a working tree. It SHALL name the tool, its version, commit and licence, the oldest supported Python from `requires-python`, the SHA-256 of the hook file and of the plugin's zip, each action the reusable workflow uses at its pinned commit, and the vendored and generated parts as development-only components with their source and licence.

#### Scenario: The bill of materials describes the release

- **WHEN** a release is published
- **THEN** a CycloneDX JSON file is attached that names the tool, the release's version and commit, the MIT licence, the oldest supported Python, the hook file's checksum, the plugin zip's checksum, each action the reusable workflow uses, and the development-only components

### Requirement: A release is not published when its bill of materials is missing or fails a check

A release SHALL NOT be published when its bill of materials cannot be written, when its reusable workflow uses an action that the bill of materials does not list, when the hook file's or the plugin zip's checksum in it differs from the file's or the README's, or when the private-reference check (see "Pull request text carries no private reference" in `project-standards`) finds a match in it or in the release's text.

#### Scenario: An action missing from the bill of materials stops the release

- **WHEN** the reusable workflow uses an action that the bill of materials does not list, or the hook file's or the plugin zip's checksum in it differs from the file's or the README's
- **THEN** no release is published

#### Scenario: A release without a bill of materials is not published

- **WHEN** writing the bill of materials fails
- **THEN** no release is published

#### Scenario: A private reference in a release stops it

- **WHEN** the private-reference check finds a match in the bill of materials or in the release's text
- **THEN** no release is published

### Requirement: Each release carries the plugin as a zip that its tag rebuilds

Each release SHALL carry the plugin as a zip built from its tag's files alone, as git's objects hold them, holding only the plugin's manifest, its hooks, the capture step and the licence, stored uncompressed with every header field fixed, so that every build on any system gives the same bytes. CI SHALL fail when the zip built from a pull request's tree has another SHA-256 than the README there gives, and the release workflow SHALL publish no release whose zip does.

#### Scenario: The plugin's zip is the same on every build

- **WHEN** the plugin's zip is built twice from one tag, at different times, once on Linux and once on Windows from a clone that git made with `core.autocrlf` set to `true`, with different umasks
- **THEN** the two zips are the same, byte for byte

#### Scenario: A pull request that leaves the zip's checksum behind fails CI

- **WHEN** a pull request changes a file that the plugin's zip holds and leaves the SHA-256 that the README gives for the zip as it was
- **THEN** CI fails, and says that the zip built from the pull request's tree has another SHA-256 than the README gives

#### Scenario: A zip whose checksum differs from the README's stops the release

- **WHEN** the zip built from a tag has another SHA-256 than the README at the tag's commit gives
- **THEN** no release is published, and the workflow says that the two differ

#### Scenario: The zip holds only the plugin

- **WHEN** a release's zip is read
- **THEN** it holds the plugin's manifest, its hooks, the capture step and the licence, each stored uncompressed, and nothing else

### Requirement: The plugin declares nothing but its hooks

The plugin that a commit builds SHALL have a manifest that holds no key but its name, version, description, author, licence and repository, hooks that are all command hooks, and the hook file, byte for byte, as its capture step, whatever the marketplace's plugin folder holds. CI SHALL fail on a pull request whose tree builds a plugin where any of these does not hold, and the release workflow SHALL publish no release where any does not.

#### Scenario: A plugin that declares anything but its hooks fails CI and stops the release

- **WHEN** the plugin that a pull request's tree builds has a manifest that holds another key, such as `hooks`, `mcpServers`, `monitors` or `dependencies`, or a hooks file that holds a hook of another type than a command, such as an HTTP hook
- **THEN** CI fails and names the key or the hook, and no release is published from a tag where it holds

#### Scenario: A capture step in the plugin that differs from the hook file fails CI

- **WHEN** the capture step in the plugin that a pull request's tree builds differs from the hook file by any byte
- **THEN** CI fails, and no release is published from a tag where it differs

#### Scenario: A changed hook file is not compared with the marketplace's folder

- **WHEN** a pull request changes the hook file, while the marketplace's plugin folder holds an earlier release's plugin, whose capture step is the earlier hook file
- **THEN** the plugin that the pull request's tree builds, with the changed hook file as its capture step, passes these checks, and the marketplace's folder is compared only with its release

### Requirement: A release is published only once its files are attached and checked

The release workflow SHALL create each release as a draft, attach its plugin's zip and its bill of materials, download each attached file again and check its size and SHA-256 against the file that it built, and only then publish the release. It SHALL publish nothing when an attachment fails or differs.

#### Scenario: A release is published only after its files are checked

- **WHEN** the release workflow runs for a tag that passes every check
- **THEN** the release is created as a draft, takes the zip and the bill of materials, and is published only once each attached file, downloaded again, has the size and SHA-256 of the file that the workflow built

#### Scenario: A release whose attached file differs stays a draft

- **WHEN** attaching a file fails, or a file downloaded again from the draft has another size or SHA-256 than the file that the workflow built
- **THEN** the release stays a draft, the workflow fails and names the file, and nothing is published

### Requirement: The marketplace serves only a release's plugin

The folder that the root marketplace file names SHALL hold the plugin as a published release's tag builds it, with that release's version in its manifest. CI SHALL fail when, compared by path, mode and content, the folder differs from what that tag's own build script builds, holds anything but regular files, or gives a version that no published release, found by its tag's full name in the default branch's first-parent history, has, or a lower one than at the base.

#### Scenario: A marketplace folder that differs from its release fails CI

- **WHEN** the marketplace's plugin folder holds a file that the plugin built from its release's tag does not hold, lacks one that it holds, or holds one with other content or another mode
- **THEN** CI fails and names the file

#### Scenario: A marketplace folder is compared with what its tag's own build script builds

- **WHEN** a pull request changes the script that builds the plugin and the marketplace's plugin folder together, so that the changed script builds what the folder holds
- **THEN** CI builds the plugin with the build script at the release's tag, run with `python3 -I`, and fails because the folder differs from what that script builds

#### Scenario: A submodule or a link in the marketplace folder fails CI

- **WHEN** the marketplace's plugin folder holds a submodule, a symbolic link or anything else that is not a regular file
- **THEN** CI fails and names it

#### Scenario: A marketplace folder whose version no published release has fails CI

- **WHEN** the plugin's manifest in the marketplace's folder gives a version whose tag names no published release, as the tag of a release that the workflow refused does not, or that only a branch named like that tag gives
- **THEN** CI fails, and reads no ref by the version's short name

#### Scenario: A marketplace folder that moves back to an earlier release fails CI

- **WHEN** a pull request changes the marketplace's plugin folder to an earlier published release's plugin than the one at its base
- **THEN** CI fails, and says that the version is lower than the base's

### Requirement: The root marketplace file names only the tool's plugin, and changes alone

The root marketplace file SHALL hold only the marketplace's name, its owner and one entry that gives the tool's plugin's name and its folder. CI SHALL fail when the file, parsed, holds any other key, value or entry, or when a pull request that adds, changes or removes the root marketplace file, or changes the folder that it names, changes anything else, and the release workflow SHALL refuse a tag whose root marketplace file lists any plugin but the tool's.

#### Scenario: The root marketplace file lists only the tool's plugin

- **WHEN** the root marketplace file lists a plugin other than the tool's, or lists the tool's from another folder than the marketplace's plugin folder
- **THEN** CI fails

#### Scenario: A root marketplace entry that declares anything else fails CI

- **WHEN** the root marketplace file's entry gives the plugin hooks, commands, agents, skills, MCP servers, `strict` or `defaultEnabled`, or the file holds any key or value that the expected file does not
- **THEN** CI fails and names the key

#### Scenario: A pull request that changes the marketplace and anything else fails CI

- **WHEN** a pull request adds, changes or removes the root marketplace file, or changes the plugin folder that it names, and also any other file, such as the script that builds the plugin, the check that compares the folder or a workflow
- **THEN** CI fails, and names the files beside the marketplace's that the pull request changes

#### Scenario: A release tag whose root marketplace file lists another plugin is refused

- **WHEN** a release's tag names a commit whose root marketplace file lists a plugin other than the tool's, as the file that loads the vendored Superpowers does
- **THEN** the release workflow publishes no release and says why

### Requirement: The capture step does nothing below its floors

The capture step SHALL check, before anything else, that it runs under Python 3.11 or later, and, before its first other git command, that git is 2.43 or later, the oldest git that CI tests. Below either floor it SHALL record nothing, stage nothing, print nothing and exit with success.

#### Scenario: An older Python is refused quietly

- **WHEN** the capture step starts under a Python older than 3.11
- **THEN** it records and stages nothing, prints nothing, and exits with success

#### Scenario: An older git is refused quietly

- **WHEN** the capture step finds a git older than 2.43
- **THEN** it records and stages nothing, prints nothing, and exits with success
