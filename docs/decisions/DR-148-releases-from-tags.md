# DR-148: Each release is made from a tag

- **Type:** process
- **Boundary:** outgoing
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-10-20
- **Requirements:** R27, R123
- **Threats:** T67, T68
- **Replaces:** none
- **Closed by:** none

## Context

Adopters take the tool at a commit that a release names (DR-156), so a release is how a version reaches them. Pushing a tag is the event the release workflow runs on, and GitHub runs that workflow as the tagged commit holds it (T67). The job that publishes a release is the only one holding `contents: write` (DR-067), and git allows shell characters in a tag name (T68).

## Decision

Each release is made by pushing a tag `vMAJOR.MINOR.PATCH` that carries the release's version number.

## Alternatives

None were recorded when this was decided.

## Consequences

- The release workflow publishes only for a pushed tag, but any identity with `contents: write` can also create a release and its tag through the API with no workflow at all (T67), so the control over releases is who may create a tag or a release (DR-073, DR-144, DR-161), and a release once published cannot change (DR-074).
- A tag name can hold shell characters, so the release job reads the tag's form before any other step, and a tag that is not `v` followed by a semantic version publishes nothing (DR-067; T68, and R27's scenario "A tag that is not a semantic version stops the workflow first").
- The tag is then compared with the version that the repository holds and with the changelog (DR-149), and the surface manifest at the tag with the one at the previous release's commit (R123, DR-123).
- Task 6.1 builds the check in that order, and task 6.3 the workflow that runs only for a pushed tag.

## Scope

This covers how a release is started and the tag it comes from. How the version in that tag is chosen is DR-096 (Versions are semantic), which commit the tag may name is DR-122 (A release tag names a commit in the default branch's first-parent history), who may create a tag is DR-073 (Only a deploy key may bypass the tag ruleset), where the version is kept and what the changelog holds is DR-149 (`pyproject.toml` holds the version, and the changelog has one entry per release), and what each release carries is DR-097 (Each release carries a bill of materials).

## What reversing it would change

R27 in `releases-and-compatibility` would change in its clauses on the tag, with its scenarios "A tag that matches the version and the changelog is released", "A tag that does not match the version is refused", "A tag on a commit outside the default branch's first-parent history is refused" and "A tag that is not a semantic version stops the workflow first", and so would R123, which compares the manifest between the previous release's commit and the tag. The design's decision 11, its decision 13 and T70's answer, the last two of which take the previous release's tag as the base of the release's test job, the threat model's boundary 8 and its data flow, the answers of T67 and T68, tasks 6.1 and 6.3, the release flow in `docs/how-it-works.md`, the feature page's account of releases, the proposal's list of what changes and the line of `CLAUDE.md` on releases would change too, and DR-073, DR-074, DR-122, DR-144, DR-149, DR-156 and DR-161 would be revisited. How a release is started is not part of the public surface, so the change would not be a breaking one for adopters.
