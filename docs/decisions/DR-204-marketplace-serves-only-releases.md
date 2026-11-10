# DR-204: The marketplace serves only a release's plugin

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R184
- **Threats:** T132, T137, T138
- **Replaces:** none
- **Closed by:** none

## Context

A person can add this repository on claude.ai as a marketplace, which is read from its default branch, and a new version of its plugin reaches the person's account when they check for updates, or by itself once they turn on syncing (DR-203, A72). Claude Code takes the version of a plugin that a marketplace lists by a path in its repository from the plugin's manifest, or else from the commit that its folder was installed at, and that of a plugin from a marketplace that claude.ai hosts from what claude.ai records (A72). Either way, whatever the plugin's folder on the default branch holds reaches each person who added the marketplace at their next sync. The default branch moves with every merged pull request, while a release is made only from a tag on the default branch, which a tag ruleset protects (DR-148). The release workflow refuses a release after its tag exists, and the tag stays until someone deletes it. Given a short name such as `v1.3.0`, git takes a branch of that name when no such tag exists. CI runs a pull request's own copy of its scripts and tests (T71). Claude Code's pages also describe plugin sources pinned to a commit or to an archive's checksum, but do not say that claude.ai's marketplaces read them.

## Decision

The repository's marketplace lists the tool's plugin from a folder in the repository that holds the plugin's files exactly as a published release's tag builds them, with that release's version in the plugin's manifest. The folder moves only in a pull request made after a release, which changes nothing else. CI takes the release's tag by its full name, `refs/tags/v<version>`, and fails unless its commit is in the default branch's first-parent history and a published release names it, when the version is lower than at the pull request's base, and when the folder, compared by path, mode and content, differs from what the tag's own build script builds, run with `python3 -I`, or holds anything but regular files. A change to the capture step reaches the marketplace only once a published release holds it. A tag that the release workflow refused names no release, and its version is not used again.

## Alternatives

- Listing the plugin's source folder itself, which would serve each merged change to every person who added the marketplace, before any release and without its checks.
- A source pinned to a release's commit or archive in the marketplace file, which Claude Code's pages describe but which claude.ai's marketplaces were not seen to read, and which a later change can move to once they are.
- A branch that only releases move, which a marketplace added on claude.ai could follow only if claude.ai's form for adding one takes a branch, which no page read on 2026-11-09 says, and which task 7.2 checks; such a branch would need a ruleset of its own to keep it to releases.
- Building the plugin with the pull request's own script, or accepting any tag that gives the version, which would let one pull request change the folder together with what it is compared with, or move it to a refused or an earlier release.

## Consequences

- Someone who can merge into the default branch can still change the folder, and CI then fails unless the folder matches what a published release's tag builds, with that tag's own script, and the pull request changes nothing else, while a pull request that changes the check with the folder runs its changed check, so the owner merges one that changes the folder only when its diff changes nothing else (T132, T137).
- A refused tag, an earlier release, or a branch named like a version does not pass the check (T138), and the README says that a tag with no published release is not a version; the owner deletes a refused tag and the next release takes a later version.
- A release reaches the marketplace with the pull request that moves the folder, after its zip.
- The repository holds a copy of each released plugin's files, which the build from the tag reproduces.

## Scope

This covers what the marketplace serves. How the plugin reaches people is DR-203 (The plugin installs from each release's zip, or from this repository as a marketplace, the zip first), what this repository's root marketplace file holds is DR-205, how a release is made is DR-148 (Each release is made from a tag), and when a release is published is DR-209.

## What reversing it would change

R184 in `releases-and-compatibility` would change, with its scenarios, and so would R190, the design's decision 11, T132, T137, T138, the CI job that checks the folder, and the tasks that build the folder and move it after a release.
