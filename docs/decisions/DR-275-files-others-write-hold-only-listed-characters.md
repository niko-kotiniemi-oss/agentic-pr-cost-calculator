# DR-275: The files that others write hold only the visible characters that a test lists

- **Type:** security and privacy
- **Boundary:** incoming
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-27
- **Requirements:** R269
- **Threats:** T252, T253, T255
- **Replaces:** none
- **Closed by:** none

## Context

Superpowers' files are vendored under `vendor/superpowers/`, and OpenSpec writes its skills under `.claude/skills/openspec-*/`. Sessions here load both, and run the vendored hook scripts at their start (T35). Their own checks compare each file with its source, and no file of theirs may be edited here (DR-041, DR-042), so the rule for this repository's own files cannot hold them. On 2026-11-21 they held 20 visible characters beyond printable ASCII, such as dashes, arrows and check marks, and three of them held variation selector 16, which a reader cannot see, each time right after a warning sign, which it shows as a picture. The plan of 2026-10-27 gave every file, theirs included, a check for characters that are invisible or change the order of text, and said that none held one, which missed those selectors. The first check of the records refused characters by their Unicode category, and let a variation selector, a filler and a blank Braille pattern through (DR-152).

## Decision

Each file that others write holds only printable ASCII characters, tabs, line feeds and the visible characters that `tests/test_conventions.py` lists, each by its code point and its Unicode name, and holds variation selector 16 only right after a character that the list gives for it. The list gives only letters, digits, marks of punctuation and symbols, by their Unicode categories, and none that shows as blank. An update that brings a character outside the list fails CI until its pull request adds that character, in a diff that the owner reads, and the list's own check refuses one that cannot be seen.

## Alternatives

- Refusing a named set of invisible and direction-changing characters and letting every other through: an update could bring a kind that the set misses, as the first check of the records showed (DR-152), and a letter of another script that looks like a Latin one would pass.
- Refusing every character beyond printable ASCII, as in this repository's own files: those files cannot be edited here, so every update that brought a dash would fail until a rule changed.
- Relying on the comparison with the source alone: it shows that a file is upstream's, not that upstream's file hides nothing (T252).

## Consequences

- `tests/test_conventions.py` fails on a character outside the list, or on variation selector 16 after a character not listed for it, naming the file, the line, the column and the character by its code point and its name, and on a list that gives a character that cannot be seen or a name other than the one that Unicode gives it (R269; T252, T253; task 1.48).
- An update of Superpowers or OpenSpec that brings a new visible character takes one more step, which its failure names (T255).
- A tab is allowed in these files, since it shows as space and hides nothing; none of them held one on 2026-11-21.

## Scope

This covers the characters of the files that others write. Which files those are, and what the repository's own files hold, is DR-274 (Everything that this repository writes holds printable ASCII). How the vendored files and the generated skills are compared with their source is DR-041 (Superpowers is vendored and compared with upstream in CI) and DR-042 (OpenSpec is pinned and its skills are regenerated in CI).

## What reversing it would change

How hard it is to reverse: reversible. The list and its check are part of one test. R269 in `project-standards` would change, with its scenarios, and so would the answers of T252, T253 and T255, design decision 23, task 1.48 and the design's risk on such updates. Nothing that adopters configure or depend on changes, so the change would not be a breaking one for adopters.
