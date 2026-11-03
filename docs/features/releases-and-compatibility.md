# Releases and compatibility

The tool is meant to be used inside other projects, so it keeps to old enough Python versions for adopters to keep up, and it is released in versions whose numbers say what changed.

**Status:** the supported versions and the update rules are in place; the capture step's floors and releases are designed, not built yet.

**Spec:** `releases-and-compatibility`

**Requirements:** R25, R99, R26, R27, R71, R122, R123, R28, R72, R32

## Expected behaviour

- **Python.** The tool runs on Python 3.11 and every later release, with the standard library only. CI tests on the oldest supported version and on the newest. `requires-python` in `pyproject.toml` is the one source of the oldest version, and a test fails when another copy of it disagrees. The oldest rises only when its version nears its end of life, or when a security fix needs a newer one, on the owner's decision.
- **Floors of the capture step.** Under a Python older than 3.11, or a git older than 2.43, the capture step records nothing, stages nothing, prints nothing and exits with success, so an old machine is never blocked from committing.
- **Dependency updates.** Minor and patch updates and vulnerability fixes are proposed as usual. A major update waits for the owner's approval on Renovate's dependency dashboard.
- **Versions.** Semantic: the major number rises for a change that adopters must act on, which is any change to the public surface: the hook's registration, by the events and matchers that it names and its command's form, and the hook file's path (the checksum that the command carries changes with every hook change and is not part of the surface), the opt-in key, the ledger's path and format, the store's format, `.pr-cost.json` and the keys and values that its format documents, the reusable workflow's path, inputs and permissions, and the Python and git floors. A manifest of that surface is kept in the repository, naming each key that `.pr-cost.json` may hold, with its values, and holding each released ledger version's schema by its hash, and a release whose manifest changed needs a raised major number and a `### Breaking` section; the minor number for new behaviour; the patch number for a fix.
- **Releases.** A release is made by pushing a tag `vMAJOR.MINOR.PATCH` for a commit in the default branch's first-parent history. The release workflow checks the tag's form before any other step, refuses a tag that does not match `pyproject.toml` and `CHANGELOG.md`, and publishes a GitHub release that names the commit to pin.
- **Bill of materials.** Every release carries a CycloneDX JSON software bill of materials. It is written from the tagged tree, and names the hook file's SHA-256 and each action the reusable workflow uses. A release whose bill of materials cannot be written, or misses an action, is not published.

## How it is validated

This feature is validated first by its spec's scenarios: each whose code is still to be written gets an acceptance test before that code, seen to fail for the expected reason, and each that a check already in place holds is named in that check's test (task 1.4). Then come the checks that DR-084 to DR-093 and DR-109 apply to all the tool's code. Beyond those, this feature has its own:

- Tests already in place: every copy of the oldest supported Python agrees with `requires-python`, CI runs on it and on the newest release, and Renovate holds major updates for the owner (task 1.11).
- The release check's tests, each of its refusals included (task 6.1), the bill of materials validated against the CycloneDX schema (task 6.2), and the release workflow's trigger and permissions (task 6.3).
- The capture step's floors, under an older Python and an older git (task 6.5).
- A CI job with git 2.43, the oldest git that CI tests, which runs the tests of the README's section on adopting the tool against git (task 4.4).
- By review rather than by a test: when the oldest Python rises, and whether a version's minor or patch number fits its change. The owner decides both.

## See also

- `releases-and-compatibility` in `openspec/`, and design decisions 10 and 11 of `add-pr-cost-calculator`.
- [`../../CHANGELOG.md`](../../CHANGELOG.md).
