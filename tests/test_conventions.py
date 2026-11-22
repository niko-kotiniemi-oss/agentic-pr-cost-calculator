"""Every tracked file holds only the characters that its writer may use.

A file that this repository writes holds only printable ASCII and line feeds, and one that
Python reads as source, by its extension or by a first line that runs Python, declares on
its first two lines no encoding but UTF-8. Every tracked path holds only printable ASCII but
the space, and differs from every other path, and from each folder that holds one, in more
than the case of its letters (R268, DR-274). The files that others write, which
`scripts/conventions.py` gives, may also hold tabs and the visible characters that `VISIBLE`
lists, each for Markdown alone or for any file, and variation selector 16 only right after a
character listed for it. A character that an escape writes by its code, `\\u` and four
hexadecimal digits or up to six in braces, `\\U` and eight or `\\x` and two, is held as that
character, and so is each character that a skill's front matter gives once YAML reads it
(R269, DR-275). The list gives only punctuation and symbols, by their Unicode categories,
none in `BLANK`, each under the name that Unicode gives it; on the oldest supported Python,
an entry that its Unicode database does not know is passed over, and every later Python
checks it (T255).

The test lists the tracked paths with `git ls-files -s -z` and reads each file as git's index
holds it, every blob through one `git cat-file --batch` that fetches nothing that the clone
lacks, and also as the working tree holds it wherever that holds a file or a link, so that an
edit not yet staged is read too; a link is read as the path that it holds, and the test
follows no link, in the working tree or in a folder on a path's way (R272). Each problem
names the file, the line and the column, a character by its code point and its name, never
by itself, and a path with each other character by its code point, so that everything that
the test prints is printable ASCII (T264).

A file whose extension, in any case, is that of an image, a PDF or a video is tracked only
where `EXCEPTIONS` gives its path, the object id that git holds for it and an accepted record
that names the path in a code span, and the list gives no other file. The test of characters
passes over a listed file only where its bytes are not UTF-8, so that a listed SVG is still
read and the list takes no page of text out of it (R270, DR-276).

Each Markdown file that this repository writes holds, outside code, no raw HTML, character
reference, link or footnote definition, image, link title, `$`, backtick that a backslash
escapes, run of backticks that its line leaves open, which GitHub may pair with one on a
later line, or table row with more cells than its header; it gives a fence no more than a
language, draws no block but Mermaid, and its Mermaid blocks hold no entity code, comment,
raw HTML, front matter, accessible title or description, link or style. A template under
`.github/` may hold HTML comments, and the README the `<details>` and `<summary>` elements
without attributes that fold its sections of detail, but no backtick or run of tildes on a
line that GitHub reads as raw HTML after either, where it opens no code. The test reads a
page's code as `scripts/wording.py` reads it, with `reading`, so that the two tests never
tell code in two ways, and names the file, the line and what it holds (R273, DR-279).

Each check is shown to fail on a git repository into which its defect is planted.
"""

from __future__ import annotations

import codecs
import html.entities
import mimetypes
import os
import re
import stat
import subprocess
import sys
import unicodedata
from collections import defaultdict
from collections.abc import Iterable, Iterator, Mapping
from pathlib import Path, PurePosixPath
from typing import NamedTuple

import pytest
import yaml
from conventions import named, shown, shown_path, written_by_others
from test_decisions import AUTHOR, CODE_SPAN, records_of
from test_decisions import record as decision_record
from test_repository import oldest_python
from test_roadmap import isolated_environment, session_free_environment
from wording import BACKTICKS, CELL_BORDER, MARKDOWN, Block, block_lines, code_spans, reading

ROOT = Path(__file__).resolve().parents[1]


class Visible(NamedTuple):
    """A visible character beyond printable ASCII that a file that others write may hold,
    by its code point and its Unicode name: in Markdown alone or in any file, and whether
    variation selector 16 may follow it."""

    code_point: int
    name: str
    markdown_only: bool
    selector: bool = False


# What the files that others write may hold beyond printable ASCII, tabs and line feeds
# (R269, DR-275). The owner decides whether the list gives a character, in the pull request
# that adds it, and `list_problems` holds each entry to punctuation or a symbol that does not
# show as blank, under the name that Unicode gives it. On 2026-11-22 those files held these
# twenty, the first seven in files other than Markdown too, and variation selector 16 only
# after the warning sign.
VISIBLE = (
    Visible(0x2014, "EM DASH", markdown_only=False),
    Visible(0x2026, "HORIZONTAL ELLIPSIS", markdown_only=False),
    Visible(0x2192, "RIGHTWARDS ARROW", markdown_only=False),
    Visible(0x26A0, "WARNING SIGN", markdown_only=False, selector=True),
    Visible(0x2705, "WHITE HEAVY CHECK MARK", markdown_only=False),
    Visible(0x1F3AF, "DIRECT HIT", markdown_only=False),
    Visible(0x1F50D, "LEFT-POINTING MAGNIFYING GLASS", markdown_only=False),
    Visible(0x00A7, "SECTION SIGN", markdown_only=True),
    Visible(0x00D7, "MULTIPLICATION SIGN", markdown_only=True),
    Visible(0x2013, "EN DASH", markdown_only=True),
    Visible(0x2190, "LEFTWARDS ARROW", markdown_only=True),
    Visible(0x2260, "NOT EQUAL TO", markdown_only=True),
    Visible(0x2264, "LESS-THAN OR EQUAL TO", markdown_only=True),
    Visible(0x2265, "GREATER-THAN OR EQUAL TO", markdown_only=True),
    Visible(0x2500, "BOX DRAWINGS LIGHT HORIZONTAL", markdown_only=True),
    Visible(0x2514, "BOX DRAWINGS LIGHT UP AND RIGHT", markdown_only=True),
    Visible(0x251C, "BOX DRAWINGS LIGHT VERTICAL AND RIGHT", markdown_only=True),
    Visible(0x2713, "CHECK MARK", markdown_only=True),
    Visible(0x2717, "BALLOT X", markdown_only=True),
    Visible(0x274C, "CROSS MARK", markdown_only=True),
)
LISTED = {chr(entry.code_point): entry for entry in VISIBLE}
SELECTED = frozenset(chr(entry.code_point) for entry in VISIBLE if entry.selector)
# Variation selector 16, which asks for a character's emoji form and shows as nothing itself.
SELECTOR = "\ufe0f"
# Characters of those categories that show as blank, which no entry may give: the blank
# Braille pattern, which a check by category alone once let through (DR-152), and the
# musical null notehead, which a font draws as nothing.
BLANK = frozenset({0x2800, 0x1D159})

# An escape that writes a character by its code, as JSON, JavaScript and YAML allow (T263).
ESCAPE = re.compile(
    r"\\(?:u\{([0-9A-Fa-f]{1,6})\}|u([0-9A-Fa-f]{4})|U([0-9A-Fa-f]{8})|x([0-9A-Fa-f]{2}))"
)
# PEP 263's declaration of a source file's encoding, which Python reads on either of its
# first two lines.
CODING = re.compile(r"^[ \t\f]*#.*?coding[:=][ \t]*([-\w.]+)")
PYTHON_FILE = re.compile(r"\.py[iw]?\Z")
PYTHON_LINE = re.compile(r"#!.*python")

FILE, EXECUTABLE, LINK, GITLINK = "100644", "100755", "120000", "160000"
IN_INDEX = ", in git's index,"
IN_TREE = ", in the working tree,"
NOT_ASCII = ", which is not printable ASCII"
NOT_LISTED = ", which the list does not give; the owner decides whether it does"
MARKDOWN_ALONE = ", which the list gives for Markdown alone"
READ_NOTHING = "the test of characters read no tracked file"


class Excepted(NamedTuple):
    """A file that the list of exceptions lets in: its path, the object id that git holds
    for it, and the accepted record whose text names that path in a code span."""

    path: str
    oid: str
    record: str


# The images, PDFs and videos that the repository tracks, each with its record (R270,
# DR-276): none so far.
EXCEPTIONS: tuple[Excepted, ...] = ()
# The extensions of an image, a PDF or a video: each that Python's own table of types gives
# one of them, which a test holds for the running release, and those of common formats that
# the table leaves out.
MEDIA = frozenset(
    (
        "ai apng avif bmp cur dib dng emf eps exr fits g3 gif heic heif icns ico ief jfif jp2 "
        "jpe jpeg jpf jpg jpm jpx jxl pbm pct pgm pic pict pjp pjpeg png pnm ppm psd ras rgb "
        "svg svgz t38 tfx tga tif tiff webp wmf xbm xcf xpm xwd "
        "pdf "
        "3g2 3gp asf avi f4v flv m1v m2ts m2v m4v mk3d mkv mov movie mp4 mpa mpe mpeg mpg mts "
        "mxf ogv qt vob webm wmv"
    ).split()
)
OBJECT_ID = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")
UNLISTED = (
    " is an image, a PDF or a video by its extension, which only an exception that gives its"
    " object id and an accepted record lets in"
)
# The files under `.github/` that GitHub offers as templates, whose comments guide whoever
# fills one in (R273).
TEMPLATE = re.compile(
    r"\.github/(?:pull_request_template\.md|(?:ISSUE|PULL_REQUEST|DISCUSSION)_TEMPLATE/[^/]+)\Z",
    re.IGNORECASE,
)
README = "README.md"
# The elements with which the README folds its sections of detail, without attributes (R200).
FOLDS = ("<details>", "</details>", "<summary>", "</summary>")
# The languages of a fenced block that GitHub draws rather than shows as code (A9), and what
# a fence may give as its language.
DRAWN = frozenset({"math", "geojson", "topojson", "stl"})
LANGUAGE = re.compile(r"[A-Za-z0-9_+#.-]+")
# Where a mark that GitHub hides or shows otherwise may start on a line read as prose: a
# CDATA section's opening is one mark, so that the `![` in it opens no image.
MARK = re.compile(r"<!\[CDATA\[|<|&|\$|\]:|!\[|\]\(")
AUTOLINK = re.compile(
    r"<(?:[A-Za-z][A-Za-z0-9+.-]{1,31}:[^\x00-\x20<>]*"
    r"|[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*)>"
)
# A link's destination that angle brackets hold, which is no raw HTML.
ANGLE = re.compile(r"<[^<>\n]*>")
# What the reading takes to open code, and GitHub, on a line that it reads as raw HTML, not.
RAW_CODE = re.compile(r"`|~{3,}")
TAG = re.compile(r"</?[A-Za-z][A-Za-z0-9-]*")
DECLARATION = re.compile(r"<![A-Za-z]")
REFERENCE = re.compile(r"&(?:#[0-9]{1,7}|#[Xx][0-9A-Fa-f]{1,6}|([A-Za-z][A-Za-z0-9]*));")
ESCAPED_BACKTICK = re.compile(r"(?<!\\)(?:\\\\)*\\`")
# A row of a table's delimiter, and what may open a row inside a quote or a list item.
DELIMITER_CELL = re.compile(r"[ \t]*:?-+:?[ \t]*")
CONTAINER = re.compile(r"^[ \t>]*(?:(?:[-*+]|\d{1,9}[.)])[ \t]+)*")
# What a Mermaid block may not hold: an entity code, which it shows as the character that it
# names, a comment or directive, and the statements that give text that the drawing does
# not show or change how it shows what it does.
ENTITY_CODE = re.compile(r"#[A-Za-z0-9_]+;")
MERMAID_STATEMENT = re.compile(r"^[ \t]*(accTitle|accDescr|click|style|classDef|linkStyle)\b")

COMMENT = "an HTML comment, which GitHub hides"
HIDES = ", which GitHub hides"
SHOWN_OTHERWISE = ", which GitHub hides or shows otherwise"
NAMES_CHARACTER = ", which GitHub shows as the character that it names"
DEFINITION = "]:, which starts a link or footnote definition that GitHub hides"
IMAGE = "![, which starts an image that GitHub fetches and shows"
TITLE = "a link with a title, which GitHub shows only under a pointer"
DOLLAR = "$, with which GitHub starts a mathematical expression"
BACKSLASHED = (
    "a backtick that a backslash escapes, which GitHub shows as itself where the test would"
    " read code"
)
INFO = "an opening fence that gives more than a language, which GitHub does not show"
IN_MERMAID = " in a Mermaid block"
MERMAID_HIDES = ", which gives text that the drawing does not show or changes how it shows it"
ENTITY_NAMES = ", which the drawing shows as the character that it names"
DIRECTIVE = ", which starts a comment or a directive that the drawing hides"
NEVER_ENDS = "an HTML comment that never closes, which GitHub hides to the end"
OPENS_NO_CODE = ", which opens no code on a line that GitHub reads as raw HTML"
OPEN_RUN = (
    "a run of backticks that its line leaves open, which GitHub may pair with one on a later line"
)
PAGES_READ_NOTHING = "the check of pages read no Markdown file that this repository writes"
# The marks that fail wherever they stand on a line read as prose.
PLAIN = {"$": DOLLAR, "]:": DEFINITION, "![": IMAGE}
MEDIA_READ_NOTHING = (
    "git lists no tracked file, so the check of images, PDFs and videos read nothing"
)


class Entry(NamedTuple):
    """A path that git's index tracks, with its mode and its object id."""

    mode: str
    oid: str
    path: str


def git(
    root: Path, *args: str, stdin: bytes = b"", extra: Mapping[str, str] | None = None
) -> subprocess.CompletedProcess[bytes]:
    """git run in the repository at root, with no git variable of the session's and no
    global or system configuration."""
    return subprocess.run(
        ["git", *args],
        cwd=root,
        input=stdin,
        capture_output=True,
        check=False,
        env={**isolated_environment(root), **(extra or {})},
    )


def tracked_entries(root: Path) -> list[Entry]:
    """Each path that git's index tracks, as `git ls-files -s -z` gives it, unquoted, with
    each byte that is not UTF-8 kept as `surrogateescape` keeps it."""
    done = git(root, "ls-files", "-s", "-z")
    done.check_returncode()
    found = []
    for record in done.stdout.split(b"\0"):
        if record:
            head, _, path = record.partition(b"\t")
            mode, oid, _ = head.decode("ascii").split(" ")
            found.append(Entry(mode, oid, path.decode("utf-8", "surrogateescape")))
    return found


def markdown_files(root: Path) -> set[str]:
    """The tracked paths that `scripts/wording.py` reads as Markdown."""
    done = git(root, "ls-files", "-z", "--", *MARKDOWN)
    done.check_returncode()
    return {path for path in done.stdout.decode("utf-8", "surrogateescape").split("\0") if path}


def blobs(root: Path, oids: Iterable[str]) -> dict[str, bytes | None]:
    """Each object's bytes, read through one `git cat-file --batch`, or None for one that
    this clone lacks. Git fetches none: in a partial clone, where it would fetch a missing
    object from the clone's remote, it stops at it instead, and the objects after it are
    read again."""
    found: dict[str, bytes | None] = {}
    pending = list(dict.fromkeys(oids))
    while pending:
        done = git(
            root,
            "cat-file",
            "--batch",
            stdin="".join(f"{oid}\n" for oid in pending).encode("ascii"),
            extra={"GIT_NO_LAZY_FETCH": "1"},
        )
        output, at, read = done.stdout, 0, 0
        for oid in pending:
            end = output.find(b"\n", at)
            if end < 0:
                break
            header = output[at:end].split(b" ")
            if header[1:] == [b"missing"]:
                found[oid], at = None, end + 1
            else:
                size = int(header[2])
                if len(output) < end + 1 + size + 1:
                    break
                found[oid], at = output[end + 1 : end + 1 + size], end + 1 + size + 1
            read += 1
        if read == len(pending):
            break
        found[pending[read]] = None
        pending = pending[read + 1 :]
    return found


def kind_of(path: Path) -> str:
    """What a path of the working tree is, read without following a link."""
    try:
        mode = os.lstat(path).st_mode
    except (FileNotFoundError, NotADirectoryError):
        return "missing"
    if stat.S_ISLNK(mode):
        return "link"
    if stat.S_ISDIR(mode):
        return "folder"
    return "file" if stat.S_ISREG(mode) else "other"


def in_working_tree(root: Path, path: str, folders: dict[str, str]) -> tuple[str, bytes] | None:
    """What the working tree holds at a tracked path, as a kind and its bytes: a file's, a
    link's path, or nothing for anything else or for a path that lies in a folder that is a
    link; or None where it holds nothing. It follows no link, and opens a file only once it
    knows the file to be one."""
    parts = path.split("/")
    for depth in range(1, len(parts)):
        folder = "/".join(parts[:depth])
        if folder not in folders:
            folders[folder] = kind_of(root / folder)
        if folders[folder] == "link":
            return ("under a link", b"")
        if folders[folder] != "folder":
            return None
    full = root / path
    kind = kind_of(full)
    if kind == "missing":
        return None
    if kind == "link":
        return ("link", os.fsencode(os.readlink(full)))
    if kind != "file":
        return ("other", b"")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    descriptor = os.open(full, flags)
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            return ("other", b"")
        with open(descriptor, "rb", closefd=False) as file:
            return ("file", file.read())
    finally:
        os.close(descriptor)


def refused(character: str, before: str, others: bool, markdown: bool) -> str:
    """Why a file may not hold a character that follows another, or nothing when it may."""
    if " " <= character <= "~" or character == "\n":
        return ""
    if not others:
        return NOT_ASCII
    if character == "\t":
        return ""
    if character == SELECTOR:
        if before in SELECTED:
            return ""
        after = named(before) if before else "the start of a line"
        return f" right after {after}, after which the list does not give it"
    entry = LISTED.get(character)
    if entry is None:
        return NOT_LISTED
    return MARKDOWN_ALONE if entry.markdown_only and not markdown else ""


def escapes(line: str) -> Iterator[tuple[int, str, str]]:
    """Each character that an escape on the line writes, with its column and the character
    before it, so that a surrogate pair is read as the character that it writes and variation
    selector 16 as what follows the character before it, as a loader reads them."""
    runs: list[list[tuple[int, int]]] = []
    end = -1
    for found in ESCAPE.finditer(line):
        code = int(next(group for group in found.groups() if group), 16)
        if runs and found.start() == end:
            runs[-1].append((found.start() + 1, code))
        else:
            runs.append([(found.start() + 1, code)])
        end = found.end()
    for run in runs:
        start = run[0][0] - 1
        before = line[start - 1] if start else ""
        index = 0
        while index < len(run):
            column, code = run[index]
            index += 1
            if 0xD800 <= code < 0xDC00 and index < len(run) and 0xDC00 <= run[index][1] < 0xE000:
                code = 0x10000 + ((code - 0xD800) << 10) + run[index][1] - 0xDC00
                index += 1
            if code <= 0x10FFFF:
                yield column, chr(code), before
                before = chr(code)


def scalars(node: yaml.Node | None, seen: set[int]) -> Iterator[yaml.ScalarNode]:
    """Each scalar of a YAML document, keys among them, each once, an alias's included."""
    if node is None or id(node) in seen:
        return
    seen.add(id(node))
    if isinstance(node, yaml.ScalarNode):
        yield node
    elif isinstance(node, yaml.SequenceNode):
        for item in node.value:
            yield from scalars(item, seen)
    elif isinstance(node, yaml.MappingNode):
        for key, value in node.value:
            yield from scalars(key, seen)
            yield from scalars(value, seen)


def front_matter_problems(path: str, text: str, where: str, markdown: bool) -> list[str]:
    """Each character that a skill's front matter gives once YAML reads it and that the file
    may not hold, other than one that the file holds as itself or by an escape there, which
    the reading of its lines names already (R269, T263)."""
    lines = text.split("\n")
    if lines[0] != "---":
        return []
    name = shown_path(path)
    closing = next((number for number in range(1, len(lines)) if lines[number] == "---"), 0)
    if not closing:
        return [f"{name}{where} opens front matter that no line of --- closes"]
    body = "\n".join(lines[1:closing])
    try:
        document = yaml.compose(body, Loader=yaml.SafeLoader)
    except yaml.YAMLError:
        return [f"{name}{where} gives front matter that the test cannot read as YAML"]
    held = set(body) | {character for line in lines[1:closing] for _, character, _ in escapes(line)}
    problems = []
    for node in scalars(document, set()):
        before = ""
        for character in str(node.value):
            reason = refused(character, before, True, markdown)
            if reason and character not in held:
                problems.append(
                    f"{name}:{node.start_mark.line + 2}{where} gives {named(character)} in its "
                    f"front matter, read as YAML{reason}"
                )
            before = character
    return problems


def encoding_problems(path: str, text: str, where: str = "") -> list[str]:
    """The encoding that a file that Python reads as source declares, by its extension or by
    a first line that runs Python, on either of its first two lines, unless it is UTF-8
    (R268, T260)."""
    lines = text.split("\n")[:2]
    if not (PYTHON_FILE.search(path) or PYTHON_LINE.match(lines[0])):
        return []
    problems = []
    for line in lines:
        declared = CODING.match(line)
        if declared:
            try:
                codec = codecs.lookup(declared.group(1)).name
            except LookupError:
                codec = ""
            if codec != "utf-8":
                problems.append(
                    f"{shown_path(path)}{where} declares to Python the encoding "
                    f"{shown(declared.group(1))}, not UTF-8"
                )
    return problems


def text_problems(path: str, text: str, where: str, others: bool, markdown: bool) -> list[str]:
    """Each character of a file's text that its writer may not use, by line and column, each
    that an escape writes in a file that others write, and each that a skill's front matter
    gives, and the encoding that a file that this repository writes declares to Python."""
    name = shown_path(path)
    problems = []
    for number, line in enumerate(text.split("\n"), 1):
        before = ""
        for column, character in enumerate(line, 1):
            reason = refused(character, before, others, markdown)
            if reason:
                problems.append(f"{name}:{number}:{column}{where} holds {named(character)}{reason}")
            before = character
        if others:
            for column, character, before in escapes(line):
                reason = refused(character, before, others, markdown)
                if reason:
                    problems.append(
                        f"{name}:{number}:{column}{where} writes {named(character)} by an "
                        f"escape{reason}"
                    )
    if not others:
        return problems + encoding_problems(path, text, where)
    if markdown and PurePosixPath(path).name.casefold() == "skill.md":
        problems += front_matter_problems(path, text, where, markdown)
    return problems


def link_problems(path: str, target: bytes, where: str) -> list[str]:
    """A link's path, which the test reads and never follows, unless it is printable ASCII."""
    held = target.decode("utf-8", "surrogateescape")
    if all(" " <= character <= "~" for character in held):
        return []
    return [f"{shown_path(path)}{where} is a link to {shown_path(held)}, beyond printable ASCII"]


def version_problems(
    entry: Entry,
    where: str,
    kind: str,
    data: bytes,
    others: bool,
    markdown: bool,
    passed: set[str],
) -> list[str]:
    """What one version of a tracked path, git's index's or the working tree's, holds that
    its writer may not use, unless it is a listed image, PDF or video whose bytes are not
    UTF-8."""
    name = shown_path(entry.path)
    if kind == "link":
        return link_problems(entry.path, data, where)
    if kind == "under a link":
        return [f"{name}{where} lies in a folder that is a link, which the test does not follow"]
    if kind != "file":
        return [f"{name}{where} is neither a file nor a link, which the test cannot read"]
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        if entry.path in passed:
            return []
        return [f"{name}{where} is not UTF-8, so the test cannot read it as text"]
    return text_problems(entry.path, text, where, others, markdown)


def path_problems(paths: Iterable[str]) -> list[str]:
    """Each tracked path that holds a character other than printable ASCII but the space,
    and each two paths, or a path and a folder that holds another, that differ only in the
    case of their letters, which a file system that ignores case holds as one (R268, T258)."""
    unique = sorted(set(paths))
    problems = [
        f"the path {shown_path(path)} holds a character other than printable ASCII but the space"
        for path in unique
        if not all("!" <= character <= "~" for character in path)
    ]
    by_case: dict[str, list[str]] = defaultdict(list)
    folders: dict[str, dict[str, str]] = defaultdict(dict)
    for path in unique:
        by_case[path.casefold()].append(path)
        parts = path.split("/")
        for depth in range(1, len(parts)):
            folder = "/".join(parts[:depth])
            folders[folder.casefold()].setdefault(folder, path)
    for same in by_case.values():
        if len(same) > 1:
            problems.append(
                f"the paths {' and '.join(map(shown_path, same))} differ only in case, which "
                "a file system that ignores case holds as one file"
            )
    for path in unique:
        for folder, inside in folders.get(path.casefold(), {}).items():
            if folder != path:
                problems.append(
                    f"the path {shown_path(path)} and the folder {shown_path(folder)}, which "
                    f"holds {shown_path(inside)}, differ only in case, which a file system "
                    "that ignores case cannot hold both of"
                )
    return problems


def versions(
    index: tuple[str, bytes], tree: tuple[str, bytes] | None
) -> list[tuple[str, tuple[str, bytes]]]:
    """The versions of a tracked path that a check reads, each with the words that tell which
    it is: git's index's alone where the working tree holds the same or nothing, and else
    both (R272)."""
    return [("", index)] if tree in (None, index) else [(IN_INDEX, index), (IN_TREE, tree)]


def character_problems(root: Path, exceptions: Iterable[Excepted] = EXCEPTIONS) -> list[str]:
    """R268, R269 and R272's reading of every path that git's index tracks, and of each file
    as git's index holds it and as the working tree holds it, where it holds one, but a listed
    image, PDF or video whose bytes are not UTF-8 (R270)."""
    entries = tracked_entries(root)
    if not entries:
        return [f"git lists no tracked file, so {READ_NOTHING}"]
    markdown = markdown_files(root)
    passed = {excepted.path for excepted in exceptions if media(excepted.path)}
    contents = blobs(root, (entry.oid for entry in entries if entry.mode != GITLINK))
    problems = path_problems(entry.path for entry in entries)
    folders: dict[str, str] = {}
    read = 0
    for entry in entries:
        name = shown_path(entry.path)
        if entry.mode not in (FILE, EXECUTABLE, LINK):
            problems.append(
                f"{name} is neither a file nor a link, but a submodule or another entry that "
                "the test cannot read"
            )
            continue
        indexed = contents.get(entry.oid)
        if indexed is None:
            problems.append(
                f"{name} names an object that this clone lacks, as a partial clone does, which "
                "the test does not fetch"
            )
            continue
        read += 1
        index = ("link" if entry.mode == LINK else "file", indexed)
        tree = in_working_tree(root, entry.path, folders)
        others, page = bool(written_by_others(entry.path)), entry.path in markdown
        for where, (kind, data) in versions(index, tree):
            problems += version_problems(entry, where, kind, data, others, page, passed)
    if not read:
        problems.append(READ_NOTHING)
    return problems


def list_problems(visible: Iterable[Visible], oldest: bool) -> list[str]:
    """Each entry of a list of visible characters that is not punctuation or a symbol by its
    Unicode category, that shows as blank, that is given twice or under a name other than
    Unicode's, or, on any Python but the oldest supported, that its database does not know
    (R269, T255)."""
    problems, seen = [], set()
    for entry in visible:
        label = f"U+{entry.code_point:04X} {shown(entry.name)}"
        if entry.code_point in seen:
            problems.append(f"the list gives {label} twice")
        seen.add(entry.code_point)
        if not 0 <= entry.code_point <= 0x10FFFF:
            problems.append(f"the list gives {label}, which is no code point")
            continue
        character = chr(entry.code_point)
        category = unicodedata.category(character)
        if category == "Cn":
            if not oldest:
                problems.append(f"the list gives {label}, which this Python's database lacks")
            continue
        if category[0] not in "PS":
            problems.append(
                f"the list gives {label}, of category {category}, no punctuation or symbol"
            )
        if entry.code_point in BLANK:
            problems.append(f"the list gives {label}, which shows as blank")
        if unicodedata.name(character, "") != entry.name:
            problems.append(f"the list gives {label}, which Unicode names {named(character)}")
    return problems


def media(path: str) -> bool:
    """Whether a path's extension, in any case, is that of an image, a PDF or a video."""
    name = path.rpartition("/")[2]
    return "." in name and name.rpartition(".")[2].lower() in MEDIA


def exception_problems(root: Path, exceptions: Iterable[Excepted]) -> list[str]:
    """Each tracked image, PDF or video that the list of exceptions does not give, and each
    entry of the list that gives a path that git does not track, a file that is not an image,
    a PDF or a video by its extension, no object id or another than git holds, or a record
    that does not exist, is not accepted or names the path in none of its code spans (R270,
    DR-276)."""
    held = {entry.path: entry for entry in tracked_entries(root)}
    if not held:
        return [MEDIA_READ_NOTHING]
    folder = root / "docs" / "decisions"
    records = records_of(folder)[0] if folder.is_dir() else {}
    problems, listed = [], set()
    for excepted in exceptions:
        listed.add(excepted.path)
        path = shown_path(excepted.path)
        entry = held.get(excepted.path)
        if entry is None:
            problems.append(f"the exception for {path} gives a path that git does not track")
        if not media(excepted.path):
            problems.append(
                f"the exception for {path} gives a file that is not an image, a PDF or a video"
                " by its extension"
            )
        if not OBJECT_ID.fullmatch(excepted.oid):
            problems.append(f"the exception for {path} gives no object id")
        elif entry is not None and entry.oid != excepted.oid:
            problems.append(
                f"{path} is held by git as {entry.oid}, and the exception for {path} gives"
                f" {excepted.oid}"
            )
        cited = f"the exception for {path} cites {shown(excepted.record)}"
        found = records.get(excepted.record)
        if found is None:
            problems.append(f"{cited}, which is no record")
        elif found.fields.get("Status") != "accepted":
            problems.append(
                f"{cited}, which is {shown(found.fields.get('Status', ''))}, not accepted"
            )
        elif excepted.path not in {span.group(2) for span in CODE_SPAN.finditer(found.text)}:
            problems.append(f"{cited}, which names {path} in no code span")
    return problems + [
        f"{shown_path(path)}{UNLISTED}" for path in held if media(path) and path not in listed
    ]


def markup(line: str, at: int, folds: bool, autolinks: bool) -> tuple[str, str] | None:
    """What the raw HTML that may start at this column of a line is and why it fails, or None
    where none starts there: an autolink is none on a line read as prose, and neither is a
    fold of the README (R273)."""
    if autolinks and AUTOLINK.match(line, at):
        return None
    if folds and line.startswith(FOLDS, at):
        return None
    if line.startswith("<!--", at):
        return "an HTML comment", HIDES
    if line.startswith("<![CDATA[", at):
        return "a CDATA section", HIDES
    if DECLARATION.match(line, at):
        return "a declaration", HIDES
    if line.startswith("<?", at):
        return "a processing instruction", HIDES
    tag = TAG.match(line, at)
    return (f"the HTML element {shown(tag.group())}", SHOWN_OTHERWISE) if tag else None


def destination(line: str, at: int) -> tuple[int | None, int]:
    """Where the destination of a link whose `](` starts at this column starts, where angle
    brackets hold it, and where it ends: after its closing bracket, or else at the first
    space, tab or closing parenthesis that no opening one matches, a backslash escaping the
    character after it."""
    start = at + 2
    while line[start : start + 1] in (" ", "\t"):
        start += 1
    angle = ANGLE.match(line, start)
    if angle:
        return start, angle.end()
    end, depth = start, 0
    while end < len(line) and line[end] not in " \t":
        if line[end] == "\\":
            end += 1
        elif line[end] == "(":
            depth += 1
        elif line[end] == ")":
            if not depth:
                break
            depth -= 1
        end += 1
    return None, end


def line_problems(seen: str, raw: str, folds: bool) -> list[tuple[int, str]]:
    """Each mark that GitHub hides or shows otherwise on a line read as prose, by its column:
    raw HTML, a character reference that GitHub knows, `$`, a link or footnote definition, an
    image, a link that may give a title, the end of the line among what may follow its
    destination since a title may start there, and a backtick that a backslash escapes,
    which the reading takes to open or close code (R273)."""
    found: list[tuple[int, str]] = []
    angles: set[int] = set()
    for mark in MARK.finditer(seen):
        at, token = mark.start(), mark.group()
        what = PLAIN.get(token, "")
        if token[0] == "<" and at not in angles:
            element = markup(seen, at, folds, autolinks=True)
            what = "".join(element) if element else ""
        elif token == "&":
            reference = REFERENCE.match(seen, at)
            if reference and (reference[1] is None or f"{reference[1]};" in html.entities.html5):
                what = f"the character reference {shown(reference.group())}{NAMES_CHARACTER}"
        elif token == "](":
            start, end = destination(seen, at)
            if start is not None:
                angles.add(start)
            if not seen[end:].lstrip(" \t").startswith(")"):
                what = TITLE
        if what:
            found.append((at + 1, what))
    found += [
        (escape.end() - 1, BACKSLASHED)
        for escape in ESCAPED_BACKTICK.finditer(raw)
        if seen[escape.end() - 2] == "\\"
    ]
    return found


def open_runs(line: str) -> list[int]:
    """The column of each run of backticks that a line leaves open, outside the code spans
    that the reading finds on it, which GitHub may pair with a run on a later line of the
    paragraph, so that the two tell code there in two ways (R273). It reads the line once."""
    spans = iter(code_spans(line)[0])
    span = next(spans, None)
    found = []
    for run in BACKTICKS.finditer(line):
        while span is not None and span[1] <= run.start():
            span = next(spans, None)
        if span is None or run.start() < span[0]:
            found.append(run.start() + 1)
    return found


def cells_of(line: str) -> list[str]:
    """The cells that GitHub reads in a table's row: the line without the markers of the
    quotes and list items that hold it, split at each pipe that no backslash escapes, in a
    code span too, without the empty cells before a leading pipe and after a final one."""
    row = CONTAINER.sub("", line).strip(" \t")
    cells = CELL_BORDER.split(row)
    if row.startswith("|"):
        cells = cells[1:]
    if row.endswith("|") and not row.endswith("\\|") and cells:
        cells = cells[:-1]
    return cells


def table_problems(lines: list[str], fenced: set[int]) -> list[tuple[int, str]]:
    """Each row of a table, by its line, that holds more cells than the table's header, whose
    cells past the header's GitHub hides (R273). A table is a line of cells and a line of
    delimiters with as many, outside code, and its rows run up to a blank line or a fence."""
    found: list[tuple[int, str]] = []
    taken: set[int] = set()
    for number in range(2, len(lines) + 1):
        line, above = lines[number - 1], lines[number - 2]
        if (
            "|" not in line
            or "-" not in line
            or not above.strip(" \t>")
            or {number - 1, number} & fenced
            or {number - 1, number} & taken
        ):
            continue
        delimiters, header = cells_of(line), cells_of(above)
        if not delimiters or len(header) != len(delimiters):
            continue
        if not all(DELIMITER_CELL.fullmatch(cell) for cell in delimiters):
            continue
        row = number + 1
        while row <= len(lines) and row not in fenced and lines[row - 1].strip(" \t>"):
            held = len(cells_of(lines[row - 1]))
            if held > len(header):
                found.append(
                    (
                        row,
                        f"a table row of {held} cells under a header of {len(header)}, whose"
                        " cells past the header's GitHub hides",
                    )
                )
            row += 1
        taken.update(range(number - 1, row))
    return found


def mermaid_problems(lines: list[str], block: Block) -> list[tuple[int, int, str]]:
    """What a Mermaid block holds that the drawing hides or shows otherwise, by its line and
    column: front matter and a statement, either of which gives text that the drawing does
    not show or changes how it shows it, an entity code, a comment or a directive, and raw
    HTML, an autolink among it (R273)."""
    found: list[tuple[int, int, str]] = []
    first = next((number for number in block.held if lines[number - 1].strip(" \t")), None)
    if first is not None and lines[first - 1].strip(" \t") == "---":
        column = lines[first - 1].index("-") + 1
        found.append((first, column, f"front matter{IN_MERMAID}{MERMAID_HIDES}"))
    for number in block.held:
        line = lines[number - 1]
        statement = MERMAID_STATEMENT.match(line)
        if statement:
            found.append(
                (number, statement.start(1) + 1, f"{statement[1]}{IN_MERMAID}{MERMAID_HIDES}")
            )
        found += [
            (
                number,
                code.start() + 1,
                f"the entity code {shown(code.group())}{IN_MERMAID}{ENTITY_NAMES}",
            )
            for code in ENTITY_CODE.finditer(line)
        ]
        comment = line.find("%%")
        if comment >= 0:
            found.append((number, comment + 1, f"%%{IN_MERMAID}{DIRECTIVE}"))
        for opening in re.finditer("<", line):
            element = markup(line, opening.start(), folds=False, autolinks=False)
            if element:
                found.append((number, opening.start() + 1, f"{element[0]}{IN_MERMAID}{element[1]}"))
    return found


def without_comments(text: str) -> tuple[str, tuple[int, int] | None, set[int]]:
    """A template's text with each HTML comment outside code made spaces, its line breaks
    kept, so that the columns after it stay as they were; where one opens that never closes,
    by its line and column, from where GitHub hides the rest; and each line on which a
    comment that opens a line closes, the rest of which GitHub reads as raw HTML (R273). Each
    comment is found as the reading reads the text once the comments before it are gone,
    since a backtick or a fence in a comment opens no code."""
    raw: set[int] = set()
    while True:
        seen = "".join(reading(text)[0])
        at = seen.find("<!--")
        if at < 0:
            return text, None, raw
        start = text.rfind("\n", 0, at) + 1
        end = text.find("-->", at + 2)
        stop = len(text) if end < 0 else end + 3
        text = text[:at] + re.sub(r"[^\n]", " ", text[at:stop]) + text[stop:]
        if end < 0:
            return text, (text.count("\n", 0, at) + 1, at - start + 1), raw
        if at - start <= 3 and not text[start:at].strip(" "):
            raw.add(text.count("\n", 0, end) + 1)


def fold_lines(lines: list[str], view: list[str]) -> set[int]:
    """The lines of the README that GitHub reads as raw HTML where the test lets its folds
    stand: from each line that a fold opens, after at most three spaces and outside code, up
    to the next blank line (R273)."""
    found: set[int] = set()
    inside = False
    for number, (raw, seen) in enumerate(zip(lines, view, strict=True), 1):
        indent = len(seen) - len(seen.lstrip(" "))
        if not raw.strip(" \t"):
            inside = False
        elif indent <= 3 and seen.startswith(FOLDS, indent):
            inside = True
        if inside:
            found.add(number)
    return found


def page_text_problems(path: str, text: str, where: str = "") -> list[str]:
    """What one version of a page holds that GitHub hides or shows otherwise, by its line
    and, for a mark on a line, its column, and where the reading of its code stopped short
    (R273, DR-279). A template's comments are passed over, and the README's folds, but code
    on a line that GitHub reads as raw HTML after either."""
    name = shown_path(path)
    found: list[tuple[int, int, str]] = []
    raw_html: set[int] = set()
    if TEMPLATE.match(path):
        text, unclosed, raw_html = without_comments(text)
        if unclosed:
            found.append((unclosed[0], unclosed[1], NEVER_ENDS))
    chars, stopped, blocks = reading(text)
    lines, view = text.split("\n"), "".join(chars).split("\n")
    if path == README:
        raw_html = fold_lines(lines, view)
    for number in sorted(raw_html):
        code = RAW_CODE.search(lines[number - 1])
        if code:
            opens = "a backtick" if code.group() == "`" else "a run of tildes"
            found.append((number, code.start() + 1, f"{opens}{OPENS_NO_CODE}"))
    for block in blocks:
        words = block.info.split()
        if len(words) > 1 or (words and not LANGUAGE.fullmatch(words[0])):
            found.append((block.line, 0, INFO))
        language = words[0].casefold() if words else ""
        if language in DRAWN:
            found.append((block.line, 0, f"a fenced block that GitHub draws as {language}"))
        elif language == "mermaid":
            found += mermaid_problems(lines, block)
    fenced = block_lines(blocks)
    found += [(row, 0, what) for row, what in table_problems(lines, fenced)]
    read_to = min((line for line, _ in stopped), default=len(lines) + 1)
    found += [
        (number, column, OPEN_RUN)
        for number, raw in enumerate(lines[: read_to - 1], 1)
        if number not in fenced
        for column in open_runs(raw)
    ]
    for number, (seen, raw) in enumerate(zip(view, lines, strict=True), 1):
        found += [
            (number, column, what) for column, what in line_problems(seen, raw, path == README)
        ]
    problems = [
        (line, column, f"{name}:{line}{f':{column}' if column else ''}{where} holds {what}")
        for line, column, what in found
    ]
    problems += [(line, 0, f"{name}:{line}{where}: {message}") for line, message in stopped]
    return [problem for _, _, problem in sorted(problems, key=lambda problem: problem[:2])]


def page_problems(root: Path) -> list[str]:
    """What each Markdown file that this repository writes holds that GitHub hides or shows
    otherwise, as git's index holds it and as the working tree holds it, where it differs
    (R272, R273). A version that is no file of UTF-8 text, and an object that this clone
    lacks, it leaves to the test of characters, which names each."""
    markdown = markdown_files(root)
    pages = [
        entry
        for entry in tracked_entries(root)
        if entry.path in markdown
        and entry.mode in (FILE, EXECUTABLE)
        and not written_by_others(entry.path)
    ]
    contents = blobs(root, (entry.oid for entry in pages))
    problems: list[str] = []
    folders: dict[str, str] = {}
    read = 0
    for entry in pages:
        indexed = contents.get(entry.oid)
        if indexed is None:
            continue
        tree = in_working_tree(root, entry.path, folders)
        for where, (kind, data) in versions(("file", indexed), tree):
            if kind != "file":
                continue
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                continue
            read += 1
            problems += page_text_problems(entry.path, text, where)
    return problems if read else [PAGES_READ_NOTHING]


def plant(
    root: Path,
    files: Mapping[str, str | bytes],
    links: Mapping[str, str] | None = None,
    executable: Iterable[str] = (),
) -> Path:
    """A git repository at root whose index holds these files, each as written, and these
    links to their paths."""
    root.mkdir(parents=True, exist_ok=True)
    git(root, "init", "-q").check_returncode()
    for name, content in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode("utf-8") if isinstance(content, str) else content)
    for name in executable:
        (root / name).chmod(0o755)
    for name, target in (links or {}).items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.symlink_to(target)
    git(root, "add", "-A").check_returncode()
    return root


def commit(root: Path) -> None:
    git(root, "commit", "-q", "-m", "Plant", extra=AUTHOR).check_returncode()


# R268: the files that this repository writes hold only printable ASCII and line feeds.

OWN_KINDS = ("page.md", "tool.py", "check.yml", "start.sh")
# Each character that the scenarios name, by the name of the folder that plants it.
OWN_CHARACTERS = {
    "tab": "\t",
    "return": "\r",
    "return-and-feed": "\r\n",
    "byte-order-mark": "\ufeff",
    "zero-width-space": "\u200b",
    "right-to-left-override": "\u202e",
    "non-breaking-space": "\u00a0",
    "em-dash": "\u2014",
    "arrow": "\u2192",
    "accented-letter": "\u00e9",
}
OTHERS_KINDS = (
    "vendor/superpowers/{}/SKILL.md",
    "vendor/superpowers/{}/start.sh",
    ".claude/skills/openspec-{}/SKILL.md",
)
OTHERS_CHARACTERS = {
    "return": "\r",
    "return-and-feed": "\r\n",
    "zero-width-space": "\u200b",
    "right-to-left-override": "\u202e",
    "byte-order-mark": "\ufeff",
    "non-breaking-space": "\u00a0",
    "tag": "\U000e0041",
    "cyrillic-letter": "\u0430",
}


def planted_line(character: str) -> str:
    """A file's text that holds the character on its second line, in its third column."""
    return f"The first line.\nab{character}cd\n"


@pytest.fixture(scope="module")
def planted_characters(tmp_path_factory: pytest.TempPathFactory) -> list[str]:
    files = {
        f"own/{case}/{kind}": planted_line(character)
        for case, character in OWN_CHARACTERS.items()
        for kind in OWN_KINDS
    }
    files |= {
        kind.format(case): planted_line(character)
        for case, character in OTHERS_CHARACTERS.items()
        for kind in OTHERS_KINDS
    }
    return character_problems(plant(tmp_path_factory.mktemp("characters"), files))


@pytest.mark.parametrize("kind", OWN_KINDS)
@pytest.mark.parametrize("case", OWN_CHARACTERS)
def test_a_character_beyond_printable_ascii_in_a_file_that_this_repository_writes_fails(
    planted_characters: list[str], case: str, kind: str
) -> None:
    character = OWN_CHARACTERS[case][0]
    assert f"own/{case}/{kind}:2:3 holds {named(character)}{NOT_ASCII}" in planted_characters


@pytest.mark.parametrize("kind", OTHERS_KINDS)
@pytest.mark.parametrize("case", OTHERS_CHARACTERS)
def test_a_character_that_a_reader_cannot_see_in_a_file_that_others_write_fails(
    planted_characters: list[str], case: str, kind: str
) -> None:
    character = OTHERS_CHARACTERS[case][0]
    assert f"{kind.format(case)}:2:3 holds {named(character)}{NOT_LISTED}" in planted_characters


def test_each_planted_character_is_named_once_and_nothing_else_is(
    planted_characters: list[str],
) -> None:
    planted = len(OWN_CHARACTERS) * len(OWN_KINDS) + len(OTHERS_CHARACTERS) * len(OTHERS_KINDS)
    assert len(planted_characters) == len(set(planted_characters)) == planted


def test_a_visible_character_that_the_list_does_not_give_is_left_to_the_owner(
    planted_characters: list[str],
) -> None:
    found = [
        problem for problem in planted_characters if "U+0430 CYRILLIC SMALL LETTER A" in problem
    ]
    assert len(found) == len(OTHERS_KINDS)
    for problem in found:
        assert problem.endswith(", which the list does not give; the owner decides whether it does")
        assert "add" not in problem and "VISIBLE" not in problem


def test_printable_ascii_and_line_feeds_pass(tmp_path: Path) -> None:
    files = {
        "README.md": "# A page\n\nPrintable ASCII, ~ and all.\n",
        "scripts/tool.py": "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\nprint('a')\n",
        ".github/workflows/check.yml": "on: push\n",
        "vendor/superpowers/UPSTREAM.lock": "commit=0123456789abcdef\n",
    }
    root = plant(
        tmp_path, files, links={"docs/link.md": "../README.md"}, executable=["scripts/tool.py"]
    )
    assert character_problems(root) == []


# R269: the files that others write hold only the characters that the list gives for them.


def test_the_characters_that_the_list_gives_pass_in_the_files_that_others_write(
    tmp_path: Path,
) -> None:
    every = "".join(chr(entry.code_point) for entry in VISIBLE)
    anywhere = "".join(chr(entry.code_point) for entry in VISIBLE if not entry.markdown_only)
    files = {
        "vendor/superpowers/skills/a/SKILL.md": f"# A\n\n{every}\tand \u26a0\ufe0f too.\n",
        "vendor/superpowers/hooks/start.sh": f"echo '{anywhere}\t\u26a0\ufe0f'\n",
        ".claude/skills/openspec-a/SKILL.md": (
            f'---\nname: a\ndescription: "\\u2014 and \\t"\n---\n\n{every}\n'
        ),
    }
    assert character_problems(plant(tmp_path, files)) == []


def test_a_character_listed_for_markdown_alone_fails_in_another_file(tmp_path: Path) -> None:
    files = {
        "vendor/superpowers/hooks/start.sh": "echo '\u00a7 1'\n",
        "vendor/superpowers/skills/a/SKILL.md": "\u00a7 1\n",
    }
    assert character_problems(plant(tmp_path, files)) == [
        f"vendor/superpowers/hooks/start.sh:1:7 holds {named(chr(0xA7))}{MARKDOWN_ALONE}"
    ]


@pytest.mark.parametrize(("before", "column"), [("\u2014", 2), ("a", 2), ("", 1)])
def test_variation_selector_16_after_a_character_not_listed_for_it_fails(
    tmp_path: Path, before: str, column: int
) -> None:
    path = "vendor/superpowers/skills/a/SKILL.md"
    after = named(before) if before else "the start of a line"
    assert character_problems(plant(tmp_path, {path: f"{before}{SELECTOR}\n"})) == [
        f"{path}:1:{column} holds {named(SELECTOR)} right after {after}, after which the list "
        "does not give it"
    ]


ESCAPED = [
    ("\\u200b", "\u200b"),
    ("\\u{202e}", "\u202e"),
    ("\\U000e0041", "\U000e0041"),
    ("\\x1b", "\x1b"),
    ("\\ud83d\\ude00", "\U0001f600"),
    ("\\ud83d", "\ud83d"),
]


@pytest.mark.parametrize("kind", ["helper.js", "SKILL.md"])
@pytest.mark.parametrize(("escape", "character"), ESCAPED)
def test_a_character_written_by_an_escape_is_held_as_the_character(
    tmp_path: Path, escape: str, character: str, kind: str
) -> None:
    path = f"vendor/superpowers/skills/a/{kind}"
    assert character_problems(plant(tmp_path, {path: f"x = '{escape}'\n"})) == [
        f"{path}:1:6 writes {named(character)} by an escape{NOT_LISTED}"
    ]


def test_an_escape_of_a_character_that_the_file_may_hold_passes(tmp_path: Path) -> None:
    files = {
        "vendor/superpowers/skills/a/helper.js": (
            "x = '\\u2014 \\ud83c\\udfaf \\x41 \\u{2192} \\x09'\n"
        ),
        "vendor/superpowers/skills/a/SKILL.md": "\\u00a7 and \\u26a0\\ufe0f\n",
    }
    assert character_problems(plant(tmp_path, files)) == []


def test_an_escape_of_a_character_listed_for_markdown_alone_fails_in_a_script(
    tmp_path: Path,
) -> None:
    path = "vendor/superpowers/skills/a/helper.js"
    assert character_problems(plant(tmp_path, {path: "x = '\\u00a7'\n"})) == [
        f"{path}:1:6 writes {named(chr(0xA7))} by an escape{MARKDOWN_ALONE}"
    ]


@pytest.mark.parametrize(
    ("escape", "character"),
    [("\\e", "\x1b"), ("\\_", "\u00a0"), ("\\N", "\x85"), ("\\L", "\u2028"), ("\\0", "\x00")],
)
def test_a_character_that_a_skill_s_front_matter_gives_once_yaml_reads_it_fails(
    tmp_path: Path, escape: str, character: str
) -> None:
    path = ".claude/skills/openspec-a/SKILL.md"
    text = f'---\nname: a\ndescription: "before {escape} after"\n---\n# A\n'
    assert character_problems(plant(tmp_path, {path: text})) == [
        f"{path}:3 gives {named(character)} in its front matter, read as YAML{NOT_LISTED}"
    ]


def test_a_key_of_a_skill_s_front_matter_is_read_too(tmp_path: Path) -> None:
    path = "vendor/superpowers/skills/a/SKILL.md"
    text = '---\nname: a\n"na\\eme": a\n---\n'
    assert character_problems(plant(tmp_path, {path: text})) == [
        f"{path}:3 gives {named(chr(0x1B))} in its front matter, read as YAML{NOT_LISTED}"
    ]


def test_an_escape_in_a_skill_s_front_matter_is_named_once(tmp_path: Path) -> None:
    path = "vendor/superpowers/skills/a/SKILL.md"
    text = '---\nname: a\ndescription: "a \\u200b b"\n---\n'
    assert character_problems(plant(tmp_path, {path: text})) == [
        f"{path}:3:17 writes {named(chr(0x200B))} by an escape{NOT_LISTED}"
    ]


@pytest.mark.parametrize(
    ("text", "problem"),
    [
        ("---\nname: [a\n---\n", "gives front matter that the test cannot read as YAML"),
        ("---\nname: a\n", "opens front matter that no line of --- closes"),
    ],
)
def test_front_matter_that_the_test_cannot_read_fails(
    tmp_path: Path, text: str, problem: str
) -> None:
    path = "vendor/superpowers/skills/a/SKILL.md"
    assert character_problems(plant(tmp_path, {path: text})) == [f"{path} {problem}"]


def test_front_matter_is_read_only_in_a_skill_that_others_write(tmp_path: Path) -> None:
    files = {
        "vendor/superpowers/skills/a/notes.md": "---\nname: [a\n---\n",
        "docs/SKILL.md": '---\nname: "\\e"\n---\n',
    }
    assert character_problems(plant(tmp_path, files)) == []


# R272: the test reads every file as git's index holds it and as the working tree holds it.


def test_a_character_that_only_git_s_index_holds_fails(tmp_path: Path) -> None:
    files: dict[str, str | bytes] = {
        ".gitattributes": "page.md working-tree-encoding=UTF-7\n",
        "page.md": planted_line("\u202e").encode("utf-7"),
    }
    source = plant(tmp_path / "source", files)
    commit(source)
    clone = tmp_path / "clone"
    subprocess.run(
        ["git", "clone", "-q", str(source), str(clone)],
        check=True,
        capture_output=True,
        env=isolated_environment(clone),
    )
    assert (clone / "page.md").read_bytes().isascii()
    assert character_problems(clone) == [
        f"page.md:2:3{IN_INDEX} holds {named(chr(0x202E))}{NOT_ASCII}"
    ]


def test_an_edit_not_yet_staged_is_read(tmp_path: Path) -> None:
    root = plant(tmp_path, {"page.md": planted_line("")})
    (root / "page.md").write_text(planted_line("\u00e9"), encoding="utf-8")
    assert character_problems(root) == [f"page.md:2:3{IN_TREE} holds {named(chr(0xE9))}{NOT_ASCII}"]


@pytest.mark.parametrize("version", ["index", "tree"])
def test_bytes_that_are_not_utf_8_fail(tmp_path: Path, version: str) -> None:
    root = plant(tmp_path, {"page.md": b"ab\xffcd\n" if version == "index" else "abcd\n"})
    if version == "tree":
        (root / "page.md").write_bytes(b"ab\xffcd\n")
    where = "" if version == "index" else IN_TREE
    assert character_problems(root) == [
        f"page.md{where} is not UTF-8, so the test cannot read it as text"
    ]


def test_a_submodule_fails(tmp_path: Path) -> None:
    root = plant(tmp_path, {"page.md": "Printable.\n"})
    git(
        root, "update-index", "--add", "--cacheinfo", f"{GITLINK},{'1' * 40},vendor/sub"
    ).check_returncode()
    assert character_problems(root) == [
        "vendor/sub is neither a file nor a link, but a submodule or another entry that the test "
        "cannot read"
    ]


def test_an_object_that_the_clone_lacks_fails(tmp_path: Path) -> None:
    root = plant(tmp_path, {"page.md": "Printable.\n"})
    git(
        root, "update-index", "--add", "--cacheinfo", f"{FILE},{'1' * 40},gone.md"
    ).check_returncode()
    assert character_problems(root) == [
        "gone.md names an object that this clone lacks, as a partial clone does, which the test "
        "does not fetch"
    ]


def test_a_partial_clone_s_missing_object_is_named_and_not_fetched(tmp_path: Path) -> None:
    source = plant(tmp_path / "source", {"page.md": "Printable.\n"})
    commit(source)
    git(source, "config", "uploadpack.allowFilter", "true").check_returncode()
    clone = tmp_path / "clone"
    subprocess.run(
        ["git", "clone", "-q", "--filter=blob:none", "--no-checkout", source.as_uri(), str(clone)],
        check=True,
        capture_output=True,
        env=isolated_environment(clone),
    )
    git(clone, "read-tree", "HEAD").check_returncode()
    (oid,) = [entry.oid for entry in tracked_entries(clone)]

    def present() -> bool:
        return git(clone, "cat-file", "-e", oid, extra={"GIT_NO_LAZY_FETCH": "1"}).returncode == 0

    assert not present()
    assert character_problems(clone) == [
        "page.md names an object that this clone lacks, as a partial clone does, which the test "
        "does not fetch",
        READ_NOTHING,
    ]
    assert not present()


def test_a_link_whose_path_is_beyond_printable_ascii_fails(tmp_path: Path) -> None:
    root = plant(
        tmp_path, {"page.md": "Printable.\n"}, links={"docs/link.md": "caf\u00e9\U000e0041.md"}
    )
    assert character_problems(root) == [
        "docs/link.md is a link to cafU+00E9U+E0041.md, beyond printable ASCII"
    ]


def test_a_link_is_read_as_the_path_that_it_holds_and_never_followed(tmp_path: Path) -> None:
    outside = tmp_path / "outside.md"
    outside.write_text(planted_line("\u202e"), encoding="utf-8")
    links = {"docs/link.md": str(outside), "docs/up.md": "../../outside.md"}
    assert character_problems(plant(tmp_path / "repo", {"page.md": "Printable.\n"}, links)) == []


def test_a_file_in_a_folder_that_the_working_tree_holds_as_a_link_is_not_read_through_it(
    tmp_path: Path,
) -> None:
    root = plant(tmp_path / "repo", {"docs/page.md": "Printable.\n"})
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    (elsewhere / "page.md").write_text(planted_line("\u202e"), encoding="utf-8")
    (root / "docs" / "page.md").unlink()
    (root / "docs").rmdir()
    (root / "docs").symlink_to(elsewhere)
    assert character_problems(root) == [
        f"docs/page.md{IN_TREE} lies in a folder that is a link, which the test does not follow"
    ]


def test_a_check_of_characters_that_reads_no_file_fails(tmp_path: Path) -> None:
    git(tmp_path, "init", "-q").check_returncode()
    assert character_problems(tmp_path) == [f"git lists no tracked file, so {READ_NOTHING}"]
    git(
        tmp_path, "update-index", "--add", "--cacheinfo", f"{GITLINK},{'1' * 40},sub"
    ).check_returncode()
    assert character_problems(tmp_path)[-1] == READ_NOTHING


# R268: paths.


@pytest.mark.parametrize(
    "path",
    ["docs/caf\u00e9.md", "docs/a b.md", "docs/a\nb.md", "docs/a\u202eb.md", "docs/\U000e0041.md"],
)
def test_a_path_beyond_printable_ascii_fails(tmp_path: Path, path: str) -> None:
    assert character_problems(plant(tmp_path, {path: "Printable.\n"})) == [
        f"the path {shown_path(path)} holds a character other than printable ASCII but the space"
    ]


def test_two_tracked_paths_that_differ_only_in_case_fail(tmp_path: Path) -> None:
    files = {".claude-plugin/Marketplace.json": "{}\n", ".claude-plugin/marketplace.json": "{}\n"}
    assert character_problems(plant(tmp_path, files)) == [
        "the paths .claude-plugin/Marketplace.json and .claude-plugin/marketplace.json differ "
        "only in case, which a file system that ignores case holds as one file"
    ]


def test_a_file_and_a_folder_that_differ_only_in_case_fail(tmp_path: Path) -> None:
    files = {
        ".claude-plugin/marketplace.json": "{}\n",
        ".claude-plugin/Marketplace.json/notes.md": "Notes.\n",
    }
    assert character_problems(plant(tmp_path, files)) == [
        "the path .claude-plugin/marketplace.json and the folder .claude-plugin/Marketplace.json, "
        "which holds .claude-plugin/Marketplace.json/notes.md, differ only in case, which a file "
        "system that ignores case cannot hold both of"
    ]


# R268: what Python reads as source declares no encoding but UTF-8.


@pytest.mark.parametrize(
    ("path", "text", "declared"),
    [
        ("scripts/tool.py", "# -*- coding: utf-7 -*-\nprint(1)\n", "utf-7"),
        ("scripts/tool.py", "#!/usr/bin/env python3\n# coding: unicode_escape\n", "unicode_escape"),
        ("scripts/stub.pyi", "# vim: set fileencoding=latin-1 :\n", "latin-1"),
        ("hooks/run", "#!/usr/bin/env python3\n# coding=cp1252\n", "cp1252"),
        ("scripts/tool.py", "# coding: no-such-encoding\n", "no-such-encoding"),
    ],
)
def test_a_python_file_that_declares_an_encoding_other_than_utf_8_fails(
    tmp_path: Path, path: str, text: str, declared: str
) -> None:
    assert character_problems(plant(tmp_path, {path: text})) == [
        f"{path} declares to Python the encoding {declared}, not UTF-8"
    ]


@pytest.mark.parametrize(
    ("path", "text"),
    [
        ("scripts/tool.py", "# -*- coding: utf-8 -*-\n"),
        ("scripts/tool.py", "#!/usr/bin/env python3\n# coding: UTF8\n"),
        ("scripts/tool.py", "print(1)\n"),
        ("docs/page.md", "# coding: utf-7\n"),
        ("hooks/run.sh", "#!/bin/sh\n# coding: utf-7\n"),
    ],
)
def test_a_file_that_declares_utf_8_or_that_python_does_not_read_passes(
    tmp_path: Path, path: str, text: str
) -> None:
    assert character_problems(plant(tmp_path, {path: text})) == []


# R269: the list gives only punctuation and symbols that show, under Unicode's names.


@pytest.mark.parametrize(
    ("entry", "problem"),
    [
        (Visible(0x0430, "CYRILLIC SMALL LETTER A", False), "of category Ll"),
        (Visible(0x3164, "HANGUL FILLER", False), "of category Lo"),
        (Visible(0x0661, "ARABIC-INDIC DIGIT ONE", False), "of category Nd"),
        (Visible(0x0301, "COMBINING ACUTE ACCENT", False), "of category Mn"),
        (Visible(0xFE0F, "VARIATION SELECTOR-16", False), "of category Mn"),
        (Visible(0x200B, "ZERO WIDTH SPACE", False), "of category Cf"),
    ],
)
def test_a_list_that_gives_a_character_that_is_no_punctuation_or_symbol_fails(
    entry: Visible, problem: str
) -> None:
    assert list_problems([entry], oldest=False) == [
        f"the list gives U+{entry.code_point:04X} {entry.name}, {problem}, no punctuation or symbol"
    ]


def test_a_list_that_gives_a_character_that_shows_as_blank_fails() -> None:
    assert list_problems([Visible(0x2800, "BRAILLE PATTERN BLANK", False)], oldest=False) == [
        "the list gives U+2800 BRAILLE PATTERN BLANK, which shows as blank"
    ]


def test_a_list_that_gives_a_wrong_name_fails() -> None:
    assert list_problems([Visible(0x2014, "EN DASH", False)], oldest=False) == [
        "the list gives U+2014 EN DASH, which Unicode names U+2014 EM DASH"
    ]


def test_a_list_that_gives_a_character_twice_fails() -> None:
    entries = [VISIBLE[0], VISIBLE[0]._replace(markdown_only=True)]
    assert list_problems(entries, oldest=False) == ["the list gives U+2014 EM DASH twice"]


@pytest.mark.parametrize("oldest", [True, False])
def test_a_listed_code_point_that_the_running_python_does_not_know_is_checked_on_a_later_one(
    oldest: bool,
) -> None:
    entries = [Visible(0x0378, "A CHARACTER YET TO COME", False)]
    assert list_problems(entries, oldest) == (
        []
        if oldest
        else ["the list gives U+0378 A CHARACTER YET TO COME, which this Python's database lacks"]
    )


def test_the_list_gives_only_punctuation_and_symbols_that_show_under_their_names() -> None:
    oldest = f"{sys.version_info.major}.{sys.version_info.minor}" == oldest_python()
    assert list_problems(VISIBLE, oldest) == []


# R270: an image, a PDF or a video is tracked only with a record that names it.

# The bytes with which a PNG file opens, which are not UTF-8.
PNG = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
RECORD = "docs/decisions/DR-001-an-image-that-a-page-shows.md"
MEDIA_PATHS = list(
    dict.fromkeys(
        f"docs/a.{form}"
        for extension in sorted(MEDIA)
        for form in (extension, extension.upper(), extension.capitalize())
    )
)
NOT_MEDIA_PATHS = [
    "docs/a.png.md",
    "docs/a.pngs",
    "docs/svg",
    "docs/png/a.md",
    "docs/v1.png/notes",
    "tools/a.ts",
    "tools/a.dot",
]


def listing(
    root: Path,
    files: Mapping[str, str | bytes],
    sentence: str = "The page shows `docs/diagram.png`.",
    status: str = "accepted",
) -> Path:
    """A repository that holds these files and an accepted record, DR-001, that says this
    sentence, or a record of another status."""
    text = decision_record(
        1,
        title="An image that a page shows",
        status=status,
        closed_by="DR-002" if status == "closed" else "none",
    ).replace("Something made a choice necessary.", sentence)
    return plant(root, {**files, RECORD: text})


def held_id(root: Path, path: str) -> str:
    """The object id that git's index holds for a path."""
    done = git(root, "rev-parse", f":{path}")
    done.check_returncode()
    return done.stdout.decode("ascii").strip()


@pytest.fixture(scope="module")
def planted_media(tmp_path_factory: pytest.TempPathFactory) -> list[str]:
    """What the check of images, PDFs and videos finds in a repository that holds a file by
    each of their extensions, in three cases, and files whose extensions are not theirs."""
    files = {path: "Planted.\n" for path in MEDIA_PATHS + NOT_MEDIA_PATHS}
    return exception_problems(plant(tmp_path_factory.mktemp("media"), files), ())


@pytest.mark.parametrize("path", MEDIA_PATHS)
def test_an_image_a_pdf_or_a_video_that_the_list_does_not_give_fails(
    planted_media: list[str], path: str
) -> None:
    assert f"{path}{UNLISTED}" in planted_media


def test_only_the_files_with_the_extension_of_an_image_a_pdf_or_a_video_are_named(
    planted_media: list[str],
) -> None:
    assert sorted(planted_media) == sorted(f"{path}{UNLISTED}" for path in MEDIA_PATHS)


def test_the_extensions_hold_each_that_python_gives_an_image_a_pdf_or_a_video() -> None:
    table = mimetypes.MimeTypes()
    known = {
        extension.lstrip(".")
        for strict in (True, False)
        for extension, kind in table.types_map[strict].items()
        if kind.startswith(("image/", "video/")) or kind == "application/pdf"
    }
    assert known
    assert sorted(known - MEDIA) == []


@pytest.mark.parametrize("path", ["docs/diagram.png", "docs/DIAGRAM.PDF", "docs/clip.Mp4"])
def test_a_file_that_the_list_gives_with_its_object_id_and_record_passes(
    tmp_path: Path, path: str
) -> None:
    root = listing(tmp_path, {path: PNG}, sentence=f"The page shows `{path}`.")
    exceptions = [Excepted(path, held_id(root, path), "DR-001")]
    assert exception_problems(root, exceptions) == []
    assert character_problems(root, exceptions) == []


def test_the_test_of_characters_passes_over_only_a_listed_file_that_is_not_utf_8(
    tmp_path: Path,
) -> None:
    root = listing(tmp_path, {"docs/diagram.png": PNG, "docs/other.png": PNG})
    exceptions = [Excepted("docs/diagram.png", held_id(root, "docs/diagram.png"), "DR-001")]
    assert character_problems(root, exceptions) == [
        "docs/other.png is not UTF-8, so the test cannot read it as text"
    ]


def test_a_listed_svg_is_still_read_by_the_test_of_characters(tmp_path: Path) -> None:
    svg = "<svg><text>a\u202eb</text></svg>\n"
    sentence = "The page shows `docs/diagram.svg`."
    root = listing(tmp_path, {"docs/diagram.svg": svg}, sentence=sentence)
    exceptions = [Excepted("docs/diagram.svg", held_id(root, "docs/diagram.svg"), "DR-001")]
    assert exception_problems(root, exceptions) == []
    assert character_problems(root, exceptions) == [
        f"docs/diagram.svg:1:13 holds U+202E RIGHT-TO-LEFT OVERRIDE{NOT_ASCII}"
    ]


def test_a_listed_file_whose_bytes_changed_fails_and_names_the_file_and_the_entry(
    tmp_path: Path,
) -> None:
    root = listing(tmp_path, {"docs/diagram.png": PNG})
    before = held_id(root, "docs/diagram.png")
    (root / "docs/diagram.png").write_bytes(PNG + b"\x00")
    git(root, "add", "docs/diagram.png").check_returncode()
    after = held_id(root, "docs/diagram.png")
    assert exception_problems(root, [Excepted("docs/diagram.png", before, "DR-001")]) == [
        f"docs/diagram.png is held by git as {after}, and the exception for docs/diagram.png"
        f" gives {before}"
    ]


class Listing(NamedTuple):
    """An exception and the repository that it is read in: an image that git tracks, listed
    with the object id that git holds for it and an accepted record that names its path in a
    code span, unless a case changes one of them."""

    files: Mapping[str, str | bytes] = {"docs/diagram.png": PNG}
    path: str = "docs/diagram.png"
    oid: str = "the object id that git holds"
    record: str = "DR-001"
    sentence: str = "The page shows `docs/diagram.png`."
    status: str = "accepted"


@pytest.mark.parametrize(
    ("case", "problem"),
    [
        (
            Listing(
                files={},
                path="docs/missing.png",
                oid="0" * 40,
                sentence="The page shows `docs/missing.png`.",
            ),
            "the exception for docs/missing.png gives a path that git does not track",
        ),
        (
            Listing(
                files={"docs/notes.txt": "Notes.\n"},
                path="docs/notes.txt",
                sentence="The page shows `docs/notes.txt`.",
            ),
            "the exception for docs/notes.txt gives a file that is not an image, a PDF or a"
            " video by its extension",
        ),
        (
            Listing(
                files={"docs/notes.txt": PNG},
                path="docs/notes.txt",
                sentence="The page shows `docs/notes.txt`.",
            ),
            "the exception for docs/notes.txt gives a file that is not an image, a PDF or a"
            " video by its extension",
        ),
        (Listing(oid=""), "the exception for docs/diagram.png gives no object id"),
        (Listing(oid="abc1234"), "the exception for docs/diagram.png gives no object id"),
        (
            Listing(record="DR-002"),
            "the exception for docs/diagram.png cites DR-002, which is no record",
        ),
        (
            Listing(status="closed"),
            "the exception for docs/diagram.png cites DR-001, which is closed, not accepted",
        ),
        (
            Listing(sentence="The page shows docs/diagram.png."),
            "the exception for docs/diagram.png cites DR-001, which names docs/diagram.png in"
            " no code span",
        ),
        (
            Listing(sentence="The page shows `docs/diagram.png.bak` and `docs/`."),
            "the exception for docs/diagram.png cites DR-001, which names docs/diagram.png in"
            " no code span",
        ),
    ],
)
def test_an_exception_out_of_its_form_fails_and_names_the_entry(
    tmp_path: Path, case: Listing, problem: str
) -> None:
    root = listing(tmp_path, case.files, sentence=case.sentence, status=case.status)
    oid = held_id(root, case.path) if case.oid == Listing().oid else case.oid
    assert exception_problems(root, [Excepted(case.path, oid, case.record)]) == [problem]


def test_an_exception_in_its_form_passes(tmp_path: Path) -> None:
    case = Listing()
    root = listing(tmp_path, case.files, sentence=case.sentence, status=case.status)
    assert exception_problems(root, [Excepted(case.path, held_id(root, case.path), "DR-001")]) == []


def test_a_listed_file_of_text_that_is_not_utf_8_is_still_refused_by_the_test_of_characters(
    tmp_path: Path,
) -> None:
    root = listing(tmp_path, {"docs/notes.txt": PNG}, sentence="It names `docs/notes.txt`.")
    exceptions = [Excepted("docs/notes.txt", held_id(root, "docs/notes.txt"), "DR-001")]
    assert character_problems(root, exceptions) == [
        "docs/notes.txt is not UTF-8, so the test cannot read it as text"
    ]


def test_a_check_of_images_that_reads_no_tracked_path_fails(tmp_path: Path) -> None:
    assert exception_problems(plant(tmp_path, {}), ()) == [MEDIA_READ_NOTHING]


# R273: the pages that this repository writes hold no text that GitHub hides.


def page(body: str) -> str:
    """A page whose third line starts this body."""
    return f"# A page\n\n{body}\n"


# Each mark of the first scenario, by the name of the page that plants it on its third line,
# with the text at whose start the problem is named and what the problem says it holds.
OUTSIDE_CODE = {
    "comment": ("A <!-- hidden --> word.", "<!--", COMMENT),
    "element": ("A <span>word.", "<span", f"the HTML element <span{SHOWN_OTHERWISE}"),
    "closing-element": ("A word.</div>", "</div", f"the HTML element </div{SHOWN_OTHERWISE}"),
    "fold-elsewhere": ("<details>", "<details", f"the HTML element <details{SHOWN_OTHERWISE}"),
    "declaration": ("<!DOCTYPE html>", "<!", f"a declaration{HIDES}"),
    "cdata": ("A <![CDATA[ hidden ]]> word.", "<![", f"a CDATA section{HIDES}"),
    "instruction": ("A <?php echo 1; ?> word.", "<?", f"a processing instruction{HIDES}"),
    "hexadecimal-reference": (
        "A &#x202E; word.",
        "&#x",
        f"the character reference &#x202E;{NAMES_CHARACTER}",
    ),
    "decimal-reference": (
        "A &#8238; word.",
        "&#",
        f"the character reference &#8238;{NAMES_CHARACTER}",
    ),
    "named-reference": ("A&nbsp;word.", "&", f"the character reference &nbsp;{NAMES_CHARACTER}"),
    "link-definition": ("[a]: https://example.com", "]:", DEFINITION),
    "footnote-definition": ("[^1]: A note.", "]:", DEFINITION),
    "image": ("An ![image](a.png) here.", "![", IMAGE),
    "double-quoted-title": ('A [link](a.md "A title") here.', "](", TITLE),
    "single-quoted-title": ("A [link](a.md 'A title') here.", "](", TITLE),
    "parenthesised-title": ("A [link](a.md (A title)) here.", "](", TITLE),
    "title-after-brackets": ('A [link](<a.md> "A title") here.', "](", TITLE),
    "target-cut-by-the-line": ("A [link](a.md", "](", TITLE),
    "dollar": ("It costs $5.", "$", DOLLAR),
    "escaped-backtick": ("A \\`<!-- hidden -->\\` word.", "\\", BACKSLASHED),
}


@pytest.fixture(scope="module")
def planted_marks(tmp_path_factory: pytest.TempPathFactory) -> list[str]:
    """What the check of pages finds in a repository that plants each mark in a page."""
    files = {f"docs/{name}.md": page(line) for name, (line, _, _) in OUTSIDE_CODE.items()}
    return page_problems(plant(tmp_path_factory.mktemp("marks"), files))


@pytest.mark.parametrize("name", OUTSIDE_CODE)
def test_text_that_github_hides_in_a_page_fails(planted_marks: list[str], name: str) -> None:
    line, start, what = OUTSIDE_CODE[name]
    assert f"docs/{name}.md:3:{line.index(start) + 1} holds {what}" in planted_marks


def test_each_planted_mark_is_named_once_and_nothing_else_is(planted_marks: list[str]) -> None:
    assert len(planted_marks) == len(OUTSIDE_CODE)


def test_a_run_of_backticks_that_its_line_leaves_open_fails(tmp_path: Path) -> None:
    body = "A `run that a later line closes,\nand then` <!-- x --> `code`.\n\n```\na ` b\n```"
    root = plant(tmp_path, {"docs/a.md": page(body)})
    assert page_problems(root) == [
        f"docs/a.md:3:3 holds {OPEN_RUN}",
        f"docs/a.md:4:27 holds {OPEN_RUN}",
    ]


def test_a_table_row_with_more_cells_than_its_header_fails(tmp_path: Path) -> None:
    table = "| A | B |\n|---|:-:|\n| 1 | 2 |\n| 1 | 2 | hidden |\n3 | 4 | hidden\n"
    root = plant(tmp_path, {"docs/table.md": page(table)})
    row = "a table row of 3 cells under a header of 2, whose cells past the header's GitHub hides"
    assert page_problems(root) == [f"docs/table.md:6 holds {row}", f"docs/table.md:7 holds {row}"]


@pytest.mark.parametrize(
    "table",
    [
        "| A | B |\n|---|---|\n| 1 | 2 |\n| 1 |\n| 1 \\| 2 | 3 |\n",
        "A | B\n--|--\n1 | 2\n",
        "> | A |\n> |---|\n> | 1 |\n",
        "| A |\n\n| 1 | 2 |\n",
        "| A | B |\n|---|---|\n```\n| 1 | 2 | 3 |\n```\n",
    ],
)
def test_a_table_whose_rows_hold_no_more_cells_than_its_header_passes(
    tmp_path: Path, table: str
) -> None:
    assert page_problems(plant(tmp_path, {"docs/table.md": page(table)})) == []


def test_a_table_row_in_a_quote_is_read_as_github_reads_it(tmp_path: Path) -> None:
    table = "> | A |\n> |---|\n> | 1 | hidden |\n"
    root = plant(tmp_path, {"docs/table.md": page(table)})
    assert page_problems(root) == [
        "docs/table.md:5 holds a table row of 2 cells under a header of 1, whose cells past the"
        " header's GitHub hides"
    ]


DRAWN_BLOCKS = [
    ("```math\nx^2\n```", "docs/a.md:3 holds a fenced block that GitHub draws as math"),
    ("~~~ MATH\nx^2\n~~~", "docs/a.md:3 holds a fenced block that GitHub draws as math"),
    ("```geojson\n{}\n```", "docs/a.md:3 holds a fenced block that GitHub draws as geojson"),
    ("```topojson\n{}\n```", "docs/a.md:3 holds a fenced block that GitHub draws as topojson"),
    ("```stl\nsolid a\n```", "docs/a.md:3 holds a fenced block that GitHub draws as stl"),
    ('```python title="hidden"\nx = 1\n```', f"docs/a.md:3 holds {INFO}"),
    ("```python<!--hidden-->\nx = 1\n```", f"docs/a.md:3 holds {INFO}"),
    (
        "```mermaid\nflowchart LR\n  A[#8238;] --> B\n```",
        f"docs/a.md:5:5 holds the entity code #8238;{IN_MERMAID}, which the drawing shows as the"
        " character that it names",
    ),
    (
        "```mermaid\nflowchart LR\n  A[#quot;] --> B\n```",
        f"docs/a.md:5:5 holds the entity code #quot;{IN_MERMAID}, which the drawing shows as the"
        " character that it names",
    ),
    (
        "```mermaid\nflowchart LR\n  %% hidden\n  A --> B\n```",
        f"docs/a.md:5:3 holds %%{IN_MERMAID}, which starts a comment or a directive that the"
        " drawing hides",
    ),
    (
        "```mermaid\n%%{init: {}}%%\nflowchart LR\n```",
        f"docs/a.md:4:1 holds %%{IN_MERMAID}, which starts a comment or a directive that the"
        " drawing hides",
    ),
    (
        "```mermaid\nflowchart LR\n  A[<span>x] --> B\n```",
        f"docs/a.md:5:5 holds the HTML element <span{IN_MERMAID}{SHOWN_OTHERWISE}",
    ),
    (
        "```mermaid\nflowchart LR\n  A[<https://example.com>] --> B\n```",
        f"docs/a.md:5:5 holds the HTML element <https{IN_MERMAID}{SHOWN_OTHERWISE}",
    ),
    (
        "```mermaid\nflowchart LR\n  A[<!-- x -->] --> B\n```",
        f"docs/a.md:5:5 holds {COMMENT.replace(', which', IN_MERMAID + ', which')}",
    ),
    (
        "```mermaid\n---\nconfig:\n  theme: dark\n---\nflowchart LR\n```",
        f"docs/a.md:4:1 holds front matter{IN_MERMAID}{MERMAID_HIDES}",
    ),
    *(
        (
            f"```mermaid\nflowchart LR\n  {statement}\n  A --> B\n```",
            f"docs/a.md:5:3 holds {statement.split()[0].rstrip(':')}{IN_MERMAID}{MERMAID_HIDES}",
        )
        for statement in (
            "accTitle: hidden",
            "accDescr: hidden",
            'click A "https://example.com" "hidden"',
            "style A color:#fff",
            "classDef hidden display:none",
            "linkStyle 0 stroke:#fff",
        )
    ),
]


@pytest.mark.parametrize(("block", "problem"), DRAWN_BLOCKS)
def test_a_drawn_block_that_can_hide_text_fails(tmp_path: Path, block: str, problem: str) -> None:
    assert page_problems(plant(tmp_path, {"docs/a.md": page(block)})) == [problem]


def test_a_mermaid_block_in_plain_text_passes(tmp_path: Path) -> None:
    block = "```mermaid\nflowchart LR\n  A[The tool, in #1 place] -->|reads| B[A file]\n```"
    assert page_problems(plant(tmp_path, {"docs/a.md": page(block)})) == []


IN_CODE = [
    "Inline `<!-- x -->`, `<span>`, `&#x202E;`, `[a]: b`, `![a](b)`, `$5` and `a\\`.",
    "Inline ``a ` <!-- x --> b``.",
    "```\n<!-- x -->\n<span>&#x202E; $5\n[a]: b\n```",
    "~~~text\n<!-- x -->\n| A |\n|---|\n| 1 | 2 |\n~~~",
    "- ```sh\n  echo '<!-- x -->'\n  ```",
    "An autolink, <https://example.com/a?b=1>, and another, <someone@example.com>.",
    "a < b, 1<2, <-, <= and <3 show as written, as do R&D, &c and &NotAnEntity;.",
    "A [link](a.md), [another](<a b.md>) and [a third](a_(b).md) give no title.",
    "An escaped backslash before code, \\\\`code`, reads as GitHub reads it.",
]


@pytest.mark.parametrize("body", IN_CODE)
def test_those_marks_in_code_or_that_github_shows_as_written_pass(
    tmp_path: Path, body: str
) -> None:
    assert page_problems(plant(tmp_path, {"docs/a.md": page(body)})) == []


TEMPLATES = (
    ".github/pull_request_template.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/PULL_REQUEST_TEMPLATE/change.md",
    ".github/ISSUE_TEMPLATE/feature_request.md",
    ".github/DISCUSSION_TEMPLATE/idea.md",
)


@pytest.mark.parametrize("path", TEMPLATES)
def test_a_template_s_comment_passes(tmp_path: Path, path: str) -> None:
    text = "## Before and after\n\n<!-- What a reader sees now. -->\n\n<!--\nTwo lines.\n-->\n"
    assert page_problems(plant(tmp_path, {path: text})) == []


@pytest.mark.parametrize(
    ("path", "text", "problem"),
    [
        (
            ".github/pull_request_template.md",
            "<!--\n```\n-->\n<span>hidden\n",
            f".github/pull_request_template.md:4:1 holds the HTML element <span{SHOWN_OTHERWISE}",
        ),
        (
            ".github/pull_request_template.md",
            "<!-- A comment. --> <span>hidden\n",
            f".github/pull_request_template.md:1:21 holds the HTML element <span{SHOWN_OTHERWISE}",
        ),
        (
            ".github/pull_request_template.md",
            "Text.\n\n<!-- A comment that never closes.\n",
            f".github/pull_request_template.md:3:1 holds {NEVER_ENDS}",
        ),
        (
            ".github/pull_request_template.md",
            "A &#x202E; word.\n",
            ".github/pull_request_template.md:1:3 holds the character reference &#x202E;"
            f"{NAMES_CHARACTER}",
        ),
        (
            ".github/CONTRIBUTING.md",
            "<!-- hidden -->\n",
            f".github/CONTRIBUTING.md:1:1 holds {COMMENT}",
        ),
        (
            "docs/pull_request_template.md",
            "<!-- x -->\n",
            f"docs/pull_request_template.md:1:1 holds {COMMENT}",
        ),
    ],
)
def test_a_template_holds_only_comments_and_no_other_page_holds_one(
    tmp_path: Path, path: str, text: str, problem: str
) -> None:
    assert page_problems(plant(tmp_path, {path: text})) == [problem]


FOLDED = (
    "## Adopt the tool\n\n<details>\n<summary>Adopt the tool</summary>\n\nText.\n\n</details>\n"
)


def test_the_readme_s_folds_pass(tmp_path: Path) -> None:
    assert page_problems(plant(tmp_path, {"README.md": FOLDED})) == []


@pytest.mark.parametrize(
    ("path", "text", "problems"),
    [
        (
            "docs/page.md",
            FOLDED,
            [(3, 1, "<details"), (4, 1, "<summary"), (4, 24, "</summary"), (8, 1, "</details")],
        ),
        (
            "docs/README.md",
            FOLDED,
            [(3, 1, "<details"), (4, 1, "<summary"), (4, 24, "</summary"), (8, 1, "</details")],
        ),
        ("README.md", FOLDED.replace("<details>", "<details open>"), [(3, 1, "<details")]),
        ("README.md", FOLDED.replace("<summary>", '<summary class="a">'), [(4, 1, "<summary")]),
        ("README.md", FOLDED.replace("<details>", "<DETAILS>"), [(3, 1, "<DETAILS")]),
    ],
)
def test_a_fold_with_an_attribute_or_in_another_page_fails(
    tmp_path: Path, path: str, text: str, problems: list[tuple[int, int, str]]
) -> None:
    assert page_problems(plant(tmp_path, {path: text})) == [
        f"{path}:{line}:{column} holds the HTML element {tag}{SHOWN_OTHERWISE}"
        for line, column, tag in problems
    ]


# A line that GitHub reads as raw HTML, from a fold of the README up to a blank line or after
# a template's comment on the line where it closes, where a backtick or a run of tildes opens
# no code, by the page that plants it, its text and what the test says.
RAW_HTML_LINES = [
    (
        "README.md",
        "<details>\n<summary>`<!-- x -->`</summary>\n\nText.\n\n</details>\n",
        f"README.md:2:10 holds a backtick{OPENS_NO_CODE}",
    ),
    (
        "README.md",
        "<details>\n```\n\n<!-- x -->\n```\n",
        f"README.md:2:1 holds a backtick{OPENS_NO_CODE}",
    ),
    (
        "README.md",
        "<details>\n<summary>A</summary>\n~~~\n\n<!-- x -->\n~~~\n",
        f"README.md:3:1 holds a run of tildes{OPENS_NO_CODE}",
    ),
    (
        ".github/pull_request_template.md",
        "<!-- A comment. --> `&#x202E;`\n",
        f".github/pull_request_template.md:1:21 holds a backtick{OPENS_NO_CODE}",
    ),
]


@pytest.mark.parametrize(("path", "text", "problem"), RAW_HTML_LINES)
def test_code_on_a_line_that_github_reads_as_raw_html_fails(
    tmp_path: Path, path: str, text: str, problem: str
) -> None:
    assert page_problems(plant(tmp_path, {path: text})) == [problem]


@pytest.mark.parametrize(
    ("path", "text"),
    [
        (".github/pull_request_template.md", "Fill in `this` <!-- A comment. --> and `that`.\n"),
        ("README.md", FOLDED.replace("Text.", "Text and `code`.")),
        ("README.md", "```\n<details>\n`x`\n```\n"),
    ],
)
def test_code_after_a_comment_within_a_line_after_a_fold_s_blank_line_or_in_code_passes(
    tmp_path: Path, path: str, text: str
) -> None:
    assert page_problems(plant(tmp_path, {path: text})) == []


def test_a_page_that_others_write_or_a_file_that_is_no_page_is_not_read(tmp_path: Path) -> None:
    files = {
        "vendor/superpowers/skills/a/SKILL.md": "<!-- x -->\n",
        ".claude/skills/openspec-a/SKILL.md": "<!-- x -->\n",
        "docs/notes.txt": "<!-- x -->\n",
        "docs/page.md": "Text.\n",
    }
    assert page_problems(plant(tmp_path, files)) == []


@pytest.mark.parametrize("path", ["docs/page.markdown", "docs/page.MD", "docs/page.mdx"])
def test_every_file_that_github_shows_as_markdown_is_read(tmp_path: Path, path: str) -> None:
    assert page_problems(plant(tmp_path, {path: "<!-- x -->\n"})) == [f"{path}:1:1 holds {COMMENT}"]


def test_a_mark_that_only_git_s_index_or_only_the_working_tree_holds_fails(tmp_path: Path) -> None:
    root = plant(tmp_path, {"docs/a.md": "A <!-- x --> word.\n", "docs/b.md": "A word.\n"})
    (root / "docs/a.md").write_text("A word.\n", encoding="utf-8")
    (root / "docs/b.md").write_text("A $5 word.\n", encoding="utf-8")
    assert page_problems(root) == [
        f"docs/a.md:1:3{IN_INDEX} holds {COMMENT}",
        f"docs/b.md:1:3{IN_TREE} holds {DOLLAR}",
    ]


@pytest.mark.parametrize(
    ("body", "problem"),
    [
        (
            "```\ncode\n",
            "docs/a.md:3: a fenced code block opens here and never closes, so the lines after it"
            " were not read",
        ),
        (
            "Text.\n\n  ```\n code\n  ```\n",
            "docs/a.md:6: GitHub reads this line in the fence that opens on line 5 or after it",
        ),
    ],
)
def test_a_page_whose_code_the_test_cannot_tell_fails(
    tmp_path: Path, body: str, problem: str
) -> None:
    problems = page_problems(plant(tmp_path, {"docs/a.md": page(body)}))
    assert [found[: len(problem)] for found in problems] == [problem]


def test_a_version_that_is_no_file_of_utf_8_text_is_left_to_the_test_of_characters(
    tmp_path: Path,
) -> None:
    root = plant(tmp_path, {"docs/a.md": b"\xff<!-- x -->\n", "docs/b.md": "A <!-- x --> word.\n"})
    (root / "docs/b.md").unlink()
    (root / "docs/b.md").symlink_to("a.md")
    git(
        root, "update-index", "--add", "--cacheinfo", f"{FILE},{'1' * 40},docs/gone.md"
    ).check_returncode()
    assert page_problems(root) == [f"docs/b.md:1:3{IN_INDEX} holds {COMMENT}"]
    assert character_problems(root) == [
        "docs/a.md is not UTF-8, so the test cannot read it as text",
        "docs/gone.md names an object that this clone lacks, as a partial clone does, which the"
        " test does not fetch",
    ]


def test_a_check_of_pages_that_reads_no_page_fails(tmp_path: Path) -> None:
    root = plant(tmp_path, {"docs/notes.txt": "Text.\n", "vendor/superpowers/a.md": "Text.\n"})
    assert page_problems(root) == [PAGES_READ_NOTHING]


@pytest.mark.parametrize(
    ("text", "blocks", "stopped"),
    [
        ("```py\na\n\n```\nb\n", [Block(1, "py", (2, 3), 4)], []),
        ("~~~ text more\na\n", [Block(1, "text more", (2, 3), None)], [1]),
        ("- ```\n  a\nb\n```\n", [Block(1, "", (2,), None), Block(4, "", (5,), None)], [4]),
        ("Text.\n\n  ```\n code\n", [Block(3, "", (), None)], [4]),
        ("No code.\n", [], []),
    ],
)
def test_the_reading_gives_each_fenced_block_s_lines_and_info_string(
    text: str, blocks: list[Block], stopped: list[int]
) -> None:
    _, stops, found = reading(text)
    assert found == blocks
    assert [line for line, _ in stops] == stopped


# The definitions that the tests share.


@pytest.mark.parametrize(
    ("path", "folder"),
    [
        ("vendor/superpowers/skills/a/SKILL.md", "vendor/superpowers/"),
        ("vendor/superpowers/LICENSE", "vendor/superpowers/"),
        ("vendor/superpowers/UPSTREAM.lock", ""),
        ("vendor/superpowers/UPSTREAM.lock/SKILL.md", "vendor/superpowers/"),
        ("vendor/superpowers/skills/UPSTREAM.lock", "vendor/superpowers/"),
        (".claude/skills/openspec-explore/SKILL.md", ".claude/skills/openspec-explore/"),
        (".claude/skills/a/SKILL.md", ""),
        (".claude/skills/openspec-explore", ""),
        ("vendor/other/SKILL.md", ""),
        ("vendor/superpowersx/SKILL.md", ""),
        ("docs/vendor/superpowers/a.md", ""),
    ],
)
def test_others_write_the_vendored_copy_but_its_lock_and_the_generated_skills(
    path: str, folder: str
) -> None:
    assert written_by_others(path) == folder


def test_a_character_is_named_by_its_code_point_and_its_unicode_name() -> None:
    assert named("\u202e") == "U+202E RIGHT-TO-LEFT OVERRIDE"
    assert named("\U000e0041") == "U+E0041 TAG LATIN CAPITAL LETTER A"


@pytest.mark.parametrize("character", ["\t", "\r", "\x1b", "\ue000", "\u0378", "\ud800"])
def test_a_character_without_a_name_is_named_by_its_code_point_and_a_fixed_phrase(
    character: str,
) -> None:
    assert named(character) == f"U+{ord(character):04X} (no name in Python's Unicode database)"


def test_a_path_is_shown_with_each_other_character_by_its_code_point() -> None:
    assert shown_path("a b\n\u202e\U000e0041/\udcff~!") == "aU+0020bU+000AU+202EU+E0041/\\xFF~!"


def test_text_is_shown_with_each_character_beyond_printable_ascii_by_its_code_point() -> None:
    assert shown("a b\t\u2014~") == "a bU+0009U+2014~"


# R272: everything that the test prints is printable ASCII.

PLANTED_TEST = """from pathlib import Path

from test_conventions import character_problems, page_problems


def test_the_planted_tree():
    assert not character_problems(Path({root!r}))


def test_the_planted_pages():
    assert not page_problems(Path({root!r}))
"""


def test_everything_that_a_failing_run_of_the_test_of_characters_prints_is_printable_ascii(
    tmp_path: Path,
) -> None:
    files = {
        "line\nfeed.md": "Printable.\n",
        "carriage\rreturn.md": "Printable.\n",
        "escape\x1b[2Jcharacter.md": "Printable.\n",
        "tag\U000e0069\U000e0067.md": "A <!-- x --> word.\n",
        "selector\ufe0f.md": "Printable.\n",
        "page.md": "ab\u202ecd\x07\ue000\u0378\n",
        "vendor/superpowers/a.md": "\U000e0041\ufe0f\n",
    }
    planted = plant(tmp_path / "planted", files, links={"link.md": "to\u202e\U000e0041\n\x1b.md"})
    test = tmp_path / "test_planted.py"
    test.write_text(PLANTED_TEST.format(root=str(planted)), encoding="ascii")
    done = subprocess.run(
        [sys.executable, "-m", "pytest", "-p", "no:cacheprovider", "--color=no", "-vv", str(test)],
        cwd=tmp_path,
        capture_output=True,
        env={
            **session_free_environment(),
            "PYTHONPATH": os.pathsep.join(str(ROOT / folder) for folder in ("tests", "scripts")),
        },
    )
    printed = done.stdout + done.stderr
    assert done.returncode == 1, printed.decode("ascii", "backslashreplace")
    assert b"U+202E RIGHT-TO-LEFT OVERRIDE" in printed
    assert b"U+E0069" in printed and b"U+000A" in printed and b"U+001B" in printed
    assert b"tagU+E0069U+E0067.md:1:3 holds an HTML comment" in printed
    beyond = sorted({byte for byte in printed if not 0x20 <= byte <= 0x7E and byte != 0x0A})
    assert not beyond, f"the run printed the bytes {beyond}"


# The repository itself.


def test_every_tracked_file_holds_only_the_characters_that_its_writer_may_use() -> None:
    assert character_problems(ROOT) == []


def test_every_image_a_pdf_or_a_video_is_tracked_only_with_its_record() -> None:
    assert exception_problems(ROOT, EXCEPTIONS) == []


def test_every_page_that_this_repository_writes_holds_only_text_that_github_shows() -> None:
    assert page_problems(ROOT) == []
