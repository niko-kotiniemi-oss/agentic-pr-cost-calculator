# DR-317: The README checks a release by its repository and tag, and checks the pin and the hook against it

- **Type:** security and privacy
- **Boundary:** outgoing
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R297, R315
- **Threats:** T28, T58, T325
- **Replaces:** none
- **Closed by:** none

## Context

The README gives `gh release verify` and `gh release verify-asset`, which check the attestation that GitHub makes for a release published while immutable releases are on (DR-074). Without `--repo`, gh checks the repository that the current folder's remote names, so a fork's own attested release passes, and a check of the release's files says nothing of the commit that an adopter pins or of the hook file that they copy. DR-074, accepted, says that turning the setting off would not break adopters, which a check that adopters run makes untrue; as an accepted record it is not edited, so this record states what holds.

## Decision

The README gives both commands with the release's tag and `--repo` naming this repository, and tells an adopter to use no file whose check fails (R297). It tells them to compare the commit that the attestation gives with the one that they pin, to check the bill of materials, and to compare the hook file's SHA-256 that it lists with the copied file's and the registration's; names the oldest gh that has both commands; and gives a check with git and a SHA-256 tool alone, which it says does not check GitHub's attestation (R315).

## Alternatives

- The two commands alone: a fork's release would pass, and the pin and the hook would go unchecked.
- No fallback: an adopter without gh, or with an older one, would skip the check without knowing what was skipped.

## Consequences

- The attestation rests on immutable releases staying on, which the threat model's settings that the owner keeps list beside T325; turning the setting off now changes what adopters' checks say.
- Whether the attestation's output names the commit, and which gh first had both commands, are checked at the build against gh itself.

## Scope

This covers what the README tells an adopter to check. That releases are immutable is DR-074, and what a release carries is DR-097.

## What reversing it would change

How hard it is to reverse: reversible. R297, R315, the README's section on adopting the tool and its test would change, and T58's and T325's answers would rest on the pin's place in the default branch's history alone.
