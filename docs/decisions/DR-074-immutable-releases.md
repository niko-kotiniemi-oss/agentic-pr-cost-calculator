# DR-074: Releases are immutable

- **Type:** security and privacy
- **Boundary:** outgoing
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** none
- **Threats:** T67
- **Replaces:** none
- **Closed by:** none

## Context

A release's text names its tag and its commit in the release workflow's fixed words (R27), and adopters pin the commit that a release names (T67). Any identity with `contents: write` can create a release and its tag through the API, with no workflow at all (T67).

## Decision

The repository's setting for immutable releases is on, so that a release, once published, cannot be changed and its tag cannot be moved.

## Alternatives

None were recorded when this was decided.

## Consequences

- No file holds the setting and no test reads it, so T67's answer rests on the owner keeping it on.
- Together with the tag ruleset, which covers every tag (DR-161), it is the control over releases, while the release workflow's own check of the tag's commit guards only against mistakes (DR-073).

## Scope

This covers a release once it is published. Who may create, move or delete a tag is DR-073 (Only a deploy key may bypass the tag ruleset), how a release is made is DR-148 (Each release is made from a tag), and what it carries is DR-097 (Each release carries a bill of materials).

## What reversing it would change

No requirement states this. The setting itself, its entry among the settings in `docs/threat-model.md`, T67's answer and residual, and the design's decision 11, which names this record, would change, and DR-073, DR-144 and DR-161 would be revisited. The setting is not part of the public surface, so the change would not be a breaking one for adopters.
