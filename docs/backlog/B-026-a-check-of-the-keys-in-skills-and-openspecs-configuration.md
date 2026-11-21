# B-026: A check of the keys in skills' front matter and OpenSpec's configuration

- **Status:** Open to feedback and contributions
- **Last changed:** 2026-11-21
- **Brief:** A test that lists the keys that a skill's front matter and OpenSpec's configuration may give, and fails on any other, so that a key which widens what a session does is read before it lands.
- **Rests on:** T265, T35, T141
- **Issue:** 60
- **Pull requests:** none

## Problem

A skill's front matter can give keys that act on a session, such as `allowed-tools`, which names the tools that a skill may use, and OpenSpec's generated skills tell the agent to apply the `context` and the `rules` that `openspec/config.yaml` gives. An update of Superpowers or OpenSpec that adds such a key passes the comparison with its source and the test of characters, and a change to the configuration steers every OpenSpec workflow, so only the owner's review of each diff reads them (T265, T35).

## What done looks like

A key that a skill's front matter or OpenSpec's configuration gives, and that the repository does not list for it, fails CI, as the keys of the tool's own plugin are held (T141), so that an update or a change that brings one is read before it lands. The change that builds it says which keys each kind of file may give, and where the list lives.

## Postponed points

- From the threat review at design of pull request 59 (its finding B9-6): a test of the keys that a skill's front matter and OpenSpec's configuration give, which goes beyond characters and which T265 records.
