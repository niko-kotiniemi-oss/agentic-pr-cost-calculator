"""The specs and pages use the glossary's words, and each term is defined once.

`docs/glossary.md` gives each term's meaning and the words to avoid for it, in a
table per topic (R137, R138; design decision 14; DR-164). This test reads the
prose of every Markdown file that git tracks and fails on each word to avoid that
it finds, naming the file, the line and the term to use. A word to avoid is
matched as a whole word in any case, and so is its plural, which adds "s" or "es"
or, after a consonant, turns a final "y" into "ies". Where a word to avoid has a
space, the page may break the line instead, so that a wrapped line hides no word.

Prose is the text that a reader reads as words. Inline code and fenced code
blocks give names, commands, paths and snippets as they must be typed, so a word
inside them keeps its spelling (T90). A code span is read on its own line, so one
that wraps onto the next line is read as prose, and a fence that never closes is
reported, since it would leave the rest of its file unread. Some files keep the
words that they were written with and are not read: the records' folder, since
an accepted record changes only to be closed (DR-121) and the index gives each
record's title as the record has it; the archived changes; the changelog's
released entries, which are the sections under a version's heading; the vendored
files; and the skills that OpenSpec generates. A requirement's or a scenario's
title that an accepted record quotes keeps its words wherever it appears, and
`tests/test_decisions.py` fails when such a title leaves the specs. In the
glossary itself, every column but the words to avoid is read.

Each entry gives a term and a meaning, no term or word to avoid is given twice,
and no word to avoid is found in a term. Each concept that a rule tells apart
from another has a term of its own, so that listing one as a word to avoid for
the other fails here (T94). Each topic is one table, and a line under a topic
that is not one of its rows is reported, so that no row goes unread. A check
that reads no file, or no word to avoid, fails.
"""

from __future__ import annotations

import bisect
import functools
import os
import re
import subprocess
from collections.abc import Iterable
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GLOSSARY = "docs/glossary.md"
CHANGELOG = "CHANGELOG.md"
DECISIONS = Path("docs") / "decisions"
HEADER = ["Term", "Meaning", "Words to avoid"]

# Kept as written: the records and their index, the archived changes, the vendored files
# and the skills that OpenSpec generates.
KEPT = re.compile(
    r"(?:docs/decisions|openspec/changes/archive|vendor)/|\.claude/skills/openspec-[^/]+/"
)
MARKDOWN = (":(icase)*.md", ":(icase)*.markdown")
TOPIC = re.compile(r"^## (.+?)\s*$")
ROW = re.compile(r"^\|.*\|\s*$")
DELIMITER = re.compile(r"^\|(?:\s*:?-{3,}:?\s*\|)+\s*$")
CELL_BORDER = re.compile(r"(?<!\\)\|")
PLAIN_WORDS = re.compile(r"[^\W_]+(?:[ '-][^\W_]+)*")
# A space in a word to avoid stands for spaces with at most one line break among them, so
# that a word that a page wraps still fails, and one that a blank line splits does not.
SPACE = r"(?:[ \t]+\n?|\n)[ \t]*"
LINE_BREAK = re.compile(r"[ \t]*\n[ \t]*")
FINAL_Y = re.compile(r"[b-df-hj-np-tv-z]y$", re.I)
OPEN_FENCE = re.compile(r"^[ \t]*(`{3,}|~{3,})(.*)$")
BACKTICKS = re.compile(r"`+")
SECTION_HEADING = re.compile(r"^#{1,2} ")
VERSION_HEADING = re.compile(r"^## \[\d+\.\d+\.\d+")
SPEC_TITLE = re.compile(r"^#{3,4} (?:Requirement|Scenario): (.+?)\s*$", re.M)
QUOTATION = re.compile(r'"([^"\n]+?)[.,;:]?"')
ACCEPTED = re.compile(r"^- \*\*Status:\*\* accepted$", re.M)
UNREAD = "\0"


@dataclass(frozen=True)
class Entry:
    topic: str
    term: str
    meaning: str
    avoid: tuple[str, ...]
    line: int


def cells(line: str) -> list[tuple[int, int]]:
    """Where each cell of a table's row starts and ends: between its borders, which are the
    pipes that no backslash escapes."""
    borders = [border.start() for border in CELL_BORDER.finditer(line)]
    return [(start + 1, end) for start, end in pairwise(borders)]


@functools.cache
def pattern(word: str) -> re.Pattern[str]:
    """What a word to avoid matches in prose: itself or its plural, as a whole word in any
    case."""
    *start, last = word.split(" ")
    if FINAL_Y.search(last):
        end = re.escape(last[:-1]) + "(?:y|ies)"
    else:
        end = re.escape(last) + "(?:e?s)?"
    body = SPACE.join([*map(re.escape, start), end])
    return re.compile(rf"(?<!\w){body}(?!\w)", re.IGNORECASE)


def entry_of(topic: str, line: str, number: int) -> tuple[Entry | None, list[str]]:
    """The entry that a row gives, and what is wrong with its form."""
    spans = cells(line)
    if len(spans) != len(HEADER):
        return None, [
            f"{GLOSSARY}:{number}: a row with {len(spans)} cells, where the table has"
            f" {len(HEADER)} columns"
        ]
    term, meaning, avoid = (line[start:end].strip() for start, end in spans)
    if not term:
        return None, [f"{GLOSSARY}:{number}: a row that gives no term"]
    words = [word.strip() for word in avoid.split(",") if word.strip()]
    plain = tuple(word for word in words if PLAIN_WORDS.fullmatch(word))
    return Entry(topic, term, meaning, plain, number), [
        f'{GLOSSARY}:{number}: the word to avoid "{word}" is not plain words, so no prose'
        " could match it"
        for word in words
        if word not in plain
    ]


def glossary(text: str) -> tuple[list[Entry], list[str]]:
    """The glossary's entries, and what is wrong with its form."""
    entries: list[Entry] = []
    problems: list[str] = []
    topic, opened, header, state = "", 0, 0, "prose"
    for number, line in enumerate(text.split("\n"), 1):
        heading = TOPIC.match(line)
        if heading:
            if state == "header":
                problems.append(f'{GLOSSARY}:{opened}: the topic "{topic}" holds no table')
            topic, opened, state = heading[1], number, "header"
        elif not line.strip():
            if state == "delimiter":
                problems.append(
                    f'{GLOSSARY}:{header}: the header of the topic "{topic}" is not followed by'
                    " a delimiter row, such as |---|---|---|"
                )
                state = "skipped"
            elif state == "rows":
                state = "after"
        elif state in ("prose", "skipped"):
            continue
        elif state == "header":
            if ROW.match(line) and [line[a:b].strip() for a, b in cells(line)] == HEADER:
                header, state = number, "delimiter"
            else:
                problems.append(
                    f'{GLOSSARY}:{number}: the topic "{topic}" does not open with the table\'s'
                    f" header, | {' | '.join(HEADER)} |"
                )
                state = "skipped"
        elif state == "delimiter":
            if DELIMITER.match(line) and len(cells(line)) == len(HEADER):
                state = "rows"
            else:
                problems.append(
                    f'{GLOSSARY}:{header}: the header of the topic "{topic}" is not followed by'
                    " a delimiter row, such as |---|---|---|"
                )
                state = "skipped"
        elif state == "rows" and ROW.match(line):
            entry, found = entry_of(topic, line, number)
            problems += found
            if entry is not None:
                entries.append(entry)
        else:
            problems.append(
                f'{GLOSSARY}:{number}: a line under the topic "{topic}" that is not one of its'
                " table's rows"
            )
    if state == "header":
        problems.append(f'{GLOSSARY}:{opened}: the topic "{topic}" holds no table')
    return entries, problems


def same(word: str, other: str) -> bool:
    """Whether one word to avoid matches the other whole, so that prose could not tell
    them apart."""
    return bool(pattern(word).fullmatch(other) or pattern(other).fullmatch(word))


def entry_problems(entries: list[Entry]) -> list[str]:
    """An entry without a meaning, a term or a word to avoid given twice, and a word to
    avoid found in a term."""
    found: list[tuple[int, str]] = []
    terms: dict[str, int] = {}
    given: list[tuple[str, int]] = []
    for entry in entries:
        if not entry.meaning:
            found.append((entry.line, f'the term "{entry.term}" gives no meaning'))
        key = " ".join(entry.term.casefold().split())
        if key in terms:
            found.append(
                (entry.line, f'the term "{entry.term}" is given twice, first on line {terms[key]}')
            )
        terms.setdefault(key, entry.line)
        for word in entry.avoid:
            first = next((line for other, line in given if same(word, other)), None)
            if first is not None:
                found.append(
                    (
                        entry.line,
                        f'the word to avoid "{word}" is given twice, first on line {first}',
                    )
                )
            given.append((word, entry.line))
    found += [
        (line, f'the word to avoid "{word}" is found in the term "{entry.term}"')
        for word, line in given
        for entry in entries
        if pattern(word).search(entry.term)
    ]
    return [
        f"{GLOSSARY}:{line}: {message}" for line, message in sorted(found, key=lambda each: each[0])
    ]


def read_files(root: Path) -> list[str]:
    """The Markdown files that git tracks and this test reads, as the working tree has them."""
    listing = subprocess.run(
        ["git", "ls-files", "-z", "--", *MARKDOWN], cwd=root, capture_output=True, check=True
    )
    return [
        path
        for path in listing.stdout.decode("utf-8").split("\0")
        if path and not KEPT.match(path) and (root / path).is_file()
    ]


def kept_titles(root: Path) -> frozenset[str]:
    """The titles in the specs that an accepted record quotes."""
    specs = [
        *(root / "openspec" / "specs").glob("*/spec.md"),
        *(root / "openspec" / "changes").glob("*/specs/*/spec.md"),
    ]
    titles = {
        title for spec in specs for title in SPEC_TITLE.findall(spec.read_text(encoding="utf-8"))
    }
    quoted: set[str] = set()
    for record in (root / DECISIONS).glob("DR-*.md"):
        text = record.read_text(encoding="utf-8")
        if ACCEPTED.search(text):
            quoted.update(QUOTATION.findall(text))
    return frozenset(titles & quoted)


def hide(chars: list[str], start: int, end: int) -> None:
    """Leave these characters unread, keeping the line breaks among them."""
    for at in range(start, end):
        if chars[at] != "\n":
            chars[at] = UNREAD


def hide_code_spans(chars: list[str], start: int, line: str) -> None:
    """Leave unread each code span of a line: a run of backticks up to the next run of as
    many. A run that no later one matches is a backtick of the prose."""
    runs = list(BACKTICKS.finditer(line))
    at = 0
    while at < len(runs):
        length = len(runs[at][0])
        close = next((n for n in range(at + 1, len(runs)) if len(runs[n][0]) == length), None)
        if close is None:
            at += 1
        else:
            hide(chars, start + runs[at].start(), start + runs[close].end())
            at = close + 1


def prose(path: str, text: str) -> tuple[list[str], list[tuple[int, str]]]:
    """A file's characters with each that is not prose left unread, and each fence that
    never closes, by its line."""
    chars = list(text)
    fence: tuple[str, int, int] | None = None
    released = False
    start = 0
    for number, line in enumerate(text.split("\n"), 1):
        end = start + len(line)
        opened = OPEN_FENCE.match(line)
        if fence is not None:
            hide(chars, start, end)
            closing = line.strip()
            if closing and set(closing) == {fence[0]} and len(closing) >= fence[1]:
                fence = None
        elif opened and not (opened[1][0] == "`" and "`" in opened[2]):
            fence = (opened[1][0], len(opened[1]), number)
            hide(chars, start, end)
        else:
            if path == CHANGELOG and SECTION_HEADING.match(line):
                released = bool(VERSION_HEADING.match(line))
            if released:
                hide(chars, start, end)
            else:
                hide_code_spans(chars, start, line)
        start = end + 1
    if fence is None:
        return chars, []
    return chars, [
        (
            fence[2],
            "a fenced code block opens here and never closes, so the lines after it were not read",
        )
    ]


def word_problems(
    root: Path, entries: list[Entry], files: Iterable[str], kept: frozenset[str]
) -> list[str]:
    """Each word to avoid in the prose of the files, with the term to use, and each fence
    that never closes."""
    words = [(pattern(word), entry.term) for entry in entries for word in entry.avoid]
    titles = [re.compile(rf"(?<!\w){re.escape(title)}(?!\w)") for title in sorted(kept)]
    found: list[tuple[str, int, int, str]] = []
    for path in files:
        text = (root / path).read_text(encoding="utf-8")
        chars, unclosed = prose(path, text)
        starts = [0, *(at + 1 for at, char in enumerate(text) if char == "\n")]
        if path == GLOSSARY:
            lines = text.split("\n")
            for entry in entries:
                start, end = cells(lines[entry.line - 1])[2]
                hide(chars, starts[entry.line - 1] + start, starts[entry.line - 1] + end)
        for title in titles:
            for match in title.finditer(text):
                hide(chars, match.start(), match.end())
        readable = "".join(chars)
        matches = sorted(
            (match.start(), match.end(), term)
            for word, term in words
            for match in word.finditer(readable)
        )
        reach = -1
        for start, end, term in sorted(matches, key=lambda each: (each[0], -each[1])):
            # A word to avoid that a longer one holds, at the same place, is named once.
            if end <= reach:
                continue
            reach = end
            line = bisect.bisect_right(starts, start)
            shown = LINE_BREAK.sub(" ", text[start:end])
            found.append(
                (path, line, start, f'{path}:{line}: "{shown}" is a word to avoid; use "{term}"')
            )
        found += [(path, line, 0, f"{path}:{line}: {message}") for line, message in unclosed]
    return [message for *_, message in sorted(found)]


def problems_in(root: Path) -> list[str]:
    """What is wrong with the glossary's form, and each word to avoid in the files that
    this test reads."""
    if not (root / GLOSSARY).is_file():
        return [f"{GLOSSARY} does not exist"]
    entries, problems = glossary((root / GLOSSARY).read_text(encoding="utf-8"))
    if not any(entry.avoid for entry in entries):
        problems.append(f"{GLOSSARY} gives no word to avoid, so no word was checked")
    files = read_files(root)
    if not files:
        problems.append("no tracked Markdown file was read, so no word was checked")
    return problems + word_problems(root, entries, files, kept_titles(root))


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


def repository(root: Path, changes: dict[str, str | None] | None = None) -> Path:
    """The passing repository with some files changed or, given None, removed, all of
    them tracked."""
    files = {**PASSING, **(changes or {})}
    for path, text in files.items():
        if text is None:
            continue
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    git(root, "init", "-q")
    git(root, "add", "-A")
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


@pytest.mark.parametrize(
    ("prose", "found", "term"),
    [
        ("THE CALCULATOR", "THE CALCULATOR", "the tool"),
        ("the  calculator", "the  calculator", "the tool"),
        ("the calculator's", "the calculator", "the tool"),
        ("two capture hooks", "capture hooks", "capture step"),
        ("the branch switches", "branch switches", "a change of branch"),
        ("two git directories", "git directories", "git common directory"),
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
    assert kept_titles(root) == {
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


def test_the_repository_s_files_are_read() -> None:
    files = read_files(ROOT)
    assert "CLAUDE.md" in files and GLOSSARY in files and CHANGELOG in files
    kept = re.compile(
        r"docs/decisions/|vendor/|openspec/changes/archive/|\.claude/skills/openspec-"
    )
    assert not [path for path in files if kept.match(path)]
    assert not [path for path in files if not re.search(r"\.(?:md|markdown)$", path, re.I)]
