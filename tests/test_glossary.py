"""The specs and pages use the glossary's words, and each term is defined once.

`docs/glossary.md` gives each term's meaning and the words to avoid for it, in a
table per topic (R137, R138; design decision 14; DR-164). This test reads the prose
of every file that git tracks and GitHub shows as Markdown, by the extensions and
the name that GitHub's language list gives it, and fails on each word to avoid that
it finds, naming the file, the line and the term to use. A word to avoid is matched
as a whole word in any case, and so is its plural, which adds "s" or "es" or, after
a consonant, turns a final "y" into "ies". Where a word to avoid has a space, the
page may break the line or use a no-break space instead, and where it has an
apostrophe, the page may curl it, so that neither hides the word; nor does emphasis,
since a word ends only where no letter or digit follows it. The space between a
word's words, and the spaces after a heading's or a title's text, are matched in one
way only, and a line's code spans are found in one pass over its backticks, so that
a long run of spaces or of backticks does not slow this test: each pattern of the
reader is timed on a long run of spaces after each shape that it reads.

Prose is the text that a reader reads as words. Inline code and fenced code
blocks give names, commands, paths and snippets as they must be typed, so a word
inside them keeps its spelling (T90). A code span is read on its own line, so one
that wraps onto the next line is read as prose. A fence closes on a run of its own
character as long as the one that opened it or longer, indented as GitHub allows.
A fence may open after a list item's marker, and then also ends at the first line
that is not blank and is indented less than it, which ends the item, so that line
is read. A fence that opens on its own line, two columns in or more, may be held
by a list item or not, and GitHub reads a line that is not blank and is indented
less than the fence, or a closing fence indented more than three columns and more
than the fence, but no more than three past it, one way in an item and another
outside one. The test does not follow lists, so it fails on such a line and reads
no further. A blank line is one of spaces and tabs alone. A file that this test
cannot read whole fails, named: a fence that never closes, which would leave the
rest of its file unread; a line that it cannot place, as above; a symbolic link,
which is not followed; and a file or a path that is not UTF-8.

Some files keep the words that they were written with and are not read: the
records' folder, since an accepted record changes only to be closed (DR-121) and
the index gives each record's title as the record has it; the archived changes;
the changelog's released entries, which are the sections under a version's
heading; the vendored files; and the skills that OpenSpec generates. A version's
heading that a pull request adds hides what follows it, up to the next `#` or `##` heading,
as a released entry would, though no tag says that the version was released: the
pull request's diff shows that heading to its review. A requirement's or a
scenario's title that an accepted record quotes keeps its words wherever it
appears, and `tests/test_decisions.py` fails when such a title leaves the specs.
The titles kept are those of the records and the specs where HEAD left the
default branch, so that a record that a pull request adds keeps no title's words;
a check that cannot find where HEAD left it keeps none, and fails saying so. In
the glossary itself, every column but the words to avoid is read. The rules are
in `scripts/wording.py`, which `scripts/rewording.py` reads with too, so that this
test and the script never read a page in two ways.

Each entry gives a term and a meaning, no term or word to avoid is given twice,
and no word to avoid is found in a term or is a term's plural. Each concept that
a rule tells apart from another has a term of its own, so that listing one as a
word to avoid for the other fails here (T94). Each topic is one table, with its
header, its delimiter row and at least one row, and a line under a topic that is
not one of its rows is reported, so that no row goes unread. A check that reads
no file, or no word to avoid, fails.
"""

from __future__ import annotations

import os
import re
import subprocess
import time
from pathlib import Path

import pytest
import wording
from wording import (
    CHANGELOG,
    DEFAULT_BRANCH,
    GLOSSARY,
    entry_problems,
    found_words,
    glossary,
    kept_at,
    pattern,
    problems_in,
    quoted_titles,
    read_files,
    readable,
    word_problems,
)

ROOT = Path(__file__).resolve().parents[1]


def test_the_specs_and_pages_use_the_glossary_s_words() -> None:
    problems = problems_in(ROOT)
    assert not problems, "\n".join(problems)


def test_each_term_is_defined_once() -> None:
    entries, problems = glossary((ROOT / GLOSSARY).read_text(encoding="utf-8"))
    problems += entry_problems(entries)
    assert entries, "the glossary holds no entry, so this test covered nothing"
    assert not problems, "\n".join(problems)


GIT_ENVIRONMENT = {
    **os.environ,
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_AUTHOR_NAME": "Test",
    "GIT_AUTHOR_EMAIL": "test@example.com",
    "GIT_COMMITTER_NAME": "Test",
    "GIT_COMMITTER_EMAIL": "test@example.com",
}

GLOSSARY_TEXT = (
    "# Glossary\n"
    "\n"
    "The words that the pages use, each with its meaning.\n"
    "\n"
    "## The tool\n"
    "\n"
    "| Term | Meaning | Words to avoid |\n"
    "|---|---|---|\n"
    "| the tool | What this repository builds. | the calculator, the product |\n"
    "| capture step | The code that records calls. | capture hook |\n"
    "\n"
    "## Branches\n"
    "\n"
    "| Term | Meaning | Words to avoid |\n"
    "|---|---|---|\n"
    "| a change of branch | Another branch checked out. | branch switch |\n"
    "| git common directory | The directory that every worktree shares. | git directory |\n"
    "| ledger | Every ledger file. | |\n"
)
SPEC = (
    "## ADDED Requirements\n"
    "\n"
    "### Requirement: The tool works\n"
    "\n"
    "The tool SHALL work.\n"
    "\n"
    "#### Scenario: The calculator says so\n"
    "\n"
    "- **WHEN** it runs\n"
    "- **THEN** it works\n"
)
RECORD = "docs/decisions/DR-001-the-calculator-is-built.md"
ACCEPTED_RECORD = (
    "# DR-001: The calculator is built\n"
    "\n"
    "- **Status:** accepted\n"
    "\n"
    '## Context\n\nIts scenario "The calculator says so" holds it. The calculator stays.\n'
)
PASSING = {
    GLOSSARY: GLOSSARY_TEXT,
    "openspec/changes/demo/specs/thing/spec.md": SPEC,
    "openspec/changes/demo/proposal.md": "The tool is proposed.\n",
    "openspec/changes/demo/design.md": "The tool is designed.\n",
    "openspec/changes/demo/tasks.md": "- [ ] 1.1 Build the tool\n",
    "docs/page.md": "A page about the tool.\n",
    "docs/requirements.md": "| R1 | functional | `thing` | The tool works |\n",
    "docs/threat-model.md": '- **Held by:** `thing`: "The calculator says so"\n',
    "CLAUDE.md": "Rules for the tool.\n",
    CHANGELOG: (
        "# Changelog\n\n## [Unreleased]\n\n- The tool.\n\n"
        "## [1.0.0] - 2026-01-01\n\n- The calculator, released.\n"
    ),
    RECORD: ACCEPTED_RECORD,
    "docs/decisions/README.md": "| [DR-001](DR-001-the-calculator.md) | The calculator |\n",
    "openspec/changes/archive/2026-01-01-old/proposal.md": "The calculator was proposed.\n",
    "vendor/superpowers/skills/plan/SKILL.md": "The calculator plans.\n",
    ".claude/skills/openspec-propose/SKILL.md": "The calculator proposes.\n",
}
CALCULATOR = '"the calculator" is a word to avoid; use "the tool"'
CAPTURE_HOOK = '"capture hook" is a word to avoid; use "capture step"'


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, env=GIT_ENVIRONMENT)


def write(root: Path, files: dict[str, str | None]) -> None:
    """Write these files, leaving out each given None."""
    for path, text in files.items():
        if text is None:
            continue
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")


def repository(root: Path, changes: dict[str, str | None] | None = None) -> Path:
    """The passing repository with some files changed or, given None, removed, all of
    them committed on the default branch, where HEAD is."""
    write(root, {**PASSING, **(changes or {})})
    git(root, "init", "-q")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "The default branch")
    git(root, "update-ref", DEFAULT_BRANCH, "HEAD")
    return root


def added(root: Path, files: dict[str, str | None]) -> Path:
    """The repository with these files written and added after the default branch, as a
    pull request adds them."""
    write(root, files)
    git(root, "add", "-A")
    return root


def committed(root: Path, files: dict[str, str | None]) -> Path:
    """The repository with these files written and committed after the default branch, as
    a pull request's branch commits them, so that HEAD has left the default branch."""
    added(root, files)
    git(root, "commit", "-q", "-m", "The pull request")
    return root


def test_the_passing_repository_has_no_problem(tmp_path: Path) -> None:
    root = repository(tmp_path)
    assert problems_in(root) == []
    entries, problems = glossary(GLOSSARY_TEXT)
    assert len(entries) == 5
    assert problems == entry_problems(entries) == []


@pytest.mark.parametrize(
    "path",
    [
        "openspec/changes/demo/specs/thing/spec.md",
        "openspec/changes/demo/proposal.md",
        "openspec/changes/demo/design.md",
        "openspec/changes/demo/tasks.md",
        "docs/page.md",
        "docs/OTHER.MD",
        "docs/other.markdown",
        "docs/page.livemd",
        "docs/page.mdown",
        "docs/page.mdwn",
        "docs/page.mkd",
        "docs/page.MKDN",
        "docs/page.mkdown",
        "docs/page.ronn",
        "docs/page.scd",
        "docs/page.workbook",
        "docs/page.mdx",
        "docs/page.litcoffee",
        "contents.lr",
        "docs/contents.lr",
        "CLAUDE.md",
        "docs/threat-model.md",
        ".claude/skills/hand-written/SKILL.md",
    ],
)
def test_a_word_to_avoid_in_a_file_that_is_read_fails(tmp_path: Path, path: str) -> None:
    before = PASSING.get(path, "A page.\n")
    root = repository(tmp_path, {path: before + "\nThe calculator counts calls.\n"})
    line = len(before.split("\n")) + 1
    assert problems_in(root) == [
        f'{path}:{line}: "The calculator" is a word to avoid; use "the tool"'
    ]


@pytest.mark.parametrize(
    "path", ["docs/page.txt", "docs/page.md.txt", "docs/xcontents.lr", "scripts/tool.py"]
)
def test_a_file_that_github_does_not_show_as_markdown_is_not_read(
    tmp_path: Path, path: str
) -> None:
    root = repository(tmp_path, {path: "The calculator counts calls.\n"})
    assert path not in read_files(root)
    assert problems_in(root) == []


def test_a_word_to_avoid_in_the_changelog_s_unreleased_entry_fails(tmp_path: Path) -> None:
    text = PASSING[CHANGELOG].replace("- The tool.\n", "- The calculator, unreleased.\n")
    assert problems_in(repository(tmp_path, {CHANGELOG: text})) == [
        f'{CHANGELOG}:5: "The calculator" is a word to avoid; use "the tool"'
    ]


@pytest.mark.parametrize(
    "path",
    [
        "docs/decisions/DR-002-a-choice.md",
        "docs/decisions/README.md",
        "openspec/changes/archive/2026-01-01-old/design.md",
        "vendor/superpowers/README.md",
        ".claude/skills/openspec-explore/SKILL.md",
    ],
)
def test_a_file_that_keeps_its_words_is_not_read(tmp_path: Path, path: str) -> None:
    planted = "The calculator, with a capture hook.\n"
    root = repository(tmp_path, {path: planted, "docs/page.md": planted})
    assert problems_in(root) == [
        'docs/page.md:1: "The calculator" is a word to avoid; use "the tool"',
        f"docs/page.md:1: {CAPTURE_HOOK}",
    ]


def test_a_released_changelog_entry_is_not_read(tmp_path: Path) -> None:
    text = PASSING[CHANGELOG] + "\n## [0.9.0] - 2025-12-01\n\n### Added\n\n- A capture hook.\n"
    root = repository(tmp_path, {CHANGELOG: text, "docs/page.md": "A capture hook.\n"})
    assert problems_in(root) == [f"docs/page.md:1: {CAPTURE_HOOK}"]


def test_a_word_to_avoid_in_code_is_left_as_written(tmp_path: Path) -> None:
    page = (
        "Set `the calculator` here, or ``a `capture hook` in double backticks``.\n"
        "\n"
        "```text\n"
        "the calculator\n"
        "```\n"
        "\n"
        "  ~~~~\n"
        "  a capture hook, indented in a list\n"
        "  ~~~~\n"
        "\n"
        "`the calculator` is in code, and the calculator is not.\n"
        "```the calculator``` is inline code, and the calculator is not.\n"
    )
    assert problems_in(repository(tmp_path, {"docs/page.md": page})) == [
        f"docs/page.md:11: {CALCULATOR}",
        f"docs/page.md:12: {CALCULATOR}",
    ]


def test_a_fence_closes_only_on_its_own_character_and_length(tmp_path: Path) -> None:
    page = "````\n```\nthe calculator\n~~~~\n````\nthe calculator\n"
    assert problems_in(repository(tmp_path, {"docs/page.md": page})) == [
        f"docs/page.md:6: {CALCULATOR}"
    ]


def test_a_fence_that_never_closes_fails(tmp_path: Path) -> None:
    page = "The tool.\n\n```text\nthe calculator\n"
    assert problems_in(repository(tmp_path, {"docs/page.md": page})) == [
        "docs/page.md:3: a fenced code block opens here and never closes, so the lines after"
        " it were not read"
    ]


def test_a_backtick_without_its_pair_on_its_line_is_read_as_prose(tmp_path: Path) -> None:
    page = "A ` alone, then the calculator.\nA `span that wraps\nthe calculator` here.\n"
    assert problems_in(repository(tmp_path, {"docs/page.md": page})) == [
        f"docs/page.md:1: {CALCULATOR}",
        f"docs/page.md:3: {CALCULATOR}",
    ]


def test_a_word_between_two_code_spans_is_read(tmp_path: Path) -> None:
    page = "Run `git add`, then the calculator counts, then `git commit`.\n"
    assert problems_in(repository(tmp_path, {"docs/page.md": page})) == [
        f"docs/page.md:1: {CALCULATOR}"
    ]


def test_a_code_span_closes_only_on_a_run_of_its_own_length(tmp_path: Path) -> None:
    page = "Code `a `` the calculator `` b` here, and the calculator in prose.\n"
    problems = problems_in(repository(tmp_path, {"docs/page.md": page}))
    assert problems == [f"docs/page.md:1: {CALCULATOR}"]


def test_a_fence_closes_on_a_longer_run_of_its_character(tmp_path: Path) -> None:
    page = "```\nthe calculator\n`````\nthe calculator\n"
    assert problems_in(repository(tmp_path, {"docs/page.md": page})) == [
        f"docs/page.md:4: {CALCULATOR}"
    ]


def test_a_fence_that_opens_after_a_list_item_s_marker_is_code(tmp_path: Path) -> None:
    page = (
        "- ```bash\n"
        "  the calculator\n"
        "  ```\n"
        "\n"
        "The calculator between the blocks.\n"
        "\n"
        "1. ~~~\n"
        "   a capture hook\n"
        "   ~~~\n"
        "\n"
        "The calculator after them.\n"
    )
    assert problems_in(repository(tmp_path, {"docs/page.md": page})) == [
        'docs/page.md:5: "The calculator" is a word to avoid; use "the tool"',
        'docs/page.md:11: "The calculator" is a word to avoid; use "the tool"',
    ]


@pytest.mark.parametrize(
    ("page", "line"),
    [
        ("- ```\n  the calculator in code\nthe calculator after the item.\n", 3),
        ("1. ```\n   the calculator in code\n  the calculator at two spaces.\n", 3),
        ("-\t```\n\tthe calculator in code\n   the calculator at three spaces.\n", 3),
        ("- ```\n  code\n\u00a0\n  the calculator after a no-break space.\n", 4),
    ],
    ids=["after a marker", "after a number", "after a tab", "after a no-break space"],
)
def test_a_fence_in_a_list_item_ends_where_a_line_less_indented_ends_the_item(
    tmp_path: Path, page: str, line: int
) -> None:
    assert problems_in(repository(tmp_path, {"docs/page.md": page})) == [
        f"docs/page.md:{line}: {CALCULATOR}"
    ]


@pytest.mark.parametrize(
    ("page", "line"),
    [
        (" ```\nx\n```\nthe calculator is prose\n```\ncode\n```\n", 4),
        ("```\n    ```\nx\n```\nthe calculator\n```\ny\n```\n", 5),
        ("```\n\u00a0```\nx\n```\nthe calculator\n```\ny\n```\n", 5),
        ("  ```\n  the calculator in code\n   ```\nthe calculator after it.\n", 4),
        ("10. Step:\n\n    ```\n    the calculator in code\n    ```\n\n    the calculator.\n", 7),
        ("- ```\n      ```\n  x\n  ```\n  the calculator\n", 5),
        ("- ```\n  code\n     ```\n  the calculator after it.\n", 4),
        ("```\ncode\n   ```\nthe calculator after it.\n", 4),
        ("  ```\n  code\n      ```\n  ```\nthe calculator after it.\n", 5),
    ],
    ids=[
        "a line less indented than its fence",
        "a run four spaces in",
        "a run after a no-break space",
        "closed three spaces in",
        "closed at its column in an item",
        "a run too deep in its item",
        "closed three columns past its item's text",
        "closed three spaces in from the margin",
        "a run four columns past its fence",
    ],
)
def test_a_fence_holds_each_line_up_to_the_one_that_github_closes_it_on(
    tmp_path: Path, page: str, line: int
) -> None:
    assert problems_in(repository(tmp_path, {"docs/page.md": page})) == [
        f"docs/page.md:{line}: {CALCULATOR}"
    ]


def unsure(line: int, fence: int) -> str:
    return (
        f"docs/page.md:{line}: GitHub reads this line in the fence that opens on line {fence}"
        " or after it, depending on whether a list item holds that fence, so the test cannot"
        " tell whether it is code and reads no further: indent the line as far as the fence,"
        " or close the fence before it"
    )


@pytest.mark.parametrize(
    ("page", "line", "fence"),
    [
        ("- An item:\n\n  ```\n  the calculator in code\nthe calculator after it.\n", 5, 3),
        (
            "- An item:\n\n    ```\n  x\n  ```\n  the calculator is prose\n  ```\n  code\n  ```\n",
            4,
            3,
        ),
        ("- An item:\n\n    ```\n    code\n  the calculator in code\n    ```\n", 5, 3),
        ("- An item:\n\n    ```\n    code\n  ```\n  the calculator is prose.\n", 5, 3),
        ("  ```\n  code\n     ```\nthe calculator in code\n", 3, 1),
    ],
    ids=[
        "a line after the item",
        "a line at the item's text, closed there",
        "a line at the item's text, in the fence",
        "a closing fence at the item's text",
        "a closing fence five spaces in",
    ],
)
def test_a_line_that_github_reads_by_a_list_item_fails(
    tmp_path: Path, page: str, line: int, fence: int
) -> None:
    assert problems_in(repository(tmp_path, {"docs/page.md": page})) == [unsure(line, fence)]


def test_a_fence_in_a_list_item_runs_on_over_a_blank_line_and_closes_on_its_fence(
    tmp_path: Path,
) -> None:
    page = "- ```\n  code\n\n  the calculator in code\n  ```\nThe calculator after it.\n"
    assert problems_in(repository(tmp_path, {"docs/page.md": page})) == [
        'docs/page.md:6: "The calculator" is a word to avoid; use "the tool"'
    ]


def test_a_fence_line_that_ends_a_list_item_opens_a_fence_of_its_own(tmp_path: Path) -> None:
    page = "- ```\n  code\nthe calculator is prose\n```\nthe calculator in code\n"
    assert problems_in(repository(tmp_path, {"docs/page.md": page})) == [
        f"docs/page.md:3: {CALCULATOR}",
        "docs/page.md:4: a fenced code block opens here and never closes, so the lines after"
        " it were not read",
    ]


@pytest.mark.parametrize(
    ("prose", "found", "term"),
    [
        ("THE CALCULATOR", "THE CALCULATOR", "the tool"),
        ("the  calculator", "the  calculator", "the tool"),
        ("the calculator's", "the calculator", "the tool"),
        ("two capture hooks", "capture hooks", "capture step"),
        ("the branch switches", "branch switches", "a change of branch"),
        ("two git directories", "git directories", "git common directory"),
        ("_the calculator_", "the calculator", "the tool"),
        ("__the calculator__", "the calculator", "the tool"),
        ("the\u00a0calculator", "the\u00a0calculator", "the tool"),
    ],
)
def test_a_word_to_avoid_in_any_case_or_plural_fails(
    tmp_path: Path, prose: str, found: str, term: str
) -> None:
    root = repository(tmp_path, {"docs/page.md": f"Of {prose} here.\n"})
    assert problems_in(root) == [f'docs/page.md:1: "{found}" is a word to avoid; use "{term}"']


@pytest.mark.parametrize(
    "prose",
    ["the calculatory", "recapture hook", "the productivity", "subranch switch", "git directoryx"],
)
def test_a_word_to_avoid_inside_a_longer_word_does_not_fail(tmp_path: Path, prose: str) -> None:
    page = f"Of {prose} here, and the calculator.\n"
    assert problems_in(repository(tmp_path, {"docs/page.md": page})) == [
        f"docs/page.md:1: {CALCULATOR}"
    ]


def test_a_word_to_avoid_that_a_line_break_splits_fails(tmp_path: Path) -> None:
    page = (
        "Of the\ncalculator, and a capture\n  hook.\n"
        "\nThe\n\ncalculator, and the |\n| calculator.\n"
    )
    assert problems_in(repository(tmp_path, {"docs/page.md": page})) == [
        f"docs/page.md:1: {CALCULATOR}",
        f"docs/page.md:2: {CAPTURE_HOOK}",
    ]


def test_a_word_that_wraps_is_named_with_one_space_where_its_line_breaks(
    tmp_path: Path,
) -> None:
    page = "Of the \u00a0\n\u00a0 calculator here.\n"
    assert problems_in(repository(tmp_path, {"docs/page.md": page})) == [
        f"docs/page.md:1: {CALCULATOR}"
    ]


def test_a_word_to_avoid_with_a_curly_apostrophe_fails(tmp_path: Path) -> None:
    text = GLOSSARY_TEXT.replace("| branch switch |", "| branch switch, the person's switch |")
    root = repository(tmp_path, {GLOSSARY: text, "docs/page.md": "Of the person\u2019s switch.\n"})
    assert problems_in(root) == [
        'docs/page.md:1: "the person\u2019s switch" is a word to avoid; use "a change of branch"'
    ]


@pytest.mark.parametrize(
    "line",
    ["common" + " " * 30 + "git" + " " * 10_000 + "x", "the" + " " * 30_000 + "x"],
)
def test_a_line_made_to_slow_the_matching_is_read_quickly(line: str) -> None:
    started = time.perf_counter()
    found = [pattern(word).search(line) for word in ("common git directory", "the calculator")]
    assert found == [None, None]
    assert time.perf_counter() - started < 1


# A run of spaces long enough that a pattern which can match it in many ways takes seconds,
# where one that matches it in one way takes milliseconds.
LONG_RUN = " " * 40_000
# What each pattern of the reader reads a run of spaces after: a heading of the glossary, a
# requirement's or a scenario's title, a table's row, a quotation and a record's field.
SHAPES = ["", "x", "## x", "### Requirement: x", "#### Scenario: x", "| x", '"x', "- **Status:** x"]


def test_no_pattern_of_the_reader_is_slowed_by_a_run_of_spaces() -> None:
    patterns = {
        name: value for name, value in vars(wording).items() if isinstance(value, re.Pattern)
    }
    assert {"TOPIC", "SPEC_TITLE", "ROW", "QUOTATION"} <= patterns.keys()
    slow = []
    for shape in SHAPES:
        for ending in ("y", "\ny"):
            for name, compiled in patterns.items():
                started = time.perf_counter()
                compiled.findall(f"{shape}{LONG_RUN}{ending}")
                if time.perf_counter() - started >= 1:
                    slow.append(f"{name}: {shape!r}, a long run of spaces, {ending!r}")
    assert not slow


def test_a_heading_or_a_title_with_a_long_run_of_spaces_is_read_quickly() -> None:
    started = time.perf_counter()
    entries, problems = glossary(
        f"## The tool{LONG_RUN}x\n\n" + GLOSSARY_TEXT[GLOSSARY_TEXT.index("| Term") :]
    )
    titles = quoted_titles([f"### Requirement: The tool{LONG_RUN}works\n"], [])
    assert time.perf_counter() - started < 1
    assert [entry.term for entry in entries][:1] == ["the tool"]
    assert problems == []
    assert titles == frozenset()


@pytest.mark.parametrize(
    "gap", [LONG_RUN, f"{LONG_RUN}\n{LONG_RUN}"], ids=["spaces", "spaces and a line break"]
)
def test_a_word_to_avoid_with_a_long_run_of_spaces_is_named_quickly(
    tmp_path: Path, gap: str
) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "page.md").write_text(f"Of the{gap}calculator.\n", encoding="utf-8")
    shown = "the calculator" if "\n" in gap else f"the{gap}calculator"
    started = time.perf_counter()
    found = word_problems(tmp_path, glossary(GLOSSARY_TEXT)[0], ["docs/page.md"], frozenset())
    assert time.perf_counter() - started < 1
    assert found == [f'docs/page.md:1: "{shown}" is a word to avoid; use "the tool"']


def test_a_line_of_many_runs_of_backticks_is_read_quickly() -> None:
    # Each of the first runs has a length that no later run has, so that each is a backtick
    # of the prose, and the single backticks after them pair into code spans.
    line = " ".join("`" * length for length in range(2, 802)) + " `a`" * 40_000
    text = f"the calculator {line} the calculator\n"
    started = time.perf_counter()
    read, unclosed = readable("docs/page.md", text, frozenset())
    assert time.perf_counter() - started < 1
    assert unclosed == []
    assert [found[2] for found in found_words(read, glossary(GLOSSARY_TEXT)[0])] == [
        "the calculator",
        "the calculator",
    ]
    assert "a" not in read.replace("calculator", "")


def test_a_word_to_avoid_that_a_longer_one_holds_is_named_once(tmp_path: Path) -> None:
    text = GLOSSARY_TEXT.replace("| git directory |", "| git directory, common git directory |")
    root = repository(tmp_path, {GLOSSARY: text, "docs/page.md": "The common git directory.\n"})
    assert problems_in(root) == [
        'docs/page.md:1: "common git directory" is a word to avoid; use "git common directory"'
    ]


def test_the_glossary_s_terms_and_meanings_are_read_and_its_words_to_avoid_are_not(
    tmp_path: Path,
) -> None:
    text = GLOSSARY_TEXT.replace("Every ledger file.", "Every ledger file, not the calculator.")
    text = text.replace("| ledger |", "| ledger of the capture hook |")
    assert problems_in(repository(tmp_path, {GLOSSARY: text})) == [
        f"{GLOSSARY}:18: {CAPTURE_HOOK}",
        f"{GLOSSARY}:18: {CALCULATOR}",
    ]


def test_the_glossary_s_own_prose_is_read(tmp_path: Path) -> None:
    text = GLOSSARY_TEXT.replace("its meaning", "its meaning, as a capture hook")
    assert problems_in(repository(tmp_path, {GLOSSARY: text})) == [f"{GLOSSARY}:3: {CAPTURE_HOOK}"]


def test_a_title_that_an_accepted_record_quotes_keeps_its_words(tmp_path: Path) -> None:
    page = 'It follows "The calculator says so", while the calculator is gone.\n'
    assert problems_in(repository(tmp_path, {"docs/page.md": page})) == [
        f"docs/page.md:1: {CALCULATOR}"
    ]


def test_a_title_that_only_a_closed_record_quotes_is_read(tmp_path: Path) -> None:
    closed = ACCEPTED_RECORD.replace("- **Status:** accepted", "- **Status:** closed")
    assert problems_in(repository(tmp_path, {RECORD: closed})) == [
        'docs/threat-model.md:1: "The calculator" is a word to avoid; use "the tool"',
        'openspec/changes/demo/specs/thing/spec.md:7: "The calculator" is a word to avoid;'
        ' use "the tool"',
    ]


def test_a_quotation_that_is_no_title_is_not_kept(tmp_path: Path) -> None:
    record = ACCEPTED_RECORD.replace('"The calculator says so"', '"The calculator says no"')
    root = repository(tmp_path, {RECORD: record, "docs/page.md": "The calculator says no.\n"})
    assert 'docs/page.md:1: "The calculator" is a word to avoid; use "the tool"' in problems_in(
        root
    )


def test_a_title_quoted_with_its_sentence_s_punctuation_is_kept(tmp_path: Path) -> None:
    record = ACCEPTED_RECORD.replace('"The calculator says so"', '"The calculator says so,"')
    assert kept_at(repository(tmp_path, {RECORD: record}), "HEAD") == {"The calculator says so"}


def test_a_kept_title_inside_a_longer_word_is_read(tmp_path: Path) -> None:
    page = 'It follows "The calculator says soon".\n'
    assert problems_in(repository(tmp_path, {"docs/page.md": page})) == [
        'docs/page.md:1: "The calculator" is a word to avoid; use "the tool"'
    ]


def test_a_kept_title_under_emphasis_keeps_its_words(tmp_path: Path) -> None:
    page = "It follows _The calculator says so_ and __The calculator says so__.\n"
    assert problems_in(repository(tmp_path, {"docs/page.md": page})) == []


COUNTS_SPEC = (
    PASSING["openspec/changes/demo/specs/thing/spec.md"]
    + "\n#### Scenario: The calculator counts\n\n- **WHEN** it counts\n- **THEN** it works\n"
)
COUNTS_RECORD = ACCEPTED_RECORD.replace(
    "# DR-001: The calculator is built", "# DR-002: It counts"
).replace("says so", "counts")
COUNTS_READ = [
    'openspec/changes/demo/specs/thing/spec.md:12: "The calculator" is a word to avoid;'
    ' use "the tool"'
]


@pytest.mark.parametrize("commit", [False, True], ids=["staged", "committed on a branch"])
def test_a_title_that_only_a_new_record_quotes_is_read(tmp_path: Path, commit: bool) -> None:
    root = repository(tmp_path)
    (committed if commit else added)(
        root,
        {
            "openspec/changes/demo/specs/thing/spec.md": COUNTS_SPEC,
            "docs/decisions/DR-002-it-counts.md": COUNTS_RECORD,
        },
    )
    assert problems_in(root) == COUNTS_READ


def test_a_record_that_the_default_branch_gains_after_head_left_it_keeps_no_title(
    tmp_path: Path,
) -> None:
    root = repository(tmp_path)
    git(root, "checkout", "-q", "-b", "later")
    committed(
        root,
        {
            "openspec/changes/demo/specs/thing/spec.md": COUNTS_SPEC,
            "docs/decisions/DR-002-it-counts.md": COUNTS_RECORD,
        },
    )
    git(root, "update-ref", DEFAULT_BRANCH, "HEAD")
    git(root, "checkout", "-q", "-")
    committed(root, {"openspec/changes/demo/specs/thing/spec.md": COUNTS_SPEC})
    assert problems_in(root) == COUNTS_READ


def test_a_check_that_cannot_find_the_default_branch_keeps_no_title(tmp_path: Path) -> None:
    root = repository(tmp_path)
    git(root, "update-ref", "-d", DEFAULT_BRANCH)
    problems = problems_in(root)
    assert problems[0].startswith(f"cannot find where HEAD left {DEFAULT_BRANCH}")
    assert problems[1:] == [
        'docs/threat-model.md:1: "The calculator" is a word to avoid; use "the tool"',
        'openspec/changes/demo/specs/thing/spec.md:7: "The calculator" is a word to avoid;'
        ' use "the tool"',
    ]


def test_the_titles_kept_are_those_in_the_specs_that_an_accepted_record_quotes(
    tmp_path: Path,
) -> None:
    removed = SPEC + "\n## REMOVED Requirements\n\n### Requirement: The calculator is gone\n"
    quotes = ", ".join(
        f'"The calculator is {each}"'
        for each in ("gone", "archived", "held", "not a title", "not in a spec")
    )
    root = repository(
        tmp_path,
        {
            "openspec/changes/demo/specs/thing/spec.md": removed,
            RECORD: ACCEPTED_RECORD.replace("holds it.", f"holds it, as {quotes} do."),
            "openspec/changes/archive/2026-01-01-old/specs/thing/spec.md": (
                "#### Scenario: The calculator is archived\n"
            ),
            "openspec/specs/other/spec.md": "### Requirement: The calculator is held\n",
            "openspec/specs/other/design.md": "### Requirement: The calculator is not a title\n",
            "docs/page.md": "#### Scenario: The calculator is not in a spec\n",
        },
    )
    assert kept_at(root, "HEAD") == {
        "The calculator says so",
        "The calculator is gone",
        "The calculator is held",
    }


@pytest.mark.parametrize(
    ("row", "expected"),
    [
        ("| a thing |  | |", 'the term "a thing" gives no meaning'),
        ("| the tool | Again. | |", 'the term "the tool" is given twice, first on line 9'),
        (
            "| Git Common  Directory | Again. | |",
            'the term "Git Common  Directory" is given twice, first on line 17',
        ),
        (
            "| another | Other. | capture hooks |",
            'the word to avoid "capture hooks" is given twice, first on line 10',
        ),
        (
            "| another | Other. | the Product |",
            'the word to avoid "the Product" is given twice, first on line 9',
        ),
        (
            "| another | Other. | change of branch |",
            'the word to avoid "change of branch" is found in the term "a change of branch"',
        ),
        (
            "| another | Other. | Git Common Directories |",
            'the word to avoid "Git Common Directories" is the plural of the term'
            ' "git common directory"',
        ),
    ],
)
def test_an_entry_without_meaning_or_given_twice_fails(row: str, expected: str) -> None:
    entries, problems = glossary(GLOSSARY_TEXT + row + "\n")
    assert problems == []
    assert entry_problems(entries) == [f"{GLOSSARY}:19: {expected}"]


def test_a_word_to_avoid_found_in_a_later_term_is_named_where_it_is_given() -> None:
    entries, _ = glossary(GLOSSARY_TEXT + "| capture hook test | Other. | |\n")
    assert entry_problems(entries) == [
        f'{GLOSSARY}:10: the word to avoid "capture hook" is found in the term "capture hook test"'
    ]


def test_a_word_to_avoid_given_after_its_plural_fails() -> None:
    text = GLOSSARY_TEXT.replace("| capture hook |", "| capture hooks |")
    entries, _ = glossary(text + "| another | Other. | capture hook |\n")
    assert entry_problems(entries) == [
        f'{GLOSSARY}:19: the word to avoid "capture hook" is given twice, first on line 10'
    ]


def test_a_word_to_avoid_given_twice_in_one_row_fails() -> None:
    text = GLOSSARY_TEXT.replace("| capture hook |", "| capture hook, Capture Hook |")
    entries, _ = glossary(text)
    assert entry_problems(entries) == [
        f'{GLOSSARY}:10: the word to avoid "Capture Hook" is given twice, first on line 10'
    ]


HEADER_PROBLEM = (
    'the topic "Branches" does not open with the table\'s header,'
    " | Term | Meaning | Words to avoid |"
)
TABLE = "## Branches\n\n| Term | Meaning | Words to avoid |\n|---|---|---|\n"
LEDGER = "| ledger | Every ledger file. | |\n"


@pytest.mark.parametrize(
    ("old", "new", "expected"),
    [
        (
            LEDGER,
            "| ledger | Every ledger file. |\n",
            "18: a row with 2 cells, where the table has 3 columns",
        ),
        (
            LEDGER,
            "| ledger | Every | file. | |\n",
            "18: a row with 4 cells, where the table has 3 columns",
        ),
        (LEDGER, LEDGER + "|  | Something. | |\n", "19: a row that gives no term"),
        (
            LEDGER,
            LEDGER + "A note.\n",
            '19: a line under the topic "Branches" that is not one of its table\'s rows',
        ),
        (
            LEDGER,
            LEDGER + "\nA note.\n",
            '20: a line under the topic "Branches" that is not one of its table\'s rows',
        ),
        (TABLE, TABLE.replace(" Words to avoid |", ""), f"14: {HEADER_PROBLEM}"),
        (
            TABLE,
            "## Branches\n\nA sentence before the table.\n\n" + TABLE[13:],
            f"14: {HEADER_PROBLEM}",
        ),
        (TABLE, "## Branches\n\n", f"14: {HEADER_PROBLEM}"),
        (
            TABLE,
            TABLE.replace("|---|---|---|\n", ""),
            '14: the header of the topic "Branches" is not followed by a delimiter row,'
            " such as |---|---|---|",
        ),
        (
            "| capture hook |",
            "| `capture hook` |",
            '10: the word to avoid "`capture hook`" is not plain words, so no prose could match it',
        ),
    ],
)
def test_a_glossary_out_of_form_fails(old: str, new: str, expected: str) -> None:
    assert GLOSSARY_TEXT.count(old) == 1
    _, problems = glossary(GLOSSARY_TEXT.replace(old, new))
    assert problems == [f"{GLOSSARY}:{expected}"]


def test_a_topic_without_a_table_fails() -> None:
    _, problems = glossary(GLOSSARY_TEXT + "\n## Empty\n")
    assert problems == [f'{GLOSSARY}:20: the topic "Empty" holds no table']


NO_DELIMITER = (
    'the header of the topic "Empty" is not followed by a delimiter row, such as |---|---|---|'
)


NEXT = "\n## Next\n" + TABLE[12:] + "| next | The next. | |\n"


@pytest.mark.parametrize("after", ["", NEXT])
def test_a_header_that_a_heading_or_the_end_follows_fails(after: str) -> None:
    text = GLOSSARY_TEXT + "\n## Empty\n\n| Term | Meaning | Words to avoid |" + after
    _, problems = glossary(text)
    assert problems == [f"{GLOSSARY}:22: {NO_DELIMITER}"]


@pytest.mark.parametrize("after", ["", "\n", NEXT, "\n" + NEXT])
def test_a_table_that_holds_no_row_fails(after: str) -> None:
    text = GLOSSARY_TEXT + "\n## Empty\n\n| Term | Meaning | Words to avoid |\n|---|---|---|"
    _, problems = glossary(text + after)
    assert problems == [f'{GLOSSARY}:20: the topic "Empty" holds no row']


def test_an_escaped_pipe_is_part_of_its_cell() -> None:
    entries, problems = glossary(GLOSSARY_TEXT.replace("Every ledger file.", "A \\| B."))
    assert problems == []
    assert entries[-1].meaning == "A \\| B."


@pytest.mark.parametrize("term", ["@someone \\\\| x", "a \\| b", "a\\b"])
def test_a_term_that_holds_a_backslash_or_a_pipe_fails(term: str) -> None:
    entries, problems = glossary(GLOSSARY_TEXT + f"| {term} | A row. | gadget |\n")
    assert problems == [
        f'{GLOSSARY}:19: the term "{term}" holds a backslash, so a pipe after it could split'
        " a table's cell"
    ]
    assert [entry for entry in entries if entry.line == 19] == []


def test_a_glossary_that_gives_no_word_to_avoid_fails(tmp_path: Path) -> None:
    text = GLOSSARY_TEXT
    for words in ("the calculator, the product", "capture hook", "branch switch", "git directory"):
        text = text.replace(f"| {words} |", "| |")
    root = repository(tmp_path, {GLOSSARY: text, "docs/page.md": "The calculator.\n"})
    assert problems_in(root) == [f"{GLOSSARY} gives no word to avoid, so no word was checked"]


def test_a_glossary_that_does_not_exist_fails(tmp_path: Path) -> None:
    assert problems_in(repository(tmp_path, {GLOSSARY: None})) == [f"{GLOSSARY} does not exist"]


def test_a_check_that_finds_no_file_to_read_fails(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / GLOSSARY).write_text(GLOSSARY_TEXT, encoding="utf-8")
    git(tmp_path, "init", "-q")
    assert problems_in(tmp_path) == ["no tracked Markdown file was read, so no word was checked"]


def test_an_untracked_page_is_not_read_and_a_tracked_one_is(tmp_path: Path) -> None:
    root = repository(tmp_path)
    (root / "docs" / "draft.md").write_text("The calculator, untracked.\n", encoding="utf-8")
    assert problems_in(root) == []
    git(root, "add", "docs/draft.md")
    assert problems_in(root) == [
        'docs/draft.md:1: "The calculator" is a word to avoid; use "the tool"'
    ]


def test_a_tracked_page_removed_from_the_working_tree_is_not_read(tmp_path: Path) -> None:
    root = repository(tmp_path, {"docs/page.md": "The calculator.\n"})
    (root / "docs" / "page.md").unlink()
    assert "docs/page.md" not in read_files(root)
    assert problems_in(root) == []


def test_a_page_that_is_a_symbolic_link_fails_and_is_not_followed(tmp_path: Path) -> None:
    outside = tmp_path / "outside.md"
    outside.write_text("The calculator, outside the repository.\n", encoding="utf-8")
    root = repository(tmp_path / "repository")
    (root / "docs" / "linked.md").symlink_to(outside)
    (root / "docs" / "dangling.md").symlink_to(tmp_path / "missing.md")
    added(root, {})
    assert problems_in(root) == [
        "docs/dangling.md: is a symbolic link, so it was not read",
        "docs/linked.md: is a symbolic link, so it was not read",
    ]


def test_a_page_that_is_not_utf_8_fails(tmp_path: Path) -> None:
    root = repository(tmp_path)
    (root / "docs" / "latin.md").write_bytes(b"Caf\xe9, the calculator.\n")
    added(root, {})
    assert problems_in(root) == ["docs/latin.md: is not UTF-8, so it was not read"]


def test_a_path_that_is_not_utf_8_fails(tmp_path: Path) -> None:
    root = repository(tmp_path)
    (root / "docs" / os.fsdecode(b"caf\xe9.md")).write_text("The calculator.\n")
    added(root, {})
    assert problems_in(root) == ["docs/caf\ufffd.md: a path that is not UTF-8, so it was not read"]


def test_the_repository_s_files_are_read() -> None:
    files = read_files(ROOT)
    assert "CLAUDE.md" in files and GLOSSARY in files and CHANGELOG in files
    kept = re.compile(
        r"docs/decisions/|vendor/|openspec/changes/archive/|\.claude/skills/openspec-"
    )
    assert not [path for path in files if kept.match(path)]
    shown_as_markdown = re.compile(
        r"(?:^|/)contents\.lr$|\.(?:md|livemd|markdown|mdown|mdwn|mkdn?|mkdown|ronn|scd|workbook"
        r"|mdx|litcoffee)$",
        re.I,
    )
    assert not [path for path in files if not shown_as_markdown.search(path)]


def test_a_page_that_calls_an_entry_anonymous_fails(tmp_path: Path) -> None:
    # A page that calls an entry `anonymous` fails the wording test, read with this
    # repository's own glossary (R159). That the check reads a spec as it reads a page, and
    # matches a word in any case, the tests above hold with the test glossary.
    own = (ROOT / GLOSSARY).read_text(encoding="utf-8")
    root = repository(tmp_path, {GLOSSARY: own, "docs/page.md": "The ledger is anonymous.\n"})
    assert problems_in(root) == ['docs/page.md:1: "anonymous" is a word to avoid; use "hashed id"']
