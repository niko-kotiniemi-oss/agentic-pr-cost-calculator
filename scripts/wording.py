"""How the glossary is read, and where a page uses a word that it says to avoid.

`tests/test_glossary.py` describes these rules and holds them (R137, R138; design
decision 14). `scripts/rewording.py` reads with them when it compares a rewording with
its base, so that the test and the script never read a page in two ways. Like the
tool, this runs on Python 3.11 and later with the standard library alone.
"""

from __future__ import annotations

import bisect
import functools
import re
import subprocess
from collections.abc import Iterable
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path

GLOSSARY = "docs/glossary.md"
CHANGELOG = "CHANGELOG.md"
HEADER = ["Term", "Meaning", "Words to avoid"]

# Kept as written: the records and their index, the archived changes, the vendored files
# and the skills that OpenSpec generates.
KEPT = re.compile(
    r"(?:docs/decisions|openspec/changes/archive|vendor)/|\.claude/skills/openspec-[^/]+/"
)
MARKDOWN = (":(top,icase)*.md", ":(top,icase)*.markdown")
# The specs are `openspec/specs/` and the active changes; an archived copy holds nothing.
SPEC_FILE = re.compile(r"openspec/(?:specs/[^/]+|changes/(?!archive/)[^/]+/specs/[^/]+)/spec\.md")
RECORD_FILE = re.compile(r"docs/decisions/DR-[^/]+\.md")
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


def quoted_titles(specs: Iterable[str], records: Iterable[str]) -> frozenset[str]:
    """The titles in these specs that one of these records quotes, if it is accepted."""
    titles = {title for spec in specs for title in SPEC_TITLE.findall(spec)}
    quoted = {
        quote
        for record in records
        if ACCEPTED.search(record)
        for quote in QUOTATION.findall(record)
    }
    return frozenset(titles & quoted)


def kept_titles(root: Path) -> frozenset[str]:
    """The titles in the working tree's specs that an accepted record quotes."""

    def texts(pattern: str, named: re.Pattern[str]) -> list[str]:
        return [
            path.read_text(encoding="utf-8")
            for path in sorted(root.glob(pattern))
            if named.fullmatch(path.relative_to(root).as_posix())
        ]

    return quoted_titles(
        texts("openspec/**/spec.md", SPEC_FILE), texts("docs/decisions/*.md", RECORD_FILE)
    )


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


def line_starts(text: str) -> list[int]:
    """Where each line of a text starts."""
    return [0, *(at + 1 for at, char in enumerate(text) if char == "\n")]


def readable(path: str, text: str, kept: frozenset[str]) -> tuple[str, list[tuple[int, str]]]:
    """A file's text with each character that is not read replaced by NUL, its line breaks
    kept, and each fence that never closes, by its line. In the glossary, its entries'
    words to avoid are not read, and in every file, nor are the titles kept."""
    chars, unclosed = prose(path, text)
    if path == GLOSSARY:
        starts, lines = line_starts(text), text.split("\n")
        for entry in glossary(text)[0]:
            start, end = cells(lines[entry.line - 1])[2]
            hide(chars, starts[entry.line - 1] + start, starts[entry.line - 1] + end)
    for title in sorted(kept):
        for match in re.finditer(rf"(?<!\w){re.escape(title)}(?!\w)", text):
            hide(chars, match.start(), match.end())
    return "".join(chars), unclosed


def found_words(text: str, entries: list[Entry]) -> list[tuple[int, int, str, str]]:
    """Where a readable text uses a word to avoid: where it starts and ends, the word as the
    glossary gives it, and the term to use. A word that a longer one holds, at the same
    place, is found once."""
    matches = sorted(
        (
            (match.start(), match.end(), word, entry.term)
            for entry in entries
            for word in entry.avoid
            for match in pattern(word).finditer(text)
        ),
        key=lambda each: (each[0], -each[1]),
    )
    found = []
    reach = -1
    for match in matches:
        if match[1] > reach:
            found.append(match)
            reach = match[1]
    return found


def word_problems(
    root: Path, entries: list[Entry], files: Iterable[str], kept: frozenset[str]
) -> list[str]:
    """Each word to avoid in the prose of the files, with the term to use, and each fence
    that never closes."""
    found: list[tuple[str, int, int, str]] = []
    for path in files:
        text = (root / path).read_text(encoding="utf-8")
        words, unclosed = readable(path, text, kept)
        starts = line_starts(text)
        for start, end, _word, term in found_words(words, entries):
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
