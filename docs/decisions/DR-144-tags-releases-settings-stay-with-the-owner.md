# DR-144: Tags, releases, settings, rulesets and secrets stay with the owner

- **Type:** security and privacy
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** none
- **Threats:** T62, T64, T67
- **Replaces:** none
- **Closed by:** none

## Context

Agent sessions act on GitHub as the owner's own account, so GitHub cannot tell an agent's action from the owner's, and whatever is reserved for the owner is within reach of an agent that is mistaken or steered (T64). A pushed tag starts a release, and any identity with `contents: write` can also create a release and its tag through the API, with no workflow at all, while adopters pin the commit that a release names (T67). Several threats' answers rest on settings of the repository, such as its rulesets, which no file here holds and no test reads (see the threat model's settings the owner keeps).

## Decision

Only the owner creates, moves or deletes a tag or a release, or changes a repository setting, a ruleset or a secret. An agent never does any of these.

## Alternatives

None were recorded when this was decided.

## Consequences

- For tags and releases, the rule stands beside two controls that answer T67: the tag ruleset, which covers every tag (DR-161) and whose only bypass is a deploy key that agent sessions never hold (DR-073), and releases that cannot change once published (DR-074).
- Adopters pin only a commit that a release names (DR-156), so a change that an agent merged reaches no adopter until the owner releases it (T64).
- Settings, rulesets and secrets are kept from agents by this rule, which is how the threat model answers a setting reserved for the owner being within an agent's reach (T62, T64).

## Scope

This covers tags, releases, the repository's settings, its rulesets and its secrets. Merges are DR-080 (The owner decides every merge), and approving an item on Renovate's dependency dashboard is DR-111 (Major updates wait for the owner's approval). The controls that stand beside this rule are DR-073 (Only a deploy key may bypass the tag ruleset), DR-074 (Releases are immutable) and DR-161 (The tag ruleset covers every tag).

## What reversing it would change

The line of `CLAUDE.md`'s section "What an agent never does here" on tags, releases, settings, rulesets and secrets would change, and so would the paragraph that names that section under the threat model's settings the owner keeps, the flow diagrams in `docs/how-it-works.md` and `docs/threat-model.md` in which the owner pushes a release's tag, and the answers of T62, T64 and T67. DR-073, which names this rule, would be revisited, and so would the other records of the settings that the owner keeps: DR-072, DR-074 to DR-078, DR-119, DR-140, DR-141 and DR-161. No requirement and no part of the public surface is involved.
