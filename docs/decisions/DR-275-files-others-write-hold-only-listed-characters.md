# DR-275: The files that others write hold only the visible characters that a test lists

- **Type:** security and privacy
- **Boundary:** incoming
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-27 and 2026-11-21
- **Requirements:** R269, R275
- **Threats:** T252, T253, T255, T261, T263
- **Replaces:** none
- **Closed by:** none

## Context

Superpowers' files are vendored under `vendor/superpowers/`, and OpenSpec writes its skills under `.claude/skills/openspec-*/`. Sessions here load both, and run the vendored hook scripts at their start (T35). Their own checks compare each file with its source, and no file of theirs may be edited here (DR-041, DR-042), so the rule for this repository's own files cannot hold them. On 2026-11-21 they held 20 visible characters beyond printable ASCII, such as dashes, arrows and check marks, 7 of them in files other than Markdown, and three of them held variation selector 16, which a reader cannot see, each time right after a warning sign, which it shows as a picture. The plan of 2026-10-27 gave every file, theirs included, a check for characters that are invisible or change the order of text, and said that none held one, which missed those selectors. The first check of the records refused characters by their Unicode category, and let a variation selector, a filler and a blank Braille pattern through (DR-152). The design-stage review of this change found that the comparison of `vendor/superpowers/` with upstream left out every file or folder named `UPSTREAM.lock`, at any depth, so that one could hold anything and pass as upstream's (T261); that an escape which a script or a skill's front matter decodes writes a character that a test of bytes never reads, as three YAML readers showed (T263); that letters hold both look-alikes of Latin letters and fillers that show as blank; and that a curly quotation mark, harmless in prose, makes bash run what a reader takes for quoted text. On 2026-11-21 the owner chose a list of the characters that pass over a list of those that fail.

## Decision

Each file that others write holds only printable ASCII characters, tabs, line feeds and the visible characters that `tests/test_conventions.py` lists, each by its code point and its Unicode name, for Markdown alone or for any file, and holds variation selector 16 only right after a character that the list gives for it. A character that an escape writes by its code, in a script or in a skill's front matter, which YAML reads, is held as that character. The list gives only marks of punctuation and symbols, by their Unicode categories, and none that shows as blank. An update that brings a character outside the list fails CI until its pull request adds that character, in a diff that the owner reads, and the list's own check refuses one that cannot be seen. The comparison of `vendor/superpowers/` with its pinned commit, which these files rest on, leaves out only the lock at its root, by its path.

## Alternatives

- Refusing a named set of invisible and direction-changing characters and letting every other through: an update could bring a kind that the set misses, as the first check of the records showed (DR-152), and a letter of another script that looks like a Latin one would pass.
- Refusing every character beyond printable ASCII, as in this repository's own files: those files cannot be edited here, so every update that brought a dash would fail until a rule changed.
- Relying on the comparison with the source alone: it shows that a file is upstream's, not that upstream's file hides nothing (T252).
- Admitting letters and digits to the list: a letter of another script that looks like a Latin one, or a filler that shows as blank, could be listed under its own true name.
- One list for every kind of file: a character listed for prose, such as a curly quotation mark, would pass in a shell script, where it reads as quoting what bash runs.
- Reading bytes alone: an escape that a loader decodes would write a character that no test of bytes reads (T263).

## Consequences

- `tests/test_conventions.py` fails on a character outside the list, on one listed for Markdown alone in another file, on one that an escape writes, or on variation selector 16 after a character not listed for it, naming the file, the line, the column and the character by its code point and its name, and saying that the owner decides whether the list gives it; and it fails on a list that gives a character that is not punctuation or a symbol, that shows as blank, or whose name is not the one that Unicode gives it (R269; T252, T253, T263; task 1.48).
- On the oldest supported Python the list's check passes over a character that its Unicode database does not yet know, which every later Python in CI checks (T255).
- An update of Superpowers or OpenSpec that brings a new visible character takes one more step, which its failure names, and one whose character only a joiner or a combining mark shows waits for the owner's decision on the rule (T255).
- A tab is allowed in these files, since it shows as space and hides nothing; none of them held one on 2026-11-21.
- `scripts/sync-superpowers.sh` compares every path below `vendor/superpowers/`, whatever its name, and leaves out only `vendor/superpowers/UPSTREAM.lock` (R275; T261; task 1.52).

## Scope

This covers the characters of the files that others write, and the comparison of the vendored files that they rest on. Which files those are, and what the repository's own files hold, is DR-274 (Everything that this repository writes holds printable ASCII). How the vendored files and the generated skills come in and are compared with their source is DR-041 (Superpowers is vendored and compared with upstream in CI) and DR-042 (OpenSpec is pinned and its skills are regenerated in CI). Which attributes the repository may set is DR-280 (The repository's attributes set nothing but line endings, and are read as git holds them).

## What reversing it would change

How hard it is to reverse: reversible. The list and its check are part of one test, and the comparison is one line of a script. R269 and R275 in `project-standards` would change, with their scenarios, and so would the answers of T252, T253, T255, T261 and T263, design decision 23, tasks 1.48 and 1.52 and the design's risk on such updates. Nothing that adopters configure or depend on changes, so the change would not be a breaking one for adopters.
