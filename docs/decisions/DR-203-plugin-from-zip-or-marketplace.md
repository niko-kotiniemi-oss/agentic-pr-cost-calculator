# DR-203: The plugin installs from each release's zip, or from this repository as a marketplace, the zip first

- **Type:** architecture
- **Status:** accepted
- **Decided by:** the owner, 2026-11-09
- **Requirements:** R183, R187
- **Threats:** T132, T133
- **Replaces:** none
- **Closed by:** none

## Context

The capture step also comes as a plugin (DR-197). On claude.ai a person adds a plugin to their account by uploading a zip that holds it, or by adding a GitHub repository whose root holds a marketplace file that lists it, and the plugins of a marketplace added there update with nothing to accept (A72). A project's threads load the plugins added in the project's settings (A69). The owner chose on 2026-11-09 that the README offers both ways, the zip first, over the change's recommendation of the zip alone.

## Decision

Each release carries the plugin as a zip, built from the release's tag alone, the same bytes on every build, whose SHA-256 the README at the tag's commit gives. A person installs the plugin by uploading that zip on claude.ai after checking its checksum, or by adding this repository there as a marketplace, whose updates then arrive with nothing to accept. The README gives the zip first, and says what each way means for updates.

## Alternatives

- The zip alone, which the change recommended, since each update is then the person's own act after a check, and which leaves those who prefer updates that arrive by themselves to take each release's zip.
- The marketplace alone, whose updates reach every session that loads the plugin with no check by the person.
- A marketplace of the tool's own in another repository, which would be one more repository to keep and to protect.

## Consequences

- A person who uploads the zip runs the release whose checksum they checked until they upload another, and the README says how to check the zip and how to update (T133).
- A person who adds the marketplace runs whichever release its folder holds, with no step of their own, so that folder only ever holds a release's files (DR-204, T132).
- A person who adds the plugin both ways can run two copies, which record each call once (DR-206).
- The copied hook file stays how a repository records the sessions of everyone who works in it (DR-197).

## Scope

This covers how the plugin reaches a person. What the marketplace serves is DR-204 (The marketplace serves only a release's plugin), what this repository's root marketplace file lists is DR-205, and how adopters take the hook file is DR-022 (Adopters copy the hook file from a pinned commit).

## What reversing it would change

R183 in `releases-and-compatibility` and R187 in `project-standards` would change, with their scenarios, and so would R184, DR-204 and DR-205, which would be closed or revisited, the design's decisions 11 and 17, T132, T133, the README's section on installing the plugin, the release workflow, and the tasks that build the zip and check the marketplace's folder.
