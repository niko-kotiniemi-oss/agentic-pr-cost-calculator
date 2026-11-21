# DR-280: The repository's attributes set nothing but line endings, and are read as git holds them

- **Type:** security and privacy
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R274
- **Threats:** T256, T259
- **Replaces:** none
- **Closed by:** none

## Context

A git attribute that the repository commits can change what a reader of a file gets: `working-tree-encoding` and `filter` change what a checkout writes, `ident` writes an object's id into a file, `export-subst` and `export-ignore` change what `git archive` writes, and `binary`, `diff` and `linguist-generated` make git or GitHub fold a diff. R134 refused the last three for the records and the files that steer, and the first three for the plugin's files, and the design of this change refused `working-tree-encoding` for every file (T256). Its design-stage review found that the other attributes give some reader other text than git holds too: in a trial with git 2.43.0 on 2026-11-21, `export-subst` wrote a commit's subject, with a direction-changing character, into the file that `git archive` gave. It also found that an attributes file which gives itself `working-tree-encoding` is written by every checkout with each line that holds a character such as `=` or `*` rewritten, which git then cannot read as the attribute that the line gives, so that a check that asks git for the attributes as the working tree holds them, as each check of R134 did, misses each such line: in a trial with git 2.43.0 on 2026-11-21, those checks passed in a fresh clone of such a commit while git, read from its index, gave `CLAUDE.md` `linguist-generated` (T259). And `working-tree-encoding=UTF-7` changes code that holds printable ASCII alone, which no test of characters can see: a checkout writes `+` as `+-`, so that `print(1+1)`, as git held it in a trial that day, printed 0. On 2026-11-21 the repository tracked no attributes file.

## Decision

The repository's attributes give a tracked file only `text` and `eol`, which set its line endings, and no other attribute, in any state. Each check of attributes, this one and each of R134, reads them as git's index holds them and as the working tree holds them, and reads none of a person's own.

## Alternatives

- Refusing a named set of attributes, as R134 does for some files: an attribute that git or GitHub adds later would pass until a threat found it, as `export-subst` and `filter` passed the design of this change.
- No attributes file at all: each clone's line endings would be left to the person's git, and a clone made with `core.autocrlf` set to `true` fails the tests and runs neither its hook nor its scripts, which DR-281 answers with `text` and `eol`, the only attributes that this rule lets in.
- Reading the attributes from the working tree alone, as the checks of R134 did: an attributes file that re-encodes itself hides from them each line that a checkout rewrites (T259).

## Consequences

- `tests/test_conventions.py` fails on any other attribute that the repository's attributes give a tracked file, naming the file and the attribute, and the helper that the checks of R134 share reads the attributes as git's index holds them too (R274; T256, T259; task 1.51).
- R134's checks stay as they are, and this rule holds every file besides, the vendored files and the tests among them.
- An attribute that a later need asks for, such as one that marks the vendored files for GitHub's statistics of languages, takes a change to the test, which the owner reads.

## Scope

This covers the attributes that the repository sets and how the checks read them. Which diffs no attribute may hide is part of DR-108 (Each decision has a record of its own, in an index) and of R134. The characters that a checkout holds are DR-274 (Everything that this repository writes holds printable ASCII), and the line endings that the attributes give are DR-281 (Every checkout holds line feeds, and the checks read Windows line endings as git stages them).

## What reversing it would change

How hard it is to reverse: reversible. The rule is part of one test, and the reading is one helper. R274 in `project-standards` would change, with its scenarios, and so would the answers of T256 and T259, design decision 23 and task 1.51. Nothing that adopters configure or depend on changes, so the change would not be a breaking one for adopters.
