# Changelog

Every change that an adopter of the tool would notice is listed here, newest first, in the form [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) describes. Versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html): the major number rises for a change that adopters must act on, the minor number for new behaviour, and the patch number for a fix. DR-096 (Versions are semantic) and DR-154 (The public surface is what adopters configure or depend on) define what counts as each.

A release's entry lists any breaking change under `### Breaking`, and the release workflow refuses a release that lists one without raising the major number.

## [Unreleased]

### Added

- The repository's foundations: the OpenSpec proposal for the tool, its threat model with a risk matrix, the requirements register, the feature pages, the page explaining how the tool works, and a record of each decision.
- The assumptions that the tool's design rests on, in `docs/assumptions/`: what each one holds up, what would change if it were wrong, and how each of its facts is checked, with those about adopters' own setups among them.
- A glossary, `docs/glossary.md`, giving each word that the pages use its meaning and the words to avoid for it, with a test that fails on a word to avoid in a page's prose, and the pages reworded to its terms.
- The proposal's privacy design: consent that holds for each recorded call, a local store for each user that keeps ids only as hashes, readable by its owner alone except on Windows, and for no longer than 30 days, and a ledger format that states its version on each file's first line and is published with a JSON Schema.
- The proposal's rule that a `.pr-cost.json` that holds a key the tool does not know, gives a key twice or has no `enabled` of `true` or `false` is not valid and leaves the tool off, so that a misspelt key is not passed over, and that the report says when a merge leaves the tool off.
