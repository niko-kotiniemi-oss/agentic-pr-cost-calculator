# DR-274: Everything that this repository writes holds printable ASCII

- **Type:** security and privacy
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-27
- **Requirements:** R268, R272
- **Threats:** T251, T256, T258, T260, T264, T271
- **Replaces:** none
- **Closed by:** none

## Context

Seven requirements held single pages to printable ASCII, each after a threat that found text in that page that GitHub or a reader does not show: the records, the specs, the README's sections of detail, the roadmap and the backlog, the guide, the risk register and the context files (R128, R176, R200, R210, R221, R246, R255). The rest of the repository, its scripts, tests, workflows and hooks and most of its pages, had no such check, and a link from the roadmap or a backlog item can lead to any of them, as the threat review of pull request 29 found. A character that changes the order in which text is shown can make code read as a comment while it runs, and an invisible one can split a word that a check looks for (T251). The owner asked on 2026-10-27 for a character set for the project, and the plan of that day gave printable ASCII for everything that the project writes, which backlog item B-005 holds. On 2026-11-21 nine of the files that the repository writes held other characters: arrows in the design's risks and in the mapping of B-022 that quotes them, signs in the formulas of the page on how the tool works, ellipses in a feature page, a script and its test, and characters that three tests plant on purpose. The design-stage review of this change found three more ways past a test of characters: a Python file of printable ASCII can declare an encoding, such as UTF-7, under which a line that reads as a comment runs as code (T260); two paths that differ only in case become one file where a file system ignores case (T258); and a failure that quotes a path or a character as it is carries that character into a log that a session reads (T264). The threat review against what was built found that two folders that differ only in case become one folder there too, so that a folder `vendor/Superpowers/` beside the vendored copy would write its files, a hook among them, into the folder of the plugin that the repository enables, while every check passed them as files of this repository's own (T258). It found too that YAML, JSON and TOML decode an escape in a string into the character that it writes, so that a `context` that `openspec/config.yaml` gives in printable ASCII gave a session tag characters that every check passed (T271), and that a Python file whose extension is in upper case, such as `tests/conftest.PY`, was not read as Python (T260).

## Decision

Every file that this repository writes holds only printable ASCII characters and line feeds, also in each string that YAML, JSON or TOML decodes from a file of that kind, by its extension in any case, or from a page's front matter, and one that Python reads as source, by its extension in any case or by its first line, declares no encoding but UTF-8. Every tracked path holds only printable ASCII characters other than the space, and differs from every other path, and from each folder that holds one, in more than the case of its letters, and so does each folder from every other folder. The files that others write, under `vendor/superpowers/` but the lock at its root and under `.claude/skills/openspec-*/`, are held as DR-275 gives it instead, and a file that DR-276 lets in is read only where its bytes are UTF-8. A test reads each file as git's index holds it and as the working tree holds it, a link as the path that it holds, and prints only printable ASCII: a character by its code point and its name, never by itself, and a path's other characters by their code points.

## Alternatives

- Holding more pages to the rule one at a time, as each threat finds one: the files between them stay unchecked, and a link can lead to any of them.
- Reading only the working tree, as the checks of single pages do: an attribute that the repository commits, `working-tree-encoding=UTF-7`, keeps in git a character, or an HTML comment, that every checkout writes otherwise, which a trial with git 2.43.0 showed on 2026-11-21, and in that trial the checks of the context files and of the guide failed on the pages so written with problems that named neither the attribute nor the comment (T256).
- Allowing the characters that the files held, such as an arrow or an accented letter: each is visible, but a list of them for the project's own files would grow with each page, and printable ASCII needs no list to be read.
- Reading the escapes of the files that this repository writes by their forms, as the files that others write are read (DR-275): the tests write the characters that they plant as escapes, which such a reading would refuse, while a loader's own reading gives each string of a file that a loader reads as that loader decodes it, whatever form its escapes take.
- Quoting a character or a path as it is in a failure, as most checks here do: the failure would carry the character that it refuses into the job's log, which a session reads when it is asked why CI fails (T264).

## Consequences

- `tests/test_conventions.py` fails on a character other than printable ASCII and a line feed in a file that this repository writes, naming the file, the line, the column and the character by its code point and its name, and on such a path, on two paths, a path and a folder, or two folders, that differ only in case, on a Python file that declares an encoding other than UTF-8, on a string that YAML, JSON or TOML decodes into such a character, keys among them, and on a file of those kinds or a page's front matter that its loader cannot read, on bytes that are not UTF-8, on a path that is neither a file nor a link, and on reading nothing (R268, R272; T251, T258, T260, T271; task 1.48).
- Everything that the test prints is printable ASCII, and the roadmap's check of a link's target names such a character by its code point too (R272; T264; task 1.48).
- The design's risks write the arrow that OpenSpec's template gives as `->`, and the roadmap's test reads that form, so an agent that follows the template meets a failure that names the arrow. The mapping of B-022 writes the arrows that it quotes from the base as `->` too, and says so at its start: it is the evidence of a sweep that has merged, which its script no longer compares.
- The page on how the tool works writes its formulas with `*` and `sum`, an ellipsis becomes three full stops, and the tests write the characters that they plant as escapes of their code points.
- The checks of single pages keep their own rules on what GitHub hides; for characters, this test covers every page that they read, as git holds it, and DR-279 holds every page to the text that GitHub shows.
- A checkout writes line feeds whatever `core.autocrlf` says, and the test reads a carriage return right before a line feed in the working tree as a line feed, as git stages it, in every file but a script, so that a file that an editor saves with Windows line endings passes as git will commit it (DR-281).
- Commit messages and the text of pull requests are not files, and a session reads them too: tasks 1.9 and 1.14 check them for private references only, and their characters are left to the owner's review (T251, B-025).

## Scope

This covers the characters of every tracked file that this repository writes and of every tracked path, and how the test reads them and reports them. What the files that others write may hold is DR-275 (The files that others write hold only the visible characters that a test lists), which files that are not text the repository tracks is DR-276 (A diagram is Mermaid in the Markdown that shows it, and an image, a PDF or a video needs a record of its own), the text that GitHub hides in a page is DR-279 (No page that this repository writes holds text that GitHub hides), and the attributes that could change what a checkout holds are DR-280 (The repository's attributes set nothing but line endings, and are read as git holds them). What a record holds beyond its characters is DR-152 (A record is plain text and links only to other records).

## What reversing it would change

How hard it is to reverse: reversible. The check is part of one test, and reversing the rule would let other characters back into the files that no check of a single page reads. R268 and R272 in `project-standards` would change, with their scenarios, and so would the answers of T251, T256, T258, T260, T264 and T271, design decision 23, task 1.48, `docs/conventions.md` and the `project-standards` feature page. DR-275, DR-276 and DR-279 would be revisited. Nothing that adopters configure or depend on changes, so the change would not be a breaking one for adopters.
