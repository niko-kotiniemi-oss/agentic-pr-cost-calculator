"""Which files others write, what a script is, how a check reads a file of the working tree,
and how a character and a path are shown in printable ASCII.

`tests/test_conventions.py` describes these rules and holds them (R268, R269, R272, R276;
design decision 23; DR-274, DR-275, DR-281). The roadmap's test reads here which files
others write, so that the two tests never tell them in two ways (R209), every check that
reads the bytes of a file of this repository from the working tree takes them through
`staged_bytes`, as git will stage them, and the specs' form shows a spec's text with
`shown`, as the tests show theirs. Like the tool, this runs on Python 3.11 and later with
the standard library alone, so that CI's `openspec` job, which installs no Python package,
runs `scripts/spec_form.py`, which imports it.
"""

from __future__ import annotations

import os
import re
import subprocess
import unicodedata
from pathlib import Path

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
        env={key: value for key, value in os.environ.items() if not key.startswith("GIT_")},
    )
    if done.returncode != 0:
        raise OSError(f"git ls-files failed in {root}: {done.stderr.decode().strip()}")
    return done.stdout.startswith(b"100755 ")


def read_staged(file: Path) -> bytes:
    """A file's bytes as `staged_bytes` gives them, with git asked whether the file is
    executable only where its bytes hold a carriage return before a line feed."""
    data = file.read_bytes()
    return staged_bytes(file.name, data, b"\r\n" in data and recorded_executable(file))


def shown(text: str) -> str:
    """The text with each character outside printable ASCII given as `U+` and its code
    point, so that a message shows no character that it names, or that would hide it."""
    return "".join(
        character if " " <= character <= "~" else f"U+{ord(character):04X}" for character in text
    )


def shown_path(path: str) -> str:
    """A path in printable ASCII: each character outside it, and the space, as `U+` and its
    code point, and each byte that is not UTF-8, read with `surrogateescape`, as `\\x` and
    its value, so that a message names a path that holds them without them (R272)."""
    return "".join(
        character
        if "!" <= character <= "~"
        else f"\\x{ord(character) - 0xDC00:02X}"
        if ord(character) in ESCAPED_BYTES
        else f"U+{ord(character):04X}"
        for character in path
    )


def named(character: str) -> str:
    """A character by its code point and its Unicode name, or, where Python's Unicode
    database gives it none, as it gives none to a tab or a carriage return, by its code
    point and a fixed phrase (R272)."""
    name = unicodedata.name(character, "")
    return f"U+{ord(character):04X} {name or NAMELESS}"
