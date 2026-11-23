"""Which files others write, what a script is, how a check reads git's index and a file of the
working tree, and how a character and a path are shown in printable ASCII.

`tests/test_conventions.py` describes these rules and holds them (R268, R269, R272, R276;
design decision 23; DR-274, DR-275, DR-281). The roadmap's test reads here which files
others write, so that the two tests never tell them in two ways (R209), every check that
reads the bytes of a file of this repository from the working tree takes them through
`staged_bytes`, as git will stage them, and the specs' form shows a spec's text with
`shown`, as the tests show theirs. Like the tool, this runs on Python 3.11 and later with
the standard library alone, so that CI's `openspec` job, which installs no Python package,
runs `scripts/spec_form.py`, which imports it, and the job of CI that saves Windows line
endings reads the index and the working tree as the test of characters does.
"""

from __future__ import annotations

import os
import re
import stat
import subprocess
import unicodedata
from collections.abc import Mapping
from pathlib import Path
from typing import NamedTuple

# The files that others write: those under `vendor/superpowers/` but the lock at its root,
# which this repository writes, and those in the folders `.claude/skills/openspec-*/`, whose
# skills the pinned OpenSpec writes (R268, DR-274). A file or a folder below the vendored
# root that bears the lock's name is upstream's like any other (T261).
OTHERS_WRITE = re.compile(
    r"vendor/superpowers/(?!UPSTREAM\.lock\Z)|\.claude/skills/openspec-[^/]+/"
)
# The surrogates that a byte which is not UTF-8 becomes, read with `surrogateescape`.
ESCAPED_BYTES = range(0xDC80, 0xDD00)
# How a character is named where Python's Unicode database gives it no name.
NAMELESS = "(no name in Python's Unicode database)"
# What a test or a job of CI says where it meets no Windows line endings that it was to
# examine, as where a later attribute makes a checkout write line feeds (R276).
NO_WINDOWS_LINE_ENDINGS = "examined no Windows line endings"
# The modes with which git's index tracks a file and an executable file.
FILE, EXECUTABLE = "100644", "100755"
# What a check says of a tracked path that the working tree cannot open (R272).
UNOPENED = (
    "cannot be opened, as where a part of its name is too long for the file system or a folder"
    " on its way cannot be searched"
)


class Entry(NamedTuple):
    """A path that git's index tracks, with its mode and its object id."""

    mode: str
    oid: str
    path: str


class UnlistedError(Exception):
    """Raised when git cannot list the files that its index tracks."""


def written_by_others(path: str) -> str:
    """The folder whose files others write that a tracked path lies in, or nothing."""
    found = OTHERS_WRITE.match(path)
    return found.group(0) if found else ""


def is_script(path: str, data: bytes, executable: bool) -> bool:
    """Whether a file is a script, which bash or the system reads with each carriage return
    as part of its line: one whose name ends in `.sh`, that starts with `#!`, or that git
    records as executable (R276, DR-281)."""
    return path.endswith(".sh") or data.startswith(b"#!") or executable


def staged_bytes(path: str, data: bytes, executable: bool) -> bytes:
    """A file's bytes with each carriage return right before a line feed taken as a line
    feed, as git takes it when it stages a text file, in every file but a script, whose
    bytes it keeps as they are. Every check that reads the bytes of a file of this repository
    from the working tree takes them through this, so that a file saved with Windows line
    endings passes as git will commit it, while a lone carriage return, and each one in a
    script, is still read (R276, DR-281)."""
    return data if is_script(path, data, executable) else data.replace(b"\r\n", b"\n")


def session_free_environment() -> dict[str, str]:
    """The environment with no git variable of the session's, such as an index file,
    that would make git read another repository than the one it runs in."""
    return {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}


def tracked_entries(root: Path, environment: Mapping[str, str] | None = None) -> list[Entry]:
    """Each path that git's index tracks, as `git ls-files --stage -z` gives it, unquoted,
    with each byte that is not UTF-8 kept as `surrogateescape` keeps it, git run at root with
    no git variable of the session's unless an environment is given. Raises UnlistedError,
    with git's words, where git cannot list them, as where root is no folder."""
    try:
        done = subprocess.run(
            ["git", "ls-files", "--stage", "-z"],
            cwd=root,
            capture_output=True,
            check=False,
            env=dict(session_free_environment() if environment is None else environment),
        )
    except OSError as error:
        raise UnlistedError(
            f"git ls-files failed: {error.strerror or type(error).__name__}"
        ) from error
    if done.returncode != 0:
        raise UnlistedError(
            f"git ls-files failed: {done.stderr.decode('utf-8', 'replace').strip()}"
        )
    found = []
    for record in done.stdout.split(b"\0"):
        if record:
            head, _, path = record.partition(b"\t")
            mode, oid, _ = head.decode("ascii").split(" ")
            found.append(Entry(mode, oid, path.decode("utf-8", "surrogateescape")))
    return found


def kind_of(path: Path) -> str:
    """What a path of the working tree is, read without following a link, or `unreadable`
    where the system cannot say, as where a part of its name is too long for the file system
    or a folder on its way cannot be searched."""
    try:
        mode = os.lstat(path).st_mode
    except (FileNotFoundError, NotADirectoryError):
        return "missing"
    except OSError:
        return "unreadable"
    if stat.S_ISLNK(mode):
        return "link"
    if stat.S_ISDIR(mode):
        return "folder"
    return "file" if stat.S_ISREG(mode) else "other"


def in_working_tree(root: Path, path: str, folders: dict[str, str]) -> tuple[str, bytes] | None:
    """What the working tree holds at a tracked path, as a kind and its bytes: a file's, a
    link's path, or nothing for anything else, for a path that lies in a folder that is a
    link and for one that the working tree cannot open, which is `unreadable`; or None where
    it holds nothing. It follows no link, and opens a file only once it knows the file to be
    one; folders keeps the kind of each folder that it read (R272)."""
    parts = path.split("/")
    for depth in range(1, len(parts)):
        folder = "/".join(parts[:depth])
        if folder not in folders:
            folders[folder] = kind_of(root / folder)
        if folders[folder] == "link":
            return ("under a link", b"")
        if folders[folder] == "unreadable":
            return ("unreadable", b"")
        if folders[folder] != "folder":
            return None
    full = root / path
    kind = kind_of(full)
    if kind == "missing":
        return None
    if kind not in ("link", "file"):
        return ("other" if kind != "unreadable" else kind, b"")
    try:
        if kind == "link":
            return ("link", os.fsencode(os.readlink(full)))
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
        descriptor = os.open(full, flags)
        try:
            if not stat.S_ISREG(os.fstat(descriptor).st_mode):
                return ("other", b"")
            with open(descriptor, "rb", closefd=False) as file:
                return ("file", file.read())
        finally:
            os.close(descriptor)
    except OSError:
        return ("unreadable", b"")


def recorded_executable(file: Path) -> bool:
    """Whether git's index records a file as executable, asked of the repository whose
    working tree holds it, with no git variable of the session's; a file that no repository
    holds, or that git does not track, is not one."""
    where = file.absolute()
    for root in where.parents:
        if (root / ".git").exists():
            break
    else:
        return False
    done = subprocess.run(
        [
            "git",
            "--literal-pathspecs",
            "ls-files",
            "--stage",
            "-z",
            "--",
            where.relative_to(root).as_posix(),
        ],
        cwd=root,
        capture_output=True,
        check=False,
        env=session_free_environment(),
    )
    if done.returncode != 0:
        raise OSError(f"git ls-files failed in {root}: {done.stderr.decode().strip()}")
    return done.stdout.startswith(f"{EXECUTABLE} ".encode("ascii"))


def read_staged(file: Path) -> bytes:
    """A file's bytes as `staged_bytes` gives them, with git asked whether the file is
    executable only where its bytes hold a carriage return before a line feed."""
    data = file.read_bytes()
    return staged_bytes(file.name, data, b"\r\n" in data and recorded_executable(file))


def printable(text: str, kept: str) -> str:
    """The text in printable ASCII: each character outside it, and the space, but those kept,
    as `U+` and its code point, and each byte that is not UTF-8, read with `surrogateescape`,
    as `\\x` and its value, so that a message shows no character that it names, or that would
    hide it (R272). `scripts/printable_log.py` keeps a copy, which its test holds to this."""
    return "".join(
        character
        if "!" <= character <= "~" or character in kept
        else f"\\x{ord(character) - 0xDC00:02X}"
        if ord(character) in ESCAPED_BYTES
        else f"U+{ord(character):04X}"
        for character in text
    )


def shown(text: str) -> str:
    """The text in printable ASCII and spaces, as `printable` gives it."""
    return printable(text, " ")


def shown_path(path: str) -> str:
    """A path in printable ASCII, its spaces among what `printable` gives by code point, so
    that a message names a path that holds them without them (R272)."""
    return printable(path, "")


def named(character: str) -> str:
    """A character by its code point and its Unicode name, or, where Python's Unicode
    database gives it none, as it gives none to a tab or a carriage return, by its code
    point and a fixed phrase (R272)."""
    name = unicodedata.name(character, "")
    return f"U+{ord(character):04X} {name or NAMELESS}"
