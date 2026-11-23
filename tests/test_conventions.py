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

The repository's attributes give a tracked file no attribute but `text` and `eol`, read as
git's index holds them and as the working tree holds them, in a git folder of the check's
own, with no person's own attributes, so that a clone's `.git/info/attributes` or a global
attributes file is not read as the repository's, and an attributes file that a checkout
re-encodes still fails (R274, DR-280).

`pyproject.toml` selects ruff's naming rules, `N`, whole, by `N` or `ALL`, and ignores none
of them, by a code, a prefix of one, `ALL` or a rule's name, for every file or for some, in
its table `lint` or in the table above it, whose settings of the rules ruff still reads, and
takes no setting from another file. Every Python file that this repository writes, by its
extension or by a first line that runs Python, passes those rules when ruff runs them with
no configuration, no `noqa` comment and no ignore file, each file given by its path, so that
no folder, setting or ignore file leaves one out; each problem names the file, the line and
the rule, and a run that fails, warns or contradicts its exit status passes nothing (R271,
DR-277).

The repository's attributes give every tracked file `text=auto` and `eol=lf`, read as the
test of attributes reads them, so that a checkout writes line feeds whatever `core.autocrlf`
says. Each check here that reads a file's bytes from the working tree takes them through
`staged_bytes` of `scripts/conventions.py`, which reads each carriage return right before a
line feed as a line feed, as git stages a text file, in every file but a script, a file
whose name ends in `.sh`, that starts with `#!` or that git records as executable. A
carriage return that git's index holds, one that no line feed follows and any in a script
still fail, and one in a script's working tree that git's index does not hold is named with
the way back: to stage the script as git normalizes it, delete it, check it out again and
unstage it, which keeps an edit not yet staged, or to clone the repository again. CI's job
`windows-line-endings` runs every check on the files that this repository writes, but its
scripts, saved with Windows line endings, and the job `ci`, for which a merge waits, needs
every job, none of which, and no step of which, a condition skips or lets fail (R276,
DR-281, DR-283).

Each check is shown to fail on a git repository into which its defect is planted.
"""

from __future__ import annotations

import builtins
import codecs
import functools
import html.entities
import io
import json
import mimetypes
import os
import re
import shlex
import shutil
import subprocess
import sys
import tarfile
import tempfile
import tomllib
import unicodedata
from collections import defaultdict
from collections.abc import Callable, Iterable, Iterator, Mapping
from pathlib import Path, PurePosixPath
from typing import Any, NamedTuple

import conventions
import pytest
import yaml
from conventions import (
    EXECUTABLE,
    FILE,
    NO_WINDOWS_LINE_ENDINGS,
    UNOPENED,
    Entry,
    in_working_tree,
    is_script,
    named,
    read_staged,
    recorded_executable,
    shown,
    shown_path,
    staged_bytes,
    written_by_others,
)
from test_decisions import (
    AUTHOR,
    CODE_SPAN,
    attribute_problems,
    attribute_readings,
    records_of,
    repository_attributes,
)
from test_decisions import record as decision_record
from test_guide import reviewed
from test_repository import load_workflow, oldest_python, pyproject
from test_roadmap import (
    isolated_environment,
    saved_with_windows_line_endings,
    session_free_environment,
)
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

# An escape that writes a character by its code, as JSON, JavaScript, YAML and bash allow
# it, the last with fewer digits too, or by its name, as Python allows it (T263).
ESCAPE = re.compile(
    r"\\(?:u\{([0-9A-Fa-f]+)\}|u([0-9A-Fa-f]{1,4})|U([0-9A-Fa-f]{1,8})|x([0-9A-Fa-f]{1,2})"
    r"|N\{([^{}\n]*)\})"
)
# PEP 263's declaration of a source file's encoding, which Python reads on either of its
# first two lines.
CODING = re.compile(r"^[ \t\f]*#.*?coding[:=][ \t]*([-\w.]+)")
PYTHON_FILE = re.compile(r"\.py[iw]?\Z", re.IGNORECASE)
PYTHON_LINE = re.compile(r"#!.*python")

# The modes with which git's index tracks a link and a submodule.
LINK, GITLINK = "120000", "160000"
IN_INDEX = ", in git's index,"
IN_TREE = ", in the working tree,"
NOT_ASCII = ", which is not printable ASCII"
NOT_LISTED = ", which the list does not give; the owner decides whether it does"
# The files that a loader decodes, by the extension that names their format in any case, and
# what the test says of one that its loader cannot read (R268).
LOADERS = {".json": "JSON", ".toml": "TOML", ".yaml": "YAML", ".yml": "YAML"}
UNLOADED = " is not {} that the test can read, so the test cannot read its strings"
NEVER_LISTED = (
    ", which the list does not give and may not, since it gives only punctuation and symbols"
    " that show"
)
MARKDOWN_ALONE = ", which the list gives for Markdown alone"
READ_NOTHING = "the test of characters read no tracked file"
# What the test of characters says of a script whose working tree holds a carriage return
# that git's index does not, as one in a clone made before the attributes does (R276, T267).
CHECK_OUT_AGAIN = (
    " is a script that holds a carriage return, which bash or the system reads as part of "
    "its line: stage it as git normalizes it, delete it, check it out again and unstage it,"
    " which keeps an edit, or clone the repository again, as CONTRIBUTING.md says"
)


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
# A link's destination that angle brackets hold, which is no raw HTML, and the text before a
# link's `](` where the link has none: an opening bracket that no backslash escapes, and
# nothing but spaces and tabs after it.
ANGLE = re.compile(r"<[^<>\n]*>")
EMPTY_TEXT = re.compile(r"(?:^|[^\\])(?:\\\\)*\[[ \t]*\Z")
# The extensions that GitHub's language list, Linguist, gives the languages that GitHub's
# markup library renders other than as Markdown, as its `languages.yml` and the library's
# `markups.rb` gave them on 2026-11-23 (R273).
OTHER_MARKUPS = re.compile(
    r"\.(?:textile|rdoc|org|creole|mediawiki|wiki|wikitext|re?st(?:\.txt)?|asciidoc|adoc|asc"
    r"|pod6?)\Z",
    re.IGNORECASE,
)
# The Emacs and the Vim modeline with which Linguist gives a file the language that it names
# ahead of the file's name, as its `modeline.rb` wrote them on 2026-11-23, the lines at a
# file's start and at its end where it looks for one, and what it takes to end a line (R273).
EMACS_MODELINE = re.compile(
    r"-\*-(?:[ \t]*(?=[^:;\s]+[ \t]*-\*-)|(?:.*?[ \t;]|(?<=-\*-))[ \t]*mode[ \t]*:[ \t]*)"
    r"([^:;\s]+)(?=[ \t;]|(?<![-*])-\*-).*?-\*-",
    re.IGNORECASE | re.ASCII,
)
VIM_MODELINE = re.compile(
    r"(?:(?:^|[ \t])(?:vi|Vi(?=m))(?:m[<=>]?[0-9]+|m)?|[ \t]ex)"
    r"(?=:(?=[ \t]*set?[ \t][^\r\n:]+:)|:(?![ \t]*set?[ \t]))"
    r"(?:(?:[ \t]*:[ \t]*|[ \t])\w*(?:[ \t]*=(?:[^\\\s]|\\.)*)?)*"
    r"[ \t:](?:filetype|ft|syntax)[ \t]*=(\w+)(?=$|\s|:)",
    re.ASCII,
)
MODELINE_LINES = 5
LINE_BREAK = re.compile(r"\r\n|\r|\n")
# What the reading takes to open code, and GitHub, on a line that it reads as raw HTML, not.
RAW_CODE = re.compile(r"`|~{3,}")
TAG = re.compile(r"</?[A-Za-z][A-Za-z0-9-]*")
DECLARATION = re.compile(r"<![A-Za-z]")
REFERENCE = re.compile(r"&(?:#[0-9]{1,7}|#[Xx][0-9A-Fa-f]{1,6}|([A-Za-z][A-Za-z0-9]*));")
ESCAPED_BACKTICK = re.compile(r"(?<!\\)(?:\\\\)*\\`")
# An opening bracket that no backslash escapes and that only spaces, tabs and a backslash
# follow to the end of its line, where it can open a link whose text is only a line break; a
# web address that GitHub links where it finds one, by its scheme or by `www.`, up to a space
# or a `<`; a definition's label, which GitHub reads before code, up to its `]:`; and the run
# that opens a fence (R273).
BRACKET_AT_END = re.compile(r"(?:^|[^\\])(?:\\\\)*(\[)[ \t]*\\?\Z")
WEB_ADDRESS_AT = re.compile(r"(?<![A-Za-z])(?i:https?|ftp)://[^\s<]*|(?<![^\s*_~(])www\.[^\s<]*")
LABEL = re.compile(r"\[(?:[^\\\[\]]|\\.)*\]:", re.DOTALL)
FENCE_RUN = re.compile(r"`{3,}|~{3,}")
# A row of a table's delimiter, and what may open a row inside a quote or a list item.
DELIMITER_CELL = re.compile(r"[ \t]*:?-+:?[ \t]*")
CONTAINER = re.compile(r"^(?:[ \t>]|(?:[-*+]|\d{1,9}[.)])[ \t])*")
# The diagrams whose comments and statements the check of Mermaid blocks reads, a flowchart,
# which `graph` also opens, and a sequence diagram, and the word that opens a diagram; what
# a block may not hold beside: an entity code, which it shows as the character that it
# names, a named character reference, which a browser reads with or without its `;`, shape
# data, and the statements, in any case and at a line's start or after a `;`, that give
# text that the drawing does not show or change how it shows what it does (R273).
MERMAID_TYPES = frozenset({"flowchart", "graph", "sequenceDiagram"})
MERMAID_TYPE = re.compile(r"[ \t]*([^ \t;]*)")
ENTITY_CODE = re.compile(r"#[A-Za-z0-9_]+;")
NAMED_REFERENCE = re.compile(r"&([A-Za-z][A-Za-z0-9]*;?)")
SHAPE = re.compile(r"@\{")
MERMAID_STATEMENT = re.compile(
    r"(?:^|;)[ \t]*(accTitle|accDescr|click|style|classDef|linkStyle|links?|callback)\b",
    re.IGNORECASE,
)

COMMENT = "an HTML comment, which GitHub hides"
HIDES = ", which GitHub hides"
SHOWN_OTHERWISE = ", which GitHub hides or shows otherwise"
NAMES_CHARACTER = ", which GitHub shows as the character that it names"
DEFINITION = "]:, which starts a link or footnote definition that GitHub hides"
IMAGE = "![, which starts an image that GitHub fetches and shows"
TITLE = "a link with a title, which GitHub shows only under a pointer"
NO_TEXT = "a link without text, which GitHub shows as nothing"
OTHER_MARKUP = (
    " is a page in a markup other than Markdown, which GitHub renders and the test of pages"
    " does not read"
)
DOLLAR = "$, with which GitHub starts a mathematical expression"
BACKSLASHED = (
    "a backtick that a backslash escapes, which GitHub shows as itself where the test would"
    " read code"
)
AUTOLINKED = (
    "an autolink that holds a backtick, which GitHub shows as a link where the test may read code"
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
QUOTED_FENCE = "a fence inside a quote, whose block the test does not read"
OPEN_BRACKET = (
    "an opening bracket that ends its line, which can open a link whose text is only a line"
    " break, which GitHub shows as nothing"
)
DESTINATION = (
    "a link whose destination holds a backtick, which GitHub reads as part of the link where"
    " the test may read code"
)
WEB_ADDRESS = (
    "a web address that holds a backtick, which GitHub shows as a link where the test may read code"
)
SPLIT_SPAN = (
    "a code span that holds a pipe that no backslash escapes, on a line of a table, whose cells"
    " GitHub splits before it reads code"
)
OTHER_DIAGRAM = (
    ", other than a flowchart or a sequence diagram, the two whose comments and statements the"
    " test reads"
)
HASH = ", which can start a comment that the drawing hides"
SHAPE_DATA = ", which opens shape data that can give an image or an icon or change how a node shows"
MODELINE = (
    "an Emacs or a Vim modeline, which can name a language in which GitHub renders the file"
    " otherwise than the test of pages reads it"
)
# The marks that fail wherever they stand on a line read as prose.
PLAIN = {"$": DOLLAR, "]:": DEFINITION, "![": IMAGE}
# The attributes that set line endings, the only ones that the repository may give (R274).
LINE_ENDINGS = frozenset({"text", "eol"})
OTHER_ATTRIBUTE = ", an attribute other than text and eol"
ATTRIBUTES_READ_NOTHING = "git lists no tracked file, so the test of attributes read nothing"
# The length from which git ignores a line of an attributes file, its line feed left out, and
# what the test of attributes says of such a line (R274).
LONG_LINE = 2048
LINE_IGNORED = " is a line of {} bytes, which git ignores, as it ignores each of 2048 or more"
# What the test of attributes says before each line that git warns while it reads them, as
# of a line that it ignores, which another reader of the attributes may not ignore.
WARNED = " while it reads the repository's attributes: "
# The line endings that the repository's attributes give every tracked file, so that a
# checkout writes line feeds whatever `core.autocrlf` says (R276).
LINE_FEEDS = {"text": "auto", "eol": "lf"}
NOT_LINE_FEEDS = ", not text=auto and eol=lf, with which a checkout writes line feeds"
LINE_FEEDS_READ_NOTHING = "git lists no tracked file, so the test of line endings read nothing"
# What Windows refuses in a name among printable ASCII, besides the slash that separates
# folders, the names that it keeps for devices, alone or before a dot and in any case, and the
# longest path that a clone on Windows, in a folder whose own path holds up to 100
# characters, can write (R277, DR-282).
REFUSED_BY_WINDOWS = '<>:"\\|?*'
DEVICES = (
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{digit}" for digit in range(10)),
    *(f"LPT{digit}" for digit in range(10)),
    "CONIN$",
    "CONOUT$",
)
LONGEST_PATH = 140
MEDIA_READ_NOTHING = (
    "git lists no tracked file, so the check of images, PDFs and videos read nothing"
)
# Where `pyproject.toml` gives which of ruff's rules ruff applies: the table `lint`, and the
# table above it, whose settings of the rules ruff 0.17 still reads, as deprecated. Ruff
# takes the `select` of `lint` over the other's and adds each `extend-select` (R271).
RUFF_TABLES = ("tool.ruff", "tool.ruff.lint")
IGNORING = ("ignore", "extend-ignore")
IGNORING_FOR_SOME = ("per-file-ignores", "extend-per-file-ignores")
NO_NAMING = "pyproject.toml selects no N, so ruff's naming rules do not run: "
IGNORES_NAMING = ", which ignores one of ruff's naming rules"
NAMES_READ_NOTHING = "the test of names read no Python file that this repository writes"
NAMES_UNREAD = "ruff's naming rules gave no reading that the test can trust: ruff exited "


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
    """Each path that git's index tracks, as `conventions.tracked_entries` reads it, with no
    global or system configuration."""
    return conventions.tracked_entries(root, isolated_environment(root))


def markdown_files(root: Path) -> set[str]:
    """The tracked paths that `scripts/wording.py` reads as Markdown."""
    done = git(root, "ls-files", "-z", "--", *MARKDOWN)
    done.check_returncode()
    return {path for path in done.stdout.decode("utf-8", "surrogateescape").split("\0") if path}


def blobs(root: Path, oids: Iterable[str]) -> dict[str, bytes | None]:
    """Each object's bytes, read through one `git cat-file --batch`, or None for one that
    this clone lacks. Git fetches none: in a partial clone, where it would fetch a missing
    object from the clone's remote, it stops at it instead, and the objects after it are
    read again. Git reads each object itself, not the one that a replace ref gives."""
    found: dict[str, bytes | None] = {}
    pending = list(dict.fromkeys(oids))
    while pending:
        done = git(
            root,
            "cat-file",
            "--batch",
            stdin="".join(f"{oid}\n" for oid in pending).encode("ascii"),
            extra={"GIT_NO_LAZY_FETCH": "1", "GIT_NO_REPLACE_OBJECTS": "1"},
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
        category = unicodedata.category(character)
        if category != "Cn" and (category[0] not in "PS" or ord(character) in BLANK):
            return NEVER_LISTED
        return NOT_LISTED
    return MARKDOWN_ALONE if entry.markdown_only and not markdown else ""


def escapes(line: str) -> Iterator[tuple[int, str, str]]:
    """Each character that an escape on the line writes, with its column and the character
    before it, so that a surrogate pair is read as the character that it writes and variation
    selector 16 as what follows the character before it, as a loader reads them."""
    runs: list[list[tuple[int, int]]] = []
    end = -1
    for found in ESCAPE.finditer(line):
        if found[5] is not None:
            try:
                written = unicodedata.lookup(found[5])
            except KeyError:
                continue
            if len(written) != 1:
                continue
            code = ord(written)
        else:
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


def front_matter_problems(
    path: str, text: str, where: str, markdown: bool, others: bool
) -> list[str]:
    """Each character that a page's front matter gives once YAML reads it and that the file
    may not hold, other than one that the file holds as itself, or, in a file that others
    write, by an escape there, which the reading of its lines names already. Front matter
    opens and closes on a line of `---` that spaces or tabs may follow, as Claude Code reads
    a skill's (R268, R269, T263)."""
    lines = text.split("\n")
    if lines[0].rstrip(" \t") != "---":
        return []
    name = shown_path(path)
    closing = next(
        (number for number in range(1, len(lines)) if lines[number].rstrip(" \t") == "---"), 0
    )
    if not closing:
        return [f"{name}{where} opens front matter that no line of --- closes"]
    body = "\n".join(lines[1:closing])
    try:
        document = yaml.compose(body, Loader=yaml.SafeLoader)
    except yaml.YAMLError:
        return [f"{name}{where} gives front matter that the test cannot read as YAML"]
    held = set(body)
    if others:
        held |= {character for line in lines[1:closing] for _, character, _ in escapes(line)}
    problems = []
    for node in scalars(document, set()):
        before = ""
        for character in str(node.value):
            reason = refused(character, before, others, markdown)
            if reason and character not in held:
                problems.append(
                    f"{name}:{node.start_mark.line + 2}{where} gives {named(character)} in its "
                    f"front matter, read as YAML{reason}"
                )
            before = character
    return problems


def strings_of(value: object) -> Iterator[str]:
    """Each string that a value that JSON or TOML gives holds, keys among them, in order."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from strings_of(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings_of(item)


def every_pair(pairs: list[tuple[str, object]]) -> list[object]:
    """A JSON object as each of its keys and values in turn, so that the value of a key that
    it gives again is read too, where a dict keeps only the last."""
    return [item for pair in pairs for item in pair]


def loaded_strings(kind: str, text: str) -> list[tuple[int, str]]:
    """Each string of a YAML, JSON or TOML file as its loader decodes it, keys among them,
    and every value of a key that JSON gives again, with its line where YAML gives one, and
    else 0."""
    if kind == "YAML":
        return [
            (node.start_mark.line + 1, str(node.value))
            for document in yaml.compose_all(text, Loader=yaml.SafeLoader)
            for node in scalars(document, set())
        ]
    value = (
        json.loads(text, object_pairs_hook=every_pair) if kind == "JSON" else tomllib.loads(text)
    )
    return [(0, string) for string in strings_of(value)]


def loaded_problems(path: str, text: str, where: str, others: bool) -> list[str]:
    """Each character that a YAML, JSON or TOML file gives once its loader reads it and that
    the file may not hold, as an escape writes one in a file of printable ASCII, other than
    one that the file holds as itself, or, in a file that others write, by an escape that the
    reading of its lines reads, which that reading names already; and the file where its
    loader cannot read it (R268, R269, T263, T271)."""
    kind = LOADERS.get(PurePosixPath(path).suffix.casefold())
    if kind is None:
        return []
    name = shown_path(path)
    try:
        strings = loaded_strings(kind, text)
    except (yaml.YAMLError, ValueError):
        return [f"{name}{where}{UNLOADED.format(kind)}"]
    held = set(text)
    if others:
        held |= {character for line in text.split("\n") for _, character, _ in escapes(line)}
    return [
        f"{name}{f':{line}' if line else ''}{where} gives {named(character)}, read as {kind}"
        f"{reason}"
        for line, value in strings
        for character in value
        if character not in held and (reason := refused(character, "", others, False))
    ]


def read_as_python(path: str, first_line: str) -> bool:
    """Whether Python reads a file as source, by its extension or by a first line that runs
    Python (R268, R271)."""
    return bool(PYTHON_FILE.search(path) or PYTHON_LINE.match(first_line))


def encoding_problems(path: str, text: str, where: str = "") -> list[str]:
    """The encoding that a file that Python reads as source declares, by its extension or by
    a first line that runs Python, on either of its first two lines, unless it is UTF-8
    (R268, T260)."""
    lines = text.split("\n")[:2]
    if not read_as_python(path, lines[0]):
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
    that an escape writes in a file that others write, each that YAML, JSON or TOML decodes
    from a file, each that the front matter of a page that this repository writes or of a
    skill gives, and the encoding that a file that this repository writes declares to
    Python."""
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
        problems += encoding_problems(path, text, where)
    problems += loaded_problems(path, text, where, others)
    if markdown and (not others or PurePosixPath(path).name.casefold() == "skill.md"):
        problems += front_matter_problems(path, text, where, markdown, others)
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
    if kind == "unreadable":
        return [f"{name}{where} {UNOPENED}"]
    if kind != "file":
        return [f"{name}{where} is neither a file nor a link, which the test cannot read"]
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        if entry.path in passed:
            return []
        return [f"{name}{where} is not UTF-8, so the test cannot read it as text"]
    return text_problems(entry.path, text, where, others, markdown)


def windows_problems(path: str) -> list[str]:
    """What Windows refuses in a tracked path or reads as another file's: each character that
    it refuses in a name, a `~`, which it writes in the short name that it gives a file or a
    folder, each part that ends in a dot, which it drops, or that is a name that it keeps for a
    device, alone or before a dot and in any case, and more than `LONGEST_PATH` characters,
    each named with the path (R277, DR-282)."""
    name = shown_path(path)
    problems = [
        f"the path {name} holds `{character}`, which Windows refuses in a name"
        for character in REFUSED_BY_WINDOWS
        if character in path
    ]
    if "~" in path:
        problems.append(
            f"the path {name} holds a `~`, which Windows writes in the short name that it gives "
            "a file or a folder"
        )
    for part in path.split("/"):
        if part.endswith("."):
            problems.append(
                f"the path {name} has the part {shown_path(part)}, which ends in a dot that "
                "Windows drops"
            )
        device = part.split(".")[0].upper()
        if device in DEVICES:
            problems.append(
                f"the path {name} has the part {shown_path(part)}, which Windows reads as the "
                f"device {device}"
            )
    if len(path) > LONGEST_PATH:
        problems.append(
            f"the path {name} holds {len(path)} characters, more than the {LONGEST_PATH} that a "
            "clone on Windows can write"
        )
    return problems


def path_problems(paths: Iterable[str]) -> list[str]:
    """Each tracked path that holds a character other than printable ASCII but the space,
    and each two paths, a path and a folder that holds another, or two folders, that differ
    only in the case of their letters, which a file system that ignores case holds as one, a
    folder named where its own name differs and not again in each folder that it holds
    (R268, T258)."""
    unique = sorted(set(paths))
    problems = [
        f"the path {shown_path(path)} holds a character other than printable ASCII but the space"
        for path in unique
        if not all("!" <= character <= "~" for character in path)
    ]
    for path in unique:
        problems += windows_problems(path)
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
    for spellings in folders.values():
        if len({folder.rpartition("/")[2] for folder in spellings}) > 1:
            problems.append(
                f"the folders {' and '.join(map(shown_path, sorted(spellings)))} differ only in "
                "case, which a file system that ignores case holds as one folder"
            )
    return problems


def versions(
    entry: Entry, index: tuple[str, bytes], tree: tuple[str, bytes] | None
) -> list[tuple[str, tuple[str, bytes]]]:
    """The versions of a tracked path that a check reads, each with the words that tell which
    it is: git's index's alone where the working tree holds the same, or the same once read
    as git stages it, or nothing, and else both, a file of the working tree as `staged_bytes`
    reads it (R272, R276)."""
    if tree is not None and tree != index and tree[0] == "file":
        tree = ("file", staged_bytes(entry.path, tree[1], entry.mode == EXECUTABLE))
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
        for where, (kind, data) in versions(entry, index, tree):
            problems += version_problems(entry, where, kind, data, others, page, passed)
        if (
            tree is not None
            and tree[0] == "file"
            and b"\r" in tree[1]
            and b"\r" not in indexed
            and is_script(entry.path, tree[1], entry.mode == EXECUTABLE)
        ):
            problems.append(f"{name}{IN_TREE}{CHECK_OUT_AGAIN}")
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
    destination since a title may start there, a link without text, other than an image's,
    which is named as an image, and an opening bracket that ends the line, which can open a
    link whose text is only a line break. Read on the raw line where its start lies outside
    code, since GitHub reads a link before code and the reading may pair the backtick with a
    later one: a link's destination that holds a backtick, which is named rather than a
    title, a backtick that a backslash escapes, which the reading takes to open or close
    code, and an autolink or a web address, other than in a destination, that holds a
    backtick (R273)."""
    found: list[tuple[int, str]] = []
    angles: set[int] = set()
    destinations: list[range] = []
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
            reach = destination(raw, at)[1]
            destinations.append(range(at + 2, reach))
            if "`" in raw[at + 2 : reach]:
                what = DESTINATION
            elif not seen[end:].lstrip(" \t").startswith(")"):
                what = TITLE
            elif EMPTY_TEXT.search(seen[:at]) and not seen[:at].rstrip(" \t").endswith("!["):
                what = NO_TEXT
        if what:
            found.append((at + 1, what))
    bracket = BRACKET_AT_END.search(seen)
    if bracket and not seen[: bracket.start(1)].endswith("!"):
        found.append((bracket.start(1) + 1, OPEN_BRACKET))
    found += [
        (escape.end() - 1, BACKSLASHED)
        for escape in ESCAPED_BACKTICK.finditer(raw)
        if seen[escape.end() - 2] == "\\"
    ]
    found += [
        (link.start() + 1, AUTOLINKED)
        for link in AUTOLINK.finditer(raw)
        if "`" in link.group() and seen[link.start()] == "<"
    ]
    found += [
        (address.start() + 1, WEB_ADDRESS)
        for address in WEB_ADDRESS_AT.finditer(raw)
        if "`" in address.group()
        and seen[address.start()] == raw[address.start()]
        and not any(address.start() in reached for reached in destinations)
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


def table_problems(lines: list[str], fenced: set[int]) -> list[tuple[int, int, str]]:
    """Each row of a table, by its line, that holds more cells than the table's header, whose
    cells past the header's GitHub hides, and each code span on a line of a table, by its
    line and column, that holds a pipe that no backslash escapes, since GitHub splits the
    line into cells before it reads code, while the reading takes what lies between the
    span's backticks for code (R273). A table is a line of cells and a line of delimiters with
    as many, outside code, and its rows run up to a blank line or a fence."""
    found: list[tuple[int, int, str]] = []
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
                        0,
                        f"a table row of {held} cells under a header of {len(header)}, whose"
                        " cells past the header's GitHub hides",
                    )
                )
            row += 1
        taken.update(range(number - 1, row))
        found += [
            (line, start + 1, SPLIT_SPAN)
            for line in range(number - 1, row)
            for start, end in code_spans(lines[line - 1])[0]
            if CELL_BORDER.search(lines[line - 1][start:end])
        ]
    return found


def mermaid_type(lines: list[str], held: list[int]) -> tuple[int, int, str] | None:
    """The diagram that a Mermaid block draws, where it is other than a flowchart or a
    sequence diagram, by the line and column of the word that opens it, the first line
    that is not blank, that opens with no `%` and that lies after the block's front matter,
    named as it is written (R273)."""
    rest = [number for number in held if lines[number - 1].strip(" \t")]
    if rest and lines[rest[0] - 1].strip(" \t") == "---":
        ends = [at for at, number in enumerate(rest) if lines[number - 1].strip(" \t") == "---"]
        rest = rest[ends[1] + 1 :] if len(ends) > 1 else []
    first = next(
        (number for number in rest if not lines[number - 1].lstrip(" \t").startswith("%")), None
    )
    if first is None:
        return None
    line = lines[first - 1]
    kind = MERMAID_TYPE.match(line)
    assert kind is not None
    if kind[1] in MERMAID_TYPES:
        return None
    word = line.split()[0]
    return (
        first,
        line.index(word) + 1,
        f"a Mermaid block that draws {shown(word)}{OTHER_DIAGRAM}",
    )


def read_reference(name: str) -> str:
    """The longest start of a name, its `;` among it, that HTML gives a character reference,
    as a browser reads the reference that opens with it, or nothing."""
    return next(
        (name[:end] for end in range(len(name), 0, -1) if name[:end] in html.entities.html5), ""
    )


def mermaid_problems(lines: list[str], block: Block) -> list[tuple[int, int, str]]:
    """What a Mermaid block holds that the drawing hides or shows otherwise, by its line and
    column: a diagram other than a flowchart or a sequence diagram, front matter and a
    statement, either of which gives text that the drawing does not show or changes how it
    shows it, each `#`, as the entity code that it opens or as one that can open a comment,
    the first `%` of a line, which opens a comment or a directive that can hide the rest of
    the line, a named character reference, shape data, and raw HTML, an autolink among it
    (R273)."""
    found: list[tuple[int, int, str]] = []
    first = next((number for number in block.held if lines[number - 1].strip(" \t")), None)
    if first is not None and lines[first - 1].strip(" \t") == "---":
        column = lines[first - 1].index("-") + 1
        found.append((first, column, f"front matter{IN_MERMAID}{MERMAID_HIDES}"))
    kind = mermaid_type(lines, list(block.held))
    if kind:
        found.append(kind)
    for number in block.held:
        line = lines[number - 1]
        found += [
            (number, statement.start(1) + 1, f"{statement[1]}{IN_MERMAID}{MERMAID_HIDES}")
            for statement in MERMAID_STATEMENT.finditer(line)
        ]
        for mark in re.finditer("#", line):
            code = ENTITY_CODE.match(line, mark.start())
            what = (
                f"the entity code {shown(code.group())}{IN_MERMAID}{ENTITY_NAMES}"
                if code
                else f"#{IN_MERMAID}{HASH}"
            )
            found.append((number, mark.start() + 1, what))
        comment = line.find("%")
        if comment >= 0:
            sign = "%%" if line.startswith("%%", comment) else "%"
            found.append((number, comment + 1, f"{sign}{IN_MERMAID}{DIRECTIVE}"))
        for reference in NAMED_REFERENCE.finditer(line):
            read = read_reference(reference[1])
            if read:
                found.append(
                    (
                        number,
                        reference.start() + 1,
                        f"the character reference {shown('&' + read)}{IN_MERMAID}{ENTITY_NAMES}",
                    )
                )
        found += [
            (number, data.start() + 1, f"@{{{IN_MERMAID}{SHAPE_DATA}")
            for data in SHAPE.finditer(line)
        ]
        for opening in re.finditer("<", line):
            element = markup(line, opening.start(), folds=False, autolinks=False)
            if element:
                found.append((number, opening.start() + 1, f"{element[0]}{IN_MERMAID}{element[1]}"))
    return found


def quoted_fences(lines: list[str], passed: set[int]) -> list[tuple[int, int, str]]:
    """Each run that would open or close a fence after the marks of a quote, by its line and
    column, on a line that it is not passed, such as one of the reading's fenced blocks or
    one that GitHub reads as raw HTML, where the check of raw HTML names the run: GitHub
    opens a fenced block inside a quote, and may draw it, while the reading takes no fence
    after a quote's mark and reads the block's lines as prose, so that the test cannot read
    it as a block (R273, T90)."""
    found: list[tuple[int, int, str]] = []
    for number, line in enumerate(lines, 1):
        marks = CONTAINER.match(line)
        assert marks is not None
        if number not in passed and ">" in marks.group() and FENCE_RUN.match(line, marks.end()):
            found.append((number, marks.end() + 1, QUOTED_FENCE))
    return found


def definition_problems(
    lines: list[str], view: list[str], fenced: set[int]
) -> list[tuple[int, int, str]]:
    """Each link or footnote definition that the reading hides, by the line and column of its
    `]:`, whose label opens a line's text after the marks of quotes and list items, read on
    the raw lines of its paragraph as GitHub reads a definition, before code, so that a
    backtick in its label opens no code span (R273)."""
    found: list[tuple[int, int, str]] = []
    for number, line in enumerate(lines, 1):
        marks = CONTAINER.match(line)
        assert marks is not None
        if number in fenced or not line.startswith("[", marks.end()):
            continue
        end = number
        while (
            end < len(lines)
            and end + 1 not in fenced
            and CONTAINER.sub("", lines[end], count=1).strip(" \t")
        ):
            end += 1
        text = "\n".join([line[marks.end() :], *lines[number:end]])
        label = LABEL.match(text)
        if not label:
            continue
        at = label.end() - 2
        row = number + text.count("\n", 0, at)
        column = at - text.rfind("\n", 0, at) if row > number else marks.end() + at + 1
        if view[row - 1][column - 1 : column + 1] != "]:":
            found.append((row, column, DEFINITION))
    return found


def modeline_problems(path: str, text: str, where: str) -> list[str]:
    """Each line among a file's first five and its last five, as Linguist splits a file into
    lines, that holds an Emacs or a Vim modeline, with which Linguist gives the file the
    language that it names whatever the file's name, so that GitHub may render the file as
    Markdown, which the test of pages does not read it as, or in another markup (R273)."""
    lines = LINE_BREAK.split(text)
    if not lines[-1]:
        lines.pop()
    window = {
        *range(min(MODELINE_LINES, len(lines))),
        *range(max(len(lines) - MODELINE_LINES, 0), len(lines)),
    }
    return [
        f"{shown_path(path)}:{number + 1}{where} holds {MODELINE}"
        for number in sorted(window)
        if EMACS_MODELINE.search(lines[number]) or VIM_MODELINE.search(lines[number])
    ]


def without_comments(text: str) -> tuple[str, tuple[int, int] | None, set[int]]:
    """A template's text with each HTML comment outside code made spaces, its line breaks
    kept, so that the columns after it stay as they were; where one opens that never closes,
    by its line and column, from where GitHub hides the rest; and each line on which a
    comment that opens a line, or the text of a quote or a list item, closes, the rest of
    which GitHub reads as raw HTML (R273). Each comment is found as the reading reads the
    text once the comments before it are gone, since a backtick or a fence in a comment
    opens no code."""
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
        if not CONTAINER.sub("", text[start:at], count=1):
            raw.add(text.count("\n", 0, end) + 1)


def fold_lines(lines: list[str], view: list[str]) -> set[int]:
    """The lines of the README that GitHub reads as raw HTML where the test lets its folds
    stand: from each line, or the text of each quote or list item, that a fold opens outside
    code, up to the next line that is blank but for the marks of quotes and list items, a
    reading that may take more lines than GitHub does, and never fewer (R273)."""
    found: set[int] = set()
    inside = False
    for number, (raw, seen) in enumerate(zip(lines, view, strict=True), 1):
        if not CONTAINER.sub("", raw, count=1).strip(" \t"):
            inside = False
        elif CONTAINER.sub("", seen, count=1).startswith(FOLDS):
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
    found += table_problems(lines, fenced)
    read_to = min((line for line, _ in stopped), default=len(lines) + 1)
    found += [
        (number, column, OPEN_RUN)
        for number, raw in enumerate(lines[: read_to - 1], 1)
        if number not in fenced
        for column in open_runs(raw)
    ]
    found += quoted_fences(lines[: read_to - 1], fenced | raw_html)
    for number, (seen, raw) in enumerate(zip(view, lines, strict=True), 1):
        found += [
            (number, column, what) for column, what in line_problems(seen, raw, path == README)
        ]
    found += definition_problems(lines[: read_to - 1], view, fenced)
    problems = [
        (line, column, f"{name}:{line}{f':{column}' if column else ''}{where} holds {what}")
        for line, column, what in found
    ]
    problems += [(line, 0, f"{name}:{line}{where}: {message}") for line, message in stopped]
    return [problem for _, _, problem in sorted(problems, key=lambda problem: problem[:2])]


def page_problems(root: Path) -> list[str]:
    """Each page that this repository writes in a markup other than Markdown, each file that
    it writes whose modeline can give it a markup, and what each Markdown file that it writes
    holds that GitHub hides or shows otherwise, each as git's index holds it and as the
    working tree holds it, where it differs (R272, R273). A version that is no file of UTF-8
    text, and an object that this clone lacks, it leaves to the test of characters, which
    names each."""
    markdown = markdown_files(root)
    entries = [
        entry
        for entry in tracked_entries(root)
        if entry.mode in (FILE, EXECUTABLE) and not written_by_others(entry.path)
    ]
    others = [
        f"{shown_path(entry.path)}{OTHER_MARKUP}"
        for entry in entries
        if OTHER_MARKUPS.search(entry.path)
    ]
    contents = blobs(root, (entry.oid for entry in entries))
    modelines: list[str] = []
    problems: list[str] = []
    folders: dict[str, str] = {}
    read = 0
    for entry in entries:
        indexed = contents.get(entry.oid)
        if indexed is None:
            continue
        tree = in_working_tree(root, entry.path, folders)
        for where, (kind, data) in versions(entry, ("file", indexed), tree):
            if kind != "file":
                continue
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                continue
            modelines += modeline_problems(entry.path, text, where)
            if entry.path in markdown:
                read += 1
                problems += page_text_problems(entry.path, text, where)
    return others + modelines + (problems if read else [PAGES_READ_NOTHING])


def attribute_line_problems(root: Path) -> list[str]:
    """Each line of a tracked attributes file, as git's index holds it and as the working
    tree holds it, that git ignores for its length, by the file, the line and its length,
    and by which of the two holds it where only one does (R274, DR-280)."""
    entries = [
        entry
        for entry in tracked_entries(root)
        if PurePosixPath(entry.path).name.casefold() == ".gitattributes"
    ]
    staged = blobs(root, [entry.oid for entry in entries])
    held: dict[str, set[tuple[str, int, int]]] = {IN_INDEX: set(), IN_TREE: set()}
    folders: dict[str, str] = {}
    for entry in entries:
        readings = {IN_INDEX: staged.get(entry.oid)}
        tree = in_working_tree(root, entry.path, folders)
        if tree is not None and tree[0] == "file":
            readings[IN_TREE] = staged_bytes(entry.path, tree[1], entry.mode == EXECUTABLE)
        for where, data in readings.items():
            for number, line in enumerate((data or b"").split(b"\n"), 1):
                if len(line) >= LONG_LINE:
                    held[where].add((entry.path, number, len(line)))
    return [
        f"{shown_path(path)}:{number}{where}{LINE_IGNORED.format(length)}"
        for (path, number, length), where in placed(held[IN_INDEX], held[IN_TREE])
    ]


def other_attribute_problems(root: Path) -> list[str]:
    """Each attribute other than `text` and `eol` that the repository's attributes give a
    tracked file or a folder that holds one, as git's index holds them and as the working
    tree holds them, read in a git folder of the test's own with no person's own attributes,
    by the file or the folder, the attribute and its value, and by which of the two gives it
    where only one does (R274, DR-280)."""
    paths = [entry.path for entry in tracked_entries(root)]
    if not paths:
        return [ATTRIBUTES_READ_NOTHING]
    # Each folder on a tracked path's way, with a slash at its end, as `git archive` asks
    # about a folder, so that a pattern that names only folders is read too.
    folders = sorted(
        {
            "/".join(parts[:end]) + "/"
            for parts in (path.split("/") for path in paths)
            for end in range(1, len(parts))
        }
    )
    (index, index_warned), (tree, tree_warned) = attribute_readings(root, paths + folders)
    return [
        f"{shown_path(path)}{where} has {shown(name)}: {shown(value)}{OTHER_ATTRIBUTE}"
        for (path, name, value), where in placed(set(index), set(tree))
        if name not in LINE_ENDINGS
    ] + [f"git warns{where}{WARNED}{line}" for line, where in placed(index_warned, tree_warned)]


def placed(index: set[Any], tree: set[Any]) -> list[tuple[Any, str]]:
    """Each item that git's index or the working tree gives, in order, with nothing where
    both give it, and else which of the two does."""
    both = index & tree
    held = {IN_INDEX: index, IN_TREE: tree}
    return sorted(
        [(item, "") for item in both]
        + [(item, where) for where, given in held.items() for item in given - both]
    )


def line_ending_problems(root: Path) -> list[str]:
    """Each tracked file to which the repository's attributes do not give both `text=auto`
    and `eol=lf`, as git's index holds them and as the working tree holds them, read as the
    test of attributes reads them, with no person's own attributes, by the file and what
    its attributes give (R276, DR-281)."""
    paths = [entry.path for entry in tracked_entries(root)]
    if not paths:
        return [LINE_FEEDS_READ_NOTHING]
    readings = []
    for attributes in repository_attributes(root, paths):
        given: dict[str, dict[str, str]] = {path: {} for path in paths}
        for path, name, value in attributes:
            if name in LINE_FEEDS:
                given[path][name] = value
        readings.append(given)
    index, tree = readings
    problems = []
    for path in paths:
        held = (
            [("", index[path])]
            if index[path] == tree[path]
            else [
                (IN_INDEX, index[path]),
                (IN_TREE, tree[path]),
            ]
        )
        problems += [
            f"{shown_path(path)}{where} has text: {shown(given.get('text', 'unspecified'))} and "
            f"eol: {shown(given.get('eol', 'unspecified'))}{NOT_LINE_FEEDS}"
            for where, given in held
            if given != LINE_FEEDS
        ]
    return problems


def ruff(root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    """The pinned ruff run in the folder at root, with none of the session's variables of
    ruff's, one of which would send its findings to a file."""
    return subprocess.run(
        [sys.executable, "-m", "ruff", *args],
        cwd=root,
        capture_output=True,
        check=False,
        env={name: value for name, value in os.environ.items() if not name.startswith("RUFF_")},
    )


@functools.cache
def naming_rules() -> dict[str, str]:
    """Each of ruff's naming rules, by its code, with its name, as the pinned ruff gives them."""
    done = ruff(ROOT, "rule", "--all", "--output-format", "json")
    done.check_returncode()
    return {
        rule["code"]: rule["name"]
        for rule in json.loads(done.stdout)
        if rule["linter"] == "pep8-naming"
    }


def ignores_naming(selector: str) -> bool:
    """Whether a selector of ruff's rules covers one of its naming rules: `ALL`, a prefix of
    the code of one, such as `N` or `N8`, or the name of one, which ruff takes in preview."""
    rules = naming_rules()
    return (
        selector == "ALL"
        or selector in rules.values()
        or any(code.startswith(selector) for code in rules)
    )


def naming_configuration_problems(config: Mapping[str, Any]) -> list[str]:
    """Each setting of `pyproject.toml`, read as `config`, that leaves ruff's naming rules
    unselected or ignores one of them, for every file or for some, or that takes ruff's
    settings from a file that the test does not read, by the setting and what it gives
    (R271)."""
    tables: dict[str, Mapping[str, Any]] = {}
    for name in RUFF_TABLES:
        table: Any = config
        for key in name.split("."):
            table = table.get(key, {}) if isinstance(table, Mapping) else {}
        tables[name] = table if isinstance(table, Mapping) else {}
    applied = next((name for name in reversed(RUFF_TABLES) if "select" in tables[name]), "")
    selected = {
        *(tables[applied]["select"] if applied else []),
        *(selector for table in tables.values() for selector in table.get("extend-select", [])),
    }
    problems = []
    if not selected & {"N", "ALL"}:
        where = f"{applied}.select, which ruff applies," if applied else "no select is set, and"
        problems.append(f"{NO_NAMING}{where} gives neither N nor ALL, and no extend-select does")
    if "extend" in tables["tool.ruff"]:
        problems.append(
            "pyproject.toml's tool.ruff.extend takes ruff's settings from "
            f"{shown(str(tables['tool.ruff']['extend']))}, which the test does not read"
        )
    for name, table in tables.items():
        for key in IGNORING:
            problems += [
                f"pyproject.toml's {name}.{key} gives {shown(selector)}{IGNORES_NAMING}"
                for selector in table.get(key, [])
                if ignores_naming(selector)
            ]
        for key in IGNORING_FOR_SOME:
            problems += [
                f"pyproject.toml's {name}.{key} gives {shown(selector)} for "
                f"{shown(pattern)}{IGNORES_NAMING}"
                for pattern, selectors in table.get(key, {}).items()
                for selector in selectors
                if ignores_naming(selector)
            ]
    return problems


def python_files(root: Path) -> list[str]:
    """Each tracked file that this repository writes and that Python reads as source, as the
    working tree holds it; a link, a submodule and a path that the working tree does not
    hold as a file are none."""
    folders: dict[str, str] = {}
    found = []
    for entry in tracked_entries(root):
        if entry.mode not in (FILE, EXECUTABLE) or written_by_others(entry.path):
            continue
        held = in_working_tree(root, entry.path, folders)
        if held is not None and held[0] == "file":
            text = staged_bytes(entry.path, held[1], entry.mode == EXECUTABLE)
            first = text.split(b"\n", 1)[0].decode("utf-8", "surrogateescape")
            if read_as_python(entry.path, first):
                found.append(entry.path)
    return found


def name_problems(root: Path) -> list[str]:
    """Each name in a Python file that this repository writes that ruff's naming rules refuse
    when ruff runs them with no configuration, no `noqa` comment and no ignore file, each
    file given by its path, so that no folder, setting or ignore file leaves one out, by the
    file, the line and the rule (R271)."""
    paths = python_files(root)
    if not paths:
        return [NAMES_READ_NOTHING]
    given = {str(root / path): path for path in paths}
    done = ruff(
        root,
        "check",
        "--isolated",
        "--select",
        "N",
        "--ignore-noqa",
        "--no-cache",
        "--output-format",
        "json",
        "--",
        *given,
    )
    return naming_findings(done, given)


def naming_findings(
    done: subprocess.CompletedProcess[bytes], given: Mapping[str, str]
) -> list[str]:
    """Each finding of a run of ruff's, by the file, the line and the rule, or that the run
    gave none that the test can trust: one that failed or warned, as ruff does of a file
    that it cannot read, or whose findings its exit status contradicts."""
    warned = done.stderr.decode("utf-8", "replace").strip()
    findings = json.loads(done.stdout) if done.returncode in (0, 1) and not warned else None
    if not isinstance(findings, list) or bool(findings) != (done.returncode == 1):
        return [f"{NAMES_UNREAD}{done.returncode}" + (f": {shown(warned)}" if warned else "")]
    return [
        f"{shown_path(given.get(found['filename'], found['filename']))}:"
        f"{found['location']['row']}: {shown(found['code'])} {shown(found['message'])}"
        for found in findings
    ]


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


def give(root: Path, attributes: str, index: str | None = None) -> Path:
    """The repository at root with this attributes file in its working tree, and in git's
    index the same or the other text given, staged by its object id, so that git applies
    none of it while it stages."""
    (root / ".gitattributes").write_bytes(attributes.encode("utf-8"))
    staged = (attributes if index is None else index).encode("utf-8")
    done = git(root, "hash-object", "-w", "--stdin", stdin=staged)
    done.check_returncode()
    oid = done.stdout.decode("ascii").strip()
    git(
        root, "update-index", "--add", "--cacheinfo", f"{FILE},{oid},.gitattributes"
    ).check_returncode()
    return root


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
    assert f"{kind.format(case)}:2:3 holds {named(character)}{NEVER_LISTED}" in planted_characters


@pytest.mark.parametrize("character", ["\u2800", "\U0001d159"])
def test_a_symbol_that_shows_as_blank_is_named_as_one_that_the_list_may_not_give(
    tmp_path: Path, character: str
) -> None:
    path = "vendor/superpowers/skills/a/helper.js"
    assert character_problems(plant(tmp_path, {path: planted_line(character)})) == [
        f"{path}:2:3 holds {named(character)}{NEVER_LISTED}"
    ]


# Shaking face, a symbol since Unicode 15, which the database of Python 3.11 does not know.
@pytest.mark.parametrize("character", ["\u2603", "\U0001f600", "\u00a9", "\U0001fae8"])
def test_a_visible_symbol_that_the_list_does_not_give_is_left_to_the_owner(
    tmp_path: Path, character: str
) -> None:
    path = "vendor/superpowers/skills/a/helper.js"
    problems = character_problems(plant(tmp_path, {path: planted_line(character)}))
    assert problems == [f"{path}:2:3 holds {named(character)}{NOT_LISTED}"]
    assert "add" not in problems[0] and "VISIBLE" not in problems[0]


def test_each_planted_character_is_named_once_and_nothing_else_is(
    planted_characters: list[str],
) -> None:
    planted = len(OWN_CHARACTERS) * len(OWN_KINDS) + len(OTHERS_CHARACTERS) * len(OTHERS_KINDS)
    # YAML refuses a tab where the workflow holds one, so the test names that file as one
    # whose strings it cannot read, too.
    assert f"own/tab/check.yml{UNLOADED.format('YAML')}" in planted_characters
    assert len(planted_characters) == len(set(planted_characters)) == planted + 1


def test_a_letter_that_looks_like_a_latin_one_is_named_as_one_that_the_list_may_not_give(
    planted_characters: list[str],
) -> None:
    found = [
        problem for problem in planted_characters if "U+0430 CYRILLIC SMALL LETTER A" in problem
    ]
    assert len(found) == len(OTHERS_KINDS)
    for problem in found:
        assert problem.endswith(NEVER_LISTED)
        assert "owner" not in problem and "add" not in problem and "VISIBLE" not in problem


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
    ("\\u200b", "\u200b", NEVER_LISTED),
    ("\\u{202e}", "\u202e", NEVER_LISTED),
    ("\\U000e0041", "\U000e0041", NEVER_LISTED),
    ("\\x1b", "\x1b", NEVER_LISTED),
    ("\\ud83d\\ude00", "\U0001f600", NOT_LISTED),
    ("\\ud83d", "\ud83d", NEVER_LISTED),
    ("\\u{000202e}", "\u202e", NEVER_LISTED),
    ("\\u{00000e0041}", "\U000e0041", NEVER_LISTED),
    ("\\U202e", "\u202e", NEVER_LISTED),
    ("\\UE0049", "\U000e0049", NEVER_LISTED),
    ("\\u7f", "\x7f", NEVER_LISTED),
    ("\\x7", "\x07", NEVER_LISTED),
    ("\\N{RIGHT-TO-LEFT OVERRIDE}", "\u202e", NEVER_LISTED),
    ("\\N{zero width space}", "\u200b", NEVER_LISTED),
]


@pytest.mark.parametrize("kind", ["helper.js", "SKILL.md"])
@pytest.mark.parametrize(("escape", "character", "reason"), ESCAPED)
def test_a_character_written_by_an_escape_is_held_as_the_character(
    tmp_path: Path, escape: str, character: str, reason: str, kind: str
) -> None:
    path = f"vendor/superpowers/skills/a/{kind}"
    assert character_problems(plant(tmp_path, {path: f"x = '{escape}'\n"})) == [
        f"{path}:1:6 writes {named(character)} by an escape{reason}"
    ]


def test_an_escape_that_writes_no_character_passes(tmp_path: Path) -> None:
    path = "vendor/superpowers/skills/a/helper.js"
    text = (
        "x = '\\u{110000} \\N{NOT A NAME} \\N{} \\usage \\u{} \\x"
        " \\N{LATIN CAPITAL LETTER A WITH MACRON AND GRAVE}'\n"
    )
    assert character_problems(plant(tmp_path, {path: text})) == []


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
        f"{path}:3 gives {named(character)} in its front matter, read as YAML{NEVER_LISTED}"
    ]


@pytest.mark.parametrize(
    ("opening", "closing"), [("--- ", "---"), ("---\t", "---  "), ("---", "--- ")]
)
def test_front_matter_opened_or_closed_after_spaces_or_tabs_is_read(
    tmp_path: Path, opening: str, closing: str
) -> None:
    path = "vendor/superpowers/skills/a/SKILL.md"
    text = f'{opening}\nname: a\ndescription: "a \\e b"\n{closing}\n# A\n'
    assert character_problems(plant(tmp_path, {path: text})) == [
        f"{path}:3 gives {named(chr(0x1B))} in its front matter, read as YAML{NEVER_LISTED}"
    ]


def test_a_key_of_a_skill_s_front_matter_is_read_too(tmp_path: Path) -> None:
    path = "vendor/superpowers/skills/a/SKILL.md"
    text = '---\nname: a\n"na\\eme": a\n---\n'
    assert character_problems(plant(tmp_path, {path: text})) == [
        f"{path}:3 gives {named(chr(0x1B))} in its front matter, read as YAML{NEVER_LISTED}"
    ]


def test_an_escape_in_a_skill_s_front_matter_is_named_once(tmp_path: Path) -> None:
    path = "vendor/superpowers/skills/a/SKILL.md"
    text = '---\nname: a\ndescription: "a \\u200b b"\n---\n'
    assert character_problems(plant(tmp_path, {path: text})) == [
        f"{path}:3:17 writes {named(chr(0x200B))} by an escape{NEVER_LISTED}"
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


def test_front_matter_of_others_is_read_only_in_a_skill(tmp_path: Path) -> None:
    files = {"vendor/superpowers/skills/a/notes.md": "---\nname: [a\n---\n"}
    assert character_problems(plant(tmp_path, files)) == []


@pytest.mark.parametrize(
    "path", ["docs/SKILL.md", ".github/ISSUE_TEMPLATE/feature_request.md", "docs/page.markdown"]
)
def test_the_front_matter_of_a_page_that_this_repository_writes_is_read_as_yaml(
    tmp_path: Path, path: str
) -> None:
    text = '---\nname: a\nabout: "b \\u202e \\e"\n---\nText.\n'
    assert character_problems(plant(tmp_path, {path: text})) == [
        f"{path}:3 gives {named(chr(0x202E))} in its front matter, read as YAML{NOT_ASCII}",
        f"{path}:3 gives {named(chr(0x1B))} in its front matter, read as YAML{NOT_ASCII}",
    ]


def test_front_matter_of_printable_ascii_in_a_page_that_this_repository_writes_passes(
    tmp_path: Path,
) -> None:
    text = '---\nname: A "quoted" \\u0041 and \\n\ntitle: "\\u0041\\n"\n---\nText.\n'
    assert character_problems(plant(tmp_path, {".github/ISSUE_TEMPLATE/a.md": text})) == []


# R268: what a loader decodes from a YAML, JSON or TOML file that this repository writes.

LOADED = [
    ("openspec/config.yaml", 'context: "Keep it short.\\U000E0049"\n', 1, "YAML", 0xE0049),
    ("ci.YML", 'a:\n  - "\\e[8m"\n', 2, "YAML", 0x1B),
    ("a.yml", '"k\\u200bey": b\n', 1, "YAML", 0x200B),
    ("a.yaml", "a: |\n  b\nc: 'd'\nd: \"\\L\"\n", 4, "YAML", 0x2028),
    ("a.yml", 'a: 1\n---\nb: "\\u202e"\n', 3, "YAML", 0x202E),
    (".claude/settings.json", '{"hooks": {"a": "\\u202e"}}\n', 0, "JSON", 0x202E),
    ("a.json", '{"\\u200b": 1}\n', 0, "JSON", 0x200B),
    ("a.JSON", '["\\ud83d\\ude00"]\n', 0, "JSON", 0x1F600),
    ("a.json", '{"a": "\\r"}\n', 0, "JSON", 0x0D),
    ("a.json", '{"a": "\\u202e", "a": "b"}\n', 0, "JSON", 0x202E),
    ("pyproject.toml", 'a = "\\u202E"\n', 0, "TOML", 0x202E),
    ("a.toml", '"\\U000E0041" = 1\n', 0, "TOML", 0xE0041),
]


@pytest.mark.parametrize(("path", "text", "line", "kind", "code"), LOADED)
def test_a_character_that_a_loader_decodes_in_a_file_that_this_repository_writes_fails(
    tmp_path: Path, path: str, text: str, line: int, kind: str, code: int
) -> None:
    where = f":{line}" if line else ""
    assert character_problems(plant(tmp_path, {path: text})) == [
        f"{path}{where} gives {named(chr(code))}, read as {kind}{NOT_ASCII}"
    ]


@pytest.mark.parametrize(
    ("path", "text", "kind"),
    [("a.json", "{\n", "JSON"), ("a.yml", "a: [b\n", "YAML"), ("a.toml", "a =\n", "TOML")],
)
def test_a_file_that_its_loader_cannot_read_fails(
    tmp_path: Path, path: str, text: str, kind: str
) -> None:
    assert character_problems(plant(tmp_path, {path: text})) == [
        f"{path} is not {kind} that the test can read, so the test cannot read its strings"
    ]


def test_a_file_that_a_loader_decodes_to_printable_ascii_passes(tmp_path: Path) -> None:
    files = {
        "a.json": '{"a": "\\u0041\\n\\"", "b": [1, true, null]}\n',
        "a.yml": 'a: "\\x41\\n"\nb: !!binary aGk=\n---\nc: 1\n',
        "a.toml": 'a = "\\u0041"\nb = 1979-05-27\n[c]\nd = [1, 2]\n',
        "vendor/superpowers/a.json": '{"a": "\\u2014 \\u26a0\\ufe0f", "b": "\\t"}\n',
        "docs/a.txt": "{\n",
    }
    assert character_problems(plant(tmp_path, files)) == []


@pytest.mark.parametrize(
    ("text", "problem"),
    [
        ('{"description": "a\\rb"}\n', f"gives {named(chr(0x0D))}, read as JSON{NEVER_LISTED}"),
        ('{"description": "a\\fb"}\n', f"gives {named(chr(0x0C))}, read as JSON{NEVER_LISTED}"),
        ("{\n", f"{UNLOADED.format('JSON')}"),
    ],
)
def test_a_file_that_others_write_and_that_a_loader_decodes_is_read_as_it_decodes(
    tmp_path: Path, text: str, problem: str
) -> None:
    path = "vendor/superpowers/.claude-plugin/plugin.json"
    separator = "" if problem.startswith(" ") else " "
    assert character_problems(plant(tmp_path, {path: text})) == [f"{path}{separator}{problem}"]


def test_an_escape_in_a_file_that_others_write_and_that_a_loader_decodes_is_named_once(
    tmp_path: Path,
) -> None:
    path = "vendor/superpowers/.claude-plugin/plugin.json"
    assert character_problems(plant(tmp_path, {path: '{"a": "\\u202e"}\n'})) == [
        f"{path}:1:8 writes {named(chr(0x202E))} by an escape{NEVER_LISTED}"
    ]


def test_a_character_that_a_file_that_a_loader_decodes_holds_as_itself_is_named_once(
    tmp_path: Path,
) -> None:
    assert character_problems(plant(tmp_path, {"a.json": '{"a": "\u202e"}\n'})) == [
        f"a.json:1:8 holds {named(chr(0x202E))}{NOT_ASCII}"
    ]


# R272: the test reads every file as git's index holds it and as the working tree holds it.


def test_a_character_that_only_git_s_index_holds_fails(tmp_path: Path) -> None:
    files: dict[str, str | bytes] = {
        ".gitattributes": "page.md working-tree-encoding=UTF-7\n",
        "page.md": planted_line("\u202e").encode("utf-7"),
    }
    source = plant(tmp_path / "source", files)
    commit(source)
    clone = cloned(source, tmp_path / "clone", {})
    assert (clone / "page.md").read_bytes().isascii()
    assert character_problems(clone) == [
        f"page.md:2:3{IN_INDEX} holds {named(chr(0x202E))}{NOT_ASCII}"
    ]


def test_a_replace_ref_hides_no_object_from_the_test(tmp_path: Path) -> None:
    # Git reads a replace ref's object in place of the one that it replaces, here a clean
    # file's, while the working tree holds the clean text, so that only git's own object
    # holds the character.
    root = plant(tmp_path, {"page.md": planted_line(chr(0x202E)), "clean.md": planted_line("")})
    staged, clean = (
        git(root, "rev-parse", f":{name}").stdout.decode("ascii").strip()
        for name in ("page.md", "clean.md")
    )
    git(root, "replace", staged, clean).check_returncode()
    (root / "page.md").write_text(planted_line(""), encoding="utf-8")
    assert character_problems(root) == [
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


def partial_clone(tmp_path: Path, files: Mapping[str, str]) -> Path:
    """A partial clone of a commit of these files whose index names each of them while the
    clone holds none of their objects, which git would fetch from the source."""
    source = plant(tmp_path / "source", files)
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
    return clone


def present(clone: Path, oid: str) -> bool:
    """Whether the clone holds the object, asked without fetching it."""
    return git(clone, "cat-file", "-e", oid, extra={"GIT_NO_LAZY_FETCH": "1"}).returncode == 0


def test_a_partial_clone_s_missing_object_is_named_and_not_fetched(tmp_path: Path) -> None:
    clone = partial_clone(tmp_path, {"page.md": "Printable.\n"})
    (oid,) = [entry.oid for entry in tracked_entries(clone)]
    assert not present(clone, oid)
    assert character_problems(clone) == [
        "page.md names an object that this clone lacks, as a partial clone does, which the test "
        "does not fetch",
        READ_NOTHING,
    ]
    assert not present(clone, oid)


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


# R272: a path that the working tree cannot open is named, and stops nothing.

# A path whose name is longer than the 255 bytes that common file systems give a part of one.
TOO_LONG = "docs/" + chr(0xFE0F) * 86 + ".md"


def unopenable(root: Path) -> Path:
    """The repository at root, whose working tree holds a folder `docs`, with git's index
    tracking a path there that the working tree cannot open, staged by its object id, as a
    mixed `git reset` or `git update-index --cacheinfo` stages one that no checkout writes."""
    done = git(root, "hash-object", "-w", "--stdin", stdin=planted_line("").encode("ascii"))
    done.check_returncode()
    oid = done.stdout.decode("ascii").strip()
    git(root, "update-index", "--add", "--cacheinfo", f"{FILE},{oid},{TOO_LONG}").check_returncode()
    return root


@pytest.mark.parametrize(
    "path", [TOO_LONG, f"docs/{'x' * 256}/page.md"], ids=["its name", "a folder on its way"]
)
def test_a_path_that_the_working_tree_cannot_open_is_read_as_one(tmp_path: Path, path: str) -> None:
    (tmp_path / "docs").mkdir()
    assert in_working_tree(tmp_path, path, {}) == ("unreadable", b"")


@pytest.mark.parametrize("call", ["os.open", "os.readlink", "open"])
def test_a_file_or_a_link_that_the_system_will_not_open_is_read_as_one(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, call: str
) -> None:
    (tmp_path / "page.md").write_bytes(b"Text.\n")
    (tmp_path / "link.md").symlink_to("page.md")
    owner, name = (os, call[3:]) if call.startswith("os.") else (builtins, call)
    real = getattr(owner, name)

    def refused(path: Any, *args: Any, **kwargs: Any) -> Any:
        if isinstance(path, int) or Path(path).name in ("page.md", "link.md"):
            raise PermissionError(13, "Permission denied")
        return real(path, *args, **kwargs)

    if owner is os:
        monkeypatch.setattr(os, name, refused)
    else:
        monkeypatch.setattr(conventions, name, refused, raising=False)
    path = "link.md" if call == "os.readlink" else "page.md"
    assert in_working_tree(tmp_path, path, {}) == ("unreadable", b"")


def test_a_path_that_the_working_tree_cannot_open_is_named(tmp_path: Path) -> None:
    root = unopenable(plant(tmp_path, {"docs/page.md": "Printable.\n"}))
    name = shown_path(TOO_LONG)
    assert character_problems(root) == [
        f"the path {name} holds a character other than printable ASCII but the space",
        f"{name}{IN_TREE} {UNOPENED}",
    ]
    # The other checks that read the working tree leave it to the test of characters.
    assert page_problems(root) == []
    assert attribute_line_problems(root) == []
    assert python_files(root) == []


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


def test_two_folders_that_differ_only_in_case_fail_once_where_their_names_differ(
    tmp_path: Path,
) -> None:
    files = {
        "vendor/Superpowers/hooks/hooks.json": "{}\n",
        "vendor/superpowers/hooks/run-hook.cmd": "Printable.\n",
    }
    assert character_problems(plant(tmp_path, files)) == [
        "the folders vendor/Superpowers and vendor/superpowers differ only in case, which a file "
        "system that ignores case holds as one folder"
    ]


def test_folders_that_differ_in_more_than_case_pass(tmp_path: Path) -> None:
    files = {"docs/Plan/a.md": "A.\n", "docs/plans/b.md": "B.\n", "docs/plans/c/d.md": "D.\n"}
    assert character_problems(plant(tmp_path, files)) == []


# R277: every tracked path is one that Windows can write.

# The names that Windows keeps for devices, as the scenario names them, written out here so
# that a name that the check leaves out fails, and the three cases that the test plants each in.
NAMED_DEVICES = (
    "CON",
    "PRN",
    "AUX",
    "NUL",
    "COM0",
    "COM1",
    "COM2",
    "COM3",
    "COM4",
    "COM5",
    "COM6",
    "COM7",
    "COM8",
    "COM9",
    "LPT0",
    "LPT1",
    "LPT2",
    "LPT3",
    "LPT4",
    "LPT5",
    "LPT6",
    "LPT7",
    "LPT8",
    "LPT9",
    "CONIN$",
    "CONOUT$",
)
CASES: dict[str, Callable[[str], str]] = {
    "upper": str.upper,
    "lower": str.lower,
    "mixed": lambda name: name[0] + name[1:].lower(),
}
# Each form that a device's name takes in a path, by the folder that plants it.
FORMS = {
    "alone": "{}",
    "before-one-dot": "{}.md",
    "before-two-dots": "{}.tar.gz",
    "folder": "{}/notes.md",
}


@pytest.fixture(scope="module")
def planted_devices(tmp_path_factory: pytest.TempPathFactory) -> tuple[list[str], list[str]]:
    """What the test of characters finds in a repository that plants each name that Windows
    keeps for a device, in each case and each form, and the problems that it should find."""
    files, expected = {}, []
    for case, spelled in CASES.items():
        for form, pattern in FORMS.items():
            for device in NAMED_DEVICES:
                part = spelled(device)
                path = f"devices/{case}/{form}/{pattern.format(part)}"
                shown_part = pattern.format(part).split("/")[0]
                files[path] = "Printable.\n"
                expected.append(
                    f"the path {path} has the part {shown_part}, which Windows reads as the "
                    f"device {device}"
                )
    return character_problems(plant(tmp_path_factory.mktemp("devices"), files)), expected


def test_each_name_that_windows_keeps_for_a_device_fails_in_each_case_and_form(
    planted_devices: tuple[list[str], list[str]],
) -> None:
    found, expected = planted_devices
    assert len(expected) == 26 * 3 * 4
    assert sorted(found) == sorted(expected)


@pytest.mark.parametrize("character", ["<", ">", ":", '"', "\\", "|", "?", "*"])
def test_a_character_that_windows_refuses_in_a_name_fails(tmp_path: Path, character: str) -> None:
    path = f"docs/a{character}b.md"
    assert character_problems(plant(tmp_path, {path: "Printable.\n"})) == [
        f"the path {path} holds `{character}`, which Windows refuses in a name"
    ]


def test_a_path_that_windows_can_read_as_a_short_name_fails(tmp_path: Path) -> None:
    path = "CLAUDE~1/marketplace.json"
    assert character_problems(plant(tmp_path, {path: "{}\n"})) == [
        f"the path {path} holds a `~`, which Windows writes in the short name that it gives a "
        "file or a folder"
    ]


@pytest.mark.parametrize(
    ("path", "part"), [("docs/page.", "page."), ("docs./page.md", "docs."), ("a../b.md", "a..")]
)
def test_a_part_that_ends_in_a_dot_fails(tmp_path: Path, path: str, part: str) -> None:
    assert character_problems(plant(tmp_path, {path: "Printable.\n"})) == [
        f"the path {path} has the part {part}, which ends in a dot that Windows drops"
    ]


def test_a_path_of_more_than_140_characters_fails(tmp_path: Path) -> None:
    path = f"docs/{'a' * 100}/{'b' * 32}.md"
    assert len(path) == LONGEST_PATH + 1
    assert character_problems(plant(tmp_path, {path: "Printable.\n"})) == [
        f"the path {path} holds 141 characters, more than the 140 that a clone on Windows can write"
    ]


def test_paths_that_windows_can_write_pass(tmp_path: Path) -> None:
    longest = f"docs/{'a' * 100}/{'b' * 31}.md"
    assert len(longest) == LONGEST_PATH
    paths = [
        longest,
        "docs/console.md",
        "scripts/com10.py",
        "docs/auxiliary/nul-terminated.md",
        "docs/lpt.md",
        "docs/conin.md",
        "docs/.prn",
        "docs/a.b.c.md",
    ]
    assert character_problems(plant(tmp_path, {path: "Printable.\n" for path in paths})) == []


# R268: what Python reads as source declares no encoding but UTF-8.


@pytest.mark.parametrize(
    ("path", "text", "declared"),
    [
        ("scripts/tool.py", "# -*- coding: utf-7 -*-\nprint(1)\n", "utf-7"),
        ("scripts/tool.py", "#!/usr/bin/env python3\n# coding: unicode_escape\n", "unicode_escape"),
        ("scripts/stub.pyi", "# vim: set fileencoding=latin-1 :\n", "latin-1"),
        ("hooks/run", "#!/usr/bin/env python3\n# coding=cp1252\n", "cp1252"),
        ("scripts/tool.py", "# coding: no-such-encoding\n", "no-such-encoding"),
        ("tests/conftest.PY", "# -*- coding: utf-7 -*-\n", "utf-7"),
        ("scripts/stub.Pyi", "# coding: utf-7\n", "utf-7"),
        ("scripts/tool.pyw", "# coding: utf-7\n", "utf-7"),
        ("scripts/tool.PYW", "# coding: utf-7\n", "utf-7"),
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
    "image-without-text": ("An ![ ](a.png) here.", "![", IMAGE),
    "image-split-by-a-line-break": ("An ![\n](a.png) here.", "![", IMAGE),
    "double-quoted-title": ('A [link](a.md "A title") here.', "](", TITLE),
    "single-quoted-title": ("A [link](a.md 'A title') here.", "](", TITLE),
    "parenthesised-title": ("A [link](a.md (A title)) here.", "](", TITLE),
    "title-after-brackets": ('A [link](<a.md> "A title") here.', "](", TITLE),
    "target-cut-by-the-line": ("A [link](a.md", "](", TITLE),
    "link-without-text": ("A [](https://example.invalid) here.", "](", NO_TEXT),
    "link-with-blank-text": ("A [ \t](a.md) here.", "](", NO_TEXT),
    "link-without-text-after-a-backslash": ("A \\\\[](a.md) here.", "](", NO_TEXT),
    "dollar": ("It costs $5.", "$", DOLLAR),
    "escaped-backtick": ("A \\`<!-- hidden -->\\` word.", "\\", BACKSLASHED),
    "autolinked-backtick": ("A <`@x.y> <!-- hidden --> ` word.", "<", AUTOLINKED),
    "autolinked-backtick-in-an-item": ("- A <`@x.y> <!-- hidden --> ` word.", "<", AUTOLINKED),
    "autolinked-backtick-in-a-quote": ("> A <`@x.y> <!-- hidden --> ` word.", "<", AUTOLINKED),
    "link-split-by-a-line-break": ("See [\n](https://example.invalid) here.", "[", OPEN_BRACKET),
    "link-split-after-spaces": ("See [ \t\n \t](a.md) here.", "[", OPEN_BRACKET),
    "link-split-by-a-hard-break": ("See [\\\n](a.md) here.", "[", OPEN_BRACKET),
    "link-split-in-an-item": ("- See [\n  ](a.md) here.", "[", OPEN_BRACKET),
    "link-split-in-a-quote": ("> See [\n> ](a.md) here.", "[", OPEN_BRACKET),
    "definition-with-a-backtick": ('[a`]: /url "a hidden title`"', "]:", DEFINITION),
    "footnote-with-a-backtick": ("[^a`]: a hidden note`", "]:", DEFINITION),
    "definition-with-a-backtick-in-an-item": ('- [a`]: /url "hidden`"', "]:", DEFINITION),
    "definition-with-a-backtick-in-a-quote": ('> [a`]: /url "hidden`"', "]:", DEFINITION),
    "destination-with-a-backtick": ("See [a](page.md#a`b) <!-- hidden --> `).", "](", DESTINATION),
    "destination-with-a-backtick-in-an-item": ("- [a](a.md#a`b) <!-- x --> `).", "](", DESTINATION),
    "destination-with-a-backtick-in-a-quote": ("> [a](a.md#a`b) <!-- x --> `).", "](", DESTINATION),
    "web-address-with-a-backtick": (
        "See https://a.example/a`b <!-- x --> ` here.",
        "h",
        WEB_ADDRESS,
    ),
    "www-address-with-a-backtick": ("See www.example.com/a`b <!-- x --> ` here.", "w", WEB_ADDRESS),
    "web-address-in-a-destination": (
        "See [a](https://a.example/a`b) <!-- x --> `).",
        "](",
        DESTINATION,
    ),
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


@pytest.mark.parametrize("address", ["<`@x.y>", "<1`@x.y>", "<a`@x.y>", "<https://a`b>"])
def test_an_autolink_that_holds_a_backtick_outside_code_fails(tmp_path: Path, address: str) -> None:
    """GitHub shows the autolink, which starts first, as a link, while the reading pairs its
    backtick with a later one, so that it takes the comment between them for code (R273).
    Where the address starts with a letter, the reading also names the element that it
    sees."""
    root = plant(tmp_path, {"docs/a.md": page(f"A {address} <!-- hidden --> ` word.")})
    assert f"docs/a.md:3:3 holds {AUTOLINKED}" in page_problems(root)


@pytest.mark.parametrize("line", ["A <a@x.y> and <https://a.b/c> here.", "A `` <`@x.y> `` here."])
def test_an_autolink_with_no_backtick_or_inside_code_passes(tmp_path: Path, line: str) -> None:
    assert page_problems(plant(tmp_path, {"docs/a.md": page(line)})) == []


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


@pytest.mark.parametrize(
    "table",
    ["> | A |\n> |---|\n> | 1 | hidden |\n", "1. > | A |\n   > |---|\n   > | 1 | hidden |\n"],
)
def test_a_table_row_in_a_quote_is_read_as_github_reads_it(tmp_path: Path, table: str) -> None:
    root = plant(tmp_path, {"docs/table.md": page(table)})
    assert page_problems(root) == [
        "docs/table.md:5 holds a table row of 2 cells under a header of 1, whose cells past the"
        " header's GitHub hides"
    ]


def test_a_definition_whose_label_a_line_breaks_is_read_as_github_reads_it(tmp_path: Path) -> None:
    """GitHub reads a definition, whose label may hold a line break, before it reads code, so
    a backtick in its label opens no code span (R273)."""
    root = plant(tmp_path, {"docs/a.md": page('[a\nb`]: /url "hidden`"\n\nText.')})
    assert page_problems(root) == [f"docs/a.md:4:3 holds {DEFINITION}"]


@pytest.mark.parametrize(
    "body",
    [
        "`[a]: b` is code.",
        "Text [a`]: b` in a paragraph, where no definition starts.",
        "[a](b.md) and [c\nd](e.md) are links, and [f] is text.",
        "- [ ] A task, and [g]",
        "[a\n\nb`]: c` is code, as a blank line ends the paragraph that a label may cross.",
        "[a\n```\nb]: c\n```",
    ],
)
def test_a_definition_in_code_or_a_bracket_that_opens_none_passes(
    tmp_path: Path, body: str
) -> None:
    assert page_problems(plant(tmp_path, {"docs/a.md": page(body)})) == []


def test_the_first_of_two_destinations_that_hide_what_lies_between_them_is_named(
    tmp_path: Path,
) -> None:
    """Two such destinations hide what lies between them with no stray backtick, the second
    among it, so the test names the first, and the rest once the first is mended (R273)."""
    body = "See [a](a.md#a`b) <!-- hidden --> [b](b.md#c`d)."
    assert page_problems(plant(tmp_path, {"docs/a.md": page(body)})) == [
        f"docs/a.md:3:7 holds {DESTINATION}"
    ]


@pytest.mark.parametrize(
    "body",
    [
        "A [link](a.md#a-b), https://example.com/a-b and www.example.com/c show as written.",
        "Code ``[a](b.md#c`d)`` and `https://example.com/a` show as code.",
        "Text awww.example.com/a`b` and xhttps://a.example/a`b` hold code: GitHub links neither.",
        "A link [`code`](a.md) holds code in its text.",
    ],
)
def test_a_link_or_a_web_address_without_a_backtick_or_in_code_passes(
    tmp_path: Path, body: str
) -> None:
    assert page_problems(plant(tmp_path, {"docs/a.md": page(body)})) == []


@pytest.mark.parametrize(
    ("table", "line", "column"),
    [
        ("| A | B | C |\n|---|---|---|\n| `x | <!-- hidden --> y` | z |\n", 5, 3),
        ("| `x | <!-- hidden --> y` |\n|---|---|\n| 1 | 2 |\n", 3, 3),
        ("A | B | C\n--|---|--\n`x | &#x202E; y` | z\n", 5, 1),
        ("> | A | B | C |\n> |---|---|---|\n> | `x | ![a](b.png) y` | z |\n", 5, 5),
        ("| A | B | C | D |\n|---|---|---|---|\n| `x | $5 | y` | z |\n", 5, 3),
    ],
    ids=["a row", "the header", "no leading pipe", "a quote", "three cells apart"],
)
def test_a_code_span_that_a_table_s_cells_split_fails(
    tmp_path: Path, table: str, line: int, column: int
) -> None:
    """GitHub splits a table's row into cells before it reads code, so a backtick in one cell
    pairs with none in a later one, while the reading pairs them and takes what lies between
    for code (R273)."""
    root = plant(tmp_path, {"docs/table.md": page(table)})
    assert page_problems(root) == [f"docs/table.md:{line}:{column} holds {SPLIT_SPAN}"]


@pytest.mark.parametrize(
    "body",
    [
        "| A | B |\n|---|---|\n| `a \\| b` | c |\n",
        "Run `a | b` in a paragraph, which no table holds.",
        "| A |\n|---|\n\nAfter the table, `a | b`.",
    ],
)
def test_a_code_span_that_holds_an_escaped_pipe_or_lies_outside_a_table_passes(
    tmp_path: Path, body: str
) -> None:
    assert page_problems(plant(tmp_path, {"docs/table.md": page(body)})) == []


@pytest.mark.parametrize(
    ("body", "problems"),
    [
        (
            '> ~~~mermaid\n> flowchart LR\n>   click A "https://example.com" "hidden"\n> ~~~',
            [(3, 3), (6, 3)],
        ),
        ("> ~~~math\n> x^2\n> ~~~", [(3, 3), (5, 3)]),
        ("> ~~~python title=hidden\n> x = 1\n> ~~~", [(3, 3), (5, 3)]),
        ("- > ~~~mermaid\n  > flowchart LR\n  > ~~~", [(3, 5), (5, 5)]),
        ("> - ~~~mermaid\n>   flowchart LR\n>   ~~~", [(3, 5), (5, 5)]),
        (">~~~\n>x\n>~~~", [(3, 2), (5, 2)]),
    ],
    ids=["mermaid", "math", "an info string", "a quote in an item", "an item in a quote", "tight"],
)
def test_a_fence_inside_a_quote_fails(
    tmp_path: Path, body: str, problems: list[tuple[int, int]]
) -> None:
    """GitHub opens a fenced block inside a quote and draws it, while the reading, as the
    test of words reads it, takes no fence after a quote's mark (R273, T90)."""
    root = plant(tmp_path, {"docs/a.md": page(body)})
    assert page_problems(root) == [
        f"docs/a.md:{line}:{column} holds {QUOTED_FENCE}" for line, column in problems
    ]


def test_a_quoted_fence_of_backticks_is_also_named_as_a_run_that_its_line_leaves_open(
    tmp_path: Path,
) -> None:
    root = plant(tmp_path, {"docs/a.md": page("> ```math\n> x^2\n> ```")})
    assert page_problems(root) == [
        f"docs/a.md:3:3 holds {OPEN_RUN}",
        f"docs/a.md:3:3 holds {QUOTED_FENCE}",
        f"docs/a.md:5:3 holds {OPEN_RUN}",
        f"docs/a.md:5:3 holds {QUOTED_FENCE}",
    ]


@pytest.mark.parametrize(
    "body", ["> A quote of ~~~ within its text.", "~~~\n> ~~~ in a fenced block\n~~~"]
)
def test_a_fence_that_no_quote_opens_passes(tmp_path: Path, body: str) -> None:
    assert page_problems(plant(tmp_path, {"docs/a.md": page(body)})) == []


def test_a_run_that_opens_no_fence_outside_a_quote_is_named_only_as_a_run_left_open(
    tmp_path: Path,
) -> None:
    """A run of backticks whose line also holds a backtick after it opens no fence, for GitHub
    as for the reading, which reads the line as prose (R273)."""
    root = plant(tmp_path, {"docs/a.md": page("```a`b c")})
    assert page_problems(root) == [
        f"docs/a.md:3:1 holds {OPEN_RUN}",
        f"docs/a.md:3:5 holds {OPEN_RUN}",
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
            "style A color:red",
            "classDef hidden display:none",
            "linkStyle 0 stroke:red",
        )
    ),
    *(
        (
            f"```mermaid\n{kind}\n  {line}\n```",
            f"docs/a.md:5:{column} holds {word}{IN_MERMAID}{MERMAID_HIDES}",
        )
        for kind, line, column, word in (
            ("flowchart LR", 'A --> B; click A "https://example.com" "hidden"', 12, "click"),
            ("flowchart LR", "A-->B;style A fill:red", 9, "style"),
            ("flowchart LR", "A --> B ; accTitle: hidden", 13, "accTitle"),
            ("flowchart LR", 'Click A "https://example.com" "hidden"', 3, "Click"),
            ("flowchart LR", "callback A hidden", 3, "callback"),
            ("sequenceDiagram", "ACCTITLE: hidden", 3, "ACCTITLE"),
            ("sequenceDiagram", "link Alice: Dashboard @ https://example.com", 3, "link"),
            ("sequenceDiagram", 'links Alice: {"Dashboard": "https://example.com"}', 3, "links"),
        )
    ),
    (
        "```mermaid\nsequenceDiagram\n  # hidden\n  Alice->>Bob: Hi\n```",
        f"docs/a.md:5:3 holds #{IN_MERMAID}{HASH}",
    ),
    (
        "```mermaid\nsequenceDiagram\n  Alice->>Bob: Shown # hidden\n```",
        f"docs/a.md:5:22 holds #{IN_MERMAID}{HASH}",
    ),
    (
        "```mermaid\nsequenceDiagram\n  % hidden\n  Alice->>Bob: Hi\n```",
        f"docs/a.md:5:3 holds %{IN_MERMAID}{DIRECTIVE}",
    ),
    *(
        (
            f'```mermaid\nflowchart LR\n  A["a{written}b"] --> B\n```',
            f"docs/a.md:5:7 holds the character reference {read}{IN_MERMAID}{ENTITY_NAMES}",
        )
        for written, read in (
            ("&rlm;", "&rlm;"),
            ("&ZeroWidthSpace;", "&ZeroWidthSpace;"),
            ("&nbsp;", "&nbsp;"),
            ("&amp;", "&amp;"),
            # A browser reads a name that HTML gives without its `;` by the longest such.
            ("&shy", "&shy"),
            ("&notit;", "&not"),
        )
    ),
    (
        '```mermaid\nflowchart LR\n  A@{ img: "https://example.com/a.png", label: "A" }\n```',
        f"docs/a.md:5:4 holds @{{{IN_MERMAID}{SHAPE_DATA}",
    ),
    *(
        (
            f"```mermaid\n{kind}\n  A --> B\n```",
            f"docs/a.md:4:1 holds a Mermaid block that draws {kind.split()[0]}{OTHER_DIAGRAM}",
        )
        for kind in (
            "stateDiagram-v2",
            "classDiagram",
            "journey",
            "gantt",
            "railroad",
            "eventmodeling",
            "flowchart-elk LR",
            "Flowchart LR",
        )
    ),
]


@pytest.mark.parametrize(("block", "problem"), DRAWN_BLOCKS)
def test_a_drawn_block_that_can_hide_text_fails(tmp_path: Path, block: str, problem: str) -> None:
    assert page_problems(plant(tmp_path, {"docs/a.md": page(block)})) == [problem]


@pytest.mark.parametrize(
    "block",
    [
        "```mermaid\nflowchart LR\n  A[The tool, in first place] -->|reads| B[A file]\n```",
        "```mermaid\n\ngraph TD\n  A & B --> C[R and D]\n```",
        "```mermaid\nsequenceDiagram\n  Alice->>Bob: Hello; Bob-->>Alice: Hi\n```",
        "```mermaid\n```",
    ],
    ids=["a flowchart", "a graph", "a sequence diagram", "an empty block"],
)
def test_a_mermaid_block_in_plain_text_passes(tmp_path: Path, block: str) -> None:
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
    "Links whose text is [`code`](a.md) or [[]](a.md) show it, and \\[](a.md) is no link.",
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
    (
        "README.md",
        "- <details>\n  `<!-- x -->`\n  </details>\n",
        f"README.md:2:3 holds a backtick{OPENS_NO_CODE}",
    ),
    (
        "README.md",
        "> <details>\n> `<!-- x -->`\n> </details>\n",
        f"README.md:2:3 holds a backtick{OPENS_NO_CODE}",
    ),
    (
        "README.md",
        "1. > <details>\n   > ~~~\n",
        f"README.md:2:6 holds a run of tildes{OPENS_NO_CODE}",
    ),
    (
        ".github/pull_request_template.md",
        "- <!-- A comment. --> `&#x202E;`\n",
        f".github/pull_request_template.md:1:23 holds a backtick{OPENS_NO_CODE}",
    ),
    (
        ".github/pull_request_template.md",
        "> <!-- A comment\n> that closes. --> `&#x202E;`\n",
        f".github/pull_request_template.md:2:20 holds a backtick{OPENS_NO_CODE}",
    ),
    (
        ".github/pull_request_template.md",
        "Text.\n\n- A list.\n  <!-- A comment. --> `&#x202E;`\n",
        f".github/pull_request_template.md:4:23 holds a backtick{OPENS_NO_CODE}",
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
        (".github/pull_request_template.md", "- Fill in `this` <!-- A comment. --> and `that`.\n"),
        ("README.md", FOLDED.replace("Text.", "Text and `code`.")),
        ("README.md", "```\n<details>\n`x`\n```\n"),
        ("README.md", "> <details>\n>\n> Text and `code`.\n"),
        ("README.md", "- Text <details>\n  and `code`.\n"),
    ],
)
def test_code_after_a_comment_within_a_line_after_a_fold_s_blank_line_or_in_code_passes(
    tmp_path: Path, path: str, text: str
) -> None:
    assert page_problems(plant(tmp_path, {path: text})) == []


# The extensions that GitHub's language list, Linguist, gives the languages that GitHub's
# markup library renders other than as Markdown, as its `languages.yml` gave them on
# 2026-11-23, written out here so that one that the check leaves out fails.
OTHER_MARKUP_EXTENSIONS = (
    "textile",
    "rdoc",
    "org",
    "creole",
    "mediawiki",
    "wiki",
    "wikitext",
    "rst",
    "rest",
    "rst.txt",
    "rest.txt",
    "asciidoc",
    "adoc",
    "asc",
    "pod",
    "pod6",
)


@pytest.mark.parametrize(
    "extension", [*OTHER_MARKUP_EXTENSIONS, "RST", "Adoc", "REST", "Rst.Txt", "WIKITEXT", "Pod6"]
)
def test_a_page_in_a_markup_other_than_markdown_fails(tmp_path: Path, extension: str) -> None:
    files = {f"docs/notes.{extension}": "Notes.\n", "docs/page.md": "Text.\n"}
    assert page_problems(plant(tmp_path, files)) == [f"docs/notes.{extension}{OTHER_MARKUP}"]


def test_a_page_in_another_markup_is_named_where_no_markdown_page_is_read(tmp_path: Path) -> None:
    assert page_problems(plant(tmp_path, {"docs/notes.rst": "Notes.\n"})) == [
        f"docs/notes.rst{OTHER_MARKUP}",
        PAGES_READ_NOTHING,
    ]


def test_a_file_that_only_names_another_markup_or_that_others_write_passes(
    tmp_path: Path,
) -> None:
    files = {
        "docs/rst-notes.md": "Text.\n",
        "docs/notes.rst.md": "Text.\n",
        "docs/notes.pod.txt": "Text.\n",
        "docs/notes.organisation": "Text.\n",
        "vendor/superpowers/docs/notes.rst": "Notes.\n",
    }
    assert page_problems(plant(tmp_path, files)) == []


# A file of twelve lines that holds a line on the line given, or on none.
def twelve_lines(line: str, at: int = 0) -> str:
    return "".join(f"{line if number == at else f'Line {number}.'}\n" for number in range(1, 13))


MODELINES = [
    "-*- mode: org -*-",
    "# -*- mode: markdown -*-",
    "-*-rst-*-",
    "-*- foo: bar; mode: rst; -*-",
    "vim: set ft=markdown:",
    "# vim: ft=rst",
    "vi: syntax=org",
    " ex: filetype=textile",
    "Vim: set filetype=markdown:",
    "vim700: ft=rst",
]


@pytest.mark.parametrize("modeline", MODELINES)
@pytest.mark.parametrize(
    ("path", "at"),
    [("docs/notes.txt", 1), ("scripts/tool.py", 5), ("docs/notes.txt", 8), ("docs/page.md", 12)],
)
def test_a_modeline_in_the_first_or_last_five_lines_of_a_file_fails(
    tmp_path: Path, modeline: str, path: str, at: int
) -> None:
    """GitHub's language list, Linguist, reads a modeline in a file's first or last five lines
    before its name, and GitHub's markup library renders the file in the language that it
    names, so a modeline can have GitHub render any file as Markdown, which the test of pages
    does not read, or a page in another markup (R273)."""
    root = plant(tmp_path, {path: twelve_lines(modeline, at)})
    assert page_problems(root)[0] == f"{path}:{at} holds {MODELINE}"


@pytest.mark.parametrize(
    "files",
    [
        {"docs/notes.txt": twelve_lines("vim: set ft=markdown:", 6)},
        {"docs/notes.txt": twelve_lines("-*- mode: org -*-", 7)},
        {"vendor/superpowers/notes.txt": "vim: set ft=markdown:\n"},
        {"docs/notes.txt": "A line about vim and its file types.\n"},
    ],
    ids=["the sixth line", "the seventh line", "a file that others write", "no modeline"],
)
def test_a_modeline_outside_those_lines_or_in_a_file_that_others_write_passes(
    tmp_path: Path, files: dict[str, str]
) -> None:
    assert page_problems(plant(tmp_path, {**files, "docs/page.md": "Text.\n"})) == []


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


# R274: the repository's attributes set nothing but line endings.

NAMED_ATTRIBUTES = (
    "working-tree-encoding",
    "filter",
    "ident",
    "export-subst",
    "export-ignore",
    "binary",
    "diff",
    "linguist-generated",
)
# How an attributes file gives an attribute in each state, and how git shows its value.
STATES = {"set": ("{}", "set"), "unset": ("-{}", "unset"), "valued": ("{}=a-value", "a-value")}


@pytest.mark.parametrize("state", STATES)
@pytest.mark.parametrize("name", NAMED_ATTRIBUTES)
def test_an_attribute_other_than_text_and_eol_fails(tmp_path: Path, name: str, state: str) -> None:
    written, value = STATES[state]
    attributes = f"docs/*.md {written.format(name)}\n"
    root = plant(tmp_path, {"docs/page.md": "Text.\n"})
    if (name, state) == ("working-tree-encoding", "set"):
        # Git dies on writing its index while an attributes file that it reads sets this
        # attribute with no value, so this one state reaches only the working tree.
        (root / ".gitattributes").write_bytes(attributes.encode("utf-8"))
        where = IN_TREE
    else:
        give(root, attributes)
        where = ""
    problems = other_attribute_problems(root)
    assert f"docs/page.md{where} has {name}: {value}{OTHER_ATTRIBUTE}" in problems
    assert all(problem.startswith("docs/page.md") for problem in problems)


def test_line_endings_alone_pass(tmp_path: Path) -> None:
    files: dict[str, str | bytes] = {
        "docs/page.md": "Text.\n",
        "start.sh": "#!/bin/sh\n",
        "a.png": PNG,
    }
    root = give(plant(tmp_path, files), "* text=auto eol=lf\n*.sh text eol=lf\n*.png -text\n")
    assert other_attribute_problems(root) == []


def test_an_attribute_that_only_git_s_index_or_only_the_working_tree_gives_fails(
    tmp_path: Path,
) -> None:
    root = plant(tmp_path, {"docs/a.md": "Text.\n", "docs/b.md": "Text.\n"})
    give(root, "docs/b.md ident\n", index="docs/a.md ident\n")
    assert other_attribute_problems(root) == [
        f"docs/a.md{IN_INDEX} has ident: set{OTHER_ATTRIBUTE}",
        f"docs/b.md{IN_TREE} has ident: set{OTHER_ATTRIBUTE}",
    ]


# An attributes file that gives itself an encoding in which a checkout rewrites each `=` and
# `*`, so that git cannot read the lines of the copy that a fresh clone writes.
REENCODED = ".gitattributes working-tree-encoding=UTF-7\n*.md diff=x linguist-generated\n"
REENCODED_FILES = ("docs/decisions/DR-001-a-choice.md", "docs/patterns.md", "docs/threat-model.md")


def test_an_attributes_file_that_a_checkout_re_encodes_is_read_as_git_holds_it(
    tmp_path: Path,
) -> None:
    source = plant(tmp_path / "source", dict.fromkeys(REENCODED_FILES, "Text.\n"))
    commit(give(source, REENCODED))
    clone = cloned(source, tmp_path / "clone", {})
    assert b"+AD0-" in (clone / ".gitattributes").read_bytes(), "no checkout re-encoded it"
    hidden = ("diff: x", "linguist-generated: set")
    # Git cannot read the copy that the checkout re-encoded, and says so, which the test names
    # too, as it names each warning of git's while it reads the attributes.
    assert other_attribute_problems(clone) == [
        f".gitattributes{IN_INDEX} has working-tree-encoding: UTF-7{OTHER_ATTRIBUTE}",
        *(
            f"{path}{IN_INDEX} has {each}{OTHER_ATTRIBUTE}"
            for path in REENCODED_FILES
            for each in hidden
        ),
        f"git warns{IN_TREE}{WARNED}diff+AD0-x is not a valid attribute name: .gitattributes:2",
        f"git warns{IN_TREE}{WARNED}working-tree-encoding+AD0-UTF-7 is not a valid attribute name:"
        " .gitattributes:1",
    ]
    for path, paths in (
        ("docs/decisions/DR-001-a-choice.md", ["docs/decisions/DR-001-a-choice.md"]),
        ("docs/threat-model.md", ["docs/threat-model.md"]),
        ("docs/patterns.md", reviewed(clone)),
    ):
        found = attribute_problems(clone, paths)
        for each in hidden:
            assert f"{path} has {each}, which changes how its diff shows" in found


def test_a_person_s_own_attributes_are_not_read_as_the_repository_s(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = plant(tmp_path / "repository", {"docs/page.md": "Text.\n"})
    (root / ".git" / "info").mkdir(exist_ok=True)
    (root / ".git" / "info" / "attributes").write_text("* ident -diff\n", encoding="utf-8")
    home = tmp_path / "home"
    (home / "git").mkdir(parents=True)
    (home / "git" / "attributes").write_text(
        "* export-subst linguist-generated\n", encoding="utf-8"
    )
    monkeypatch.setenv("XDG_CONFIG_HOME", str(home))
    # The tests' own runs of git read no attributes file of the person's, so this one names
    # the planted file.
    personal = f"core.attributesFile={home / 'git' / 'attributes'}"
    plain = git(root, "-c", personal, "check-attr", "-a", "--", "docs/page.md")
    assert "ident: set" in plain.stdout.decode() and "export-subst: set" in plain.stdout.decode(), (
        "git reads neither file"
    )
    assert other_attribute_problems(root) == []
    assert attribute_problems(root, ["docs/page.md"]) == []


def test_a_partial_clone_s_missing_attributes_file_is_not_fetched(tmp_path: Path) -> None:
    files = {".gitattributes": "docs/*.md diff=x\n", "docs/page.md": "Text.\n"}
    clone = partial_clone(tmp_path, files)
    (oid,) = [entry.oid for entry in tracked_entries(clone) if entry.path == ".gitattributes"]
    assert not present(clone, oid)
    other_attribute_problems(clone)
    attribute_problems(clone, ["docs/page.md"])
    assert not present(clone, oid)
    assert (
        ".gitattributes names an object that this clone lacks, as a partial clone does, which "
        "the test does not fetch"
    ) in character_problems(clone)


def test_a_check_of_attributes_that_reads_no_tracked_file_fails(tmp_path: Path) -> None:
    git(tmp_path, "init", "-q").check_returncode()
    assert other_attribute_problems(tmp_path) == [ATTRIBUTES_READ_NOTHING]


# Attributes that a folder's own pattern gives it, which `git archive` applies to the folder
# and so to every file in it, while `git check-attr` gives them to no file in it, each with
# the folder that the test names and what it says that the folder has.
FOLDER_ATTRIBUTES = [
    ("vendor export-ignore\n", "vendor/", "export-ignore: set"),
    ("/docs export-ignore\n", "docs/", "export-ignore: set"),
    ("docs/decisions export-ignore\n", "docs/decisions/", "export-ignore: set"),
    ("docs/ export-ignore\n", "docs/", "export-ignore: set"),
    ("vendor -diff\n", "vendor/", "diff: unset"),
]
FOLDER_FILES = {
    "docs/decisions/DR-001-a-choice.md": "Text.\n",
    "vendor/a/SKILL.md": "Text.\n",
    "README.md": "Text.\n",
}


def test_git_archive_leaves_out_a_folder_that_its_attributes_give_export_ignore(
    tmp_path: Path,
) -> None:
    root = give(plant(tmp_path, FOLDER_FILES), "vendor export-ignore\n")
    commit(root)
    done = git(root, "archive", "HEAD")
    done.check_returncode()
    with tarfile.open(fileobj=io.BytesIO(done.stdout)) as archive:
        names = {member.name.rstrip("/") for member in archive.getmembers()}
    assert names == {".gitattributes", "README.md", "docs", "docs/decisions"} | {
        "docs/decisions/DR-001-a-choice.md"
    }
    assert [entry.path for entry in tracked_entries(root) if entry.path.startswith("vendor/")]


@pytest.mark.parametrize(
    ("attributes", "folder", "given"),
    FOLDER_ATTRIBUTES,
    ids=["vendor", "/docs", "docs/decisions", "docs/", "vendor -diff"],
)
def test_an_attribute_on_a_folder_that_holds_a_tracked_file_fails(
    tmp_path: Path, attributes: str, folder: str, given: str
) -> None:
    root = give(plant(tmp_path, FOLDER_FILES), attributes)
    assert other_attribute_problems(root) == [f"{folder} has {given}{OTHER_ATTRIBUTE}"]


def test_line_endings_on_a_folder_and_attributes_on_a_folder_that_holds_none_pass(
    tmp_path: Path,
) -> None:
    root = give(plant(tmp_path, FOLDER_FILES), "docs text=auto eol=lf\nbuild export-ignore\n")
    assert other_attribute_problems(root) == []


def long_line(length: int) -> str:
    """A line that gives `docs/page.md` the attribute `ident`, as long as the length given."""
    head, tail = "docs/page.md", " ident"
    return head + " " * (length - len(head) - len(tail)) + tail


@pytest.mark.parametrize("length", [LONG_LINE, LONG_LINE + 79])
def test_an_attributes_line_that_git_ignores_for_its_length_fails(
    tmp_path: Path, length: int
) -> None:
    root = give(plant(tmp_path, {"docs/page.md": "Text.\n"}), f"* text\n{long_line(length)}\n")
    assert attribute_line_problems(root) == [f".gitattributes:2{LINE_IGNORED.format(length)}"]
    assert other_attribute_problems(root) == [
        f"git warns{WARNED}warning: ignoring overly long attributes line 2"
    ]


def test_a_long_attributes_line_that_only_git_s_index_or_only_the_working_tree_holds_fails(
    tmp_path: Path,
) -> None:
    root = plant(tmp_path, {"docs/page.md": "Text.\n", "docs/.gitattributes": "* text\n"})
    give(root, f"{long_line(LONG_LINE)}\n", index="* text\n")
    (root / "docs" / ".gitattributes").write_text(
        f"* text\n{long_line(LONG_LINE)}\n", encoding="utf-8"
    )
    assert attribute_line_problems(root) == [
        f".gitattributes:1{IN_TREE}{LINE_IGNORED.format(LONG_LINE)}",
        f"docs/.gitattributes:2{IN_TREE}{LINE_IGNORED.format(LONG_LINE)}",
    ]


def test_an_attributes_file_named_in_another_case_is_read_for_its_lines(tmp_path: Path) -> None:
    root = plant(tmp_path, {"docs/page.md": "Text.\n", "docs/.GitAttributes": "* text\n"})
    (root / "docs" / ".GitAttributes").write_text(f"{long_line(LONG_LINE)}\n", encoding="utf-8")
    assert attribute_line_problems(root) == [
        f"docs/.GitAttributes:1{IN_TREE}{LINE_IGNORED.format(LONG_LINE)}"
    ]


def test_an_attributes_line_one_byte_short_of_the_limit_is_read(tmp_path: Path) -> None:
    root = give(plant(tmp_path, {"docs/page.md": "Text.\n"}), f"{long_line(LONG_LINE - 1)}\n")
    assert attribute_line_problems(root) == []
    assert other_attribute_problems(root) == [f"docs/page.md has ident: set{OTHER_ATTRIBUTE}"]


def test_an_attributes_line_saved_with_a_windows_line_ending_is_measured_as_git_reads_it(
    tmp_path: Path,
) -> None:
    # Git reads the working tree's attributes line by line without the carriage return
    # before each line feed (R276).
    root = give(plant(tmp_path, {"docs/page.md": "Text.\n"}), f"{long_line(LONG_LINE - 1)}\n")
    saved_with_windows_line_endings(root, [".gitattributes"])
    assert attribute_line_problems(root) == []
    assert other_attribute_problems(root) == [f"docs/page.md has ident: set{OTHER_ATTRIBUTE}"]
    (root / ".gitattributes").write_bytes(f"{long_line(LONG_LINE)}\r\n".encode())
    assert attribute_line_problems(root) == [
        f".gitattributes:1{IN_TREE}{LINE_IGNORED.format(LONG_LINE)}"
    ]


@pytest.mark.parametrize(
    ("line", "warned"),
    [
        (
            "!docs/page.md ident",
            [
                "Use '\\!' for literal leading exclamation.",
                "warning: Negative patterns are ignored in git attributes",
            ],
        ),
        ("docs/page.md a@b", ["a@b is not a valid attribute name: .gitattributes:1"]),
        (
            "docs/page.md \N{RIGHT-TO-LEFT OVERRIDE}",
            ["U+202E is not a valid attribute name: .gitattributes:1"],
        ),
    ],
    ids=["a negative pattern", "a name that no attribute may take", "a hidden name"],
)
def test_a_warning_that_git_gives_while_it_reads_the_attributes_fails(
    tmp_path: Path, line: str, warned: list[str]
) -> None:
    root = give(plant(tmp_path, {"docs/page.md": "Text.\n"}), f"{line}\n")
    assert other_attribute_problems(root) == [f"git warns{WARNED}{each}" for each in warned]


def test_a_warning_that_only_the_working_tree_s_attributes_bring_is_named_as_its(
    tmp_path: Path,
) -> None:
    root = give(plant(tmp_path, {"docs/page.md": "Text.\n"}), "!docs/x a\n", index="* text\n")
    assert other_attribute_problems(root) == [
        f"git warns{IN_TREE}{WARNED}Use '\\!' for literal leading exclamation.",
        f"git warns{IN_TREE}{WARNED}warning: Negative patterns are ignored in git attributes",
    ]


def test_a_split_index_is_read_as_git_reads_it(tmp_path: Path) -> None:
    root = give(plant(tmp_path, {"docs/page.md": "Text.\n"}), "docs/*.md ident diff=x\n")
    git(root, "update-index", "--split-index").check_returncode()
    assert list((root / ".git").glob("sharedindex.*")), "git split no index"
    assert other_attribute_problems(root) == [
        f"docs/page.md has diff: x{OTHER_ATTRIBUTE}",
        f"docs/page.md has ident: set{OTHER_ATTRIBUTE}",
    ]
    assert attribute_problems(root, ["docs/page.md"]) == [
        "docs/page.md has diff: x, which changes how its diff shows"
    ]


# R271: Python names follow PEP 8, as ruff's naming rules check them.

# Settings of ruff's in `pyproject.toml` that leave a naming rule out of its check, for every
# file or for some, each with what the test says of it.
UNNAMING = [
    ('[tool.ruff.lint]\nselect = ["E", "F"]\n', f"{NO_NAMING}tool.ruff.lint.select, which"),
    ("[tool.ruff]\nline-length = 100\n", f"{NO_NAMING}no select is set"),
    (
        '[tool.ruff]\nselect = ["N"]\n[tool.ruff.lint]\nselect = ["E"]\n',
        f"{NO_NAMING}tool.ruff.lint.select, which",
    ),
    ('[tool.ruff.lint]\nselect = ["N8", "N9"]\n', f"{NO_NAMING}tool.ruff.lint.select, which"),
    ('[tool.ruff.lint]\nselect = ["N"]\nignore = ["N801"]\n', "tool.ruff.lint.ignore gives N801,"),
    (
        '[tool.ruff.lint]\nselect = ["N"]\nextend-ignore = ["N8"]\n',
        "tool.ruff.lint.extend-ignore gives N8,",
    ),
    ('[tool.ruff.lint]\nselect = ["ALL"]\nignore = ["N"]\n', "tool.ruff.lint.ignore gives N,"),
    ('[tool.ruff.lint]\nselect = ["N"]\nignore = ["ALL"]\n', "tool.ruff.lint.ignore gives ALL,"),
    (
        '[tool.ruff.lint]\npreview = true\nselect = ["N"]\n'
        'ignore = ["error-suffix-on-exception-name"]\n',
        "tool.ruff.lint.ignore gives error-suffix-on-exception-name,",
    ),
    (
        '[tool.ruff]\nignore = ["N818"]\n[tool.ruff.lint]\nselect = ["N"]\n',
        "tool.ruff.ignore gives N818,",
    ),
    (
        '[tool.ruff.lint]\nselect = ["N"]\n'
        '[tool.ruff.lint.per-file-ignores]\n"tests/*.py" = ["N802"]\n',
        "tool.ruff.lint.per-file-ignores gives N802 for tests/*.py,",
    ),
    (
        '[tool.ruff.lint]\nselect = ["N"]\nextend-per-file-ignores = {"scripts/*" = ["N999"]}\n',
        "tool.ruff.lint.extend-per-file-ignores gives N999 for scripts/*,",
    ),
    (
        '[tool.ruff]\nper-file-ignores = {"x.py" = ["ALL"]}\n[tool.ruff.lint]\nselect = ["N"]\n',
        "tool.ruff.per-file-ignores gives ALL for x.py,",
    ),
    (
        '[tool.ruff]\nextend = "base.toml"\n[tool.ruff.lint]\nselect = ["N"]\n',
        "tool.ruff.extend takes ruff's settings from base.toml,",
    ),
]


@pytest.mark.parametrize(("settings", "problem"), UNNAMING)
def test_ruff_s_configuration_without_the_naming_rules_fails_and_names_the_setting(
    settings: str, problem: str
) -> None:
    found = naming_configuration_problems(tomllib.loads(settings))
    assert len(found) == 1 and problem in found[0], found


@pytest.mark.parametrize(
    "settings",
    [
        '[tool.ruff.lint]\nselect = ["N"]\n',
        '[tool.ruff.lint]\nselect = ["E"]\nextend-select = ["N"]\n',
        '[tool.ruff]\nextend-select = ["N"]\n[tool.ruff.lint]\nselect = ["E"]\n',
        '[tool.ruff.lint]\nselect = ["ALL"]\nignore = ["NPY", "D", "E501"]\n'
        'per-file-ignores = {"tests/*.py" = ["S101"]}\n',
    ],
)
def test_ruff_s_configuration_that_selects_every_naming_rule_and_ignores_none_passes(
    settings: str,
) -> None:
    assert naming_configuration_problems(tomllib.loads(settings)) == []


def planted_module(definition: str = "class lower:\n    pass\n", opening: str = "") -> str:
    """A Python module whose fifth line opens this definition, after an opening line that may
    run Python or keep names from ruff's check."""
    return f'{opening}\n"""A planted module."""\n\n\n{definition}'


def configured(root: Path, files: Mapping[str, str]) -> Path:
    """A folder at root with the repository's own `pyproject.toml` and these files."""
    for name, content in {
        "pyproject.toml": (ROOT / "pyproject.toml").read_text(encoding="utf-8"),
        **files,
    }.items():
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text(content, encoding="utf-8")
    return root


CONCISE = re.compile(r"([^:]+):(\d+):\d+: (\S+) .*")


def concise_findings(done: subprocess.CompletedProcess[bytes]) -> list[tuple[str, int, str]]:
    """Each finding of a run of `ruff check --output-format concise`, by file, line and rule."""
    return [
        (found.group(1), int(found.group(2)), found.group(3))
        for found in map(CONCISE.fullmatch, done.stdout.decode("utf-8").splitlines())
        if found
    ]


@pytest.mark.parametrize(
    ("definition", "rule"),
    [
        ("class lower:\n    pass\n", "N801"),
        ("def mixedCase() -> None:\n    pass\n", "N802"),
        ("class Refused(Exception):\n    pass\n", "N818"),
    ],
)
def test_a_name_that_pep_8_does_not_give_fails_ruff_s_check_and_names_the_rule_and_the_line(
    tmp_path: Path, definition: str, rule: str
) -> None:
    configured(tmp_path, {"names.py": planted_module(definition)})
    done = ruff(tmp_path, "check", "--no-cache", "--output-format", "concise", ".")
    assert done.returncode == 1
    assert concise_findings(done) == [("names.py", 5, rule)]


# Names of each kind that the naming rules check, as PEP 8 gives them.
PEP_8 = (
    "class Lower:\n    pass\n\n\ndef snake_case() -> None:\n    pass\n\n\n"
    "class RefusedError(Exception):\n    pass\n"
)


def test_names_that_pep_8_gives_pass_ruff_s_check(tmp_path: Path) -> None:
    configured(tmp_path, {"names.py": planted_module(PEP_8)})
    done = ruff(tmp_path, "check", "--no-cache", "--output-format", "concise", ".")
    assert (done.returncode, concise_findings(done)) == (0, [])


def test_ruff_s_configuration_leaves_out_the_vendored_copy_alone(tmp_path: Path) -> None:
    configured(
        tmp_path,
        {
            "vendor/superpowers/skills/names.py": planted_module(),
            "vendor/names.py": planted_module(),
            "tests/vendor/names.py": planted_module(),
        },
    )
    done = ruff(tmp_path, "check", "--no-cache", "--output-format", "concise", ".")
    assert concise_findings(done) == [
        ("tests/vendor/names.py", 5, "N801"),
        ("vendor/names.py", 5, "N801"),
    ]


# The settings with which a planted repository's own `ruff check` applies the naming rules.
SELECTS_NAMING = '[tool.ruff.lint]\nselect = ["N"]\n'
# Each way in which a file, its folder or a setting keeps a class named in lower case from
# `ruff check`, by the files that plant it and the file that gives the name.
KEPT = {
    "a noqa comment": (
        {"names.py": planted_module("class lower:  # noqa: N801\n    pass\n")},
        "names.py",
    ),
    "a bare noqa comment": (
        {"names.py": planted_module("class lower:  # noqa\n    pass\n")},
        "names.py",
    ),
    "a ruff: noqa comment": (
        {"names.py": planted_module(opening="# ruff: noqa: N801")},
        "names.py",
    ),
    "a bare ruff: noqa comment": ({"names.py": planted_module(opening="# ruff: noqa")}, "names.py"),
    "a flake8: noqa comment": ({"names.py": planted_module(opening="# flake8: noqa")}, "names.py"),
    "a ruff.toml in its folder": (
        {
            "tool/ruff.toml": '[lint]\nselect = ["N"]\nignore = ["N801"]\n',
            "tool/names.py": planted_module(),
        },
        "tool/names.py",
    ),
    "a .ruff.toml in its folder": (
        {"tool/.ruff.toml": '[lint]\nselect = ["E"]\n', "tool/names.py": planted_module()},
        "tool/names.py",
    ),
    "a pyproject.toml in its folder": (
        {
            "tool/pyproject.toml": '[tool.ruff.lint]\nselect = ["N"]\nignore = ["N801"]\n',
            "tool/names.py": planted_module(),
        },
        "tool/names.py",
    ),
    "a .gitignore line": ({".gitignore": "names.py\n", "names.py": planted_module()}, "names.py"),
    "an .ignore line": ({".ignore": "names.py\n", "names.py": planted_module()}, "names.py"),
    "a setting of the naming rules": (
        {
            "pyproject.toml": (
                f'{SELECTS_NAMING}[tool.ruff.lint.pep8-naming]\nignore-names = ["lower"]\n'
            ),
            "names.py": planted_module(),
        },
        "names.py",
    ),
    "a folder named vendor": (
        {
            "pyproject.toml": f'[tool.ruff]\nextend-exclude = ["vendor"]\n{SELECTS_NAMING}',
            "tests/vendor/names.py": planted_module(),
        },
        "tests/vendor/names.py",
    ),
    "an extension that ruff does not read unasked": ({"names.pyw": planted_module()}, "names.pyw"),
    "an extension in upper case": ({"names.PY": planted_module()}, "names.PY"),
    "a script without an extension": (
        {"scripts/names": planted_module(opening="#!/usr/bin/env python3")},
        "scripts/names",
    ),
}
LOWER_CLASS = "N801 Class name `lower` should use CapWords convention"


@pytest.mark.parametrize("case", sorted(KEPT))
def test_a_name_kept_from_ruff_s_check_fails_the_test_of_names(tmp_path: Path, case: str) -> None:
    files, path = KEPT[case]
    root = plant(tmp_path, {"pyproject.toml": SELECTS_NAMING, **files})
    git(root, "add", "-f", "--", path).check_returncode()
    kept = ruff(root, "check", "--no-cache", "--output-format", "concise", ".")
    assert (kept.returncode, concise_findings(kept)) == (0, []), "the planted name is not kept"
    assert name_problems(root) == [f"{path}:5: {LOWER_CLASS}"]


def test_names_in_the_files_that_others_write_are_left_to_them(tmp_path: Path) -> None:
    root = plant(
        tmp_path,
        {
            "vendor/superpowers/skills/names.py": planted_module(),
            ".claude/skills/openspec-explore/names.py": planted_module(),
            "names.py": planted_module(PEP_8),
        },
    )
    assert name_problems(root) == []


def test_a_file_that_python_does_not_read_or_a_link_is_not_given_to_ruff(tmp_path: Path) -> None:
    root = plant(
        tmp_path,
        {
            "scripts/names.sh": "#!/bin/sh\nclass lower:\n",
            "notes.txt": "class lower:\n",
            "vendor/superpowers/names.py": planted_module(),
            "names.py": planted_module(PEP_8),
        },
        links={"linked.py": "vendor/superpowers/names.py"},
    )
    assert name_problems(root) == []


def test_a_python_file_that_ruff_cannot_parse_fails_the_test_of_names(tmp_path: Path) -> None:
    root = plant(tmp_path, {"broken.py": "def broken(:\n"})
    found = name_problems(root)
    assert found and all(problem.startswith("broken.py:") for problem in found), found
    assert "broken.py:1: invalid-syntax " in found[0]


def test_a_test_of_names_that_reads_no_python_file_fails(tmp_path: Path) -> None:
    root = plant(tmp_path, {"README.md": "A page.\n", "scripts/run.sh": "#!/bin/sh\n"})
    assert name_problems(root) == [NAMES_READ_NOTHING]


@pytest.mark.parametrize(
    ("status", "output", "warning", "problem"),
    [
        (
            2,
            b"",
            b"ruff failed\n  Cause: a cause",
            f"{NAMES_UNREAD}2: ruff failedU+000A  Cause: a cause",
        ),
        (
            0,
            b"[]",
            b"warning: Failed to lint names.py: denied",
            f"{NAMES_UNREAD}0: warning: Failed to lint names.py: denied",
        ),
        (1, b"[]", b"", f"{NAMES_UNREAD}1"),
        (
            0,
            b'[{"filename": "/names.py", "location": {"row": 5}, "code": "N801", "message": "m"}]',
            b"",
            f"{NAMES_UNREAD}0",
        ),
    ],
)
def test_a_run_of_ruff_that_fails_warns_or_contradicts_its_status_passes_nothing(
    status: int, output: bytes, warning: bytes, problem: str
) -> None:
    done = subprocess.CompletedProcess[bytes]([], status, output, warning)
    assert naming_findings(done, {"/names.py": "names.py"}) == [problem]


def test_a_finding_names_the_file_by_its_tracked_path_in_printable_ascii() -> None:
    done = subprocess.CompletedProcess[bytes](
        [],
        1,
        '[{"filename": "/root/n\u00e4mes.py", "location": {"row": 5}, "code": "N801", '
        '"message": "Class name `l\u00f6wer` should use CapWords convention"}]'.encode(),
        b"",
    )
    assert naming_findings(done, {"/root/n\u00e4mes.py": "n\u00e4mes.py"}) == [
        "nU+00E4mes.py:5: N801 Class name `lU+00F6wer` should use CapWords convention"
    ]


# R276: a checkout writes line feeds whatever `core.autocrlf` says, and the checks read Windows
# line endings as git stages them.

RETURN = "\r"
# A file of each kind that this repository writes and that others write.
SAVED = {
    "docs/page.md": "# A page\n\nText.\n",
    "scripts/tool.py": "import os\n",
    ".github/workflows/check.yml": "on: push\n",
    "vendor/superpowers/skills/a/SKILL.md": "Text.\n",
    ".claude/skills/openspec-a/SKILL.md": "Text.\n",
}


def test_a_file_saved_with_windows_line_endings_is_read_as_git_stages_it(tmp_path: Path) -> None:
    root = plant(tmp_path, SAVED)
    saved_with_windows_line_endings(root, SAVED)
    assert character_problems(root) == []
    assert page_problems(root) == []
    assert python_files(root) == ["scripts/tool.py"]


@pytest.mark.parametrize("held", ["ab\r\ncd\n", "ab\rcd\n"])
def test_a_carriage_return_that_git_s_index_holds_fails(tmp_path: Path, held: str) -> None:
    root = plant(tmp_path, {"docs/page.md": f"The first line.\n{held}"})
    without = f"The first line.\n{held.replace(RETURN, '')}"
    (root / "docs" / "page.md").write_bytes(without.encode("ascii"))
    assert character_problems(root) == [
        f"docs/page.md:2:3{IN_INDEX} holds {named(RETURN)}{NOT_ASCII}"
    ]


@pytest.mark.parametrize("held", ["ab\rcd\n", "ab\r", "ab\r\r\n"])
def test_a_carriage_return_that_no_line_feed_follows_in_the_working_tree_fails(
    tmp_path: Path, held: str
) -> None:
    root = plant(tmp_path, {"docs/page.md": "The first line.\nabcd\n"})
    (root / "docs" / "page.md").write_bytes(f"The first line.\n{held}".encode("ascii"))
    assert character_problems(root) == [
        f"docs/page.md:2:3{IN_TREE} holds {named(RETURN)}{NOT_ASCII}"
    ]


# A script of each kind, by what makes it one, with its text and whether git records it as
# executable.
SCRIPTS = {
    "scripts/start.sh": ("echo a\necho b\n", False),
    "scripts/tool": ("#!/bin/sh\necho a\n", False),
    "hooks/run-hook.cmd": (": x\necho a\n", True),
    "vendor/superpowers/hooks/run-hook.cmd": (": x\necho a\n", True),
    "vendor/superpowers/hooks/session-start": ("#!/usr/bin/env bash\necho a\n", True),
}


@pytest.mark.parametrize("path", SCRIPTS)
def test_a_carriage_return_before_a_line_feed_in_a_script_fails_and_says_how_to_write_it_again(
    tmp_path: Path, path: str
) -> None:
    text, executable = SCRIPTS[path]
    root = plant(tmp_path, {path: text}, executable=[path] if executable else [])
    saved_with_windows_line_endings(root, [path])
    reason = NEVER_LISTED if written_by_others(path) else NOT_ASCII
    assert character_problems(root) == [
        *(
            f"{path}:{number}:{len(line) + 1}{IN_TREE} holds {named(RETURN)}{reason}"
            for number, line in enumerate(text.split("\n")[:-1], 1)
        ),
        f"{path}{IN_TREE}{CHECK_OUT_AGAIN}",
    ]


def test_a_script_whose_carriage_return_git_s_index_holds_is_not_told_to_be_checked_out_again(
    tmp_path: Path,
) -> None:
    root = plant(tmp_path, {"scripts/start.sh": "echo a\r\n"})
    held = f"holds {named(RETURN)}{NOT_ASCII}"
    assert character_problems(root) == [f"scripts/start.sh:1:7 {held}"]
    (root / "scripts" / "start.sh").write_bytes(b"echo b\r\n")
    assert character_problems(root) == [
        f"scripts/start.sh:1:7{IN_INDEX} {held}",
        f"scripts/start.sh:1:7{IN_TREE} {held}",
    ]


def test_line_feeds_given_to_every_file_pass(tmp_path: Path) -> None:
    files: dict[str, str | bytes] = {"docs/page.md": "Text.\n", "start.sh": "echo\n", "a.png": PNG}
    root = give(plant(tmp_path, files), "* text=auto eol=lf\n")
    assert line_ending_problems(root) == []


@pytest.mark.parametrize(
    ("attributes", "given"),
    [
        ("", "text: unspecified and eol: unspecified"),
        ("* text=auto eol=lf\n*.md text\n", "text: set and eol: lf"),
        ("* text=auto eol=lf\n*.md -text\n", "text: unset and eol: lf"),
        ("* text=auto eol=lf\n*.md eol=crlf\n", "text: auto and eol: crlf"),
        ("* text=auto\n", "text: auto and eol: unspecified"),
        ("* eol=lf\n", "text: unspecified and eol: lf"),
    ],
)
def test_attributes_that_give_a_file_other_line_endings_fail_and_name_what_they_give(
    tmp_path: Path, attributes: str, given: str
) -> None:
    root = give(plant(tmp_path, {"docs/page.md": "Text.\n"}), attributes)
    problems = line_ending_problems(root)
    assert f"docs/page.md has {given}{NOT_LINE_FEEDS}" in problems
    assert all(problem.startswith((".gitattributes ", "docs/page.md ")) for problem in problems)


def test_a_folder_s_own_attributes_that_give_other_line_endings_fail(tmp_path: Path) -> None:
    files = {".gitattributes": "* text=auto eol=lf\n", "docs/.gitattributes": "* -text\n"}
    root = plant(tmp_path, {**files, "docs/page.md": "Text.\n", "README.md": "Text.\n"})
    assert line_ending_problems(root) == [
        f"docs/.gitattributes has text: unset and eol: lf{NOT_LINE_FEEDS}",
        f"docs/page.md has text: unset and eol: lf{NOT_LINE_FEEDS}",
    ]


def test_line_endings_that_only_git_s_index_or_only_the_working_tree_gives_fail(
    tmp_path: Path,
) -> None:
    root = plant(tmp_path, {"docs/page.md": "Text.\n"})
    give(root, "* text=auto eol=lf\n", index="* text=auto\n")
    assert line_ending_problems(root) == [
        f".gitattributes{IN_INDEX} has text: auto and eol: unspecified{NOT_LINE_FEEDS}",
        f"docs/page.md{IN_INDEX} has text: auto and eol: unspecified{NOT_LINE_FEEDS}",
    ]
    give(root, "* text=auto\n", index="* text=auto eol=lf\n")
    assert line_ending_problems(root) == [
        f".gitattributes{IN_TREE} has text: auto and eol: unspecified{NOT_LINE_FEEDS}",
        f"docs/page.md{IN_TREE} has text: auto and eol: unspecified{NOT_LINE_FEEDS}",
    ]


def test_a_person_s_own_line_endings_are_not_read_as_the_repository_s(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = give(plant(tmp_path / "repository", {"docs/page.md": "Text.\n"}), "* text=auto eol=lf\n")
    (root / ".git" / "info").mkdir(exist_ok=True)
    (root / ".git" / "info" / "attributes").write_text("* eol=crlf\n", encoding="utf-8")
    home = tmp_path / "home"
    (home / "git").mkdir(parents=True)
    (home / "git" / "attributes").write_text("* -text eol=crlf\n", encoding="utf-8")
    monkeypatch.setenv("XDG_CONFIG_HOME", str(home))
    plain = git(root, "check-attr", "-a", "--", "docs/page.md").stdout.decode("utf-8")
    assert "eol: crlf" in plain, "git reads no person's own attributes"
    assert line_ending_problems(root) == []


def test_a_test_of_line_endings_that_reads_no_tracked_file_fails(tmp_path: Path) -> None:
    git(tmp_path, "init", "-q").check_returncode()
    assert line_ending_problems(tmp_path) == [LINE_FEEDS_READ_NOTHING]


# The job of CI for which a merge waits, the job that runs every check of CI on the files
# saved with Windows line endings, the step with which it saves them, and the checks that it
# runs after it.
MERGE_CHECK = "ci"
WINDOWS_JOB = "windows-line-endings"
SAVE_STEP = "python scripts/windows_line_endings.py"
CHECKS = (
    "ruff check .",
    "ruff format --check .",
    "mypy",
    "pytest",
    "scripts/verify-openspec.sh",
    "scripts/sync-superpowers.sh --check",
)


def unneeded_job_problems(doc: Mapping[str, Any]) -> list[str]:
    """Each job of CI that the job `ci` does not need, by its name, so that a merge, which
    waits for `ci` alone, does not wait for it (R276)."""
    jobs = doc.get("jobs") or {}
    if MERGE_CHECK not in jobs:
        return [f"CI has no job `{MERGE_CHECK}`, for which a merge waits"]
    needs = jobs[MERGE_CHECK].get("needs") or []
    needed = {needs} if isinstance(needs, str) else set(needs)
    return [
        f"the job `{MERGE_CHECK}` does not need the job `{name}`, so a merge does not wait for it"
        for name in jobs
        if name != MERGE_CHECK and name not in needed
    ]


def windows_job_problems(doc: Mapping[str, Any]) -> list[str]:
    """What keeps CI from running each of its checks on the files that this repository
    writes, but its scripts, saved with Windows line endings (R276)."""
    job = (doc.get("jobs") or {}).get(WINDOWS_JOB)
    if job is None:
        return [f"CI has no job `{WINDOWS_JOB}`"]
    runs = [step.get("run") for step in job.get("steps") or []]
    if SAVE_STEP not in runs:
        return [f"the job `{WINDOWS_JOB}` saves no file with Windows line endings"]
    after = runs[runs.index(SAVE_STEP) + 1 :]
    return [
        f"the job `{WINDOWS_JOB}` does not run `{check}` after it saves the files"
        for check in CHECKS
        if check not in after
    ]


# The keys that let a job or a step of CI be skipped, or fail while its job passes, so that a
# merge, which waits for the job `ci` alone, would pass where a check did not run or failed,
# with what each lets happen. The job `ci` runs whatever the others give, by its `if`, which
# the test of the job `ci` holds to `always()`.
SKIPPING = {"if": "is skipped", "continue-on-error": "fails"}


def skipping_problems(doc: Mapping[str, Any]) -> list[str]:
    """Each job of CI, and each step of one, that a key lets be skipped or fail while a merge
    passes, by its job, its number and the key (R276)."""
    problems = []
    for name, job in (doc.get("jobs") or {}).items():
        for key, happens in SKIPPING.items():
            if key in job and (name, key) != (MERGE_CHECK, "if"):
                problems.append(
                    f"the job `{name}` sets `{key}`, so a merge can pass where it {happens}"
                )
        for number, step in enumerate(job.get("steps") or [], 1):
            problems.extend(
                f"the job `{name}`, step {number}, sets `{key}`, so a merge can pass where it "
                f"{happens}"
                for key, happens in SKIPPING.items()
                if key in step
            )
    return problems


def ci_workflow() -> Any:
    return load_workflow(read_staged(ROOT / ".github" / "workflows" / "ci.yml").decode("utf-8"))


def gated(**changes: Any) -> dict[str, Any]:
    """A workflow shaped as CI's, with a job that saves files and runs a check, and the job
    `ci` that needs it, with the keys given changed in the job, its steps or the job `ci`."""
    job: dict[str, Any] = {
        "steps": [{"uses": "actions/checkout@0123"}, {"run": SAVE_STEP}, {"run": "pytest"}]
    }
    merge: dict[str, Any] = {"if": "always()", "needs": [WINDOWS_JOB], "steps": [{"run": "x"}]}
    for where, keys in changes.items():
        target = {"job": job, "save": job["steps"][1], "check": job["steps"][2]}.get(where)
        (merge if target is None else target).update(keys)
    return {"jobs": {WINDOWS_JOB: job, MERGE_CHECK: merge}}


@pytest.mark.parametrize(
    ("doc", "problems"),
    [
        (gated(), []),
        (
            gated(job={"if": "false"}),
            [f"the job `{WINDOWS_JOB}` sets `if`, so a merge can pass where it is skipped"],
        ),
        (
            gated(job={"continue-on-error": True}),
            [
                f"the job `{WINDOWS_JOB}` sets `continue-on-error`, so a merge can pass where it"
                " fails"
            ],
        ),
        (
            gated(save={"if": "false"}),
            [
                f"the job `{WINDOWS_JOB}`, step 2, sets `if`, so a merge can pass where it is"
                " skipped"
            ],
        ),
        (
            gated(check={"continue-on-error": True}),
            [
                f"the job `{WINDOWS_JOB}`, step 3, sets `continue-on-error`, so a merge can pass"
                " where it fails"
            ],
        ),
        (
            gated(merge={"continue-on-error": True}),
            ["the job `ci` sets `continue-on-error`, so a merge can pass where it fails"],
        ),
    ],
    ids=[
        "as CI gives it",
        "a job with a condition",
        "a job that may fail",
        "a step with a condition",
        "a step that may fail",
        "the job ci that may fail",
    ],
)
def test_a_job_or_a_step_that_a_merge_could_pass_without_is_named(
    doc: dict[str, Any], problems: list[str]
) -> None:
    assert skipping_problems(doc) == problems


def test_no_job_or_step_of_ci_may_be_skipped_or_fail_while_a_merge_passes() -> None:
    assert skipping_problems(ci_workflow()) == []


# The condition with which the job `ci` runs where a job that it needs failed or was skipped,
# without which GitHub skips it and reports it as passing, the expression that gives its last
# step the results of the jobs that it needs, the results that a job can give, and the shell
# that a step takes where its workflow gives none, GitHub's own for `bash` (R276).
ALWAYS = "always()"
RESULTS = "${{ toJSON(needs.*.result) }}"
OUTCOMES = ("success", "failure", "cancelled", "skipped")
GITHUB_BASH = "bash --noprofile --norc -eo pipefail {0}"


def step_passes(doc: Mapping[str, Any], script: str, root: Path) -> bool:
    """Whether a step's script exits 0, run at root under the shell that its workflow's
    defaults give it, or GitHub's own for `bash`."""
    shell = ((doc.get("defaults") or {}).get("run") or {}).get("shell") or GITHUB_BASH
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "step"
        path.write_text(script, encoding="utf-8")
        command = shlex.split(shell.replace("{0}", str(path)))
        return subprocess.run(command, cwd=root, capture_output=True, check=False).returncode == 0


def merge_check_problems(doc: Mapping[str, Any], root: Path = ROOT) -> list[str]:
    """What lets the job `ci` pass where a job that it needs did not succeed: an `if` other
    than `always()`, and a last step that reads no result of the jobs that it needs, or that
    passes where one gives other than success, or fails where each succeeded, run with a
    success beside each result that a job can give (R276)."""
    job = (doc.get("jobs") or {}).get(MERGE_CHECK) or {}
    problems = [] if job.get("if") == ALWAYS else [NOT_ALWAYS]
    steps = job.get("steps") or []
    script = str(steps[-1].get("run", "")) if steps else ""
    if RESULTS not in script:
        return [
            *problems,
            f"the last step of the job `{MERGE_CHECK}` reads no result of the jobs that it needs",
        ]
    for outcome in OUTCOMES:
        results = json.dumps(["success", outcome], indent=2)
        if step_passes(doc, script.replace(RESULTS, results), root) != (outcome == "success"):
            problems.append(SKIPPED.format("fails" if outcome == "success" else "passes", outcome))
    return problems


# The last step of a job `ci`: one that fails unless each job that it needs succeeded, one
# that fails only where one failed, one that never fails and one that always does.
READ_RESULTS = f"results='{RESULTS}'\n"
EVERY_RESULT = (
    READ_RESULTS + "python3 -I -c 'import json, sys; sys.exit(set(json.loads(sys.argv[1])) "
    '- {"success"} != set())\' "$results"\n'
)
SKIPPED = "the last step of the job `ci` {} where the jobs that it needs give success and {}"
NOT_ALWAYS = (
    "the job `ci` sets no `if: always()`, so GitHub skips it where a job that it needs fails,"
    " and reports it as passing"
)


@pytest.mark.parametrize(
    ("job", "problems"),
    [
        ({"if": "always()", "steps": [{"run": EVERY_RESULT}]}, []),
        ({"steps": [{"run": EVERY_RESULT}]}, [NOT_ALWAYS]),
        ({"if": "success()", "steps": [{"run": EVERY_RESULT}]}, [NOT_ALWAYS]),
        (
            {
                "if": "always()",
                "steps": [{"run": READ_RESULTS + '! grep -q failure <<< "$results"\n'}],
            },
            [SKIPPED.format("passes", "cancelled"), SKIPPED.format("passes", "skipped")],
        ),
        (
            {"if": "always()", "steps": [{"run": READ_RESULTS + 'echo "$results"\n'}]},
            [SKIPPED.format("passes", outcome) for outcome in OUTCOMES[1:]],
        ),
        (
            {"if": "always()", "steps": [{"run": READ_RESULTS + "exit 1\n"}]},
            [SKIPPED.format("fails", "success")],
        ),
        (
            {"if": "always()", "steps": [{"run": EVERY_RESULT}, {"run": "exit 0"}]},
            ["the last step of the job `ci` reads no result of the jobs that it needs"],
        ),
        (
            {"if": "always()", "steps": []},
            ["the last step of the job `ci` reads no result of the jobs that it needs"],
        ),
    ],
    ids=[
        "as CI gives it",
        "no condition",
        "another condition",
        "a check of failures alone",
        "no check",
        "a check that always fails",
        "a last step that reads no result",
        "no step",
    ],
)
def test_a_job_ci_that_could_pass_where_a_job_that_it_needs_did_not_succeed_is_named(
    tmp_path: Path, job: dict[str, Any], problems: list[str]
) -> None:
    assert merge_check_problems({"jobs": {MERGE_CHECK: job}}, tmp_path) == problems


def test_the_last_step_of_the_job_ci_runs_under_the_shell_that_its_workflow_gives(
    tmp_path: Path,
) -> None:
    """A check that a command follows passes where the shell runs on after a command fails,
    and fails where it stops, as GitHub's own for `bash` does."""
    job = {"if": ALWAYS, "steps": [{"run": EVERY_RESULT + 'echo "checked"\n'}]}
    doc = {
        "defaults": {"run": {"shell": "bash --noprofile --norc {0}"}},
        "jobs": {MERGE_CHECK: job},
    }
    assert merge_check_problems(doc, tmp_path) == [
        SKIPPED.format("passes", outcome) for outcome in OUTCOMES[1:]
    ]
    assert merge_check_problems({"jobs": {MERGE_CHECK: job}}, tmp_path) == []


def test_the_job_ci_fails_unless_each_job_that_it_needs_succeeded() -> None:
    assert merge_check_problems(ci_workflow()) == []


@pytest.mark.parametrize(
    ("needs", "problems"),
    [
        (["python", "vendor"], []),
        (
            ["python"],
            ["the job `ci` does not need the job `vendor`, so a merge does not wait for it"],
        ),
        (
            "python",
            ["the job `ci` does not need the job `vendor`, so a merge does not wait for it"],
        ),
        (
            None,
            [
                "the job `ci` does not need the job `python`, so a merge does not wait for it",
                "the job `ci` does not need the job `vendor`, so a merge does not wait for it",
            ],
        ),
    ],
)
def test_a_job_that_the_job_ci_does_not_need_is_named(
    needs: list[str] | str | None, problems: list[str]
) -> None:
    jobs: dict[str, Any] = {
        "python": {},
        "vendor": {},
        "ci": {} if needs is None else {"needs": needs},
    }
    assert unneeded_job_problems({"jobs": jobs}) == problems
    assert unneeded_job_problems({"jobs": {"python": {}}}) == [
        "CI has no job `ci`, for which a merge waits"
    ]


def test_a_job_of_windows_line_endings_that_leaves_out_a_check_is_named() -> None:
    def steps(*runs: str) -> dict[str, Any]:
        return {
            "jobs": {
                WINDOWS_JOB: {
                    "steps": [{"uses": "actions/checkout@0123"}] + [{"run": run} for run in runs]
                }
            }
        }

    assert windows_job_problems(steps(SAVE_STEP, *CHECKS)) == []
    assert windows_job_problems({"jobs": {}}) == [f"CI has no job `{WINDOWS_JOB}`"]
    assert windows_job_problems(steps(*CHECKS)) == [
        f"the job `{WINDOWS_JOB}` saves no file with Windows line endings"
    ]
    assert windows_job_problems(steps("mypy", SAVE_STEP, *CHECKS[:2], *CHECKS[4:])) == [
        f"the job `{WINDOWS_JOB}` does not run `mypy` after it saves the files",
        f"the job `{WINDOWS_JOB}` does not run `pytest` after it saves the files",
    ]


def test_every_job_of_ci_is_one_that_a_merge_waits_for() -> None:
    assert unneeded_job_problems(ci_workflow()) == []


def test_ci_runs_every_check_on_the_files_saved_with_windows_line_endings() -> None:
    assert windows_job_problems(ci_workflow()) == []


# What the job of Windows line endings saves, and what it leaves as it is: each file that
# this repository writes but its scripts, and not the files that others write, a script of
# each kind, a link, or a file with no line feed.
JOB_FILES = {
    "docs/page.md": "# A page\n\nText.\n",
    "docs/saved.md": "Saved.\nNot yet.\n",
    "scripts/tool.py": "import os\n",
    "vendor/superpowers/UPSTREAM.lock": "sha=0123\n",
    "scripts/start.sh": "echo a\n",
    "scripts/run": "#!/bin/sh\necho a\n",
    "hooks/run-hook.cmd": ": x\necho a\n",
    "vendor/superpowers/skills/a/SKILL.md": "Text.\n",
    ".claude/skills/openspec-a/SKILL.md": "Text.\n",
    "openspec/specs/.gitkeep": "",
}
SAVED_BY_THE_JOB = (
    "docs/page.md",
    "docs/saved.md",
    "scripts/tool.py",
    "vendor/superpowers/UPSTREAM.lock",
)
WINDOWS_SCRIPT = ROOT / "scripts" / "windows_line_endings.py"


def run_the_job(
    root: Path, session: Mapping[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    """The job's script run on the repository at root, in an environment with no git
    variable of the session's but those given."""
    return subprocess.run(
        [sys.executable, str(WINDOWS_SCRIPT), str(root)],
        capture_output=True,
        text=True,
        check=False,
        env={**isolated_environment(root), **(session or {})},
    )


def test_the_job_saves_each_file_that_this_repository_writes_but_its_scripts(
    tmp_path: Path,
) -> None:
    root = plant(
        tmp_path, JOB_FILES, links={"docs/link.md": "page.md"}, executable=["hooks/run-hook.cmd"]
    )
    commit(root)
    # A line that an editor already saved with Windows line endings is not saved again.
    (root / "docs" / "saved.md").write_bytes(b"Saved.\r\nNot yet.\n")
    staged = git(root, "ls-files", "--stage", "-z").stdout
    done = run_the_job(root)
    assert done.returncode == 0, done.stderr
    assert "saved 4 files" in done.stdout
    for path, text in JOB_FILES.items():
        expected = text.replace("\n", "\r\n") if path in SAVED_BY_THE_JOB else text
        assert (root / path).read_bytes() == expected.encode("ascii"), path
    assert os.readlink(root / "docs" / "link.md") == "page.md"
    assert git(root, "ls-files", "--stage", "-z").stdout == staged
    assert git(root, "diff", "--cached", "--quiet").returncode == 0


def test_the_job_fails_where_it_saves_nothing(tmp_path: Path) -> None:
    unsaved = {path: text for path, text in JOB_FILES.items() if path not in SAVED_BY_THE_JOB}
    root = plant(tmp_path, unsaved, executable=["hooks/run-hook.cmd"])
    done = run_the_job(root)
    assert (done.returncode, done.stdout) == (1, "")
    assert NO_WINDOWS_LINE_ENDINGS in done.stderr


@pytest.mark.parametrize("where", ["a folder that no repository holds", "no folder"])
def test_the_job_that_cannot_list_the_tracked_files_says_so(tmp_path: Path, where: str) -> None:
    done = run_the_job(tmp_path if where == "a folder that no repository holds" else tmp_path / "x")
    assert (done.returncode, done.stdout) == (2, "")
    assert done.stderr.startswith("windows-line-endings: git ls-files failed: ")
    assert done.stderr.count("\n") == 1


def test_the_job_that_cannot_tell_where_its_root_lies_says_so(tmp_path: Path) -> None:
    root = plant(tmp_path / "repository", {"docs/page.md": "Text.\n"})
    real = shutil.which("git")
    assert real
    wrapper = tmp_path / "bin" / "git"
    wrapper.parent.mkdir()
    wrapper.write_text(
        '#!/usr/bin/env bash\n[ "$1" = rev-parse ] && echo refused >&2 && exit 128\n'
        f'exec "{real}" "$@"\n',
        encoding="utf-8",
    )
    wrapper.chmod(0o755)
    done = run_the_job(root, {"PATH": f"{wrapper.parent}{os.pathsep}{os.environ['PATH']}"})
    assert (done.returncode, done.stdout) == (2, "")
    assert done.stderr == "windows-line-endings: git rev-parse failed: refused\n"
    assert (root / "docs" / "page.md").read_bytes() == b"Text.\n"


def test_the_job_lists_the_files_of_the_repository_that_it_is_given(tmp_path: Path) -> None:
    root = plant(tmp_path / "repository", {"docs/page.md": "Text.\n"})
    # An index file of the session's is not the repository's.
    done = run_the_job(root, {"GIT_INDEX_FILE": str(tmp_path / "another-index")})
    assert done.returncode == 0, done.stderr
    assert (root / "docs" / "page.md").read_bytes() == b"Text.\r\n"


def test_the_job_writes_through_no_link_and_over_no_link_that_git_s_index_holds(
    tmp_path: Path,
) -> None:
    # Its name holds a line feed, so that the link's own text holds one too.
    outside = tmp_path / "out\nside.md"
    outside.write_bytes(b"Outside.\n")
    files = {"docs/page.md": "Text.\n", "docs/held.md": "Held.\n"}
    root = plant(tmp_path / "repository", files, links={"docs/link.md": "page.md"})
    commit(root)
    # A file that git's index holds and the working tree holds as a link, here to a file
    # outside the repository, and a link that git's index holds and the working tree holds as
    # a file of its target's path, as a checkout writes it where `core.symlinks` is `false`.
    (root / "docs" / "held.md").unlink()
    (root / "docs" / "held.md").symlink_to(outside)
    (root / "docs" / "link.md").unlink()
    (root / "docs" / "link.md").write_bytes(b"page.md\nmore\n")
    done = run_the_job(root)
    assert done.returncode == 0, done.stderr
    assert outside.read_bytes() == b"Outside.\n"
    assert (root / "docs" / "link.md").read_bytes() == b"page.md\nmore\n"
    assert (root / "docs" / "page.md").read_bytes() == b"Text.\r\n"


def test_the_job_writes_into_no_folder_that_the_working_tree_holds_as_a_link(
    tmp_path: Path,
) -> None:
    """A folder on a tracked path's way that the working tree holds as a link, here to a
    folder outside the repository, which git's index cannot hold beside a file below it, is
    read as the test of characters reads it, through no link (R272, R276)."""
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "page.md").write_bytes(b"Outside.\n")
    root = plant(tmp_path / "repository", {"docs/page.md": "Text.\n", "notes/kept.md": "Kept.\n"})
    commit(root)
    (root / "docs" / "page.md").unlink()
    (root / "docs").rmdir()
    (root / "docs").symlink_to(outside, target_is_directory=True)
    done = run_the_job(root)
    assert done.returncode == 0, done.stderr
    assert "saved 1 files" in done.stdout
    assert (outside / "page.md").read_bytes() == b"Outside.\n"
    assert (root / "notes" / "kept.md").read_bytes() == b"Kept.\r\n"


def test_the_job_that_cannot_open_a_tracked_path_says_so_and_saves_nothing(tmp_path: Path) -> None:
    root = unopenable(plant(tmp_path, {"docs/page.md": "Text.\n"}))
    done = run_the_job(root)
    assert (done.returncode, done.stdout) == (2, "")
    assert done.stderr == f"windows-line-endings: {shown_path(TOO_LONG)}{IN_TREE} {UNOPENED}\n"
    assert (root / "docs" / "page.md").read_bytes() == b"Text.\n"


def test_the_job_refuses_a_root_below_the_top_of_its_working_tree(tmp_path: Path) -> None:
    """Below the top, git gives each path from the root that it is given, which the files
    that others write do not match, so that the job would rewrite vendored files (R276)."""
    vendored = {"vendor/superpowers/skills/a.md": "Upstream.\n", "docs/page.md": "Text.\n"}
    root = plant(tmp_path, vendored)
    done = run_the_job(root / "vendor")
    assert (done.returncode, done.stdout) == (2, "")
    assert done.stderr == (
        f"windows-line-endings: {shown_path(str(root / 'vendor'))} is a folder below the top of"
        " its working tree, vendor/, where git would give each path from that folder\n"
    )
    for path, text in vendored.items():
        assert (root / path).read_bytes() == text.encode("ascii"), path


# A file of each kind that a clone writes: a page, a script by each of its marks, and a file
# with no line feed.
CLONED = {
    "docs/page.md": "# A page\n\nText.\n",
    "scripts/start.sh": "echo a\n",
    "scripts/tool": "#!/bin/sh\necho a\n",
    "vendor/superpowers/hooks/run-hook.cmd": ": x\necho a\n",
    "openspec/specs/.gitkeep": "",
}
CLONED_SCRIPTS = ("scripts/start.sh", "scripts/tool", "vendor/superpowers/hooks/run-hook.cmd")


def attributes_line() -> bytes:
    """The repository's own attributes file, as git would stage it, or nothing."""
    attributes = ROOT / ".gitattributes"
    return read_staged(attributes) if attributes.is_file() else b""


def cloned(source: Path, clone: Path, environment: Mapping[str, str], *options: str) -> Path:
    subprocess.run(
        ["git", "clone", "-q", *options, str(source), str(clone)],
        check=True,
        capture_output=True,
        env={**isolated_environment(clone), **environment},
    )
    return clone


def held_as_git_s_index_holds(clone: Path) -> dict[str, bytes]:
    """Each tracked file of a clone whose working tree differs from git's index, by its path,
    with what its working tree holds."""
    entries = tracked_entries(clone)
    contents = blobs(clone, (entry.oid for entry in entries))
    return {
        entry.path: (clone / entry.path).read_bytes()
        for entry in entries
        if (clone / entry.path).read_bytes() != contents[entry.oid]
    }


@pytest.mark.parametrize("where", ["the clone's own configuration", "the global configuration"])
def test_a_clone_made_with_windows_line_endings_holds_what_git_s_index_holds(
    tmp_path: Path, where: str
) -> None:
    options: tuple[str, ...] = ("-c", "core.autocrlf=true")
    environment: dict[str, str] = {}
    if where == "the global configuration":
        configuration = tmp_path / "gitconfig"
        configuration.write_bytes(b"[core]\n\tautocrlf = true\n")
        environment, options = {"GIT_CONFIG_GLOBAL": str(configuration)}, ()
    executable = ["vendor/superpowers/hooks/run-hook.cmd"]
    unattributed = plant(tmp_path / "unattributed", CLONED, executable=executable)
    commit(unattributed)
    without = cloned(unattributed, tmp_path / "without", environment, *options)
    differing = held_as_git_s_index_holds(without)
    assert b"\r\n" in differing.get("docs/page.md", b""), f"the test {NO_WINDOWS_LINE_ENDINGS}"
    files: dict[str, str | bytes] = {**CLONED, ".gitattributes": attributes_line()}
    source = plant(tmp_path / "source", files, executable=executable)
    commit(source)
    clone = cloned(source, tmp_path / "clone", environment, *options)
    assert held_as_git_s_index_holds(clone) == {}
    assert character_problems(clone) == []


def clone_made_before_the_attributes(tmp_path: Path) -> Path:
    """A clone made with `core.autocrlf` set to `true` before the commit that adds the
    attributes, then pulled past it, whose page and scripts still hold a carriage return
    before each line feed while `git status` shows nothing."""
    executable = ["vendor/superpowers/hooks/run-hook.cmd"]
    source = plant(tmp_path / "source", CLONED, executable=executable)
    commit(source)
    clone = cloned(source, tmp_path / "clone", {}, "-c", "core.autocrlf=true")
    for path in ("docs/page.md", *CLONED_SCRIPTS):
        held = (clone / path).read_bytes()
        assert b"\r\n" in held, f"{path}: the test {NO_WINDOWS_LINE_ENDINGS}"
    (source / ".gitattributes").write_bytes(attributes_line())
    git(source, "add", ".gitattributes").check_returncode()
    commit(source)
    git(clone, "pull", "-q", "--ff-only").check_returncode()
    assert git(clone, "status", "--porcelain").stdout == b""
    return clone


def way_back() -> str:
    """The command that `CONTRIBUTING.md` gives to write a script again, with `<path>` where
    the script's path goes (R276)."""
    commands = [
        line[start:end].strip("`").strip()
        for line in (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8").splitlines()
        for start, end in code_spans(line)[0]
        if "<path>" in line[start:end]
    ]
    assert len(commands) == 1, f"CONTRIBUTING.md gives {len(commands)} commands with <path>"
    return commands[0]


def written_again(clone: Path, path: str) -> None:
    """The script at the path written again in the clone, as `CONTRIBUTING.md` gives it."""
    subprocess.run(
        ["bash", "-c", way_back().replace("<path>", shlex.quote(path))],
        cwd=clone,
        env=isolated_environment(clone),
        check=True,
        capture_output=True,
    )


def test_the_advice_for_a_script_says_to_stage_it_as_git_normalizes_it() -> None:
    """Plain `git add` stops where `core.safecrlf` is `true`, so the advice names the step
    that the command in `CONTRIBUTING.md` takes first, whatever that setting says (R276)."""
    assert "stage it as git normalizes it, delete it, check it out again" in CHECK_OUT_AGAIN
    assert way_back().startswith("git add --renormalize <path> && ")


# Git's own setting, and one that stops `git add` where staging would change a file's line
# endings.
SAFE_CRLF = [None, "true"]


@pytest.mark.parametrize("safe", SAFE_CRLF, ids=["by default", "with core.safecrlf true"])
def test_a_clone_made_before_the_attributes_is_told_to_write_each_script_again(
    tmp_path: Path, safe: str | None
) -> None:
    clone = clone_made_before_the_attributes(tmp_path)
    if safe is not None:
        git(clone, "config", "core.safecrlf", safe).check_returncode()
    problems = character_problems(clone)
    assert [problem for problem in problems if problem.endswith(CHECK_OUT_AGAIN)] == [
        f"{path}{IN_TREE}{CHECK_OUT_AGAIN}" for path in CLONED_SCRIPTS
    ]
    assert not [problem for problem in problems if problem.startswith("docs/page.md")]
    for path in CLONED_SCRIPTS:
        written_again(clone, path)
    assert character_problems(clone) == []
    assert git(clone, "status", "--porcelain").stdout == b""


@pytest.mark.parametrize("safe", SAFE_CRLF, ids=["by default", "with core.safecrlf true"])
def test_the_way_back_keeps_an_edit_of_a_script_that_is_not_staged(
    tmp_path: Path, safe: str | None
) -> None:
    clone = clone_made_before_the_attributes(tmp_path)
    if safe is not None:
        git(clone, "config", "core.safecrlf", safe).check_returncode()
    script = clone / "scripts" / "start.sh"
    # An edit saved as an editor on Windows saves it, with a carriage return before each line
    # feed, and not staged.
    script.write_bytes(script.read_bytes() + b"echo an edit\r\n")
    assert script.read_bytes().count(b"\r\n") == 2, f"the test {NO_WINDOWS_LINE_ENDINGS}"
    assert f"scripts/start.sh{IN_TREE}{CHECK_OUT_AGAIN}" in character_problems(clone)
    written_again(clone, "scripts/start.sh")
    assert script.read_bytes() == b"echo a\necho an edit\n"
    assert git(clone, "status", "--porcelain").stdout == b" M scripts/start.sh\n"
    assert not [p for p in character_problems(clone) if p.startswith("scripts/start.sh")]


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


def test_a_byte_that_is_not_utf_8_is_shown_by_its_value_in_text_as_in_a_path() -> None:
    # Git's warnings and the attributes that git gives are read with `surrogateescape`, and a
    # message names a path beside them that can hold the same byte.
    byte = b"\xff".decode("utf-8", "surrogateescape")
    assert shown(f"b{byte}") == "b\\xFF"
    assert shown_path(f"a{byte}.md") == "a\\xFF.md"
    assert shown(chr(0xDC7F) + chr(0xDD00)) == "U+DC7FU+DD00"


@pytest.mark.parametrize(
    ("data", "staged"),
    [
        (b"One.\r\nTwo.\r\n", b"One.\nTwo.\n"),
        (b"One.\r\r\n", b"One.\r\n"),
        (b"One.\rTwo.\n", b"One.\rTwo.\n"),
        (b"One.\r", b"One.\r"),
        (b"\r\n\r\n", b"\n\n"),
        (b"One.\n", b"One.\n"),
        (b"", b""),
    ],
)
def test_a_file_but_a_script_is_read_with_each_return_before_a_line_feed_as_a_line_feed(
    data: bytes, staged: bytes
) -> None:
    assert not is_script("docs/page.md", data, False)
    assert staged_bytes("docs/page.md", data, False) == staged


@pytest.mark.parametrize(
    ("path", "data", "executable"),
    [
        ("scripts/sync.sh", b"set -eu\r\n", False),
        ("tools/run", b"#!/bin/sh\r\necho\r\n", False),
        ("hooks/run-hook.cmd", b": << 'CMDBLOCK'\r\n", True),
    ],
)
def test_a_script_is_read_with_every_carriage_return_that_it_holds(
    path: str, data: bytes, executable: bool
) -> None:
    assert is_script(path, data, executable)
    assert staged_bytes(path, data, executable) == data


@pytest.mark.parametrize(
    ("path", "data"),
    [
        ("docs/sh", b"Text.\r\n"),
        ("docs/page.sh.md", b"Text.\r\n"),
        ("docs/page.md", b" #!/bin/sh\r\n"),
        ("docs/page.md", b"Text.\r\n#!/bin/sh\r\n"),
    ],
)
def test_a_file_that_only_looks_like_a_script_is_none(path: str, data: bytes) -> None:
    assert not is_script(path, data, False)
    assert b"\r" not in staged_bytes(path, data, False)


def test_whether_a_file_is_executable_is_asked_of_git_s_index(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    files = {"hooks/run-hook.cmd": ": x\r\n", "hooks/other.cmd": ": x\r\n"}
    root = plant(tmp_path / "repository", files, executable=["hooks/run-hook.cmd"])
    # The working tree's bits are not what git records, as on Windows, which has none.
    (root / "hooks" / "run-hook.cmd").chmod(0o644)
    (root / "hooks" / "other.cmd").chmod(0o755)
    # An index file of the session's is not the repository's.
    monkeypatch.setenv("GIT_INDEX_FILE", str(tmp_path / "another-index"))
    assert recorded_executable(root / "hooks" / "run-hook.cmd")
    assert not recorded_executable(root / "hooks" / "other.cmd")
    assert read_staged(root / "hooks" / "run-hook.cmd") == b": x\r\n"
    assert read_staged(root / "hooks" / "other.cmd") == b": x\n"


def test_a_file_that_git_does_not_track_is_not_executable_to_git(tmp_path: Path) -> None:
    root = plant(tmp_path / "repository", {"docs/page.md": "Text.\n"})
    untracked = root / "run.cmd"
    outside = tmp_path / "outside" / "run.cmd"
    outside.parent.mkdir()
    for path in (untracked, outside):
        path.write_bytes(b": x\r\n")
        path.chmod(0o755)
        assert not recorded_executable(path)
        assert read_staged(path) == b": x\n"


def test_a_repository_that_git_cannot_read_is_named(tmp_path: Path) -> None:
    (tmp_path / ".git").write_text("gitdir: missing\n", encoding="utf-8")
    (tmp_path / "run.cmd").write_bytes(b": x\r\n")
    with pytest.raises(OSError, match="git ls-files failed in "):
        read_staged(tmp_path / "run.cmd")


def test_git_is_asked_whether_a_file_is_executable_only_where_it_holds_windows_line_endings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = plant(tmp_path, {"docs/page.md": "One.\rTwo.\n"})

    def asked(file: Path) -> bool:
        raise AssertionError(f"git was asked about {file}")

    monkeypatch.setattr(conventions, "recorded_executable", asked)
    assert read_staged(root / "docs" / "page.md") == b"One.\rTwo.\n"


# R272: everything that the test prints is printable ASCII.

PLANTED_TEST = """from pathlib import Path

from test_conventions import (
    character_problems,
    line_ending_problems,
    other_attribute_problems,
    page_problems,
)


def test_the_planted_tree():
    assert not character_problems(Path({root!r}))


def test_the_planted_pages():
    assert not page_problems(Path({root!r}))


def test_the_planted_attributes():
    assert not other_attribute_problems(Path({root!r}))


def test_the_planted_line_endings():
    assert not line_ending_problems(Path({root!r}))
"""


def test_everything_that_a_failing_run_of_the_test_of_characters_prints_is_printable_ascii(
    tmp_path: Path,
) -> None:
    files = {
        "line\nfeed.md": "Printable.\n",
        "carriage\rreturn.md": "Printable.\n",
        "escape\x1b[2Jcharacter.md": "Printable.\n",
        "tag\U000e0069\U000e0067.md": "A <!-- x --> word.\n",
        "tag\U000e0069\U000e0067~1./aux.md": "Printable.\n",
        "selector\ufe0f.md": "Printable.\n",
        "page.md": "ab\u202ecd\x07\ue000\u0378\n",
        "vendor/superpowers/a.md": "\U000e0041\ufe0f\n",
        ".gitattributes": "tag\U000e0069\U000e0067.md answer=\U000e0041\x1b eol=\U000e0041\x1b\n",
    }
    files["docs/page.md"] = "Printable.\n"
    planted = plant(tmp_path / "planted", files, links={"link.md": "to\u202e\U000e0041\n\x1b.md"})
    # A path that the working tree cannot open, whose name is too long for the file system.
    unopenable(planted)
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
    assert b"tagU+E0069U+E0067.md has answer: U+E0041U+001B, an attribute other than" in printed
    assert b"tagU+E0069U+E0067.md has text: unspecified and eol: U+E0041U+001B, not" in printed
    assert b"has the part tagU+E0069U+E0067~1., which ends in a dot that Windows drops" in printed
    assert b"the path tagU+E0069U+E0067~1./aux.md holds a `~`" in printed
    assert f"{shown_path(TOO_LONG)}{IN_TREE} {UNOPENED}".encode("ascii") in printed
    beyond = sorted({byte for byte in printed if not 0x20 <= byte <= 0x7E and byte != 0x0A})
    assert not beyond, f"the run printed the bytes {beyond}"


# The repository itself.


def test_every_tracked_file_holds_only_the_characters_that_its_writer_may_use() -> None:
    assert character_problems(ROOT) == []


def test_every_image_a_pdf_or_a_video_is_tracked_only_with_its_record() -> None:
    assert exception_problems(ROOT, EXCEPTIONS) == []


def test_every_page_that_this_repository_writes_holds_only_text_that_github_shows() -> None:
    assert page_problems(ROOT) == []


def test_the_repository_s_attributes_set_nothing_but_line_endings() -> None:
    assert other_attribute_problems(ROOT) == []


def test_every_line_of_the_repository_s_attributes_is_one_that_git_reads() -> None:
    assert ".gitattributes" in {entry.path for entry in tracked_entries(ROOT)}
    assert attribute_line_problems(ROOT) == []


def test_the_repository_s_attributes_give_every_tracked_file_line_feeds() -> None:
    assert line_ending_problems(ROOT) == []


def test_the_repository_s_ruff_settings_select_every_naming_rule_and_ignore_none() -> None:
    assert naming_configuration_problems(pyproject()) == []


def test_every_python_file_that_this_repository_writes_gives_only_names_that_pep_8_gives() -> None:
    assert name_problems(ROOT) == []
