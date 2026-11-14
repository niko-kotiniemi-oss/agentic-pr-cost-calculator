# Releases and compatibility

The tool is meant to be used inside other projects, so it keeps to old enough Python versions for adopters to keep up, and it is released in versions whose numbers say what changed.

**Status:** the supported versions and the update rules are in place; the capture step's floors and releases are designed, not built yet.

**Spec:** `releases-and-compatibility`

**Requirements:** R25, R99, R26, R27, R230, R71, R122, R123, R28, R72, R183, R188, R189, R184, R190, R32

## Expected behaviour

- **Python.** The tool runs on Python 3.11 and every later release, with the standard library only. CI tests on the oldest supported version and on the newest. `requires-python` in `pyproject.toml` is the one source of the oldest version, and a test fails when another copy of it disagrees. The oldest rises only when its version nears its end of life, or when a security fix needs a newer one, on the owner's decision.
- **Floors of the capture step.** Under a Python older than 3.11, or a git older than 2.43, the capture step records nothing, stages nothing, prints nothing and exits with success, so an old machine is never blocked from committing.
- **Dependency updates.** Minor and patch updates and vulnerability fixes are proposed as usual. A major update waits for the owner's approval on Renovate's dependency dashboard.
- **Versions.** Semantic: the major number rises for a change that adopters must act on, which is any change to the public surface: the hook's registration, by the events and matchers that it names and its command's form, and the hook file's path (the checksum that the command carries changes with every hook change and is not part of the surface), the plugin's name and hooks, by the events and matchers that they name and their command's form, not the checksum that it carries, the marketplace's name, the opt-in key and each agent that it records, the ledger's path and format, the store's format and how its fingerprint is made, `.pr-cost.json` and the keys and values that its format documents, the reusable workflow's path, inputs and permissions, and the Python and git floors. A manifest of that surface is kept in the repository, naming the plugin's name, each event and matcher that its hooks name and their command's form, the marketplace's name, each agent that the opt-in records, and each key that `.pr-cost.json` may hold, with its values, and holding each released ledger version's schema by its hash, and a release whose manifest changed needs a raised major number and a `### Breaking` section; the minor number for new behaviour; the patch number for a fix.
- **Releases.** A release is made by pushing a tag `vMAJOR.MINOR.PATCH` for a commit in the default branch's first-parent history. The release workflow checks the tag's form before any other step, refuses a tag that does not match `pyproject.toml`, the plugin's manifest and `CHANGELOG.md`, or whose root marketplace file lists any plugin but the tool's, or whose guide was not read for it or leaves a gap that adopters rely on out of its changelog entry, as R230 gives it, and creates the GitHub release as a draft, attaches the plugin's zip and the bill of materials, downloads each again to check its size and SHA-256, and only then publishes the release, which names the commit to pin (DR-209). A tag that the workflow refused names no release, and its version is not used again.
- **Bill of materials.** Every release carries a CycloneDX JSON software bill of materials. It is written from the tagged tree, and names the hook file's SHA-256, the plugin's zip's SHA-256 and each action the reusable workflow uses. A release whose bill of materials cannot be written, misses an action or gives a checksum that differs from the file's or the README's is not published.
- **The plugin's zip.** Each release carries the plugin as a zip built from its tag's files alone, as git's objects hold them, holding only the plugin's manifest, its hooks, the capture step and the licence, stored uncompressed with every header field fixed, so that a build on Linux and one on Windows give the same bytes. The README gives its SHA-256, CI fails on a pull request after which the zip built from its tree has another, and the release workflow publishes no release whose zip has another, so a person can check a zip against the README at the release's commit before they upload it (DR-203).
- **What the plugin declares.** Each commit builds the plugin from the hook file, byte for byte, as its capture step, the licence and the plugin's own manifest and hooks files, never from the marketplace's plugin folder. Its manifest holds only its name, version, description, author, licence and repository, its hooks are all command hooks, and CI checks the plugin that each pull request's tree builds, so that it runs nothing that its zip's list of files, its checksum and the bill of materials do not show.
- **The marketplace.** The repository's root marketplace file holds only the marketplace's name, its owner and one entry that gives the tool's plugin's name and its folder, and that folder holds the plugin as a published release's tag builds it, with that release's version in its manifest. The folder moves only in a pull request made after a release, which changes nothing else, and CI fails when the folder, compared by path, mode and content, differs from what the release tag's own build script builds, holds anything but regular files, or gives a version that no published release has, or a lower one than before, and when the root file holds anything else. So a person who adds the repository as a marketplace gets only a release's plugin, once their account syncs it (DR-204, DR-205). The marketplace that loads the vendored Superpowers into this repository's own sessions moves to a folder under `vendor/`, and the root marketplace file is then removed, in a pull request of its own, before the checks that hold it, which pass while there is none, and comes back in the pull request after the first release that carries the plugin, which changes nothing else.

## How it is validated

This feature is validated first by its spec's scenarios: each whose code is still to be written gets an acceptance test before that code, seen to fail for the expected reason, and each that a check already in place holds is named in that check's test (task 1.4). Then come the checks that DR-084 to DR-093 and DR-109 apply to all the tool's code. Beyond those, this feature has its own:

- Tests already in place: every copy of the oldest supported Python agrees with `requires-python`, CI runs on it and on the newest release, and Renovate holds major updates for the owner (task 1.11).
- The release check's tests, each of its refusals included, a tag whose root marketplace file lists another plugin among them (task 6.1), the bill of materials validated against the CycloneDX schema (task 6.2), and the release workflow's trigger and permissions (task 6.3).
- The capture step's floors, under an older Python and an older git (task 6.5).
- The plugin's zip built twice from one tag, at different times, on Linux and on Windows from a clone that git made with `core.autocrlf` set to `true`, and with different umasks, a planted difference in the README's checksum, which fails CI and stops the release, a planted extra file, which fails the check of what the zip holds, a planted manifest key or HTTP hook, a changed hook file, which passes while the marketplace's plugin folder holds an earlier release's plugin, and a release whose attached file differs, which stays a draft (tasks 6.3 and 6.6).
- The marketplace's checks, each shown to fail on a planted defect in a fixture tree: a folder that differs from its release's plugin, one that a changed build script matches, a submodule or a link in it, a version that no published release has, that only a branch gives or that is lower than the base's, a root file that holds anything else, and a pull request that adds or changes the marketplace with anything else, and to pass on a tree that holds no root marketplace file (task 6.9).
- A CI job with git 2.43, the oldest git that CI tests, which runs the tests of the README's section on adopting the tool against git (task 4.4).
- By review rather than by a test: when the oldest Python rises, and whether a version's minor or patch number fits its change. The owner decides both.

## Known limitations and the roadmap

The design's risks that concern this feature and are not on the roadmap, each with what it means:

- **A person's plugin is of another release than the report that a repository pins**: the report refuses what it does not know, and the comment says that some ledger files come from a later release.
- **No release can be made while any acceptance test is still expected to fail**: releases wait until the code reaches every scenario and reproduces the golden set.

The [roadmap](../roadmap.md) gives what is planned next and later, and the limitations that an adopter notices.

## See also

- `releases-and-compatibility` in `openspec/`, design decisions 10 and 11 of `add-pr-cost-calculator`, DR-203 to DR-205 for how the plugin reaches people, and DR-209 for how a release takes its files.
- [`../../CHANGELOG.md`](../../CHANGELOG.md).
