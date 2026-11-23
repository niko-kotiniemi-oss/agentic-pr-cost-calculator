# B-026: A check of the keys in skills' front matter, OpenSpec's configuration and the vendored plugin's manifest

- **Status:** Open to feedback and contributions
- **Last changed:** 2026-11-22
- **Brief:** A test that lists the keys that a skill's front matter, OpenSpec's configuration and the vendored plugin's manifest may give, and fails on any other, so that a key which widens what a session does is read before it lands.
- **Rests on:** T265, T35, T141
- **Issue:** 60
- **Pull requests:** none

## Problem

A skill's front matter can give keys that act on a session, such as `allowed-tools`, which names the tools that a skill may use. OpenSpec's generated skills tell the agent to apply the `context` and the `rules` that `openspec/config.yaml` gives, and the guidance that its `operations` gives, and for a `references` entry with a `remote` OpenSpec gives the agent a command that clones that repository. The vendored plugin's manifest can give keys with which a session runs more, such as `hooks` and `mcpServers`. An update of Superpowers or OpenSpec that adds such a key passes the comparison with its source and the test of characters, and a change to the configuration steers OpenSpec's workflows, so only the owner's review of each diff reads them (T265, T35).

## What done looks like

A key that a skill's front matter, OpenSpec's configuration or the vendored plugin's manifest gives, and that the repository does not list for it, fails CI, as the keys of the tool's own plugin are held (T141), so that an update or a change that brings one is read before it lands. The change that builds it says which keys each kind of file may give, and where the list lives.

## Postponed points

- From the threat review at design of pull request 59 (its finding B9-6): a test of the keys that a skill's front matter and OpenSpec's configuration give, which goes beyond characters and which T265 records.
- From the threat review of pull request 59 against what was built (its finding D4 of boundary 9): the keys of the vendored plugin's manifest, which T265 records too.
