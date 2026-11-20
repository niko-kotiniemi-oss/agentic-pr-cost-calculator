# DR-073: Only a deploy key may bypass the tag ruleset

- **Type:** security and privacy
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** none
- **Threats:** T28, T64, T67
- **Replaces:** none
- **Closed by:** none

## Context

A release starts when a tag is pushed (DR-148), and adopters pin the commit that a release names (DR-156). GitHub runs the release workflow as it stands at the tagged commit, so the workflow's own check that the commit is on the default branch guards against mistakes, not against someone who can push a tag. Any identity with `contents: write` can also create a release and its tag through the API, with no workflow at all (T67).

## Decision

The control is who can create a tag or a release at all: a tag ruleset that restricts creating, moving and deleting tags, whose only bypass is a deploy key kept on the owner's machine, an identity that agent sessions never hold, not the owner's account, since agent sessions act on GitHub as that account.

## Alternatives

- Letting the owner's account bypass the ruleset, which would let agent sessions bypass it too (T64).

## Consequences

- `docs/threat-model.md` lists the ruleset under the owner's settings, beside `CLAUDE.md`'s rule that agents never create, move or delete tags or releases (DR-144).
- Agent sessions never hold the deploy key, which the threat model's settings keep for releases on the owner's own machine, so an agent's merge reaches no adopter until the owner releases it, since adopters pin only a commit that a release names (T64).
- No file holds the ruleset and no test reads it, so T67's answer rests on the owner keeping it.

## Scope

This covers who may create, move or delete a tag. Which tags the ruleset covers is DR-161 (The tag ruleset covers every tag), that a published release cannot change is DR-074 (Releases are immutable), how a release's version is numbered is DR-096 (Versions are semantic), that each release is made from a tag is DR-148 (Each release is made from a tag), which commit a release tag may name is DR-122 (A release tag names a commit in the default branch's first-parent history), and that only the owner creates, moves or deletes a tag or a release, or changes a setting, is DR-144 (Tags, releases, settings, rulesets and secrets stay with the owner).

## What reversing it would change

No requirement states this. The ruleset itself, its entry among the settings in `docs/threat-model.md`, the design's decision 11, and the answers of T28, T64 and T67, with T67's residual, would change. DR-074, DR-080, DR-144 and DR-161 would be revisited. The ruleset is not part of the public surface, so the change would not be a breaking one for adopters.
