"""How the glossary is read, and where a page uses a word that it says to avoid.

`tests/test_glossary.py` describes these rules and holds them (R137, R138; design
decision 14). `scripts/rewording.py` reads with them when it compares a rewording with
its base, so that the test and the script never read a page in two ways.
`tests/test_decisions.py` finds the specs, their titles, the accepted records and their
quotations with the same patterns, so that the two tests never tell a quoted title in
two ways, and `scripts/spec_form.py` finds the code spans of a spec's line as this finds
those of a page's line. Like the tool, this runs on Python 3.11 and later with the standard library
alone.
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
from typing import NamedTuple

GLOSSARY = "docs/glossary.md"
DEFAULT_BRANCH = "refs/remotes/origin/main"
CHANGELOG = "CHANGELOG.md"
HEADER = ["Term", "Meaning", "Words to avoid"]

# Kept as written: the records and their index, the archived changes, the vendored files
# and the skills that OpenSpec generates.
KEPT = re.compile(
    r"(?:docs/decisions|openspec/changes/archive|vendor)/|\.claude/skills/openspec-[^/]+/"
)
# The files that GitHub shows as Markdown: those with the extensions and the name that
# GitHub's language list, linguist, gives Markdown, MDX and Literate CoffeeScript, the
# languages that its markup library renders as Markdown.
MARKDOWN = (
    *(
        f":(top,icase)*.{extension}"
        for extension in (
            "md",
            "livemd",
            "markdown",
            "mdown",
            "mdwn",
            "mkd",
            "mkdn",
            "mkdown",
            "ronn",
            "scd",
            "workbook",
            "mdx",
            "litcoffee",
        )
    ),
    ":(top,glob,icase)**/contents.lr",
)
# The specs are `openspec/specs/` and the active changes; an archived copy holds nothing.
SPEC_FILE = re.compile(r"openspec/(?:specs/[^/]+|changes/(?!archive/)[^/]+/specs/[^/]+)/spec\.md")
RECORD_FILE = re.compile(r"docs/decisions/DR-[^/]+\.md")
# A heading's text, here and in a spec's titles below, ends on a character that is not a
# space, so that the spaces after it are matched in one way only, however many they are.
TOPIC = re.compile(r"^## (.*\S)\s*$")
ROW = re.compile(r"^\|.*\|\s*$")
DELIMITER = re.compile(r"^\|(?:\s*:?-{3,}:?\s*\|)+\s*$")
CELL_BORDER = re.compile(r"(?<!\\)\|")
PLAIN_WORDS = re.compile(r"[^\W_]+(?:[ '-][^\W_]+)*")
# A space in a word to avoid stands for spaces, no-break spaces among them, with at most
# one line break, so that a word that a page wraps still fails, and one that a blank line
# splits does not. A run of them matches in one way only, so that a long run does not slow
# the matching.
SPACE = r"(?:[ \t\u00a0]+(?:\n[ \t\u00a0]*)?|\n[ \t\u00a0]*)"
APOSTROPHE = "['\u2019]"
# A letter or a digit: a word to avoid or a kept title ends where neither follows, so that
# the underscores of emphasis hide neither.
WORD = re.compile(r"[^\W_]")
FINAL_Y = re.compile(r"[b-df-hj-np-tv-z]y$", re.I)
# A fence may open after the markers of list items, which leave its lines indented.
OPEN_FENCE = re.compile(r"^[ \t]*(?:(?:[-*+]|\d{1,9}[.)])[ \t]+)*(`{3,}|~{3,})(.*)$")
BACKTICKS = re.compile(r"`+")
SECTION_HEADING = re.compile(r"^#{1,2} ")
VERSION_HEADING = re.compile(r"^## \[\d+\.\d+\.\d+")
SPEC_TITLE = re.compile(r"^#{3,4} (?:Requirement|Scenario): (.*\S)\s*$", re.M)
QUOTATION = re.compile(r'"([^"\n]+?)[.,;:]?"')
ACCEPTED = re.compile(r"^- \*\*Status:\*\* accepted$", re.M)
UNREAD = "\0"


@dataclass(frozen=True)
class Entry:
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
    case, its apostrophe straight or curly."""
    *start, last = word.split(" ")
    if FINAL_Y.search(last):
        end = re.escape(last[:-1]) + "(?:y|ies)"
    else:
        end = re.escape(last) + "(?:e?s)?"
    body = SPACE.join([*map(re.escape, start), end]).replace("'", APOSTROPHE)
    return re.compile(rf"(?<!{WORD.pattern}){body}(?!{WORD.pattern})", re.IGNORECASE)


def entry_of(line: str, number: int) -> tuple[Entry | None, list[str]]:
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
    if "\\" in term:
        # A pipe after an escaped backslash is a border of the table's cell that the
        # rewording script writes the term in, even inside a code span, and a term can hold
        # a pipe only after a backslash.
        return None, [
            f'{GLOSSARY}:{number}: the term "{term}" holds a backslash, so a pipe after it'
            " could split a table's cell"
        ]
    words = [word.strip() for word in avoid.split(",") if word.strip()]
    plain = tuple(word for word in words if PLAIN_WORDS.fullmatch(word))
    return Entry(term, meaning, plain, number), [
        f'{GLOSSARY}:{number}: the word to avoid "{word}" is not plain words, so no prose'
        " could match it"
        for word in words
        if word not in plain
    ]


def glossary(text: str) -> tuple[list[Entry], list[str]]:
    """The glossary's entries, and what is wrong with its form."""
    entries: list[Entry] = []
    problems: list[str] = []
    topic, opened, header, state, rows = "", 0, 0, "prose", 0

    def unfinished() -> list[str]:
        """What is wrong with the topic that ends here: a table that it lacks, a header with
        no delimiter row, or a table that holds no row."""
        if state == "header":
            return [f'{GLOSSARY}:{opened}: the topic "{topic}" holds no table']
        if state == "delimiter":
            return [
                f'{GLOSSARY}:{header}: the header of the topic "{topic}" is not followed by a'
                " delimiter row, such as |---|---|---|"
            ]
        if state in ("rows", "after") and not rows:
            return [f'{GLOSSARY}:{opened}: the topic "{topic}" holds no row']
        return []

    for number, line in enumerate(text.split("\n"), 1):
        heading = TOPIC.match(line)
        if heading:
            problems += unfinished()
            topic, opened, state, rows = heading[1], number, "header", 0
        elif state == "delimiter":
            if DELIMITER.match(line) and len(cells(line)) == len(HEADER):
                state = "rows"
            else:
                problems += unfinished()
                state = "skipped"
        elif not line.strip():
            if state == "rows":
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
        elif state == "rows" and ROW.match(line):
            entry, found = entry_of(line, number)
            problems += found
            rows += 1
            if entry is not None:
                entries.append(entry)
        else:
            problems.append(
                f'{GLOSSARY}:{number}: a line under the topic "{topic}" that is not one of its'
                " table's rows"
            )
    return entries, problems + unfinished()


def same(word: str, other: str) -> bool:
    """Whether one word to avoid matches the other whole, so that prose could not tell
    them apart."""
    return bool(pattern(word).fullmatch(other) or pattern(other).fullmatch(word))


def entry_problems(entries: list[Entry]) -> list[str]:
    """An entry without a meaning, a term or a word to avoid given twice, and a word to
    avoid found in a term or given as a term's plural."""
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
    for word, line in given:
        for entry in entries:
            if pattern(word).search(entry.term):
                found.append(
                    (line, f'the word to avoid "{word}" is found in the term "{entry.term}"')
                )
            elif pattern(entry.term).fullmatch(word):
                found.append(
                    (line, f'the word to avoid "{word}" is the plural of the term "{entry.term}"')
                )
    return [
        f"{GLOSSARY}:{line}: {message}" for line, message in sorted(found, key=lambda each: each[0])
    ]


def git(root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    """A git command run in this repository, which may fail."""
    return subprocess.run(["git", *args], cwd=root, capture_output=True, check=False)


def shown(root: Path, *args: str) -> str:
    """What a git command prints in this repository. Raises CalledProcessError when it
    fails."""
    done = git(root, *args)
    done.check_returncode()
    return done.stdout.decode("utf-8", "surrogateescape")


def read_files(root: Path) -> list[str]:
    """The Markdown files that git tracks and this test reads, as the working tree has them,
    a symbolic link among them, to be named rather than followed."""
    return [
        path
        for path in shown(root, "ls-files", "-z", "--", *MARKDOWN).split("\0")
        if path and not KEPT.match(path) and ((root / path).is_symlink() or (root / path).is_file())
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


def kept_at(root: Path, commit: str) -> frozenset[str]:
    """The titles in a commit's specs that one of its accepted records quotes. Where HEAD
    left the default branch, these are the titles that the default branch's records keep.
    Raises CalledProcessError when git cannot read the commit."""
    listing = shown(
        root,
        "ls-tree",
        "-r",
        "-z",
        "--name-only",
        "--full-tree",
        commit,
        "--",
        "openspec",
        "docs/decisions",
    )
    paths = listing.split("\0")

    def texts(named: re.Pattern[str]) -> list[str]:
        return [
            shown(root, "cat-file", "blob", f"{commit}:{path}")
            for path in paths
            if named.fullmatch(path)
        ]

    return quoted_titles(texts(SPEC_FILE), texts(RECORD_FILE))


def hide(chars: list[str], start: int, end: int) -> None:
    """Leave these characters unread, keeping the line breaks among them."""
    for at in range(start, end):
        if chars[at] != "\n":
            chars[at] = UNREAD


def code_spans(line: str) -> tuple[list[tuple[int, int]], list[int]]:
    """Where each code span of a line starts and ends, and the length of each run of
    backticks that no later run as long closes on the line. A code span is a run of
    backticks up to the next run of as many; a run that no later one matches is a backtick
    of the prose."""
    runs = list(BACKTICKS.finditer(line))
    # The next run of the same length after each run, found in one pass from the end, so
    # that a line of many runs is read in time that grows with the line.
    closes: list[int | None] = [None] * len(runs)
    latest: dict[int, int] = {}
    for at in reversed(range(len(runs))):
        closes[at] = latest.get(len(runs[at][0]))
        latest[len(runs[at][0])] = at
    spans: list[tuple[int, int]] = []
    unclosed: list[int] = []
    at = 0
    while at < len(runs):
        close = closes[at]
        if close is None:
            unclosed.append(len(runs[at][0]))
            at += 1
        else:
            spans.append((runs[at].start(), runs[close].end()))
            at = close + 1
    return spans, unclosed


def hide_code_spans(chars: list[str], start: int, line: str) -> None:
    """Leave unread each code span of a line."""
    for begin, end in code_spans(line)[0]:
        hide(chars, start + begin, start + end)


def width(text: str) -> int:
    """How many columns the spaces and tabs that start a text fill, each tab reaching the
    next multiple of four, as GitHub counts them."""
    return len(text[: len(text) - len(text.lstrip(" \t"))].expandtabs(4))


class Fence(NamedTuple):
    """An open fence: its character, its length, its line, the column where it starts, and
    whether a list item's marker opens it on its line."""

    char: str
    length: int
    line: int
    column: int
    marker: bool


UNSURE = (
    "GitHub reads this line in the fence that opens on line {} or after it, depending on"
    " whether a list item holds that fence, so the test cannot tell whether it is code and"
    " reads no further: indent the line as far as the fence, or close the fence before it"
)


def fence_line(fence: Fence, line: str) -> str:
    """What a line that is not blank is to an open fence: "text", "close", "end" where it
    ends the list item that holds the fence, or "unsure" where GitHub reads it one way in a
    list item and another outside one. Where a list item's marker opens the fence, the
    item's text starts where the fence does. Elsewhere an item whose text starts up to
    three columns before the fence may hold it, or none may, and the test does not follow
    the lists that would tell. A closing fence may be indented up to three columns past
    the item's text, or past the margin outside a list."""
    indent = width(line)
    run = line.strip(" \t")
    closing = set(run) == {fence.char} and len(run) >= fence.length
    if fence.marker:
        if indent < fence.column:
            return "end"
        return "close" if closing and indent <= fence.column + 3 else "text"
    if fence.column < 2:
        # A list item's text starts two columns in or more, so no item holds this fence.
        return "close" if closing and indent <= 3 else "text"
    if indent < fence.column:
        return "unsure"
    if closing and indent <= max(fence.column, 3):
        return "close"
    if closing and indent <= fence.column + 3:
        return "unsure"
    return "text"


def prose(path: str, text: str) -> tuple[list[str], list[tuple[int, str]]]:
    """A file's characters with each that is not prose left unread, and where the reading
    stopped short: a fence that never closes, or a line that the test cannot place, by its
    line. A blank line is one of spaces and tabs alone."""
    chars = list(text)
    fence: Fence | None = None
    released = False
    start = 0
    for number, line in enumerate(text.split("\n"), 1):
        end = start + len(line)
        if fence is not None:
            kind = fence_line(fence, line) if line.strip(" \t") else "text"
            if kind == "unsure":
                hide(chars, start, len(text))
                return chars, [(number, UNSURE.format(fence.line))]
            if kind != "end":
                hide(chars, start, end)
                if kind == "close":
                    fence = None
                start = end + 1
                continue
            # The line ends the list item that holds the fence, and the fence with it, so
            # it is read as any other line.
            fence = None
        opened = OPEN_FENCE.match(line)
        if opened and not (opened[1][0] == "`" and "`" in opened[2]):
            fence = Fence(
                opened[1][0],
                len(opened[1]),
                number,
                len(line[: opened.start(1)].expandtabs(4)),
                bool(line[: opened.start(1)].strip(" \t")),
            )
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
            fence.line,
            "a fenced code block opens here and never closes, so the lines after it were not read",
        )
    ]


def line_starts(text: str) -> list[int]:
    """Where each line of a text starts."""
    return [0, *(at + 1 for at, char in enumerate(text) if char == "\n")]


def readable(path: str, text: str, kept: frozenset[str]) -> tuple[str, list[tuple[int, str]]]:
    """A file's text with each character that is not read replaced by NUL, its line breaks
    kept, and where the reading stopped short, by its line. In the glossary, its entries'
    words to avoid are not read, and in every file, nor are the titles kept."""
    chars, unclosed = prose(path, text)
    if path == GLOSSARY:
        starts, lines = line_starts(text), text.split("\n")
        for entry in glossary(text)[0]:
            start, end = cells(lines[entry.line - 1])[2]
            hide(chars, starts[entry.line - 1] + start, starts[entry.line - 1] + end)
    for title in kept:
        at = text.find(title)
        while at != -1:
            end = at + len(title)
            if (at and WORD.match(text, at - 1)) or WORD.match(text, end):
                at = text.find(title, at + 1)
            else:
                hide(chars, at, end)
                at = text.find(title, end)
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
    """Each word to avoid in the prose of the files, with the term to use, and each file
    that was not read whole."""
    found: list[tuple[str, int, int, str]] = []
    for path in files:
        named = path.encode("utf-8", "surrogateescape").decode("utf-8", "replace")
        if named != path:
            found.append((named, 0, 0, f"{named}: a path that is not UTF-8, so it was not read"))
            continue
        if (root / path).is_symlink():
            found.append((path, 0, 0, f"{path}: is a symbolic link, so it was not read"))
            continue
        try:
            text = (root / path).read_text(encoding="utf-8")
        except UnicodeDecodeError:
            found.append((path, 0, 0, f"{path}: is not UTF-8, so it was not read"))
            continue
        words, unclosed = readable(path, text, kept)
        starts = line_starts(text)
        for start, end, _word, term in found_words(words, entries):
            line = bisect.bisect_right(starts, start)
            # A word that wraps is named on one line, each line break and the spaces around
            # it written as one space.
            shown = " ".join(part.strip(" \t\u00a0") for part in text[start:end].split("\n"))
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
        return [*problems, "no tracked Markdown file was read, so no word was checked"]
    base = git(root, "merge-base", "HEAD", DEFAULT_BRANCH)
    if base.returncode:
        problems.append(
            f"cannot find where HEAD left {DEFAULT_BRANCH}, so no title that a record quotes"
            " was kept: fetch the default branch, with all of its history if this clone is"
            " shallow"
        )
        kept: frozenset[str] = frozenset()
    else:
        kept = kept_at(root, base.stdout.decode("utf-8").strip())
    return problems + word_problems(root, entries, files, kept)
