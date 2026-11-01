## What changes

<!-- Before: what a reader sees now. After: what they see once this merges. -->

Before:

After:

## OpenSpec change

<!-- The change under openspec/changes/ that this pull request implements, or why it needs none. -->

## Checklist

- [ ] Tests written first, positive and negative, and seen failing for the expected reason
- [ ] `pytest`, `ruff check`, `ruff format --check`, `mypy` and `scripts/verify-openspec.sh` pass
- [ ] Threat model revisited at design and against what was built, with each threat's impact and likelihood
- [ ] `docs/requirements.md`, the feature page and `docs/how-it-works.md` match the change
- [ ] A line under `## [Unreleased]` in `CHANGELOG.md`, if adopters would notice the change
- [ ] If it rewords pages to the glossary or adds a word to avoid, the output of `python3 scripts/rewording.py`, run at its head, is in a comment
- [ ] Nothing private: no transcripts, session identifiers, private cost figures, internal names or secrets
