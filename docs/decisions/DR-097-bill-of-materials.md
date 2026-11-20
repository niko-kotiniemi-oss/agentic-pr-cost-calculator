# DR-097: Each release carries a bill of materials

- **Type:** process
- **Boundary:** outgoing
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-20
- **Requirements:** R28, R72, R99
- **Threats:** T69
- **Replaces:** none
- **Closed by:** none

## Context

Beyond Python's standard library, the tool depends on nothing (DR-023), so there is little for a bill of materials to list. The bill of materials is still what an adopter's own supply-chain checks read, and it shows at once if a dependency ever creeps in. A release also runs actions in adopters' CI, through the reusable workflow, and GitHub's source archive of every release holds the vendored and generated parts (T69).

## Decision

Each release carries a CycloneDX JSON software bill of materials, which a standard-library Python script in this repository writes from the tagged tree, never from a working tree. A release whose bill of materials cannot be written, or fails one of its checks, is not published.

## Alternatives

- Releases without a bill of materials, which would leave adopters' checks with nothing to read.

## Consequences

- It lists the actions that the report runs and the development-only parts as well as the tool, so that it does not understate what a release holds and runs (T69).
- Written from the tagged commit's tree, it cannot pick up untracked files or paths on the runner (T69).
- Its hook checksum is compared with the hook file's and the README's, and the private-reference check reads it, before anything is published (R72).
- It is one of the copies of the oldest supported Python that a test holds to `requires-python` (R99, DR-026).
- Task 6.2 validates it against the CycloneDX schema, in a recorded copy.

## Scope

This covers what each release carries for supply-chain checks. How a release is made is DR-148 (Each release is made from a tag), how it is numbered is DR-096 (Versions are semantic), the licence it names is DR-099 (The licence is MIT), that the private-reference check reads it is DR-069 (The public repository holds no private data), and how the actions it lists are pinned is DR-068 (Every action is pinned to a commit that its repository tagged).

## What reversing it would change

R28 and R72 in `releases-and-compatibility` would change, with their scenarios, and so would R99's list of copies. The design's decision 11, its decision 10 where it lists the bill of materials among the copies of the oldest Python, the proposal's list of what changes, the threat model's data flow, T69's answer, tasks 6.2 and 6.3, the README, `SECURITY.md`, `CLAUDE.md`, the feature page, and the parts, outputs, credentials, connections and release flow in `docs/how-it-works.md` would change too, and DR-023, DR-026, DR-041, DR-068, DR-069 and DR-099, whose text names the bill of materials, would be revisited. The bill of materials is not in the public surface's list, so the release check would not take the change for a breaking one, though adopters' own checks read it.
