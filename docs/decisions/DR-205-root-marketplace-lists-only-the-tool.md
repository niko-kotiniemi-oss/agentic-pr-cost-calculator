# DR-205: This repository's root marketplace file lists only the tool's plugin

- **Type:** technical
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R184, R190
- **Threats:** T35, T132, T140
- **Replaces:** none
- **Closed by:** none

## Context

A marketplace that a person adds on claude.ai is read from the file `.claude-plugin/marketplace.json` at the root of the repository that they name (A72), and this repository becomes one so that a person can install the plugin from it (DR-203). That file now lists only the vendored Superpowers, as the marketplace that this repository's own `.claude/settings.json` names for its terminal sessions and that `.claude/hooks/session-start.sh` adds in its cloud sessions, whose plugins `.claude/settings.json` does not install (DR-041), so a person who added the repository would be offered this repository's copy of Superpowers, which only its development uses. Claude Code combines a marketplace's entry for a plugin with the plugin's own manifest: with `strict` at its default it adds the entry's commands, agents and skills to the plugin, and the entry's hooks replace the manifest's for the same event, while `"strict": false` beside any of those stops the plugin loading and `"defaultEnabled": false` starts it turned off (A72). The root file is served from the default branch, so a change to it reaches everyone who added the marketplace before any release.

## Decision

The root marketplace file holds only the marketplace's name, its owner and one entry that gives the tool's plugin's name and its folder, and CI fails when the file, parsed, holds any other key, value or entry. The marketplace that loads the vendored Superpowers in this repository's own sessions moves to a folder under `vendor/`, and both places that add it follow: `.claude/settings.json` names its folder, and `.claude/hooks/session-start.sh` adds it, so that a person who adds this repository as a marketplace is offered only the tool. Once Superpowers loads from there, the root file is removed, in a pull request that changes nothing else, the checks that hold it follow, in a pull request that changes no marketplace file, and the root file comes back, holding only the tool's plugin, in the pull request after the first release that carries the plugin, which changes nothing else.

## Alternatives

- Listing both plugins in the root file, which would offer every person who adds the marketplace a copy of Superpowers from this repository, pinned for this repository's development, rather than from its upstream.
- A marketplace of the tool's own in another repository, which DR-203 turned down.
- Checking only which plugin the root file lists and from which folder, which would let an entry's other fields add to the plugin, replace its hooks or stop it loading, before any release.

## Consequences

- This repository's own sessions load Superpowers as before, from the marketplace's new path. A test holds the vendored marketplace's file, the settings keys that name it and the folder that the session-start hook adds, and task 6.7 checks in a cloud session, on a branch whose root file no longer lists Superpowers, that Superpowers still loads before the old file changes (T35).
- The marketplace file under `vendor/` is the repository's own, like `UPSTREAM.lock`, and lies outside the vendored copy, so CI's comparison of that copy with its upstream leaves it out, while a change to it is reviewed as one to `.claude/` would be (T35).
- The root file is part of what the marketplace serves, so CI holds it whole, a pull request that adds, changes or removes it changes nothing else (DR-204), and the README gives no command that pins the marketplace to a tag, since a release's own tag holds an earlier release's plugin (DR-203, T132, T140).
- Until the root file comes back, a person who adds this repository as a marketplace is offered no plugin, neither Superpowers nor the tool, and the checks that hold the root file are on the default branch before it comes back, so that the pull request that brings it back is held by checks that it does not change (DR-204).

## Scope

This covers what this repository's root marketplace file holds. What the marketplace serves is DR-204 (The marketplace serves only a release's plugin), and how Superpowers is vendored is DR-041 (Superpowers is vendored and compared with upstream in CI).

## What reversing it would change

R184 and R190 in `releases-and-compatibility` would change, with their scenarios, and so would `.claude/settings.json`, `.claude/hooks/session-start.sh`, the design's decision 11, T35, T132, T140 and the tasks that move the development marketplace, remove the root file and bring it back.
