# DR-134: The oldest supported Python rises only near its end of life or for a security fix

- **Type:** technical
- **Boundary:** outgoing
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-20 and 2026-10-27
- **Requirements:** R26
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

The oldest supported Python is 3.11 (DR-025). The hook runs with whatever `python3` an adopter's machine has, so each rise of that floor leaves out the adopters who cannot follow it, while each Python version's release schedule sets when it reaches its end of life. On 2026-10-27 the owner explained what the rule is for: developers tend to update a major component, such as Python, only when they must, since it can be a hassle, while the owner wants the tool to run on secure, patched versions that cause no security issues for those who use it. The owner counts the tool among the repositories that patch a critical or major vulnerability when it is found and make no sweeps to change what is not broken.

## Decision

The oldest supported Python rises only when its version nears its end of life, or when a security fix needs a newer one, and that rise is a decision recorded with its reason.

## Alternatives

- Raising the floor with each new Python release, which DR-025 records as keeping the tool's own code simplest while leaving adopters behind.
- Keeping a version as the floor past its end of life, which DR-025 records as not chosen because that version no longer gets security fixes.
- Raising the floor also when a version's backward compatibility becomes poor, as the owner asked on 2026-10-20. On 2026-10-27 the owner left it to the change whether the rule should include that condition. Poor backward compatibility has no clear measure, so that condition could let the floor rise for convenience rather than need.

## Consequences

- A rise closes DR-025 by a record that replaces it, which gives the reason and restates what still holds, while this record stands (DR-121).
- Only the owner decides a rise (R26), as `CLAUDE.md` also says. No test holds when a rise is due, and the `releases-and-compatibility` feature page leaves it to review.
- A feature that the oldest supported Python lacks is not, by itself, a reason for a rise.
- Each rise changes the Python floor, which is part of the public surface, so it is released as a new major version (DR-096).

## Scope

This covers when the oldest supported Python rises, and how a rise is made. Which version is the floor is DR-025 (The oldest supported Python is 3.11), and where it is declared is DR-026 (`requires-python` is the one source of the oldest supported Python). When Renovate proposes dependency updates is DR-028 (Renovate waits 14 days, and proposes vulnerability fixes at once), and the approval that a major update waits for is DR-111 (Major updates wait for the owner's approval).

## What reversing it would change

R26's first sentence in `releases-and-compatibility` would change. So would the `releases-and-compatibility` feature page where it says when the oldest Python rises and leaves that to review, the README's section on compatibility and releases, the proposal's line on dependency updates, and the comments on the oldest Python in `.github/workflows/ci.yml` and `tests/test_repository.py`. The rule is not part of the public surface, so changing it would not be a breaking change for adopters, and DR-025 would be revisited.
