# DR-161: The tag ruleset covers every tag

- **Type:** security and privacy
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the owner, 2026-10-27
- **Requirements:** none
- **Threats:** T28, T67
- **Replaces:** none
- **Closed by:** none

## Context

R27 says that a release is made only by pushing a tag `vMAJOR.MINOR.PATCH`, but any identity with `contents: write` can also create a release and its tag through the API, with no workflow at all, and that tag need not start with `v` (T67). The tag ruleset restricts creating, moving and deleting tags, and only a deploy key may bypass it (DR-073). Which tags it covers was put to the owner, who chose every tag on 2026-10-27.

## Decision

The tag ruleset covers every tag, not only the `v*` tags that releases are made from.

## Alternatives

- A tag ruleset on `v*` tags alone, which would not stop an identity with `contents: write` from creating a release through the API with a tag of another name (T67).

## Consequences

- `docs/threat-model.md` lists the ruleset on every tag under the owner's settings, which the answers of T28 and T67 rest on.
- Creating, moving or deleting any tag, whatever its name, takes the deploy key that DR-073 names, so a tag that marks no release takes it too.
- No file holds the ruleset and no test reads it, so this rests on the owner keeping it, as T67's residual says.

## Scope

This covers which tags the tag ruleset covers. Who may bypass it is DR-073 (Only a deploy key may bypass the tag ruleset), that a published release cannot change is DR-074 (Releases are immutable), and that each release is made from a tag is DR-148 (Each release is made from a tag).

## What reversing it would change

No requirement states this. The ruleset itself, its entry among the settings in `docs/threat-model.md`, the answers of T28 and T67, with T67's residual, and the design's decision 11, which names this record, would change, and DR-073 would be revisited. The ruleset is not part of the public surface, so the change would not be a breaking one for adopters.
