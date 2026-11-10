# DR-202: Capture needs an opt-in that the person sets, or that the environment they use sets

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the owner, 2026-10-18 and 2026-11-09
- **Requirements:** R1, R182, R186
- **Threats:** T3, T134
- **Replaces:** DR-046
- **Closed by:** none

## Context

When a repository's owner turns the tool on, the usage of everyone who works there, outside contributors who never agreed among them, could be committed and published with their pull requests (T3), and the ledger and the comment are as public as the repository (T31). In a public repository, publishing someone's usage needs their own consent. The owner decided on 2026-10-18 that capture also needs the person's own opt-in, which DR-046 records.

The tool now also comes as a plugin (DR-197), which a person adds for themselves, or which an organization turns on for its members, or requires, on claude.ai, and in a cloud environment the opt-in is one line in the environment's setup script (DR-201). An Owner of a Team or Enterprise organization can share a cloud environment with every member, and its setup script runs in each session that a member starts in it; an Owner also chooses the organization's default environment, which fills a member's selection until they pick another, and an organization's managed settings run their hooks in its members' terminal and cloud sessions (A71). On 2026-11-09 the owner chose to include, documented, the option for an organization to turn capture on for its members, with the plugin turned on for them and the line in a shared environment, with no code of its own, while a mode that members cannot turn off stays for later (DR-189). Claude Code's pages, read on 2026-11-09, say that Projects aren't offered on Team or Enterprise plans yet. This record restates DR-046 with the organization's option added.

## Decision

Capture records a session's calls only when the repository has turned the tool on and the opt-in holds in the global git configuration where the session runs. The person sets it there, or the setup script of the cloud environment that they use does, or their organization's managed settings do. An organization can put the line in a shared environment's setup script, or in the environment that it makes its default, which a member who has picked no environment uses, and that opts in its members' sessions in that environment. It can also turn the plugin on for its members, or require it, which opts no one in: the plugin, however it came to a session, never opts anyone in. The repository decides whether the tool is used there, and only the person, or the environment or the organization's settings that their sessions run under, decides whether their session's usage is published, so an outside contributor's usage is not committed merely because the repository's owner turned the tool on.

## Alternatives

- The repository's setting alone, which would publish the usage of everyone who works in the repository, including people who never agreed to it.
- The person's own setting alone, with no route for an organization, which the owner set aside on 2026-11-09 for a documented option.
- Taking the plugin's presence as the opt-in, which an organization can require for its members, who then could not turn capture off.
- A mode in which an organization turns capture on and its members cannot turn it off, which DR-189 leaves to a later change.

## Consequences

- Nothing is recorded unless both switches are on, so a pull request made without anyone's opt-in has no ledger, and its comment gives the CI cost and says that no agent usage was recorded (R20).
- An opt-in applies in every repository that has the tool on, until the person turns it off in one (DR-050, DR-185).
- A member whose shared or default environment opts in, or whose organization's managed settings write the opt-in, has their usage published in every repository that turns the tool on where those sessions work, so the README's section on organizations says that the organization tells its members so, how a member sees what turns their capture on, with git's `--show-origin` and Claude Code's `/hooks`, that a person's own line belongs in an environment of their own, and how a member turns capture off (R186, T134).
- In a terminal session the opt-in is the person's own global configuration, which the person writes unless their organization's managed settings run a hook that writes it, so the plugin, however it came, opts no one in there, while the organization's settings can.
- The option reaches members' project threads only once Projects are offered on their organization's plan.
- The README's section on adopting the tool, which task 4.4 writes, says how each person opts in, before they start a session, and what a public repository publishes when the tool is on (T31).

## Scope

This covers whose consent capture needs and who may give it. The repository's switch is DR-021 (One file, `.pr-cost.json`, turns the tool on or off). Where the opt-in is read is DR-183 (The opt-in is read only from the person's global git configuration, and git's own reading of it can only turn capture off), and how it is applied is DR-049 (The opt-in is read strictly), DR-050 (A repository's git configuration can turn capture off, never on) and DR-168 (Consent holds for each call, inside intervals that runs begin and end). Which repositories one opt-in covers is DR-185, how a person opts in within a cloud environment is DR-201, and a mode that members cannot turn off is DR-189 (An organization mode, in which capture cannot be turned off, is left to a later change).

## What reversing it would change

R1 and R182 in `switch-and-opt-in` would change, with their scenarios, and so would R186, the design's decision 6, T3's answer, T134, T31's answer where it names how each person opts in, the proposal, the README, `SECURITY.md`, the `switch-and-opt-in` feature page, `docs/how-it-works.md`, and tasks 1.2, 2.4, 4.4 and 7.1. DR-201 would be revisited. The opt-in key is part of the public surface, so removing it would be a breaking change for adopters (DR-096).
