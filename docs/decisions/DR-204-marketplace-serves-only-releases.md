# DR-204: The marketplace serves only a release's plugin

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R184
- **Threats:** T132
- **Replaces:** none
- **Closed by:** none

## Context

A person can add this repository on claude.ai as a marketplace, which is read from its default branch, and whose plugins then update with nothing to accept (DR-203, A72). Claude Code takes the version of a plugin that a marketplace lists by a path in its repository from the plugin's manifest, or else from the commit that its folder was installed at, and that of a plugin from a marketplace that claude.ai hosts from what claude.ai records (A72). Either way, whatever the plugin's folder on the default branch holds reaches each person who added the marketplace at their next update. The default branch moves with every merged pull request, while a release is made only from a tag on the default branch, which a tag ruleset protects (DR-148). Claude Code's pages also describe plugin sources pinned to a commit or to an archive's checksum, but do not say that claude.ai's marketplaces read them.

## Decision

The repository's marketplace lists the tool's plugin from a folder in the repository that holds the plugin's files exactly as a release's tag builds them, with that release's version in the plugin's manifest. The folder moves only in a pull request made after a release, and CI fails when the folder differs from the plugin built from the tag of the release that its manifest names, or when no release tag holds that version. A change to the capture step reaches the marketplace only once a release holds it.

## Alternatives

- Listing the plugin's source folder itself, which would serve each merged change to every person who added the marketplace, before any release and without its checks.
- A source pinned to a release's commit or archive in the marketplace file, which Claude Code's pages describe but which claude.ai's marketplaces were not seen to read, and which a later change can move to once they are.
- A branch that only releases move, at which a marketplace added on claude.ai cannot be pointed.

## Consequences

- Someone who can merge into the default branch can still change the folder, and CI then fails unless the folder matches the build of a release's tag, which only the owner can push (T132).
- A release reaches the marketplace with the pull request that moves the folder, after its zip.
- The repository holds a copy of each released plugin's files, which the build from the tag reproduces.

## Scope

This covers what the marketplace serves. How the plugin reaches people is DR-203 (The plugin installs from each release's zip, or from this repository as a marketplace, the zip first), what this repository's root marketplace file lists is DR-205, and how a release is made is DR-148 (Each release is made from a tag).

## What reversing it would change

R184 in `releases-and-compatibility` would change, with its scenarios, and so would the design's decision 11, T132, the CI job that checks the folder, and the tasks that build the folder and move it after a release.
