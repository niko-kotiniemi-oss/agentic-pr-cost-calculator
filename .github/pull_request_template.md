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
- [ ] `docs/requirements.md`, the feature page, `docs/how-it-works.md` `docs/roadmap.md` and each backlog item in `docs/backlog/` that the change finishes, adds or moves match the change
- [ ] If it adds a backlog item at `Planned`, moves one to `Planned`, or changes what an agreed item's What done looks like says, the description says so, and where the owner asked for it
- [ ] A line under `## [Unreleased]` in `CHANGELOG.md`, if adopters would notice the change
- [ ] If it rewords pages to the glossary or adds a word to avoid, the output of the default branch's copy of `scripts/rewording.py`, run at its head as that script's docstring shows, is in a comment
- [ ] Nothing private: no transcripts, session identifiers, private cost figures, internal names or secrets
