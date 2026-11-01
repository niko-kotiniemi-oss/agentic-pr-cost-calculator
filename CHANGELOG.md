# Changelog

Every change that an adopter of the tool would notice is listed here, newest first, in the form [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) describes. Versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html): the major number rises for a change that adopters must act on, the minor number for new behaviour, and the patch number for a fix. DR-096 (Versions are semantic) and DR-154 (The public surface is what adopters configure or depend on) define what counts as each.

A release's entry lists any breaking change under `### Breaking`, and the release workflow refuses a release that lists one without raising the major number.

## [Unreleased]

### Added

- The repository's foundations: the OpenSpec proposal for the tool, its threat model with a risk matrix, the requirements register, the feature pages, the page explaining how the tool works, and a record of each decision.
- The assumptions that the tool's design rests on, in `docs/assumptions/`: what each one holds up, what would change if it were wrong, and how each of its facts is checked, with those about adopters' own setups among them.
