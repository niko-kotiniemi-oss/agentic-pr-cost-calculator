# DR-189: An organization mode, in which capture cannot be turned off, is left to a later change

- **Type:** scope
- **Status:** accepted
- **Decided by:** the owner, 2026-11-03
- **Requirements:** R1, R37, R160
- **Threats:** none
- **Replaces:** none
- **Closed by:** none

## Context

Capture records a person's calls only when the repository has turned the tool on and the person has opted in, and only the person decides whether their usage is published (DR-046). The way capture checks consent has limits, which task 4.4 has the README state: a routine write to the person's global configuration ends every open interval, a session given its first prompt before it starts can lose its first calls, and an opt-out and back in the repository's own configuration between two runs goes unseen. The owner said on 2026-11-03 that these are as intended, since the tool is an open-source product that people opt in to, not one built to catch a person who avoids being counted on purpose. The owner also said that an organization could later want its members' capture always on, so that they always understand what their work costs, and asked that no choice in this change rule that out, leaving the decision and its development to the future, where feedback and contributions may call for it.

## Decision

Capture is built for people who opt in, and does not try to stop a person who avoids it on purpose, who can turn it off (DR-046). A mode in which an organization turns capture on for its members, and they cannot turn it off, is left to a later change, with its own spec, its own threat review and the owner's decision, and no choice in this change rules it out.

## Alternatives

- Building an organization mode in this change, before anyone has asked for it.
- Hardening capture against a person who avoids it on purpose, which would mean checking the person's own machine against them, and which a tool that people opt in to does not need.

## Consequences

- The threat model rates no threat for a person who avoids capture on purpose, since turning it off is theirs to do.
- A later mode can be added without undoing this change: each ledger file states its format's version, so a later version can say under which rule its calls were recorded; the store states its version, and a later release upgrades it (DR-187); and the rule that only the person turns capture on is DR-046, DR-050 and DR-183, which later records can close.
- The opt-in key and the ledger format are part of the public surface, so such a mode would come with a raised major number (DR-096).

## Scope

This covers whether capture tries to stop a person who avoids it, and whether anyone other than the person may turn capture on. Who decides whether a person's usage is published is DR-046 (Each person turns on capture of their own sessions), and where the opt-in is read from is DR-183 (The opt-in is read only from the person's global git configuration, and git's own reading of it can only turn capture off).

## What reversing it would change

Building the mode would change R1, R37 and R160 in `switch-and-opt-in`, with their scenarios, close DR-046, DR-050 and DR-183 with records that restate what still holds, add a trust boundary for the organization's policy to the threat model, with its threats, add a version of the ledger format, and change the design's decision 6, the README and the opt-in's feature page. Hardening capture against a person who avoids it would add threats for that person, with their answers.
