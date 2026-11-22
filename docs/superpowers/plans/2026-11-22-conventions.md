# Conventions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task, with superpowers:test-driven-development for each task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build tasks 1.48 to 1.55 of `add-pr-cost-calculator`, which finish backlog item B-005: every tracked file held to the characters that its writer may use, pages without text that GitHub hides, images, PDFs and videos only with a record, attributes that set only line endings, the vendored copy compared path by path and synced from git's objects, ruff's naming rules and a page of conventions, line feeds in every checkout with Windows line endings read as git stages them, and paths that Windows can write.

**Architecture:** What the tests and the scripts share lives in one standard-library module, `scripts/conventions.py`: which files others write, what a script is, the one function through which every check reads a file of the working tree as git will stage it, how a character and a path are shown in printable ASCII, and the rules for paths that Windows can write. `scripts/spec_form.py` and the tests import it, as they import `scripts/wording.py` today; `scripts/risk_register.py`, which runs isolated and so imports no file beside it, keeps a copy of which files others write, which a test holds equal to the module's. The list of visible characters that the files of others may hold is the test's own, as R269 and DR-275 give it. The checks themselves live in `tests/test_conventions.py`, as the other checks of this repository live in their tests, each returning problems that name the file and what is wrong, and each shown to fail on a temporary git repository into which its defect is planted. The vendor sync stays a bash script, and the CI job on Windows line endings runs a small standard-library script that rewrites the working tree.

**Tech Stack:** Python 3.11 standard library for `scripts/`; pytest and PyYAML for the tests, which `requirements-dev.txt` pins; git; bash for the vendor sync; ruff for the naming rules.

**Spec:** R268 to R277 in `openspec/changes/add-pr-cost-calculator/specs/project-standards/spec.md`, with the changed scenarios of R176, R210 and R255; design decision 23; DR-274 to DR-282; T251 to T269.

## Global Constraints

- Every file that this repository writes holds printable ASCII and line feeds, this plan and every new test among them: a test writes each character that it plants as an escape of its code point.
- Everything that a check prints is printable ASCII: a character by its code point and its Unicode name, or by its code point and a fixed phrase where Python's database gives it no name, and a path with each other character by its code point.
- No test uses the network. Each git command that a test runs reads no global or system configuration and no git variable of the session's, through `isolated_environment` of `tests/test_roadmap.py`, unless the test plants that configuration on purpose; the suite never runs with `GIT_INDEX_FILE` set.
- `scripts/` stays on the standard library of Python 3.11 and later, so that CI's `openspec` job, which installs no package, still runs `scripts/spec_form.py`.
- Each check is seen to fail for the expected reason before the code or the page that passes it, and every acceptance test traces to a scenario of R268 to R277.
- Each task ends with `pytest`, `ruff check`, `ruff format --check`, `python3 -m mypy` and `scripts/verify-openspec.sh` passing, a commit that stages each file by its path, and its box ticked in the change's `tasks.md`.

## Review Focus

- A clone made before the attributes, with `core.autocrlf` set to `true`, keeps a carriage return in each script that a pull leaves alone: the test of characters names each one and says to delete it and check it out again (task 1.54).
- A blob that git's index names but the clone lacks, as in a partial clone: the test of characters reads blobs with `GIT_NO_LAZY_FETCH=1` and fails, naming the path, rather than fetching it (task 1.48).
- A path that holds a line feed, a tab, a quote or a tag character reaches every message through the same function that shows it by its code points, and git is always read with `-z`, so that no path is quoted or cut (tasks 1.48, 1.55).
- Reading every tracked file twice must not slow the suite much: the test reads every blob through one `git cat-file --batch` process (task 1.48).
- A Markdown autolink, such as one in angle brackets that the assumptions give, is not raw HTML, while a tag, a comment, a declaration and a processing instruction are (task 1.50).

## Tasks

- [x] **1.48 The test of characters.** `scripts/conventions.py` with `written_by_others`, `shown`, `shown_path` and `named`; `tests/test_conventions.py` with the list `VISIBLE` and its selector rule, `character_problems`, `path_problems`, `encoding_problems` and `list_problems`; `tests/test_roadmap.py`, `tests/test_guide.py` and `scripts/risk_register.py` tell the files that others write by that one definition, and the roadmap's test shows a link's target by its code points; then the nine files rewritten as printable ASCII, each compared with its base.
- [ ] **1.49 Images, PDFs and videos.** `EXCEPTIONS`, empty, and `exception_problems` in `tests/test_conventions.py`, planted in temporary repositories.
- [ ] **1.50 Pages.** `page_problems` in `tests/test_conventions.py`, reading code as `scripts/wording.py` reads it, with a function there that gives each fenced block's opening line and info string, so that the two never tell code in two ways.
- [ ] **1.51 Attributes.** A reading of every tracked file's attributes, as git's index and as the working tree hold them, in a git folder of the test's own with no `info/attributes` and no global attributes file, which `attribute_problems` in `tests/test_decisions.py` uses too.
- [ ] **1.52 The vendored copy.** `scripts/sync-superpowers.sh` writes each file from the pinned commit's objects with its mode, reads its lock as git would stage it, and compares with the lock copied into the tree that it builds; `.editorconfig` gives the lock line feeds; `tests/test_vendor_sync.py` plants each case.
- [ ] **1.53 Names.** `N` in `pyproject.toml`, `vendor/superpowers` excluded by its path, `Refused` and `Unreadable` renamed, the tests of the configuration and of a name kept from the rules, and `docs/conventions.md` with its links.
- [ ] **1.54 Line endings.** `.gitattributes`, `is_script` and `staged_bytes` in `scripts/conventions.py`, every check that reads the working tree reading through them, the advice for a clone made before the attributes in the test and in `CONTRIBUTING.md`, the CI job and its script, and the test that the job `ci` needs every job.
- [ ] **1.55 Windows paths.** `windows_problems` in `scripts/conventions.py`, read by the test of characters for every tracked path; then `CHANGELOG.md`, B-005 set to Done, and the roadmap.

## What the build found in the spec

- **Task 1.48, the files that others write.** R209, the requirement of the guide, the design's paragraph on the guide and the answers of T160 and T163 named every file under `vendor/` and `.claude/skills/` as one that others write, and so as one that no page links to. The design's one definition, which R269 rests on, is narrower: `vendor/superpowers/` but the lock at its root, and `.claude/skills/openspec-*/`. Those texts now say a file that others write, every test reads it from `scripts/conventions.py`, and the lock, which this repository writes, is a file that a page may name.
- **Task 1.48, escapes.** The scenario of R269 on escapes named `\u` and four hexadecimal digits, `\U` and eight, and `\x` and two. T263 names JavaScript, whose `\u{...}` writes any code point with up to six digits in braces, so the scenario names that form too, and the test reads it.
- **Task 1.48, where the list lives.** This plan put the list `VISIBLE` in `scripts/conventions.py`; R269 and DR-275 give it to the test, so it lives in `tests/test_conventions.py`, and no script reads it.
- **Task 1.48, the roadmap's addresses.** The roadmap's test quoted an unknown path, or a word that reads as an IP address, as it is, as it quoted a link's target; it shows each by its code points now.
- **For the threat review against what was built.** An HTML character reference, such as `&#x202E;`, in a vendored HTML file names a character that a browser shows and that the test of characters does not decode, since R269 names escapes in scripts and in a skill's front matter alone.

## Checks of the tests themselves

Filled in as each task ends: what failed first, and for which reason.

- **1.48.** Against stubs of every new function that returned nothing, 139 of the 158 tests of `tests/test_conventions.py` failed, each on an assertion that the problem it planted was named; the 19 that passed expect no problem, and the real tree's test was one of them until the implementation, against which 157 passed and the real tree's test failed with 126 problems in the nine files that the task rewrites. A clone of the base commit, 2df1efa, gives the same 126 problems in the same nine files. Before the shared definition, 37 tests of the roadmap, the guide and the risk register failed, each on a file that others write, or on a path or an address shown by its code points; before the roadmap's test read the arrow written as `->`, 13 of its tests failed; before `scripts/rewording.py` wrote three full stops, 5 of its tests failed.
