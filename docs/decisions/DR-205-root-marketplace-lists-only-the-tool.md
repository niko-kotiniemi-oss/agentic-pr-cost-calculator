# DR-205: This repository's root marketplace file lists only the tool's plugin

- **Type:** technical
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R184
- **Threats:** T35, T132
- **Replaces:** none
- **Closed by:** none

## Context

A marketplace that a person adds on claude.ai is read from the file `.claude-plugin/marketplace.json` at the root of the repository that they name (A72), and this repository becomes one so that a person can install the plugin from it (DR-203). That file now lists only the vendored Superpowers, as the marketplace that this repository's own `.claude/settings.json` names for its development sessions (DR-041), so a person who added the repository would be offered this repository's copy of Superpowers, which only its development uses.

## Decision

The root marketplace file lists only the tool's plugin. The marketplace that loads the vendored Superpowers in this repository's own sessions moves to a folder under `vendor/`, whose path `.claude/settings.json` names, so that a person who adds this repository as a marketplace is offered only the tool.

## Alternatives

- Listing both plugins in the root file, which would offer every person who adds the marketplace a copy of Superpowers from this repository, pinned for this repository's development, rather than from its upstream.
- A marketplace of the tool's own in another repository, which DR-203 turned down.

## Consequences

- This repository's own sessions load Superpowers as before, from the marketplace's new path, which the build checks before the old file changes.
- The marketplace file under `vendor/` is the repository's own, like `UPSTREAM.lock`, and lies outside the vendored copy, so CI's comparison of that copy with its upstream leaves it out, while a change to it is reviewed as one to `.claude/` would be (T35).
- The root file is part of what the marketplace serves, so the check that holds the plugin's folder to a release (DR-204) also holds that the root file lists only the tool's plugin, from that folder (T132).

## Scope

This covers what this repository's root marketplace file lists. What the marketplace serves is DR-204 (The marketplace serves only a release's plugin), and how Superpowers is vendored is DR-041 (Superpowers is vendored and compared with upstream in CI).

## What reversing it would change

R184 in `releases-and-compatibility` would change, with its scenario on what the root file lists, and so would `.claude/settings.json`, the design's decision 11, T35, T132 and the task that moves the development marketplace.
