"""Which files others write, and how a character and a path are shown in printable ASCII.

`tests/test_conventions.py` describes these rules and holds them (R268, R269, R272;
design decision 23; DR-274, DR-275). The roadmap's test reads here which files others
write, so that the two tests never tell them in two ways (R209), and the specs' form
shows a spec's text with `shown`, as the tests show theirs. Like the tool, this runs on
Python 3.11 and later with the standard library alone, so that CI's `openspec` job,
which installs no Python package, runs `scripts/spec_form.py`, which imports it.
"""

from __future__ import annotations

import re
import unicodedata

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


def written_by_others(path: str) -> str:
    """The folder whose files others write that a tracked path lies in, or nothing."""
    found = OTHERS_WRITE.match(path)
    return found.group(0) if found else ""


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
