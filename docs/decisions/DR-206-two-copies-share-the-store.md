# DR-206: Two copies of the capture step in one session share the store

- **Type:** technical
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R181, R191, R192
- **Threats:** T44, T130, T136
- **Replaces:** none
- **Closed by:** none

## Context

A repository that turns the tool on registers the hook file for everyone who works in it, and a person who has the plugin runs it in every session that loads it (DR-197), so a terminal session in such a repository runs both, at the same events, and Claude Code runs the hooks that match an event in parallel. A person who adds the plugin both ways runs one copy of it, since Claude Code registers the hooks of one plugin per name (A69). A repository's store keeps its notes, replaced whole under a lock (DR-036), and a call is identified by its message id (DR-033). The two copies can be of different releases, since a person's plugin follows their account and a repository's hook file follows its pin, and they tell each other apart only by the store's version (DR-187). Two releases that write the same store version can still differ in how they make the fingerprint of the opt-in's files, in which keys of the configuration file they know, or in which calls they record, and a copy that makes the fingerprint otherwise takes each of the other's runs for an opt-out, while one that does not know a key that the configuration file holds takes the tool to be off and ends the session's interval.

## Decision

Every copy of the capture step that runs in a session works through the same store of each repository, under its lock, so that each call is recorded once, by its message id, and a run before a command for which another run has staged a ledger file stages nothing more, so that each commit gets one ledger file at most. A run that finds the store at a version that it does not know records, stages, takes back and puts back nothing there (DR-187), and leaves the session's calls there to the copy whose release wrote that version. Every release that writes a version of the store keeps its path, its lock and its fields, and makes its fingerprint the same way, and a test holds the fingerprint that a fixed set of files gives for each version to the hash recorded for it. Each run notes, for its session, the latest release whose copy has run in it, and a run of an earlier release than that records, stages, takes back, puts back and ends nothing for that session there, and exits with success, leaving the session to the later release's copy.

## Alternatives

- Having the plugin stand down where the repository registers the hook file, which the plugin cannot tell from what it is given, and which would leave the repository's calls unrecorded where the hook file cannot run, as when its checksum does not match.
- Having the hook file stand down where the plugin runs, which it cannot tell either.
- A store for each copy, which would record one call twice and stage two ledger files for one commit.
- Raising the store's version whenever anything that the copies share changes, without a check that holds what a version fixes, which would rest on each release's authors remembering to.

## Consequences

- A session that runs two copies records each call once and stages one ledger file for each commit, whichever copy's run comes first.
- Where the two copies are of different releases and the later one writes a store format that the earlier one does not know, the earlier copy leaves the store alone in that clone, and once the later copy no longer runs there, as when the person removes the plugin, the earlier one records nothing in that clone, with no flag, until it is updated, which the README says (T130).
- Where the two copies write the same store version, the earlier one leaves each session in which the later one has run to that copy, so that neither ends the other's intervals and the session's ledger files are written by the later release, as the README says (T136).
- A release that makes the fingerprint another way, or changes the store's path, lock or fields, writes a new store version, which the surface manifest names, so that the release check asks for a raised major number (DR-096, T44).
- Two copies double the runs at each event, each within its own time budget.

## Scope

This covers how two copies of the capture step in one session record. How a run treats a store of a version that it does not know is DR-187 (The store states its format's version, a later release upgrades an earlier one, and an unknown one is left alone), and how a call is identified is DR-033 (A call is identified by its message id).

## What reversing it would change

R181, R191 and R192 in `usage-capture` would change, with their scenarios, and so would the design's decisions 1 and 17, T44, T130, T136, the README's section on installing the plugin, which task 4.4 writes, the surface manifest, and the tasks that test two copies in one session.
