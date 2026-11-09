# DR-203: The plugin installs from each release's zip, or from this repository as a marketplace, the zip first

- **Type:** architecture
- **Status:** accepted
- **Decided by:** the owner, 2026-11-09
- **Requirements:** R183, R187
- **Threats:** T132, T133, T142
- **Replaces:** none
- **Closed by:** none

## Context

The capture step also comes as a plugin (DR-197). On claude.ai a person adds a plugin to their account by uploading a zip that holds it, or by adding a GitHub repository whose root holds a marketplace file that lists it, and a new version of a marketplace's plugin reaches the person's account when they check for updates, or by itself once they turn on syncing, with nothing to accept once it has synced (A72). Claude Code's own command adds a marketplace from a repository pinned to a tag, as in `owner/repo#v1.2.0` (A72). A project's threads load the plugins added in the project's settings (A69). Python's `zipfile` writes into each entry the system that it runs on and compresses with whatever zlib it links, so fixed times, modes and order alone do not give the same bytes on every system. The owner chose on 2026-11-09 that the README offers both ways, the zip first, over the change's recommendation of the zip alone.

## Decision

Each release carries the plugin as a zip, built from the release's tag alone, with its entries stored uncompressed and every header field fixed, so that a build on any system gives the same bytes, whose SHA-256 the README gives. CI builds the zip from every pull request's tree, on Linux and on Windows, and fails when its SHA-256 differs from the README's, so that a checksum left behind is found before a tag. A person installs the plugin by uploading that zip on claude.ai after checking its checksum, or by adding this repository as a marketplace, on claude.ai or with Claude Code's command pinned to a release's tag. The README gives the zip first, says what each way means for updates, and says that a zip follows no address.

## Alternatives

- The zip alone, which the change recommended, since each update is then the person's own act after a check, and which leaves those who prefer updates that arrive by themselves to take each release's zip.
- The marketplace alone, whose updates reach every session that loads the plugin with no check by the person.
- A marketplace of the tool's own in another repository, which would be one more repository to keep and to protect.
- A zip compressed as Python compresses it, whose bytes would differ between a build on Linux and one on Windows, so that a person could not check a zip built on another system against the README.

## Consequences

- A person who uploads the zip runs the release whose checksum they checked until they upload another, and the README says how to check the zip and how to update (T133).
- A person who adds the marketplace runs whichever release its folder holds, once their account syncs it, with no step of their own, so that folder only ever holds a published release's files (DR-204, T132).
- A person who adds the plugin both ways runs one copy, since Claude Code registers the hooks of one plugin per name, and the README says how to see which (DR-206).
- A marketplace is followed by its address, so the owner keeps the account's and the repository's names, which someone else could otherwise take after a rename and serve another plugin of the same name from, while a zip follows no address (T142).
- The copied hook file stays how a repository records the sessions of everyone who works in it (DR-197).

## Scope

This covers how the plugin reaches a person. What the marketplace serves is DR-204 (The marketplace serves only a release's plugin), what this repository's root marketplace file lists is DR-205, how a release is published once its files are checked is DR-209, and how adopters take the hook file is DR-022 (Adopters copy the hook file from a pinned commit).

## What reversing it would change

R183 in `releases-and-compatibility` and R187 in `project-standards` would change, with their scenarios, and so would R184, DR-204 and DR-205, which would be closed or revisited, the design's decisions 11 and 17, T132, T133, T142, the README's section on installing the plugin, the release workflow, the CI job that builds the zip, and the tasks that build the zip and check the marketplace's folder.
